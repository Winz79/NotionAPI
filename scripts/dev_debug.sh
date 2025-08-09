#!/usr/bin/env bash
# Start dev container with debugpy listening
set -e

docker compose -f docker-compose.dev.yml up --build -d

echo "To attach debugger: run the 'Attach to Docker: Notion API' launch config in VS Code (connect to localhost:5678)"

echo "To start container with debugpy enabled, exec into the container and run uvicorn with debugpy:"

echo "docker compose exec notion-api bash -c \"python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000\""
