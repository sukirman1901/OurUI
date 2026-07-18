from __future__ import annotations

import threading
import time
from pathlib import Path


class HmrHub:
    """Tracks source mtime and wakes SSE waiters when the file changes."""

    def __init__(self, source: Path) -> None:
        self.source = source.resolve()
        self.generation = 0
        self.mtime_ns = self._read_mtime()
        self._cond = threading.Condition()
        self._stop = False
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()

    def _read_mtime(self) -> int:
        try:
            return self.source.stat().st_mtime_ns
        except OSError:
            return 0

    def _watch_loop(self) -> None:
        while not self._stop:
            time.sleep(0.25)
            current = self._read_mtime()
            if current != self.mtime_ns:
                with self._cond:
                    self.mtime_ns = current
                    self.generation += 1
                    self._cond.notify_all()

    def wait_changed(self, since_generation: int, timeout: float = 20.0) -> int:
        with self._cond:
            if self.generation != since_generation:
                return self.generation
            self._cond.wait(timeout=timeout)
            return self.generation

    def snapshot(self) -> dict[str, int]:
        with self._cond:
            return {"generation": self.generation, "mtime_ns": self.mtime_ns}

    def stop(self) -> None:
        self._stop = True
        with self._cond:
            self._cond.notify_all()
