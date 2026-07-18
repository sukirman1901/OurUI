from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ourui.lsp.server import run_stdio_server
from ourui.pipeline import dump_json, emit_html
from ourui.runtime import serve


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ourui", description="OurUI compiler CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    dump_p = sub.add_parser(
        "dump",
        help="Dump Semantic Graph, Dependency Graph, IIR, LTR, and RTR as JSON",
    )
    dump_p.add_argument("source", type=Path, help="Path to a Python OurUI module")
    dump_p.add_argument("-o", "--output", type=Path, default=None, help="Write JSON to file instead of stdout")

    emit_p = sub.add_parser(
        "emit",
        help="Emit HTML from HostNode RTR (does not consume Python AST in emitter)",
    )
    emit_p.add_argument("source", type=Path, help="Path to a Python OurUI module")
    emit_p.add_argument("-o", "--output", type=Path, default=None, help="Write HTML to file instead of stdout")
    emit_p.add_argument("--title", default=None, help="HTML document title")

    serve_p = sub.add_parser(
        "serve",
        help="Serve app: GET / emits HTML; POST /__ourui/call/<handler> runs @server fns",
    )
    serve_p.add_argument("source", type=Path, help="Path to a Python OurUI module")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8765)
    serve_p.add_argument("--title", default=None)
    serve_p.add_argument(
        "--prod",
        action="store_true",
        help="Production mode: no HMR, session State, safe errors, /__ourui/health",
    )
    serve_p.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Worker processes (requires --prod; uses file session store when >1)",
    )
    serve_p.add_argument(
        "--session-dir",
        type=Path,
        default=None,
        help="Directory for file-backed sessions (or set OURUI_SESSION_DIR)",
    )

    sub.add_parser(
        "lsp",
        help="Start the OurUI Language Server (stdio JSON-RPC for editors)",
    )

    args = parser.parse_args(argv)

    if args.command == "dump":
        if not args.source.exists():
            print(f"error: file not found: {args.source}", file=sys.stderr)
            return 1
        text = dump_json(args.source)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        return 0

    if args.command == "emit":
        if not args.source.exists():
            print(f"error: file not found: {args.source}", file=sys.stderr)
            return 1
        text = emit_html(args.source, title=args.title)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        return 0

    if args.command == "serve":
        if not args.source.exists():
            print(f"error: file not found: {args.source}", file=sys.stderr)
            return 1
        serve(
            args.source,
            host=args.host,
            port=args.port,
            title=args.title,
            prod=args.prod,
            workers=args.workers,
            session_dir=args.session_dir,
        )
        return 0

    if args.command == "lsp":
        run_stdio_server()
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
