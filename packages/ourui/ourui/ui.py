"""Authoring helpers for examples and future runtime eval.

The compiler parses AST for dump/emit; State/server objects are used at runtime by `ourui serve`.
"""

from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

F = TypeVar("F", bound=Callable[..., Any])
T = TypeVar("T")


def server(fn: F) -> F:
    """Mark a function as a server handler (Behavior Domain)."""
    setattr(fn, "__ourui_server__", True)
    return fn


class State(Generic[T]):
    """Reactive server-side state (Phase H). Mutate via get/set in @server handlers."""

    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value


class Component:
    """Base class for class-style components (expanded at Analyze)."""

    def build(self) -> Any:
        raise NotImplementedError


def component(fn: F) -> F:
    """Optional marker for function components (auto-detected by return ui.*)."""
    setattr(fn, "__ourui_component__", True)
    return fn


class _UINamespace:
    def __getattr__(self, name: str) -> Any:
        def factory(*args: Any, **kwargs: Any) -> dict[str, Any]:
            children: list[Any] = []
            props = dict(kwargs)
            for arg in args:
                if isinstance(arg, dict) and arg.get("_ourui"):
                    children.append(arg)
                elif isinstance(arg, State):
                    props["text"] = arg
                elif "children" not in props and isinstance(arg, list):
                    props["children"] = arg
                elif "children" not in props and not isinstance(arg, (str, int, float, bool)):
                    children.append(arg)
                else:
                    if "text" not in props and isinstance(arg, str) and name in {
                        "Button", "Text", "Card", "Link", "CopyButton", "Code", "Menu"
                    }:
                        props["text"] = arg
                    elif name == "Icon" and "name" not in props and isinstance(arg, str):
                        props["name"] = arg
                    elif name == "Image" and "src" not in props and isinstance(arg, str):
                        props["src"] = arg
                    elif name in {"Input", "Select", "Toggle", "Slider"} and "name" not in props and isinstance(arg, str):
                        props["name"] = arg
                    elif "title" not in props and isinstance(arg, str):
                        props["title"] = arg
                    else:
                        props.setdefault("_args", []).append(arg)
            if children:
                props["children"] = props.get("children", []) + children
            return {"_ourui": True, "kind": name, "props": props}

        return factory


ui = _UINamespace()
