from __future__ import annotations

import argparse
import sys
from pathlib import Path

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
        help="Dev server: GET / emits HTML; POST /__ourui/call/<handler> runs @server fns",
    )
    serve_p.add_argument("source", type=Path, help="Path to a Python OurUI module")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8765)
    serve_p.add_argument("--title", default=None)

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
        serve(args.source, host=args.host, port=args.port, title=args.title)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
