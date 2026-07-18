from __future__ import annotations

import importlib.util
import sys
import threading
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from ourui.ui import State

_MODULE_CACHE: dict[str, ModuleType] = {}
_STATE_DEFAULTS: dict[str, dict[str, Any]] = {}
_INVOKE_LOCK = threading.RLock()


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
    _STATE_DEFAULTS[key] = snapshot_states(module)
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


def apply_states(module: ModuleType, values: dict[str, Any] | None, *, path: Path | None = None) -> None:
    """Apply session overlay onto module State.

    When ``values`` is not None, start from module defaults then overlay so an
    empty session does not leak another request's in-memory State.
    """
    if values is None:
        return
    key = path.resolve().as_posix() if path is not None else None
    defaults = _STATE_DEFAULTS.get(key, {}) if key else {}
    merged = {**defaults, **values}
    for name, obj in vars(module).items():
        if name.startswith("_") or not isinstance(obj, State):
            continue
        if name in merged:
            obj.set(merged[name])


def invoke_handler(
    path: Path,
    name: str,
    payload: dict[str, Any] | None = None,
    *,
    state_values: dict[str, Any] | None = None,
    use_lock: bool = False,
) -> dict[str, Any]:
    """Execute a handler; return result + live State snapshot.

    When ``state_values`` is provided, those values are applied onto module
    ``State`` objects before the call (session hydrate). Pass ``use_lock=True``
    from the HTTP server so concurrent requests do not race on module State.
    """

    def _run() -> dict[str, Any]:
        module = load_source_module(path)
        if state_values is not None:
            apply_states(module, state_values, path=path)
        fn = resolve_handler(module, name)
        payload_local = payload or {}
        try:
            result = fn(**payload_local)
        except TypeError:
            result = fn()
        return {"result": result, "state": snapshot_states(module)}

    if use_lock:
        with _INVOKE_LOCK:
            return _run()
    return _run()
