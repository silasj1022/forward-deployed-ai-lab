#!/usr/bin/env python3
"""Minimal production-image smoke test."""

from fastapi.testclient import TestClient

from forward_deployed_ai_lab.app import create_app

client = TestClient(create_app())
response = client.get("/api/v1/health")
response.raise_for_status()
assert response.json()["status"] == "ok"
print("smoke test passed")
