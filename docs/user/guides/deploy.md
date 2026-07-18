# Deploy an OurUI app

OurUI apps are Python modules compiled to HTML/CSS/JS and served with `ourui serve`.

## Local

```bash
pip install ourui
ourui serve app.py --port 8765
```

Production-ish (sessions, no HMR):

```bash
ourui serve app.py --prod --workers 2 --session-dir /var/lib/ourui/sessions
```

## Docker (recipe)

Sample charts live under [`deploy/`](../../../deploy/) in the repo:

| File | Purpose |
|------|---------|
| `deploy/Dockerfile` | Slim image; `ourui serve … --prod` |
| `deploy/docker-compose.yml` | Local compose with port publish |
| `deploy/k8s/deployment.yaml` | Minimal Deployment + Service |

Build and run Compose from the repo root (after copying your app into the image context, or mounting it):

```bash
docker compose -f deploy/docker-compose.yml up --build
```

Standalone Dockerfile sketch (same idea as `deploy/Dockerfile`):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir ourui>=1.9.1
COPY app.py .
EXPOSE 8765
CMD ["ourui", "serve", "app.py", "--host", "0.0.0.0", "--port", "8765", "--prod"]
```

Pin `ourui` to the release you ship (see [CHANGELOG](../../../CHANGELOG.md)).

## Kubernetes

Apply the sample chart (edit image/name/command for your registry):

```bash
kubectl apply -f deploy/k8s/deployment.yaml
```

The sample runs `ourui serve` with `--prod` on port **8765** and exposes a ClusterIP Service. Add Ingress, probes (`GET /__ourui/health`), and session volume mounts as needed for multi-replica.

## Static emit + RPC

```bash
ourui emit app.py -o dist/index.html
```

Static HTML still needs a host that implements `POST /__ourui/call/<handler>` (the same contract as `ourui serve`) for `@server` handlers. Prefer `ourui serve` unless you embed the host yourself.

## Health

With `--prod`, `GET /__ourui/health` returns JSON status.

## Production security env

| Variable | Default | Effect |
|----------|---------|--------|
| `OURUI_COOKIE_SECURE` | off | Add `Secure` to `ourui_sid` (use behind HTTPS) |
| `OURUI_RPC_RATE_LIMIT` | `60` | Max RPC calls per minute per client key; `0` disables |
| `OURUI_SESSION_DIR` | (see CLI) | File session store directory |

See [Trust and compliance](trust-and-compliance.md) and [Threat model](threat-model.md). Auth belongs in front of the host — [enterprise gateway](../../../examples/enterprise/gateway/).

## CI emit

See [`.github/workflows/ci-emit.yml`](../../../.github/workflows/ci-emit.yml) — on PR/push: secret scan, install editable package, `pytest tests/p0`, `ourui check` on enterprise examples, and `ourui emit` for `crud_app`.

## Trusted Publishing (PyPI)

Release workflow: [`.github/workflows/publish-pypi.yml`](../../../.github/workflows/publish-pypi.yml) (triggered by GitHub Release or `workflow_dispatch`).

**API token (recommended):** create a PyPI token, then:

```bash
gh secret set PYPI_API_TOKEN --body 'pypi-…'
gh workflow run publish-pypi.yml
```

**Trusted Publisher (OIDC):** on [PyPI → ourui → Publishing](https://pypi.org/manage/project/ourui/settings/publishing/), add:

| Field | Value |
|-------|--------|
| Owner | `sukirman1901` |
| Repository | `OurUI` |
| Workflow | `publish-pypi.yml` |
| Environment | *(leave blank)* |

Until one of those is configured, local upload:

```bash
python -m build packages/ourui
TWINE_USERNAME=__token__ TWINE_PASSWORD=pypi-… twine upload packages/ourui/dist/*
```
