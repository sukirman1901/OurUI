from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ourui.analysis.components import (
    collect_components,
    component_call_name,
    expand_component_call,
)
from ourui.node import (
    FORM_CONTROL_KINDS,
    INPUT_TYPES,
    NAV_PLACEMENTS,
    NAV_TONES,
    THEME_ATTR_KEYS,
    Node,
)
from ourui.parse import call_kind, literal_value, parse_file, span_for
from ourui.theme import apply_theme_overrides, default_tokens, theme_kwargs_to_overrides


@dataclass
class SemanticGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    roots: list[str] = field(default_factory=list)
    edges: list[dict[str, str]] = field(default_factory=list)
    handlers: dict[str, dict[str, Any]] = field(default_factory=dict)
    states: dict[str, dict[str, Any]] = field(default_factory=dict)
    components: dict[str, dict[str, Any]] = field(default_factory=dict)
    routes: dict[str, str] = field(default_factory=dict)
    tokens: dict[str, dict[str, str]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": {nid: n.to_dict() for nid, n in sorted(self.nodes.items())},
            "roots": list(self.roots),
            "routes": {k: self.routes[k] for k in sorted(self.routes)},
            "edges": sorted(self.edges, key=lambda e: (e["from"], e["to"], e["kind"])),
            "handlers": {k: self.handlers[k] for k in sorted(self.handlers)},
            "states": {k: self.states[k] for k in sorted(self.states)},
            "components": {k: self.components[k] for k in sorted(self.components)},
            "tokens": {
                "light": {k: self.tokens.get("light", {})[k] for k in sorted(self.tokens.get("light", {}))},
                "dark": {k: self.tokens.get("dark", {})[k] for k in sorted(self.tokens.get("dark", {}))},
            },
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


def _is_state_call(call: ast.Call) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id == "State":
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "State":
        return True
    return False


def _is_theme_call(call: ast.Call) -> bool:
    if isinstance(call.func, ast.Attribute) and call.func.attr == "Theme":
        if isinstance(call.func.value, ast.Name) and call.func.value.id == "ui":
            return True
    if isinstance(call.func, ast.Name) and call.func.id == "Theme":
        return True
    return False


class _GraphBuilder:
    def __init__(self, path: str, components: dict) -> None:
        self.path = path
        self.counter = 0
        self.graph = SemanticGraph(tokens=default_tokens())
        self.dep = DependencyGraph()
        self._theme_nodes: dict[str, str] = {}
        self._page_route_by_node: dict[str, str] = {}
        self.components = components
        for name, cdef in components.items():
            self.graph.components[name] = {
                "name": name,
                "style": cdef.style,
                "params": list(cdef.params),
                "line": cdef.span_line,
            }

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

    def register_state(self, name: str, call: ast.Call) -> None:
        initial: Any = None
        if call.args:
            initial = literal_value(call.args[0])
        self.graph.states[name] = {
            "name": name,
            "initial": initial,
            "span": span_for(self.path, call).to_dict(),
        }

    def register_theme(self, call: ast.Call) -> None:
        attrs: dict[str, Any] = {}
        for kw in call.keywords:
            if kw.arg is None:
                continue
            attrs[kw.arg] = literal_value(kw.value)
        light, dark = theme_kwargs_to_overrides(attrs)
        self.graph.tokens = apply_theme_overrides(self.graph.tokens, light=light, dark=dark)

    def _maybe_state_ref(self, node: ast.AST) -> dict[str, str] | None:
        if isinstance(node, ast.Name) and node.id in self.graph.states:
            return {"__state__": node.id}
        return None

    def _resolve_call(self, call: ast.Call, trail: list[str]) -> tuple[ast.Call, list[str]]:
        """Expand user components until a ui.* call remains."""
        while component_call_name(call, self.components):
            name = component_call_name(call, self.components)
            assert name is not None
            expanded = expand_component_call(call, self.components)
            if expanded is None:
                break
            trail = [*trail, name]
            call = expanded
        return call, trail

    def build_call(
        self,
        call: ast.Call,
        parent_id: str | None = None,
        expansion_trail: list[str] | None = None,
    ) -> str | None:
        trail = list(expansion_trail or [])
        call, trail = self._resolve_call(call, trail)

        kind = call_kind(call)
        if kind is None:
            return None

        nid = self.next_id()
        attrs: dict[str, Any] = {}
        child_ids: list[str] = []

        for arg in call.args:
            if isinstance(arg, ast.Call):
                cid = self.build_call(arg, parent_id=nid, expansion_trail=trail)
                if cid:
                    child_ids.append(cid)
                    continue
            if isinstance(arg, ast.List):
                for elt in arg.elts:
                    if isinstance(elt, ast.Call):
                        cid = self.build_call(elt, parent_id=nid, expansion_trail=trail)
                        if cid:
                            child_ids.append(cid)
                continue
            state_ref = self._maybe_state_ref(arg)
            if state_ref and kind in {"Button", "Text", "Card", "Link"} and "text" not in attrs:
                attrs["text"] = state_ref
                continue
            val = literal_value(arg)
            if isinstance(val, str):
                if kind in {"Button", "Text", "Card", "Link"} and "text" not in attrs:
                    attrs["text"] = val
                elif kind in FORM_CONTROL_KINDS and "name" not in attrs:
                    attrs["name"] = val
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
                        if isinstance(elt, ast.Call):
                            cid = self.build_call(elt, parent_id=nid, expansion_trail=trail)
                            if cid:
                                child_ids.append(cid)
                elif isinstance(val_node, ast.Call):
                    cid = self.build_call(val_node, parent_id=nid, expansion_trail=trail)
                    if cid:
                        child_ids.append(cid)
                continue
            if kind == "Nav" and kw.arg == "brand" and isinstance(kw.value, ast.Call):
                cid = self.build_call(kw.value, parent_id=nid, expansion_trail=trail)
                if cid:
                    attrs["brand"] = cid
                    child_ids.append(cid)
                continue
            if kind == "Nav" and kw.arg in {"items", "actions"}:
                slot_ids: list[str] = []
                val_node = kw.value
                if isinstance(val_node, (ast.List, ast.Tuple)):
                    for elt in val_node.elts:
                        if isinstance(elt, ast.Call):
                            cid = self.build_call(elt, parent_id=nid, expansion_trail=trail)
                            if cid:
                                slot_ids.append(cid)
                                child_ids.append(cid)
                elif isinstance(val_node, ast.Call):
                    cid = self.build_call(val_node, parent_id=nid, expansion_trail=trail)
                    if cid:
                        slot_ids.append(cid)
                        child_ids.append(cid)
                attrs[kw.arg] = slot_ids
                continue
            if kind == "Nav" and kw.arg == "placement":
                place = literal_value(kw.value)
                if isinstance(place, str):
                    attrs["placement"] = place if place in NAV_PLACEMENTS else "sticky-top"
                continue
            if kind == "Nav" and kw.arg == "tone":
                tone = literal_value(kw.value)
                if isinstance(tone, str):
                    attrs["tone"] = tone if tone in NAV_TONES else "solid"
                continue
            if kw.arg == "route" and kind == "Page":
                route_val = literal_value(kw.value)
                if isinstance(route_val, str):
                    self._page_route_by_node[nid] = route_val
                continue
            if kw.arg == "on_click":
                if isinstance(kw.value, ast.Name):
                    attrs["on_click"] = {"__handler__": kw.value.id}
                elif isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    attrs["on_click"] = {"__handler__": kw.value.value}
                else:
                    attrs["on_click"] = literal_value(kw.value)
                continue
            if kw.arg in {"text", "title", "subtitle", "bind", "value"}:
                state_ref = self._maybe_state_ref(kw.value)
                if state_ref:
                    if kw.arg == "bind":
                        attrs["value" if kind in FORM_CONTROL_KINDS else "text"] = state_ref
                    elif kw.arg == "value":
                        attrs["value"] = state_ref
                    else:
                        attrs[kw.arg] = state_ref
                    continue
            if kw.arg == "type" and kind == "Input":
                type_val = literal_value(kw.value)
                if isinstance(type_val, str):
                    attrs["type"] = type_val if type_val in INPUT_TYPES else "text"
                continue
            if isinstance(kw.value, ast.Call):
                cid = self.build_call(kw.value, parent_id=nid, expansion_trail=trail)
                if cid:
                    attrs[kw.arg] = {"__node__": cid}
                    child_ids.append(cid)
                    continue
            attrs[kw.arg] = literal_value(kw.value)

        if kind == "Nav":
            attrs.setdefault("placement", "sticky-top")
            attrs.setdefault("tone", "solid")

        provenance = ["parse:ui_call", "analyze:semantic_graph", *[f"expand:{n}" for n in trail]]
        node = Node(
            id=nid,
            kind=kind,
            span=span_for(self.path, call),
            attributes=attrs,
            children=child_ids,
            provenance=provenance,
            metadata={"expanded_from": list(trail)} if trail else {},
        ).with_hash()
        self.graph.nodes[nid] = node

        if parent_id:
            self.graph.edges.append({"from": parent_id, "to": nid, "kind": "contains"})
        else:
            self.graph.roots.append(nid)
            if kind == "Page" and nid in self._page_route_by_node:
                route_path = self._page_route_by_node[nid]
                if route_path in self.graph.routes:
                    raise ValueError(f"Duplicate route: {route_path!r}")
                self.graph.routes[route_path] = nid

        for key, value in attrs.items():
            if key in THEME_ATTR_KEYS and isinstance(value, str):
                tid = self.theme_node(value, call)
                self.dep.edges.append({"from": nid, "to": tid, "kind": "uses_theme"})
                self.graph.edges.append({"from": nid, "to": tid, "kind": "uses_theme"})
            if key == "on_click" and isinstance(value, dict) and "__handler__" in value:
                handler = value["__handler__"]
                self.dep.edges.append({"from": nid, "to": handler, "kind": "on_click"})
                self.graph.edges.append({"from": nid, "to": handler, "kind": "calls_handler"})
            if isinstance(value, dict) and "__state__" in value:
                state_name = value["__state__"]
                self.dep.edges.append({"from": nid, "to": state_name, "kind": "reads_state"})
                self.graph.edges.append({"from": nid, "to": state_name, "kind": "reads_state"})

        return nid

    def visit_module(self, module: ast.Module) -> None:
        for stmt in module.body:
            if isinstance(stmt, ast.FunctionDef):
                if any(_is_server_decorator(d) for d in stmt.decorator_list):
                    self.register_handler(stmt.name, kind="server", at=stmt)
                elif stmt.name not in self.components:
                    self.register_handler(stmt.name, kind="client", at=stmt)
            elif isinstance(stmt, ast.Assign):
                if isinstance(stmt.value, ast.Call) and _is_state_call(stmt.value):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name):
                            self.register_state(target.id, stmt.value)
                elif isinstance(stmt.value, ast.Call) and _is_theme_call(stmt.value):
                    self.register_theme(stmt.value)
                elif isinstance(stmt.value, ast.Call):
                    self.build_call(stmt.value)
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                if _is_theme_call(stmt.value):
                    self.register_theme(stmt.value)
                else:
                    self.build_call(stmt.value)
        self._finalize_routes()

    def _finalize_routes(self) -> None:
        page_roots = [nid for nid in self.graph.roots if self.graph.nodes[nid].kind == "Page"]
        unrouted = [nid for nid in page_roots if nid not in self._page_route_by_node]
        if len(page_roots) == 1 and not self.graph.routes:
            self.graph.routes["/"] = page_roots[0]
        elif unrouted:
            raise ValueError(
                "Multiple ui.Page definitions require route= on each page "
                f"(missing route on {len(unrouted)} page(s))"
            )


def _display_path(path: Path) -> str:
    path = path.resolve()
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_semantic_graph(path: str | Path) -> tuple[SemanticGraph, DependencyGraph]:
    path = Path(path)
    module = parse_file(path)
    components = collect_components(module)
    builder = _GraphBuilder(_display_path(path), components)
    builder.visit_module(module)
    builder.graph.roots = sorted(set(builder.graph.roots))
    return builder.graph, builder.dep
