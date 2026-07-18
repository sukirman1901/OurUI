from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from ourui.node import KNOWN_KINDS, SourceSpan


def parse_file(path: str | Path) -> ast.Module:
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    return ast.parse(source, filename=str(path))


def span_for(path: str, node: ast.AST) -> SourceSpan:
    end_line = getattr(node, "end_lineno", None) or node.lineno
    end_col = getattr(node, "end_col_offset", None)
    if end_col is None:
        end_col = node.col_offset
    return SourceSpan(
        path=path,
        start_line=node.lineno,
        start_col=node.col_offset,
        end_line=end_line,
        end_col=end_col,
    )


def literal_value(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.List):
        return [literal_value(elt) for elt in node.elts]
    if isinstance(node, ast.Tuple):
        return [literal_value(elt) for elt in node.elts]
    if isinstance(node, ast.Dict):
        out: dict[str, Any] = {}
        for k, v in zip(node.keys, node.values, strict=True):
            if k is None:
                continue
            key = literal_value(k)
            out[str(key)] = literal_value(v)
        return out
    if isinstance(node, ast.Name):
        return {"__ref__": node.id}
    if isinstance(node, ast.Attribute):
        parts: list[str] = []
        cur: ast.AST = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
            return {"__ref__": ".".join(reversed(parts))}
        return {"__unsupported__": type(node).__name__}
    if isinstance(node, ast.Call):
        return {"__call__": True}
    return {"__unsupported__": type(node).__name__}


def call_kind(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        if func.value.id == "ui" and func.attr in KNOWN_KINDS:
            return func.attr
    if isinstance(func, ast.Name) and func.id in KNOWN_KINDS:
        return func.id
    return None
