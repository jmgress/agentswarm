import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add backend directory to path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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