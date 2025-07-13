import pytest
from fastapi.testclient import TestClient
from main import app, agents_storage

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_agents_storage():
    """Clear agents storage before each test"""
    agents_storage.clear()

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_app_title():
    """Test that the app has the correct title"""
    assert app.title == "AgentSwarm API"
    assert app.version == "1.0.0"

def test_create_agent():
    """Test creating a new agent"""
    agent_data = {
        "name": "Test Agent",
        "agent_type": "utility",
        "description": "A test agent for testing purposes",
        "mcp_connection": {
            "endpoint_url": "http://localhost:8080/mcp",
            "metadata": {"version": "1.0", "protocol": "http"}
        }
    }
    
    response = client.post("/agents", json=agent_data)
    assert response.status_code == 200
    
    response_data = response.json()
    assert response_data["name"] == agent_data["name"]
    assert response_data["agent_type"] == agent_data["agent_type"]
    assert response_data["description"] == agent_data["description"]
    assert response_data["mcp_connection"]["endpoint_url"] == agent_data["mcp_connection"]["endpoint_url"]
    assert "id" in response_data
    assert "created_at" in response_data

def test_create_agent_duplicate_name():
    """Test creating an agent with duplicate name fails"""
    agent_data = {
        "name": "Duplicate Agent",
        "agent_type": "task",
        "description": "A test agent",
        "mcp_connection": {
            "endpoint_url": "http://localhost:8080/mcp"
        }
    }
    
    # Create first agent
    response1 = client.post("/agents", json=agent_data)
    assert response1.status_code == 200
    
    # Try to create second agent with same name
    response2 = client.post("/agents", json=agent_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_get_agents_empty():
    """Test getting agents when none exist"""
    response = client.get("/agents")
    assert response.status_code == 200
    assert response.json() == []

def test_get_agents_with_data():
    """Test getting agents after creating some"""
    # Create two agents
    agent1_data = {
        "name": "Agent 1",
        "agent_type": "utility",
        "description": "First agent",
        "mcp_connection": {"endpoint_url": "http://localhost:8080/mcp1"}
    }
    
    agent2_data = {
        "name": "Agent 2", 
        "agent_type": "orchestration",
        "description": "Second agent",
        "mcp_connection": {"endpoint_url": "http://localhost:8080/mcp2"}
    }
    
    client.post("/agents", json=agent1_data)
    client.post("/agents", json=agent2_data)
    
    # Get all agents
    response = client.get("/agents")
    assert response.status_code == 200
    
    agents = response.json()
    assert len(agents) == 2
    assert agents[0]["name"] == "Agent 1"
    assert agents[1]["name"] == "Agent 2"