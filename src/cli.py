import argparse
import sys
from src.simulator import generate_log
from src.parser import parse_log
from src.analyzer import analyze
from src.reporter import save_json, save_html


def print_banner():
    print("""
╔══════════════════════════════════════╗
║       🚗 CAN Bus Analyzer v1.0       ║
║   Automotive Log Analysis Toolkit    ║
╚══════════════════════════════════════╝
""")


def print_summary(report):
    print(f"📊 Total frames  : {report.total_frames}")
    print(f"🔑 Unique IDs    : {len(report.unique_ids)}")
    print(f"🔍 Anomalies     : {len(report.anomalies)}")
    print()

    if report.is_clean:
        print("✅ Clean — no anomalies detected.")
    else:
        print("⚠️  Anomalies found:")
        for a in report.anomalies:
            icon = "🔴" if a.severity == "CRITICAL" else "🟡"
            print(f"  {icon} [{a.severity}] {a.kind}: {a.description}")


def main():
    parser = argparse.ArgumentParser(
        prog="cantool",
        description="Analyze CAN bus log files and generate reports.",
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a log file")
    analyze_parser.add_argument("log_file", help="Path to .log file")
    analyze_parser.add_argument("--json", default="output/report.json", help="JSON output path")
    analyze_parser.add_argument("--html", default="output/report.html", help="HTML output path")

    sim_parser = subparsers.add_parser("simulate", help="Generate a simulated log file")
    sim_parser.add_argument("--output", default="samples/drive_session.log", help="Output path")
    sim_parser.add_argument("--frames", type=int, default=500, help="Number of frames")
    sim_parser.add_argument("--clean", action="store_true", help="Generate anomaly-free log")

    args = parser.parse_args()
    print_banner()

    if args.command == "simulate":
        generate_log(
            output_path=args.output,
            total_frames=args.frames,
            inject_anomaly=not args.clean,
        )

    elif args.command == "analyze":
        try:
            frames = parse_log(args.log_file)
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

        report = analyze(frames)
        print_summary(report)
        save_json(report, args.json)
        save_html(report, args.html)
        print()
        print(f"📁 Reports saved: {args.json} | {args.html}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()