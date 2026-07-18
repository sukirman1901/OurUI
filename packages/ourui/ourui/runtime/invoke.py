from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


def load_source_module(path: Path) -> ModuleType:
    path = path.resolve()
    name = f"ourui_user_{path.stem}_{abs(hash(path.as_posix()))}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def resolve_handler(module: ModuleType, name: str) -> Callable[..., Any]:
    if not hasattr(module, name):
        raise KeyError(f"handler not found: {name}")
    fn = getattr(module, name)
    if not callable(fn):
        raise TypeError(f"handler is not callable: {name}")
    return fn


def invoke_handler(path: Path, name: str, payload: dict[str, Any] | None = None) -> Any:
    """Execute a handler from the authoring module (dev runtime only)."""
    module = load_source_module(path)
    fn = resolve_handler(module, name)
    payload = payload or {}
    # Prefer kwargs if the function accepts them; otherwise no-arg call.
    try:
        return fn(**payload)
    except TypeError:
        return fn()
