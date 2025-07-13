import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_app_title():
    """Test that the app has the correct title"""
    assert app.title == "AgentSwarm API"
    assert app.version == "1.0.0"