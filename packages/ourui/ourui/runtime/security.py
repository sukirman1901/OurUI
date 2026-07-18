"""Production security helpers: CSRF, rate limit, cookies, headers."""

from __future__ import annotations

import os
import secrets
import threading
import time
from collections import defaultdict, deque
from typing import Any

CSRF_HEADER = "X-OurUI-CSRF"
CSRF_META = "ourui-csrf"
CSRF_BODY_KEY = "_csrf"

SECURITY_HEADERS: tuple[tuple[str, str], ...] = (
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("X-Frame-Options", "SAMEORIGIN"),
    ("Permissions-Policy", "camera=(), microphone=(), geolocation=()"),
)


def new_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def new_csp_nonce() -> str:
    return secrets.token_urlsafe(16)


def validate_csrf(session_token: str | None, provided: str | None) -> bool:
    if not session_token or not provided:
        return False
    return secrets.compare_digest(str(session_token), str(provided))


def extract_csrf_from_payload(payload: dict[str, Any] | None) -> str | None:
    if not payload:
        return None
    raw = payload.get(CSRF_BODY_KEY)
    return str(raw) if raw is not None else None


def cookie_secure_enabled(env: dict[str, str] | None = None) -> bool:
    environ = env if env is not None else os.environ
    return environ.get("OURUI_COOKIE_SECURE", "").strip() in {"1", "true", "yes", "on"}


def rpc_rate_limit(env: dict[str, str] | None = None) -> int:
    """Max RPC calls per minute per client key; 0 disables."""
    environ = env if env is not None else os.environ
    raw = environ.get("OURUI_RPC_RATE_LIMIT", "60").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 60


class RateLimiter:
    """Sliding-window limiter: max ``limit`` events per ``window_s`` per key."""

    def __init__(self, *, limit: int = 60, window_s: float = 60.0) -> None:
        self.limit = limit
        self.window_s = window_s
        self._lock = threading.Lock()
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        if self.limit <= 0:
            return True
        now = time.monotonic()
        with self._lock:
            q = self._hits[key]
            cutoff = now - self.window_s
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= self.limit:
                return False
            q.append(now)
            return True


def csp_content(*, nonce: str | None = None) -> str:
    if nonce:
        script = f"'self' 'nonce-{nonce}'"
    else:
        script = "'self' 'unsafe-inline'"
    return (
        f"default-src 'self'; "
        f"script-src {script}; "
        f"style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        f"font-src 'self' https://fonts.gstatic.com; "
        f"frame-src 'self' blob:; "
        f"base-uri 'self'; "
        f"form-action 'self'"
    )
