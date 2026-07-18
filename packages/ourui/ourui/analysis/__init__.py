from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ourui.node import THEME_ATTR_KEYS, Node
from ourui.parse import call_kind, literal_value, parse_file, span_for


@dataclass
class SemanticGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)
    edges: list[dict[str, str]] = field(default_factory=list)
    handlers: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: n.to_dict() for nid, n in sorted(self.nodes.items())},
            "roots": list(self.roots),
            "edges": sorted(self.edges, key=lambda e: (e["from"], e["to"], e["kind"])),
            "handlers": {k: self.handlers[k] for k in sorted(self.handlers)},
        }


@dataclass
class DependencyGraph:
    edges: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "edges": sorted(self.edges, key=lambda e: (e["from"], e["to"], e["kind"])),
        }


def _is_server_decorator(dec: ast.AST) -> bool:
    if isinstance(dec, ast.Name) and dec.id == "server":
        return True
    if isinstance(dec, ast.Attribute) and dec.attr == "server":
        return True
    return False


class _GraphBuilder:
    def __init__(self, path: str) -> None:
        self.path = path
        self.counter = 0
        self.graph = SemanticGraph()
        self.dep = DependencyGraph()
        self._theme_nodes: dict[str, str] = {}

    def next_id(self, prefix: str = "n") -> str:
        self.counter += 1
        return f"{prefix}{self.counter:04d}"

    def theme_node(self, token: str, at: ast.AST) -> str:
        if token in self._theme_nodes:
            return self._theme_nodes[token]
        nid = self.next_id("theme")
        node = Node(
            id=nid,
            kind="ThemeToken",
            span=span_for(self.path, at),
            attributes={"token": token},
            provenance=["analyze:theme_token"],
        ).with_hash()
        self.graph.nodes[nid] = node
        self._theme_nodes[token] = nid
        return nid

    def register_handler(self, name: str, *, kind: str, at: ast.AST) -> None:
        self.graph.handlers[name] = {
            "name": name,
            "kind": kind,
            "span": span_for(self.path, at).to_dict(),
        }

    def build_call(self, call: ast.Call, parent_id: str | None = None) -> str | None:
        kind = call_kind(call)
        if kind is None:
            return None

        nid = self.next_id()
        attrs: dict[str, Any] = {}
        child_ids: list[str] = []

        for arg in call.args:
            if isinstance(arg, ast.Call) and call_kind(arg):
                cid = self.build_call(arg, parent_id=nid)
                if cid:
                    child_ids.append(cid)
            elif isinstance(arg, ast.List):
                for elt in arg.elts:
                    if isinstance(elt, ast.Call) and call_kind(elt):
                        cid = self.build_call(elt, parent_id=nid)
                        if cid:
                            child_ids.append(cid)
            else:
                val = literal_value(arg)
                if isinstance(val, str):
                    if kind in {"Button", "Text", "Card"} and "text" not in attrs:
                        attrs["text"] = val
                    elif "title" not in attrs:
                        attrs["title"] = val
                    else:
                        attrs.setdefault("_args", []).append(val)
                else:
                    attrs.setdefault("_args", []).append(val)

        for kw in call.keywords:
            if kw.arg is None:
                continue
            if kw.arg == "children":
                val_node = kw.value
                if isinstance(val_node, (ast.List, ast.Tuple)):
                    for elt in val_node.elts:
                        if isinstance(elt, ast.Call) and call_kind(elt):
                            cid = self.build_call(elt, parent_id=nid)
                            if cid:
                                child_ids.append(cid)
                elif isinstance(val_node, ast.Call) and call_kind(val_node):
                    cid = self.build_call(val_node, parent_id=nid)
                    if cid:
                        child_ids.append(cid)
                continue
            if kw.arg == "on_click":
                if isinstance(kw.value, ast.Name):
                    attrs["on_click"] = {"__handler__": kw.value.id}
                elif isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    attrs["on_click"] = {"__handler__": kw.value.value}
                else:
                    attrs["on_click"] = literal_value(kw.value)
                continue
            if isinstance(kw.value, ast.Call) and call_kind(kw.value):
                cid = self.build_call(kw.value, parent_id=nid)
                if cid:
                    attrs[kw.arg] = {"__node__": cid}
                    child_ids.append(cid)
                continue
            attrs[kw.arg] = literal_value(kw.value)

        node = Node(
            id=nid,
            kind=kind,
            span=span_for(self.path, call),
            attributes=attrs,
            children=child_ids,
            provenance=["parse:ui_call", "analyze:semantic_graph"],
        ).with_hash()
        self.graph.nodes[nid] = node

        if parent_id:
            self.graph.edges.append({"from": parent_id, "to": nid, "kind": "contains"})
        else:
            self.graph.roots.append(nid)

        for key, value in attrs.items():
            if key in THEME_ATTR_KEYS and isinstance(value, str):
                tid = self.theme_node(value, call)
                self.dep.edges.append({"from": nid, "to": tid, "kind": "uses_theme"})
                self.graph.edges.append({"from": nid, "to": tid, "kind": "uses_theme"})
            if key == "on_click" and isinstance(value, dict) and "__handler__" in value:
                handler = value["__handler__"]
                self.dep.edges.append({"from": nid, "to": handler, "kind": "on_click"})
                self.graph.edges.append({"from": nid, "to": handler, "kind": "calls_handler"})

        return nid

    def visit_module(self, module: ast.Module) -> None:
        for stmt in module.body:
            if isinstance(stmt, ast.FunctionDef):
                kind = "server" if any(_is_server_decorator(d) for d in stmt.decorator_list) else "client"
                self.register_handler(stmt.name, kind=kind, at=stmt)
            elif isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.Call) and call_kind(stmt.value):
                    self.build_call(stmt.value)
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if call_kind(stmt.value):
                    self.build_call(stmt.value)


def _display_path(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_semantic_graph(path: str | Path) -> tuple[SemanticGraph, DependencyGraph]:
    path = Path(path)
    module = parse_file(path)
    builder = _GraphBuilder(_display_path(path))
    builder.visit_module(module)
    builder.graph.roots = sorted(set(builder.graph.roots))
    return builder.graph, builder.dep
