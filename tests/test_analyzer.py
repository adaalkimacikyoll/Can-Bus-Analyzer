import pytest
from src.parser import CANFrame
from src.analyzer import analyze


def make_frame(can_id: int, timestamp: float = 0.1) -> CANFrame:
    return CANFrame(
        timestamp=timestamp,
        can_id=can_id,
        dlc=8,
        data=[0] * 8,
        raw="",
    )


def test_clean_log_no_flooding():
    # Her bilinen ID'den eşit sayıda frame — hiçbiri %40'ı geçmemeli
    frames = [make_frame(can_id) for can_id in [0x0C8, 0x0D0, 0x1A0, 0x2B0, 0x3C0] for _ in range(10)]
    report = analyze(frames)
    flooding = [a for a in report.anomalies if a.kind == "FLOODING"]
    assert len(flooding) == 0

def test_unknown_id_detected():
    frames = [make_frame(0x0C8) for _ in range(10)]
    frames += [make_frame(0x999) for _ in range(5)]
    report = analyze(frames)
    unknown = [a for a in report.anomalies if a.kind == "UNKNOWN_ID"]
    assert len(unknown) == 1
    assert unknown[0].can_id == 0x999


def test_flooding_detected():
    normal = [make_frame(0x0C8) for _ in range(50)]
    flood = [make_frame(0x7FF) for _ in range(50)]
    report = analyze(normal + flood)
    flooding = [a for a in report.anomalies if a.kind == "FLOODING"]
    assert len(flooding) >= 1


def test_dropout_detected():
    frames = [make_frame(0x0C8) for _ in range(20)]
    report = analyze(frames)
    dropouts = [a for a in report.anomalies if a.kind == "DROPOUT"]
    assert len(dropouts) > 0


def test_report_total_frames():
    frames = [make_frame(0x0C8) for _ in range(42)]
    report = analyze(frames)
    assert report.total_frames == 42


def test_empty_frames_raises():
    with pytest.raises(ValueError):
        analyze([])


def test_is_clean_property():
    frames = [make_frame(can_id) for can_id in [0x0C8, 0x0D0, 0x1A0, 0x2B0, 0x3C0] for _ in range(5)]
    report = analyze(frames)
    flooding = [a for a in report.anomalies if a.kind == "FLOODING"]
    assert len(flooding) == 0