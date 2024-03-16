#!/bin/bash

echo "Running alembic migrations"
alembic upgrade head

echo "Starting server"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8002