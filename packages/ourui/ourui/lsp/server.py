"""Stdio Language Server for OurUI authoring."""

from __future__ import annotations

import sys
from typing import Any

from ourui.lsp.completions import get_completions, get_hover
from ourui.lsp import protocol


class DocumentStore:
    def __init__(self) -> None:
        self._documents: dict[str, str] = {}

    def open(self, uri: str, text: str) -> None:
        self._documents[uri] = text

    def change(self, uri: str, text: str) -> None:
        self._documents[uri] = text

    def get(self, uri: str) -> str:
        return self._documents.get(uri, "")


class LSPServer:
    def __init__(self, *, stdin: Any = None, stdout: Any = None) -> None:
        self._stdin = stdin or sys.stdin.buffer
        self._stdout = stdout or sys.stdout
        self._documents = DocumentStore()
        self._shutdown = False

    def run(self) -> int:
        while True:
            message = protocol.read_message(self._stdin)
            if message is None:
                return 0 if self._shutdown else 1

            method = message.get("method")
            params = message.get("params") or {}
            request_id = message.get("id")

            if method == "initialize":
                self._handle_initialize(request_id, params)
            elif method == "initialized":
                pass
            elif method == "shutdown":
                self._shutdown = True
                if request_id is not None:
                    protocol.write_response(self._stdout, request_id, None)
            elif method == "exit":
                return 0 if self._shutdown else 1
            elif method == "textDocument/didOpen":
                doc = params.get("textDocument") or {}
                self._documents.open(doc.get("uri", ""), doc.get("text", ""))
            elif method == "textDocument/didChange":
                doc_uri = (params.get("textDocument") or {}).get("uri", "")
                changes = params.get("contentChanges") or []
                if changes:
                    self._documents.change(doc_uri, changes[-1].get("text", ""))
            elif method == "textDocument/completion":
                self._handle_completion(request_id, params)
            elif method == "textDocument/hover":
                self._handle_hover(request_id, params)
            elif request_id is not None:
                protocol.write_error(self._stdout, request_id, -32601, f"Method not found: {method}")

    def _handle_initialize(self, request_id: Any, params: dict[str, Any]) -> None:
        if request_id is None:
            return
        protocol.write_response(
            self._stdout,
            request_id,
            {
                "capabilities": {
                    "textDocumentSync": 1,
                    "completionProvider": {"triggerCharacters": ["."]},
                    "hoverProvider": True,
                },
                "serverInfo": {"name": "ourui-lsp", "version": "0.4.1"},
            },
        )

    def _document_context(self, params: dict[str, Any]) -> tuple[str, int, int] | None:
        text_doc = params.get("textDocument") or {}
        uri = text_doc.get("uri", "")
        text = self._documents.get(uri)
        position = params.get("position") or {}
        return text, int(position.get("line", 0)), int(position.get("character", 0))

    def _handle_completion(self, request_id: Any, params: dict[str, Any]) -> None:
        if request_id is None:
            return
        ctx = self._document_context(params)
        if ctx is None:
            protocol.write_response(self._stdout, request_id, {"isIncomplete": False, "items": []})
            return
        text, line, character = ctx
        items = get_completions(text, line, character)
        protocol.write_response(self._stdout, request_id, {"isIncomplete": False, "items": items})

    def _handle_hover(self, request_id: Any, params: dict[str, Any]) -> None:
        if request_id is None:
            return
        ctx = self._document_context(params)
        if ctx is None:
            protocol.write_response(self._stdout, request_id, None)
            return
        text, line, character = ctx
        protocol.write_response(self._stdout, request_id, get_hover(text, line, character))


def run_stdio_server() -> None:
    raise SystemExit(LSPServer().run())
