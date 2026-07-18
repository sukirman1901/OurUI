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
from ourui.design.motion import is_known_motion, resolve_motion
from ourui.node import (
    ALERT_SEVERITIES,
    ALIGN_INTENTS,
    CANVAS_MODES,
    FORM_CONTROL_KINDS,
    IMAGE_FITS,
    INPUT_TYPES,
    JUSTIFY_INTENTS,
    NAV_MENUS,
    NAV_PLACEMENTS,
    NAV_TONES,
    REDUCED_MOTION,
    SPACE_INTENTS,
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
    derived: dict[str, dict[str, Any]] = field(default_factory=dict)
    components: dict[str, dict[str, Any]] = field(default_factory=dict)
    routes: dict[str, str] = field(default_factory=dict)
    tokens: dict[str, dict[str, str]] = field(default_factory=dict)
    density: str = "comfortable"
    page: dict[str, str] | None = None
    scale_overrides: dict[str, dict[str, str]] = field(default_factory=dict)
    author_css: str | None = None
    diagnostics: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "nodes": {nid: n.to_dict() for nid, n in sorted(self.nodes.items())},
            "roots": list(self.roots),
            "routes": {k: self.routes[k] for k in sorted(self.routes)},
            "edges": sorted(self.edges, key=lambda e: (e["from"], e["to"], e["kind"])),
            "handlers": {k: self.handlers[k] for k in sorted(self.handlers)},
            "states": {k: self.states[k] for k in sorted(self.states)},
            "derived": {k: self.derived[k] for k in sorted(self.derived)},
            "components": {k: self.components[k] for k in sorted(self.components)},
            "diagnostics": list(self.diagnostics),
            "density": self.density,
            "tokens": {
                "light": {k: self.tokens.get("light", {})[k] for k in sorted(self.tokens.get("light", {}))},
                "dark": {k: self.tokens.get("dark", {})[k] for k in sorted(self.tokens.get("dark", {}))},
            },
        }
        if self.page:
            out["page"] = dict(self.page)
        if self.scale_overrides:
            out["scale_overrides"] = {k: dict(v) for k, v in self.scale_overrides.items()}
        if self.author_css:
            out["author_css"] = self.author_css
        return out


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


def _is_derived_call(call: ast.Call) -> bool:
    if isinstance(call.func, ast.Name) and call.func.id == "Derived":
        return True
    if isinstance(call.func, ast.Attribute) and call.func.attr == "Derived":
        return True
    return False


def _derived_deps(call: ast.Call) -> list[str]:
    """Collect Name ids referenced inside Derived(...) body (best-effort)."""
    names: set[str] = set()
    for node in ast.walk(call):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id not in {"Derived", "State", "ui", "server"}:
                names.add(node.id)
    return sorted(names)


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
        self._string_constants: dict[str, str] = {}
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
            if isinstance(initial, dict) and "__ref__" in initial:
                ref = str(initial["__ref__"])
                if ref in self._string_constants:
                    initial = self._string_constants[ref]
        self.graph.states[name] = {
            "name": name,
            "initial": initial,
            "span": span_for(self.path, call).to_dict(),
        }

    def register_derived(self, name: str, call: ast.Call) -> None:
        deps = _derived_deps(call)
        # Drop self-name if present
        deps = [d for d in deps if d != name]
        self.graph.derived[name] = {
            "name": name,
            "deps": deps,
            "status": "draft",
            "span": span_for(self.path, call).to_dict(),
        }
        for dep in deps:
            if dep in self.graph.states:
                self.dep.edges.append({"from": name, "to": dep, "kind": "derived_from"})
                self.graph.edges.append({"from": name, "to": dep, "kind": "derived_from"})

    def add_diagnostic(
        self,
        code: str,
        message: str,
        *,
        at: ast.AST | None = None,
    ) -> None:
        span = span_for(self.path, at).to_dict() if at is not None else {
            "path": self.path,
            "start_line": 1,
            "start_col": 0,
            "end_line": 1,
            "end_col": 0,
        }
        self.graph.diagnostics.append(
            {
                "code": code,
                "message": message,
                "path": span.get("path", self.path),
                "start_line": span.get("start_line", 1),
                "end_line": span.get("end_line", 1),
                "start_col": span.get("start_col", 0),
                "end_col": span.get("end_col", 0),
            }
        )

    def register_theme(self, call: ast.Call) -> None:
        attrs: dict[str, Any] = {}
        for kw in call.keywords:
            if kw.arg is None:
                continue
            attrs[kw.arg] = literal_value(kw.value)

        if isinstance(attrs.get("recipe"), str) and str(attrs.get("recipe")).strip():
            self.add_diagnostic(
                "E_THEME",
                "recipe= was removed. Use Theme(density=, page={...}, color overrides) + style intents.",
                at=call,
            )
        if isinstance(attrs.get("pack"), str) and str(attrs.get("pack")).strip():
            self.add_diagnostic(
                "E_THEME",
                "pack= was removed. Use Theme(density=, page={...}, color overrides) + style intents.",
                at=call,
            )

        self.graph.tokens = default_tokens()

        density_explicit = attrs.get("density")
        if isinstance(density_explicit, str) and density_explicit in {"compact", "comfortable"}:
            self.graph.density = density_explicit

        page_raw = attrs.get("page")
        if isinstance(page_raw, dict) and page_raw:
            self.graph.page = {str(k): str(v) for k, v in page_raw.items() if v is not None}

        light, dark = theme_kwargs_to_overrides(attrs)
        self.graph.tokens = apply_theme_overrides(self.graph.tokens, light=light, dark=dark)

        for family in ("space", "sizes", "type"):
            raw = attrs.get(family)
            if isinstance(raw, dict) and raw:
                self.graph.scale_overrides[family] = {
                    str(k): str(v) for k, v in raw.items() if v is not None
                }

        css_raw = attrs.get("css")
        if isinstance(css_raw, dict) and "__ref__" in css_raw:
            ref = str(css_raw["__ref__"])
            if ref in self._string_constants:
                css_raw = self._string_constants[ref]
        if isinstance(css_raw, str) and css_raw.strip():
            self.graph.author_css = css_raw

    def _maybe_state_ref(self, node: ast.AST) -> dict[str, str] | None:
        if isinstance(node, ast.Name) and node.id in self.graph.states:
            return {"__state__": node.id}
        return None

    def _resolve_value(self, node: ast.AST) -> Any:
        """Literal, State ref, or module-level string constant."""
        state_ref = self._maybe_state_ref(node)
        if state_ref:
            return state_ref
        val = literal_value(node)
        if isinstance(val, dict) and "__ref__" in val:
            name = str(val["__ref__"])
            if name in self._string_constants:
                return self._string_constants[name]
            if name in self.graph.states:
                return {"__state__": name}
        return val

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
            if state_ref and kind == "Frame" and "srcdoc" not in attrs:
                attrs["srcdoc"] = state_ref
                continue
            if state_ref and kind in {
                "Button",
                "Text",
                "Card",
                "Link",
                "Code",
                "CopyButton",
            } and "text" not in attrs:
                attrs["text"] = state_ref
                continue
            val = self._resolve_value(arg)
            if isinstance(val, dict) and "__state__" in val:
                if kind == "Frame" and "srcdoc" not in attrs:
                    attrs["srcdoc"] = val
                elif kind in {"Button", "Text", "Card", "Link", "Code", "CopyButton"} and "text" not in attrs:
                    attrs["text"] = val
                else:
                    attrs.setdefault("_args", []).append(val)
                continue
            if isinstance(val, str):
                if kind == "Frame" and "srcdoc" not in attrs:
                    attrs["srcdoc"] = val
                elif kind in {"Button", "Text", "Card", "Link", "CopyButton", "Code", "ThemeToggle", "Menu"} and "text" not in attrs:
                    attrs["text"] = val
                elif kind == "Icon" and "name" not in attrs:
                    attrs["name"] = val
                elif kind == "Image" and "src" not in attrs:
                    attrs["src"] = val
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
            if kind in {"Nav", "Footer"} and kw.arg == "brand" and isinstance(kw.value, ast.Call):
                cid = self.build_call(kw.value, parent_id=nid, expansion_trail=trail)
                if cid:
                    attrs["brand"] = cid
                    child_ids.append(cid)
                continue
            if kind in {"Nav", "Footer", "Menu", "Dialog"} and kw.arg in {"items", "actions", "links", "meta"}:
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
            if kind == "Nav" and kw.arg == "menu":
                menu = literal_value(kw.value)
                if isinstance(menu, str):
                    attrs["menu"] = menu if menu in NAV_MENUS else "none"
                continue
            if kw.arg == "gap":
                gap = literal_value(kw.value)
                if isinstance(gap, str):
                    attrs["gap"] = gap if gap in SPACE_INTENTS else "md"
                continue
            if kw.arg == "pad":
                pad = literal_value(kw.value)
                if isinstance(pad, str):
                    attrs["pad"] = pad if pad in SPACE_INTENTS else "md"
                continue
            if kw.arg == "align":
                align = literal_value(kw.value)
                if isinstance(align, str):
                    attrs["align"] = align if align in ALIGN_INTENTS else "stretch"
                continue
            if kw.arg == "justify":
                justify = literal_value(kw.value)
                if isinstance(justify, str):
                    attrs["justify"] = justify if justify in JUSTIFY_INTENTS else "start"
                continue
            if kw.arg == "motion":
                motion = literal_value(kw.value)
                if isinstance(motion, str):
                    attrs["motion"] = (
                        resolve_motion(motion) if is_known_motion(motion) else "none"
                    )
                continue
            if kind == "Canvas" and kw.arg == "mode":
                mode = literal_value(kw.value)
                if isinstance(mode, str):
                    attrs["mode"] = mode if mode in CANVAS_MODES else "gradient"
                continue
            if kind == "Canvas" and kw.arg == "reduced_motion":
                rm = literal_value(kw.value)
                if isinstance(rm, str):
                    attrs["reduced_motion"] = rm if rm in REDUCED_MOTION else "static"
                continue
            if kind == "Image" and kw.arg == "fit":
                fit = literal_value(kw.value)
                if isinstance(fit, str):
                    attrs["fit"] = fit if fit in IMAGE_FITS else "cover"
                continue
            if kw.arg == "route" and kind == "Page":
                route_val = literal_value(kw.value)
                if isinstance(route_val, str):
                    self._page_route_by_node[nid] = route_val
                continue
            if kw.arg in {"on_click", "on_submit"}:
                if isinstance(kw.value, ast.Name):
                    attrs[kw.arg] = {"__handler__": kw.value.id}
                elif isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    attrs[kw.arg] = {"__handler__": kw.value.value}
                else:
                    attrs[kw.arg] = literal_value(kw.value)
                continue
            if kw.arg in {
                "text",
                "title",
                "subtitle",
                "bind",
                "value",
                "copy",
                "srcdoc",
                "open",
                "show",
                "items",
                "rows",
                "helper",
                "message",
                "disabled",
                "loading",
            }:
                state_ref = self._maybe_state_ref(kw.value)
                if state_ref:
                    if kw.arg == "bind":
                        if kind in FORM_CONTROL_KINDS:
                            attrs["value"] = state_ref
                        elif kind == "Frame":
                            attrs["srcdoc"] = state_ref
                        elif kind in {"Dialog", "Toast"}:
                            attrs["open"] = state_ref
                        elif kind in {"Show", "When"}:
                            attrs["show"] = state_ref
                        elif kind == "List":
                            attrs["items"] = state_ref
                        elif kind == "Table":
                            attrs["rows"] = state_ref
                        else:
                            attrs["text"] = state_ref
                    elif kw.arg == "value":
                        attrs["value"] = state_ref
                    elif kw.arg == "copy":
                        attrs["copy"] = state_ref
                    elif kw.arg == "srcdoc":
                        attrs["srcdoc"] = state_ref
                    elif kw.arg == "open":
                        attrs["open"] = state_ref
                    elif kw.arg == "show":
                        attrs["show"] = state_ref
                    elif kw.arg == "items":
                        attrs["items"] = state_ref
                    elif kw.arg == "rows":
                        attrs["rows"] = state_ref
                    elif kw.arg == "disabled":
                        attrs["disabled"] = state_ref
                    elif kw.arg == "loading":
                        attrs["loading"] = state_ref
                    else:
                        attrs[kw.arg] = state_ref
                    continue
                resolved = self._resolve_value(kw.value)
                if kw.arg == "copy" and isinstance(resolved, str):
                    attrs["copy"] = resolved
                    continue
                if isinstance(resolved, str) and kw.arg in {
                    "text",
                    "title",
                    "subtitle",
                    "srcdoc",
                    "helper",
                    "message",
                }:
                    attrs[kw.arg] = resolved
                    continue
                if isinstance(resolved, dict) and "__state__" in resolved:
                    if kw.arg == "bind":
                        if kind in FORM_CONTROL_KINDS:
                            attrs["value"] = resolved
                        elif kind == "Frame":
                            attrs["srcdoc"] = resolved
                        elif kind in {"Dialog", "Toast"}:
                            attrs["open"] = resolved
                        elif kind in {"Show", "When"}:
                            attrs["show"] = resolved
                        elif kind == "List":
                            attrs["items"] = resolved
                        elif kind == "Table":
                            attrs["rows"] = resolved
                        else:
                            attrs["text"] = resolved
                    else:
                        attrs[kw.arg] = resolved
                    continue
                if kw.arg in {"items", "rows", "disabled", "loading", "show", "open"} and resolved is not None:
                    attrs[kw.arg] = resolved
                    continue
            if kw.arg == "type" and kind == "Input":
                type_val = literal_value(kw.value)
                if isinstance(type_val, str):
                    attrs["type"] = type_val if type_val in INPUT_TYPES else "text"
                continue
            if kw.arg == "severity" and kind == "Alert":
                sev = literal_value(kw.value)
                if isinstance(sev, str):
                    attrs["severity"] = sev if sev in ALERT_SEVERITIES else "info"
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
            attrs.setdefault("menu", "none")
        if kind == "Canvas":
            attrs.setdefault("mode", "gradient")
            attrs.setdefault("reduced_motion", "static")
        if kind == "Image":
            attrs.setdefault("fit", "cover")
            # Do not default alt — missing key is an enterprise a11y signal (empty alt OK).
        if kind == "ThemeToggle":
            attrs.setdefault("text", "Theme")
        if kind == "CopyButton":
            attrs.setdefault("text", "Copy")
        if kind == "Frame":
            attrs.setdefault("title", "Result")
        if kind == "Alert":
            attrs.setdefault("severity", "info")
        if kind == "Empty":
            attrs.setdefault("title", "Nothing here")
        if kind == "Toast":
            attrs.setdefault("text", "Saved")

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
                    self.add_diagnostic(
                        "E001",
                        f"Duplicate route: {route_path!r}",
                        at=call,
                    )
                    raise ValueError(f"Duplicate route: {route_path!r}")
                self.graph.routes[route_path] = nid

        for key, value in attrs.items():
            if key in THEME_ATTR_KEYS and isinstance(value, str):
                tid = self.theme_node(value, call)
                self.dep.edges.append({"from": nid, "to": tid, "kind": "uses_theme"})
                self.graph.edges.append({"from": nid, "to": tid, "kind": "uses_theme"})
            if key in {"on_click", "on_submit"} and isinstance(value, dict) and "__handler__" in value:
                handler = value["__handler__"]
                self.dep.edges.append({"from": nid, "to": handler, "kind": key})
                self.graph.edges.append({"from": nid, "to": handler, "kind": "calls_handler"})
            if isinstance(value, dict) and "__state__" in value:
                state_name = value["__state__"]
                self.dep.edges.append({"from": nid, "to": state_name, "kind": "reads_state"})
                self.graph.edges.append({"from": nid, "to": state_name, "kind": "reads_state"})

        return nid

    def _ingest_sibling_import_strings(self, module: ast.Module) -> None:
        """Load string literals from same-dir `from sibling import NAME` (playground artifacts)."""
        base = Path(self.path).resolve().parent
        for stmt in module.body:
            if not isinstance(stmt, ast.ImportFrom) or not stmt.module:
                continue
            if stmt.level > 1:
                continue
            mod_name = stmt.module.rsplit(".", 1)[-1]
            candidate = base / f"{mod_name}.py"
            if not candidate.is_file():
                continue
            try:
                tree = ast.parse(candidate.read_text(encoding="utf-8"), filename=str(candidate))
            except (OSError, SyntaxError, UnicodeError):
                continue
            aliases = {
                alias.name: (alias.asname or alias.name)
                for alias in stmt.names
                if alias.name != "*"
            }
            if not aliases:
                continue
            for node in tree.body:
                if not isinstance(node, ast.Assign):
                    continue
                if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                    continue
                src_name = node.targets[0].id
                if src_name not in aliases:
                    continue
                raw = literal_value(node.value)
                if isinstance(raw, str):
                    self._string_constants[aliases[src_name]] = raw

    def visit_module(self, module: ast.Module) -> None:
        # First pass: module-level string constants (for ui.Code(NAME) etc.)
        for stmt in module.body:
            if not isinstance(stmt, ast.Assign):
                continue
            if len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
                continue
            raw = literal_value(stmt.value)
            if isinstance(raw, str):
                self._string_constants[stmt.targets[0].id] = raw
        self._ingest_sibling_import_strings(module)

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
                elif isinstance(stmt.value, ast.Call) and _is_derived_call(stmt.value):
                    for target in stmt.targets:
                        if isinstance(target, ast.Name):
                            self.register_derived(target.id, stmt.value)
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
