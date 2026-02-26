import random
import time
from pathlib import Path

# Gerçek arabalarda yaygın CAN ID'leri
NORMAL_IDS = [
    0x0C8,  # Motor RPM
    0x0D0,  # Hız
    0x1A0,  # Fren
    0x2B0,  # Batarya voltajı
    0x3C0,  # Sıcaklık
]

ANOMALY_ID = 0x7FF  # Normalde bu kadar sık gelmemeli


def generate_frame(timestamp: float, can_id: int) -> str:
    """Tek bir CAN frame satırı üretir."""
    data = " ".join(f"{random.randint(0, 255):02X}" for _ in range(8))
    return f"{timestamp:.4f}  {can_id:#05X}  8  {data}\n"


def generate_log(
    output_path: str = "samples/drive_session.log",
    total_frames: int = 500,
    inject_anomaly: bool = True,
) -> str:
    """
    Sürüş simülasyonu log dosyası oluşturur.
    inject_anomaly=True ise ortaya bir flooding anomalisi gömer.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    timestamp = 0.0
    anomaly_start = total_frames // 2  # Ortada anomali başlar

    with open(output_path, "w") as f:
        f.write("# CAN Bus Log - Simulated Drive Session\n")
        f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Format: timestamp  ID  DLC  DATA\n\n")

        for i in range(total_frames):
            timestamp += random.uniform(0.001, 0.010)

            # Anomali penceresi: 50 frame boyunca 0x7FF'den sel gibi mesaj
            if inject_anomaly and anomaly_start <= i < anomaly_start + 50:
                f.write(generate_frame(timestamp, ANOMALY_ID))
            else:
                can_id = random.choice(NORMAL_IDS)
                f.write(generate_frame(timestamp, can_id))

    print(f"✅ Log generated: {output_path} ({total_frames} frames)")
    return output_path


if __name__ == "__main__":
    generate_log()