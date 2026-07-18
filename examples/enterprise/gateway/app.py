"""FastAPI auth gateway in front of OurUI (app-layer — not `ui.*`).

Run (from repo root, with ourui editable + fastapi/uvicorn):

    pip install fastapi uvicorn httpx
    ourui serve examples/enterprise/crud_app.py --prod --port 8765 &
    uvicorn examples.enterprise.gateway.app:app --port 8080

Or: python -m examples.enterprise.gateway.app
"""

from __future__ import annotations

import os
from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

OURUI_UPSTREAM = os.environ.get("OURUI_UPSTREAM", "http://127.0.0.1:8765")
GATEWAY_TOKEN = os.environ.get("OURUI_GATEWAY_TOKEN", "dev-token")

app = FastAPI(title="OurUI auth gateway", version="1.0.0")


def require_bearer(request: Request) -> str:
    """Illustrative auth: Bearer token. Swap for OIDC/session cookie in production."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = auth[7:].strip()
    if token != GATEWAY_TOKEN:
        raise HTTPException(status_code=403, detail="invalid token")
    return token


AuthUser = Annotated[str, Depends(require_bearer)]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"ok": "true", "upstream": OURUI_UPSTREAM}


@app.api_route("/{path:path}", methods=["GET", "POST"])
async def proxy(path: str, request: Request, _user: AuthUser) -> Response:
    """Proxy authenticated traffic to `ourui serve --prod`."""
    target = f"{OURUI_UPSTREAM.rstrip('/')}/{path}"
    if request.url.query:
        target = f"{target}?{request.url.query}"
    body = await request.body()
    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in {"host", "content-length", "authorization"}
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        upstream = await client.request(
            request.method,
            target,
            content=body,
            headers=headers,
        )
    excluded = {"content-encoding", "transfer-encoding", "content-length"}
    out_headers = {
        k: v for k, v in upstream.headers.items() if k.lower() not in excluded
    }
    media = upstream.headers.get("content-type", "application/octet-stream")
    if "text/html" in media:
        return HTMLResponse(content=upstream.content, status_code=upstream.status_code, headers=out_headers)
    if "application/json" in media:
        return JSONResponse(
            content=upstream.json() if upstream.content else {},
            status_code=upstream.status_code,
            headers=out_headers,
        )
    return Response(content=upstream.content, status_code=upstream.status_code, headers=out_headers, media_type=media)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", "8080")))
