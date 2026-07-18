from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from ourui.ui import State

_MODULE_CACHE: dict[str, ModuleType] = {}


def load_source_module(path: Path, *, reload: bool = False) -> ModuleType:
    path = path.resolve()
    key = path.as_posix()
    if not reload and key in _MODULE_CACHE:
        return _MODULE_CACHE[key]
    name = f"ourui_user_{path.stem}_{abs(hash(key)) % (10**8)}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    _MODULE_CACHE[key] = module
    return module


def resolve_handler(module: ModuleType, name: str) -> Callable[..., Any]:
    if not hasattr(module, name):
        raise KeyError(f"handler not found: {name}")
    fn = getattr(module, name)
    if not callable(fn):
        raise TypeError(f"handler is not callable: {name}")
    return fn


def snapshot_states(module: ModuleType) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, value in vars(module).items():
        if name.startswith("_"):
            continue
        if isinstance(value, State):
            out[name] = value.get()
    return out


def invoke_handler(path: Path, name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a handler; return result + live State snapshot."""
    module = load_source_module(path)
    fn = resolve_handler(module, name)
    payload = payload or {}
    try:
        result = fn(**payload)
    except TypeError:
        result = fn()
    return {"result": result, "state": snapshot_states(module)}
