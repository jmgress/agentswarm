import os
import pytest
from fastapi.testclient import TestClient

os.environ["AGENTSWARM_DB"] = ":memory:"
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


def test_create_and_list_agents():
    """Test creating a new agent and listing agents"""
    response = client.post(
        "/agents",
        json={
            "name": "TestAgent",
            "agent_type": "utility",
            "description": "test agent",
            "mcp_url": "http://localhost",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "TestAgent"

    # fetch list
    list_resp = client.get("/agents")
    assert list_resp.status_code == 200
    agents = list_resp.json()
    assert any(a["name"] == "TestAgent" for a in agents)