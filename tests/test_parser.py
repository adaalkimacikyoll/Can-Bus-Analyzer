import pytest
from src.parser import parse_line, parse_log, CANFrame


def test_parse_valid_line():
    line = "0.0033  0X2B0  8  E8 96 50 2E EF 82 97 84"
    frame = parse_line(line)
    assert frame is not None
    assert frame.timestamp == 0.0033
    assert frame.can_id == 0x2B0
    assert frame.dlc == 8
    assert len(frame.data) == 8


def test_parse_comment_line():
    assert parse_line("# this is a comment") is None


def test_parse_empty_line():
    assert parse_line("") is None
    assert parse_line("   ") is None


def test_parse_invalid_line():
    assert parse_line("not a valid line at all!!!") is None


def test_parse_log_file(tmp_path):
    log = tmp_path / "test.log"
    log.write_text(
        "# comment\n"
        "0.001  0X0C8  8  01 02 03 04 05 06 07 08\n"
        "0.002  0X0D0  8  FF AA BB CC DD EE 11 22\n"
    )
    frames = parse_log(str(log))
    assert len(frames) == 2
    assert frames[0].can_id == 0x0C8
    assert frames[1].can_id == 0x0D0


def test_parse_log_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_log("nonexistent/file.log")