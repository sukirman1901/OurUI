# ADR-003: File-backed multi-worker sessions

**Status:** Accepted  
**Date:** 2026-07-18  
**Tag:** `compiler-p0o`

## Context

Phase N shipped single-process `--prod` with in-memory sessions. Horizontal scale needed a shared store without introducing Redis yet.

## Decision

1. Add `FileSessionStore`: one JSON file per `ourui_sid` under `--session-dir` or `OURUI_SESSION_DIR`, locked with `fcntl.flock`.
2. Auto-select file store when `--workers > 1` or a session directory is set; otherwise keep in-memory for single-process `--prod`.
3. Multi-worker serve: parent binds a listening socket; `N` forked children share it (`--workers` requires `--prod`).
4. Defer Redis / external stores to a later phase.

## Consequences

- Workers can share session State on one machine via the filesystem.
- Cross-host multi-machine deploy still needs a networked store (future ADR).
- Runtime (multi-worker, file-backed) is Stable on Unix; Windows without `fcntl` is unsupported for file store.
