from dataclasses import dataclass, field
from collections import defaultdict
from src.parser import CANFrame


@dataclass
class Anomaly:
    """Tespit edilen bir anomaliyi temsil eder."""
    kind: str          # Anomali türü
    can_id: int        # Hangi ID'de
    description: str   # Ne oldu
    severity: str      # "WARNING" veya "CRITICAL"
    frame_count: int = 0


@dataclass
class AnalysisReport:
    """Tüm analiz sonuçlarını tutar."""
    total_frames: int
    unique_ids: list[int]
    id_frequencies: dict[int, int]
    anomalies: list[Anomaly] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.anomalies) == 0


# Bilinen normal CAN ID'leri
KNOWN_IDS = {0x0C8, 0x0D0, 0x1A0, 0x2B0, 0x3C0}

# Flooding eşiği: bir ID bu kadar frame'den fazla gelirse şüpheli
FLOOD_RATIO_THRESHOLD = 0.40


def analyze(frames: list[CANFrame]) -> AnalysisReport:
    """
    Frame listesini analiz eder, anomalileri tespit eder.
    """
    if not frames:
        raise ValueError("Analiz edilecek frame yok.")

    # Her ID'nin kaç kez geldiğini say
    id_counts: dict[int, int] = defaultdict(int)
    for frame in frames:
        id_counts[frame.can_id] += 1

    anomalies = []

    for can_id, count in id_counts.items():

         # 1. Flooding tespiti — çok sık gelen ID
        ratio = count / len(frames)
        if ratio > FLOOD_RATIO_THRESHOLD:
            anomalies.append(Anomaly(
                kind="FLOODING",
                can_id=can_id,
                description=(
                  f"ID {can_id:#05X} toplam {count} kez geldi "
                    f"(frame'lerin %{ratio*100:.1f}'i) — flooding şüphesi"
                ),
                severity="CRITICAL",
                frame_count=count,
            ))

        # 2. Bilinmeyen ID tespiti
        if can_id not in KNOWN_IDS:
            anomalies.append(Anomaly(
                kind="UNKNOWN_ID",
                can_id=can_id,
                description=(
                    f"ID {can_id:#05X} tanımlanmış ID listesinde yok"
                ),
                severity="WARNING",
                frame_count=count,
            ))

    # 3. Dropout tespiti — beklenen ID hiç gelmemişse
    for known_id in KNOWN_IDS:
        if known_id not in id_counts:
            anomalies.append(Anomaly(
                kind="DROPOUT",
                can_id=known_id,
                description=(
                    f"ID {known_id:#05X} log boyunca hiç gelmedi — "
                    f"sinyal kaybı olabilir"
                ),
                severity="WARNING",
                frame_count=0,
            ))

    return AnalysisReport(
        total_frames=len(frames),
        unique_ids=list(id_counts.keys()),
        id_frequencies=dict(id_counts),
        anomalies=anomalies,
    )