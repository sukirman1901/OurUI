"""Session stores for production runtime (memory + file-backed)."""

from __future__ import annotations

import json
import os
import re
import secrets
import threading
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

try:
    import fcntl
except ImportError:  # pragma: no cover — non-Unix
    fcntl = None  # type: ignore[assignment]

COOKIE_NAME = "ourui_sid"
_SAFE_SID = re.compile(r"^[A-Za-z0-9_-]+$")


@runtime_checkable
class SessionStoreProtocol(Protocol):
    def new_sid(self) -> str: ...

    def get_or_create(self, sid: str | None) -> tuple[str, dict[str, Any], bool]: ...

    def get(self, sid: str) -> dict[str, Any]: ...

    def set(self, sid: str, values: dict[str, Any]) -> None: ...


class SessionStore:
    """Process-local session bag: sid → state snapshot dict."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._sessions: dict[str, dict[str, Any]] = {}

    def new_sid(self) -> str:
        return secrets.token_urlsafe(16)

    def get_or_create(self, sid: str | None) -> tuple[str, dict[str, Any], bool]:
        """Return (sid, values_copy, created)."""
        with self._lock:
            if sid and sid in self._sessions:
                return sid, dict(self._sessions[sid]), False
            new_id = self.new_sid()
            self._sessions[new_id] = {}
            return new_id, {}, True

    def get(self, sid: str) -> dict[str, Any]:
        with self._lock:
            return dict(self._sessions.get(sid, {}))

    def set(self, sid: str, values: dict[str, Any]) -> None:
        with self._lock:
            self._sessions[sid] = dict(values)


class FileSessionStore:
    """Shared session bag on disk (JSON per sid) with exclusive file locks."""

    def __init__(self, directory: Path) -> None:
        if fcntl is None:
            raise RuntimeError("FileSessionStore requires fcntl (Unix)")
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def new_sid(self) -> str:
        return secrets.token_urlsafe(16)

    def _paths(self, sid: str) -> tuple[Path, Path]:
        if not _SAFE_SID.match(sid):
            raise ValueError(f"invalid session id: {sid!r}")
        data = self.directory / f"{sid}.json"
        lock = self.directory / f"{sid}.lock"
        return data, lock

    def _locked(self, sid: str, fn: Any) -> Any:
        data_path, lock_path = self._paths(sid)
        lock_path.touch(exist_ok=True)
        with open(lock_path, "a+", encoding="utf-8") as lf:
            fcntl.flock(lf.fileno(), fcntl.LOCK_EX)
            try:
                return fn(data_path)
            finally:
                fcntl.flock(lf.fileno(), fcntl.LOCK_UN)

    def get_or_create(self, sid: str | None) -> tuple[str, dict[str, Any], bool]:
        if sid and _SAFE_SID.match(sid):
            data_path, _ = self._paths(sid)
            if data_path.exists():
                return sid, self.get(sid), False

        new_id = self.new_sid()

        def write_empty(path: Path) -> None:
            path.write_text("{}", encoding="utf-8")

        self._locked(new_id, write_empty)
        return new_id, {}, True

    def get(self, sid: str) -> dict[str, Any]:
        def read(path: Path) -> dict[str, Any]:
            if not path.exists():
                return {}
            raw = path.read_text(encoding="utf-8")
            if not raw.strip():
                return {}
            data = json.loads(raw)
            return dict(data) if isinstance(data, dict) else {}

        return self._locked(sid, read)

    def set(self, sid: str, values: dict[str, Any]) -> None:
        payload = json.dumps(values, default=str, sort_keys=True)

        def write(path: Path) -> None:
            tmp = path.with_suffix(".tmp")
            tmp.write_text(payload, encoding="utf-8")
            os.replace(tmp, path)

        self._locked(sid, write)


def parse_sid_cookie(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if part.startswith(COOKIE_NAME + "="):
            return part[len(COOKIE_NAME) + 1 :].strip() or None
    return None


def set_cookie_header(sid: str) -> str:
    return f"{COOKIE_NAME}={sid}; Path=/; HttpOnly; SameSite=Lax"


def make_session_store(
    *,
    workers: int = 1,
    session_dir: Path | None = None,
    env: dict[str, str] | None = None,
) -> SessionStoreProtocol:
    """Pick memory vs file store per Phase O rules."""
    environ = env if env is not None else os.environ
    env_dir = environ.get("OURUI_SESSION_DIR")
    directory = session_dir
    if directory is None and env_dir:
        directory = Path(env_dir)
    if workers > 1 or directory is not None:
        if directory is None:
            directory = Path(environ.get("TMPDIR", "/tmp")) / "ourui-sessions"
        return FileSessionStore(directory)
    return SessionStore()
