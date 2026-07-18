FROM python:3.12-slim

WORKDIR /app

# Install OurUI from the monorepo package (CI/build context = repo root).
COPY packages/ourui /tmp/ourui-pkg
RUN pip install --no-cache-dir /tmp/ourui-pkg && rm -rf /tmp/ourui-pkg

# Default app: enterprise CRUD reference (override via compose/k8s).
COPY examples/enterprise/crud_app.py /app/app.py

EXPOSE 8765

CMD ["ourui", "serve", "app.py", "--host", "0.0.0.0", "--port", "8765", "--prod"]
