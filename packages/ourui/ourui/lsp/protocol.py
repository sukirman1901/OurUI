"""Minimal JSON-RPC framing for LSP over stdio (Content-Length headers)."""

from __future__ import annotations

import json
import sys
from typing import Any, BinaryIO, TextIO


def read_message(stream: BinaryIO) -> dict[str, Any] | None:
    """Read one LSP message from stdin. Returns None on EOF."""
    headers: dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        decoded = line.decode("utf-8").strip()
        if not decoded:
            break
        key, _, value = decoded.partition(":")
        headers[key.strip().lower()] = value.strip()

    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = stream.read(length)
    if not body:
        return None
    return json.loads(body.decode("utf-8"))


def write_message(stream: TextIO, payload: dict[str, Any]) -> None:
    """Write one LSP message to stdout."""
    encoded = json.dumps(payload, separators=(",", ":"))
    stream.write(f"Content-Length: {len(encoded.encode('utf-8'))}\r\n\r\n{encoded}")
    stream.flush()


def write_response(stream: TextIO, request_id: Any, result: Any) -> None:
    write_message(stream, {"jsonrpc": "2.0", "id": request_id, "result": result})


def write_error(stream: TextIO, request_id: Any, code: int, message: str) -> None:
    write_message(
        stream,
        {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        },
    )


def write_notification(stream: TextIO, method: str, params: dict[str, Any] | None = None) -> None:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        payload["params"] = params
    write_message(stream, payload)
