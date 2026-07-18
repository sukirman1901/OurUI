from __future__ import annotations

import io
import json

from ourui.lsp.completions import UI_COMPONENTS, get_completions, get_hover
from ourui.lsp.protocol import read_message, write_message
from ourui.lsp.server import LSPServer


def test_ui_dot_completions_include_button_and_page() -> None:
    text = "from ourui.ui import ui\n\npage = ui."
    items = get_completions(text, line=2, character=10)
    labels = {item["label"] for item in items}
    assert "Button" in labels
    assert "Page" in labels
    assert labels.issubset(set(UI_COMPONENTS))


def test_ui_dot_completions_filter_prefix() -> None:
    text = "x = ui.But"
    items = get_completions(text, line=0, character=10)
    labels = [item["label"] for item in items]
    assert labels == ["Button"]


def test_top_level_keyword_completions() -> None:
    text = "Sta"
    items = get_completions(text, line=0, character=3)
    labels = {item["label"] for item in items}
    assert "State" in labels
    assert "server" not in labels or "State" in labels


def test_top_level_server_completion() -> None:
    text = "ser"
    items = get_completions(text, line=0, character=3)
    labels = {item["label"] for item in items}
    assert "server" in labels


def test_hover_for_ui_button() -> None:
    text = "btn = ui.Button('Go')"
    hover = get_hover(text, line=0, character=10)
    assert hover is not None
    assert "ui.Button" in hover["contents"]["value"]
    assert "clickable" in hover["contents"]["value"].lower()


def test_hover_none_for_unknown() -> None:
    text = "count = 1"
    assert get_hover(text, line=0, character=3) is None


def test_protocol_roundtrip() -> None:
    payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    out = io.StringIO()
    write_message(out, payload)
    raw = out.getvalue().encode("utf-8")
    stream = io.BytesIO(raw)
    assert read_message(stream) == payload


def test_lsp_initialize_and_completion() -> None:
    stdin = io.BytesIO()
    stdout = io.StringIO()

    def send(msg: dict) -> None:
        body = json.dumps(msg).encode("utf-8")
        stdin.write(f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8"))
        stdin.write(body)

    send(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"capabilities": {}},
        }
    )
    send(
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///tmp/example.py",
                    "languageId": "python",
                    "version": 1,
                    "text": "from ourui.ui import ui\n\npage = ui.",
                }
            },
        }
    )
    send(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": "file:///tmp/example.py"},
                "position": {"line": 2, "character": 10},
            },
        }
    )
    send({"jsonrpc": "2.0", "id": 3, "method": "shutdown", "params": None})
    send({"jsonrpc": "2.0", "method": "exit", "params": None})
    stdin.seek(0)

    code = LSPServer(stdin=stdin, stdout=stdout).run()
    assert code == 0

    output = stdout.getvalue()
    assert '"Button"' in output
    assert '"Page"' in output
