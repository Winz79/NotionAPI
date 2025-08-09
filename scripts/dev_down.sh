#!/usr/bin/env bash
# Stop development environment
set -e

docker compose -f docker-compose.dev.yml down
