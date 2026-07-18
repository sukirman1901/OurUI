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

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8765
CMD ["ourui", "serve", "app.py", "--host", "0.0.0.0", "--port", "8765", "--prod"]
```

`requirements.txt` should pin `ourui>=1.0.0`.

## Static emit + RPC

```bash
ourui emit app.py -o dist/index.html
```

Static HTML still needs a host that implements `POST /__ourui/call/<handler>` (the same contract as `ourui serve`) for `@server` handlers. Prefer `ourui serve` unless you embed the host yourself.

## Health

With `--prod`, `GET /__ourui/health` returns JSON status.
