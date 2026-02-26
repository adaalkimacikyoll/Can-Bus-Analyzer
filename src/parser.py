from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CANFrame:
    """Represents a single CAN bus frame."""
    timestamp: float
    can_id: int
    dlc: int
    data: list[int]
    raw: str


def parse_line(line: str) -> Optional[CANFrame]:
    """
    Parses a single log line into a CANFrame object.
    Skips comments and empty lines.
    """
    line = line.strip()

    if not line or line.startswith("#"):
        return None

    parts = line.split()

    if len(parts) < 4:
        return None

    try:
        timestamp = float(parts[0])
        can_id = int(parts[1], 16)
        dlc = int(parts[2])
        data = [int(b, 16) for b in parts[3:3 + dlc]]

        return CANFrame(
            timestamp=timestamp,
            can_id=can_id,
            dlc=dlc,
            data=data,
            raw=line,
        )
    except (ValueError, IndexError):
        return None


def parse_log(file_path: str) -> list[CANFrame]:
    """
    Reads an entire log file and returns valid frames.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    frames = []
    errors = 0

    with open(path, "r") as f:
        for line in f:
            frame = parse_line(line)
            if frame:
                frames.append(frame)
            elif line.strip() and not line.startswith("#"):
                errors += 1

    print(f"✅ {len(frames)} frames parsed, {errors} lines skipped")
    return frames