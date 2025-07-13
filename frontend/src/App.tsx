import { useState, useEffect } from 'react';
import AgentForm from './components/AgentForm';
import './App.css';

interface Agent {
  name: string;
  type: string;
  description: string;
  mcp_connection: {
    endpoint: string;
    metadata?: object;
  };
}

function App() {
  const [agents, setAgents] = useState<Agent[]>([]);

  const fetchAgents = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents');
      if (response.ok) {
        const data = await response.json();
        setAgents(data);
      }
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  return (
    <div className="App">
      <h1>AgentSwarm</h1>
      <AgentForm onAgentCreated={fetchAgents} />
      <div className="agents-list">
        <h2>Available Agents</h2>
        {agents.length === 0 ? (
          <p>No agents created yet.</p>
        ) : (
          <ul>
            {agents.map((agent, index) => (
              <li key={index}>
                <strong>{agent.name}</strong> ({agent.type}) - {agent.description}
                <br />
                <small>MCP Endpoint: {agent.mcp_connection.endpoint}</small>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
