"""In-memory session store for single-process production runtime."""

from __future__ import annotations

import secrets
import threading
from typing import Any


COOKIE_NAME = "ourui_sid"


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
