"""Authoring helpers for examples and future runtime eval.

The P0 compiler does not execute these callables for dump; it parses AST.
They exist so example modules import cleanly if executed.
"""

from __future__ import annotations

from typing import Any


class _UINamespace:
    def __getattr__(self, name: str) -> Any:
        def factory(*args: Any, **kwargs: Any) -> dict[str, Any]:
            children: list[Any] = []
            props = dict(kwargs)
            for arg in args:
                if isinstance(arg, dict) and arg.get("_ourui"):
                    children.append(arg)
                elif "children" not in props and isinstance(arg, list):
                    props["children"] = arg
                elif "children" not in props and not isinstance(arg, (str, int, float, bool)):
                    children.append(arg)
                else:
                    # positional string/content → text/title heuristics
                    if "text" not in props and isinstance(arg, str) and name in {"Button", "Text", "Card"}:
                        props["text"] = arg
                    elif "title" not in props and isinstance(arg, str):
                        props["title"] = arg
                    else:
                        props.setdefault("_args", []).append(arg)
            if children:
                props["children"] = props.get("children", []) + children
            return {"_ourui": True, "kind": name, "props": props}

        return factory


ui = _UINamespace()
