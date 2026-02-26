import json
from datetime import datetime
from pathlib import Path
from src.analyzer import AnalysisReport


def save_json(report: AnalysisReport, output_path: str = "output/report.json") -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    data = {
        "generated_at": datetime.now().isoformat(),
        "total_frames": report.total_frames,
        "unique_ids": [f"{i:#05X}" for i in report.unique_ids],
        "id_frequencies": {f"{k:#05X}": v for k, v in report.id_frequencies.items()},
        "clean": report.is_clean,
        "anomaly_count": len(report.anomalies),
        "anomalies": [
            {
                "kind": a.kind,
                "can_id": f"{a.can_id:#05X}",
                "severity": a.severity,
                "description": a.description,
                "frame_count": a.frame_count,
            }
            for a in report.anomalies
        ],
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"📄 JSON report: {output_path}")
    return output_path


def save_html(report: AnalysisReport, output_path: str = "output/report.html") -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    anomaly_rows = ""
    for a in report.anomalies:
        color = "#ff4444" if a.severity == "CRITICAL" else "#ffaa00"
        anomaly_rows += (
            "<tr>"
            f"<td><span style='color:{color};font-weight:bold'>{a.severity}</span></td>"
            f"<td>{a.kind}</td>"
            f"<td style='font-family:monospace'>{a.can_id:#05X}</td>"
            f"<td>{a.description}</td>"
            "</tr>"
        )

    freq_rows = ""
    for can_id, count in sorted(report.id_frequencies.items(), key=lambda x: -x[1]):
        freq_rows += (
            "<tr>"
            f"<td style='font-family:monospace'>{can_id:#05X}</td>"
            f"<td>{count}</td>"
            f"<td>{count / report.total_frames * 100:.1f}%</td>"
            "</tr>"
        )

    status_color = "#ff4444" if not report.is_clean else "#44ff88"
    status_text = "⚠️ ANOMALY DETECTED" if not report.is_clean else "✅ CLEAN"

    if report.anomalies:
        anomaly_section = (
            "<table><tr><th>Severity</th><th>Type</th><th>ID</th><th>Description</th></tr>"
            + anomaly_rows
            + "</table>"
        )
    else:
        anomaly_section = "<p style='color:#44ff88'>No anomalies detected.</p>"

    html = (
        "<!DOCTYPE html>\n"
        "<html lang='en'>\n"
        "<head>\n"
        "<meta charset='UTF-8'>\n"
        "<title>CAN Bus Analysis Report</title>\n"
        "<style>\n"
        "body{font-family:-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;padding:2rem}\n"
        "h1{color:#38bdf8}h2{color:#94a3b8;border-bottom:1px solid #1e293b;padding-bottom:.5rem}\n"
        f".status{{font-size:1.4rem;font-weight:bold;color:{status_color};margin:1rem 0}}\n"
        ".stats{display:flex;gap:2rem;margin:1rem 0}\n"
        ".stat{background:#1e293b;padding:1rem 2rem;border-radius:8px;text-align:center}\n"
        ".stat-value{font-size:2rem;font-weight:bold;color:#38bdf8}\n"
        ".stat-label{color:#64748b;font-size:.85rem}\n"
        "table{width:100%;border-collapse:collapse;margin:1rem 0}\n"
        "th{background:#1e293b;padding:.75rem;text-align:left;color:#94a3b8}\n"
        "td{padding:.75rem;border-bottom:1px solid #1e293b}\n"
        "tr:hover td{background:#1e293b}\n"
        ".footer{color:#334155;margin-top:2rem;font-size:.8rem}\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        "<h1>🚗 CAN Bus Analysis Report</h1>\n"
        f"<div class='status'>{status_text}</div>\n"
        f"<p style='color:#64748b'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
        "<div class='stats'>\n"
        f"<div class='stat'><div class='stat-value'>{report.total_frames}</div><div class='stat-label'>Total Frames</div></div>\n"
        f"<div class='stat'><div class='stat-value'>{len(report.unique_ids)}</div><div class='stat-label'>Unique IDs</div></div>\n"
        f"<div class='stat'><div class='stat-value'>{len(report.anomalies)}</div><div class='stat-label'>Anomalies</div></div>\n"
        "</div>\n"
        "<h2>Anomalies</h2>\n"
        + anomaly_section
        + "\n<h2>ID Frequency Distribution</h2>\n"
        "<table><tr><th>CAN ID</th><th>Frame Count</th><th>Ratio</th></tr>\n"
        + freq_rows
        + "</table>\n"
        "<div class='footer'>CAN Bus Analyzer — github.com/adaalkimacikyoll</div>\n"
        "</body>\n"
        "</html>"
    )

    with open(output_path, "w") as f:
        f.write(html)

    print(f"🌐 HTML report: {output_path}")
    return output_path