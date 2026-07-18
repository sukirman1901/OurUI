from __future__ import annotations

import ast
import copy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ComponentDef:
    name: str
    params: list[str]
    template: ast.Call
    style: str  # "function" | "class"
    span_line: int = 0


def _is_ui_call(call: ast.Call) -> bool:
    func = call.func
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id == "ui"
    return False


def _inherits_component(bases: list[ast.expr]) -> bool:
    for base in bases:
        if isinstance(base, ast.Name) and base.id == "Component":
            return True
        if isinstance(base, ast.Attribute) and base.attr == "Component":
            return True
    return False


def _return_call(fn: ast.FunctionDef) -> ast.Call | None:
    body = [s for s in fn.body if not isinstance(s, (ast.Pass, ast.Expr))]
    # allow docstring Expr as first
    stmts = list(fn.body)
    if stmts and isinstance(stmts[0], ast.Expr) and isinstance(stmts[0].value, ast.Constant):
        stmts = stmts[1:]
    if len(stmts) != 1 or not isinstance(stmts[0], ast.Return):
        return None
    value = stmts[0].value
    if isinstance(value, ast.Call):
        return value
    return None


def collect_components(module: ast.Module) -> dict[str, ComponentDef]:
    components: dict[str, ComponentDef] = {}

    for stmt in module.body:
        if isinstance(stmt, ast.FunctionDef):
            # skip @server handlers
            if any(
                (isinstance(d, ast.Name) and d.id == "server")
                or (isinstance(d, ast.Attribute) and d.attr == "server")
                for d in stmt.decorator_list
            ):
                continue
            ret = _return_call(stmt)
            if ret is None:
                continue
            # Must be ui.* or another component name (resolved later)
            params = [a.arg for a in stmt.args.args]
            components[stmt.name] = ComponentDef(
                name=stmt.name,
                params=params,
                template=ret,
                style="function",
                span_line=stmt.lineno,
            )
        elif isinstance(stmt, ast.ClassDef) and _inherits_component(stmt.bases):
            init_params: list[str] = []
            build_fn: ast.FunctionDef | None = None
            for item in stmt.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    # skip self
                    init_params = [a.arg for a in item.args.args[1:]]
                if isinstance(item, ast.FunctionDef) and item.name == "build":
                    build_fn = item
            if build_fn is None:
                continue
            ret = _return_call(build_fn)
            if ret is None:
                continue
            # Prefer __init__ params; else build params without self
            params = init_params or [a.arg for a in build_fn.args.args[1:]]
            components[stmt.name] = ComponentDef(
                name=stmt.name,
                params=params,
                template=ret,
                style="class",
                span_line=stmt.lineno,
            )

    return components


class _Subst(ast.NodeTransformer):
    def __init__(self, mapping: dict[str, ast.AST], *, class_style: bool) -> None:
        self.mapping = mapping
        self.class_style = class_style

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id in self.mapping:
            return copy.deepcopy(self.mapping[node.id])
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
        self.generic_visit(node)
        if (
            self.class_style
            and isinstance(node.value, ast.Name)
            and node.value.id == "self"
            and node.attr in self.mapping
        ):
            return copy.deepcopy(self.mapping[node.attr])
        return node


def bind_call_args(call: ast.Call, params: list[str]) -> dict[str, ast.AST]:
    mapping: dict[str, ast.AST] = {}
    for i, arg in enumerate(call.args):
        if i < len(params):
            mapping[params[i]] = arg
    for kw in call.keywords:
        if kw.arg and kw.arg in params:
            mapping[kw.arg] = kw.value
    return mapping


def expand_component_call(
    call: ast.Call,
    components: dict[str, ComponentDef],
    *,
    depth: int = 0,
) -> ast.Call | None:
    """If call is a user component, return expanded ui.* Call (fully expanded)."""
    if depth > 16:
        raise RecursionError("component expansion exceeded depth limit")
    if not isinstance(call.func, ast.Name):
        return None
    name = call.func.id
    if name not in components:
        return None
    cdef = components[name]
    mapping = bind_call_args(call, cdef.params)
    template = copy.deepcopy(cdef.template)
    substituted = _Subst(mapping, class_style=cdef.style == "class").visit(template)
    ast.fix_missing_locations(substituted)
    if not isinstance(substituted, ast.Call):
        return None
    # Recurse if still a component
    while isinstance(substituted.func, ast.Name) and substituted.func.id in components:
        nested = expand_component_call(substituted, components, depth=depth + 1)
        if nested is None:
            break
        substituted = nested
    return substituted


def component_call_name(call: ast.Call, components: dict[str, ComponentDef]) -> str | None:
    if isinstance(call.func, ast.Name) and call.func.id in components:
        return call.func.id
    return None
