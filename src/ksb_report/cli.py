"""
KSB-Report — CLI
Entry point for running the API server or generating PDFs from the command line.
"""

from __future__ import annotations

import argparse
import json
import sys


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="ksb-report",
        description="KSB-Report — Generate customizable PDF reports",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Start the API server")
    serve_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8500, help="Port to listen on (default: 8500)"
    )
    serve_parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )

    # generate command
    gen_parser = subparsers.add_parser(
        "generate", help="Generate a PDF from a JSON template file"
    )
    gen_parser.add_argument("input", help="Path to JSON template file")
    gen_parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="Output PDF path (default: output.pdf)",
    )

    args = parser.parse_args()

    if args.command == "serve":
        _run_server(args.host, args.port, args.reload)
    elif args.command == "generate":
        _generate_pdf(args.input, args.output)
    else:
        parser.print_help()
        sys.exit(1)


def _run_server(host: str, port: int, reload: bool) -> None:
    """Start the FastAPI server with uvicorn."""
    import uvicorn

    print(f"🚀 KSB-Report API starting on http://{host}:{port}")
    print(f"📖 API docs: http://{host}:{port}/docs")
    uvicorn.run(
        "ksb_report.api:app",
        host=host,
        port=port,
        reload=reload,
    )


def _generate_pdf(input_path: str, output_path: str) -> None:
    """Generate a PDF from a JSON template file."""
    from ksb_report.engine import ReportEngine
    from ksb_report.schemas import ReportTemplate

    try:
        with open(input_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {input_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)

    try:
        template = ReportTemplate(**data)
    except Exception as e:
        print(f"❌ Template validation error: {e}")
        sys.exit(1)

    engine = ReportEngine()
    engine.generate_to_file(template, output_path)
    print(f"✅ PDF generated: {output_path}")


if __name__ == "__main__":
    main()
