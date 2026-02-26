## 🚗 CAN Bus Analyzer

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker)
![Tests](https://img.shields.io/badge/tests-13%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

A CLI tool for parsing, analyzing, and reporting on CAN bus log files —
the communication protocol used by every modern vehicle for ECU-to-ECU
messaging. Detects anomalies, generates structured reports, and simulates
realistic drive sessions for testing.

## The Problem

After a vehicle test drive, engineers are left with raw CAN bus logs
containing thousands of frames. Manually identifying flooding attacks,
unknown IDs, or signal dropouts is slow and error-prone. This tool
automates that process.

## Features

- 🔍 **Anomaly Detection** — flooding, unknown IDs, signal dropouts
- 📄 **Dual Report Output** — structured JSON + visual HTML report
- 🎮 **Log Simulator** — generate realistic drive sessions with injected anomalies
- 🐳 **Dockerized** — fully reproducible environment
- ✅ **13 Pytest Tests** — parser and analyzer logic fully covered

## Architecture
```
.log file → Parser → Analyzer → Reporter
                         ↓
               Anomaly Detection Engine
               (Flooding / Unknown ID / Dropout)
```

## Quick Start

**With Docker:**
```bash
docker build -t can-bus-analyzer .
docker run can-bus-analyzer
```

**Without Docker:**
```bash
pip install pytest
python3 -m src.cli simulate          # generate sample log
python3 -m src.cli analyze samples/drive_session.log
```

## CLI Usage
```bash
# Generate a simulated log with injected anomaly
python3 -m src.cli simulate --frames 1000

# Generate a clean log (no anomalies)
python3 -m src.cli simulate --clean

# Analyze a log file
python3 -m src.cli analyze samples/drive_session.log

# Custom output paths
python3 -m src.cli analyze samples/drive_session.log \
  --json output/my_report.json \
  --html output/my_report.html
```

## Example Output
```
╔══════════════════════════════════════╗
║       🚗 CAN Bus Analyzer v1.0       ║
║   Automotive Log Analysis Toolkit    ║
╚══════════════════════════════════════╝

✅ 500 frames parsed, 0 lines skipped

📊 Total frames  : 500
🔑 Unique IDs    : 6
🔍 Anomalies     : 1

⚠️  Anomalies found:
  🟡 [WARNING] UNKNOWN_ID: ID 0X7FF not in known ID list

📁 Reports saved: output/report.json | output/report.html
```

## Anomaly Types

| Type | Severity | Description |
|------|----------|-------------|
| `FLOODING` | CRITICAL | An ID occupies >40% of all frames |
| `UNKNOWN_ID` | WARNING | An ID not in the known whitelist |
| `DROPOUT` | WARNING | An expected ID never appears in the log |

## Running Tests
```bash
python3 -m pytest tests/ -v
```

## Project Structure
```
├── src/
│   ├── simulator.py   # Drive session log generator
│   ├── parser.py      # CAN frame parser
│   ├── analyzer.py    # Anomaly detection engine
│   ├── reporter.py    # JSON + HTML report generator
│   └── cli.py         # Command-line interface
├── tests/
│   ├── test_parser.py
│   └── test_analyzer.py
├── samples/           # Sample log files
├── output/            # Generated reports
├── Dockerfile
└── requirements.txt
```

## Relevance

CAN bus analysis is a core task in automotive and EV engineering pipelines.
This tool mirrors real-world workflows where post-drive log files are
processed to validate ECU behavior before firmware updates or hardware sign-off.
```