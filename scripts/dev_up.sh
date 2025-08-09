#!/usr/bin/env bash
# Start development docker-compose environment
set -e

docker compose -f docker-compose.dev.yml up --build
