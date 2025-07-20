import { useState } from 'react'
import { AgentForm, type AgentFormData, type Agent } from './AgentForm'
import './AgentPanel.css'

interface AgentPanelProps {
  agents: Agent[];
  enabledAgents: Set<string>;
  onToggleAgent: (agentId: string) => void;
  onAgentsUpdated: () => Promise<void>;
  isLoading: boolean;
}

export function AgentPanel({ agents, enabledAgents, onToggleAgent, onAgentsUpdated, isLoading }: AgentPanelProps) {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [isCreatingAgent, setIsCreatingAgent] = useState(false);
  const [agentMessage, setAgentMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);

  const createAgent = async (agentData: AgentFormData) => {
    setIsCreatingAgent(true);
    setAgentMessage(null);
    
    try {
      const response = await fetch('http://localhost:8000/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(agentData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create agent');
      }

      const newAgent: Agent = await response.json();
      await onAgentsUpdated();
      setAgentMessage({ type: 'success', text: `Agent "${newAgent.name}" created successfully!` });
      setShowCreateForm(false);
      
      // Clear success message after 3 seconds
      setTimeout(() => setAgentMessage(null), 3000);
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create agent';
      setAgentMessage({ type: 'error', text: errorMessage });
    } finally {
      setIsCreatingAgent(false);
    }
  };

  return (
    <div className="agent-panel">
      <div className="agent-panel-header">
        <h2>Agents</h2>
        <button 
          className="add-agent-button"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? '×' : '+'}
        </button>
      </div>

      {agentMessage && (
        <div className={`agent-message ${agentMessage.type}`}>
          {agentMessage.type === 'success' ? '✅' : '❌'} {agentMessage.text}
        </div>
      )}

      {showCreateForm && (
        <div className="create-agent-section">
          <AgentForm onSubmit={createAgent} isLoading={isCreatingAgent} compact />
        </div>
      )}

      <div className="agents-list">
        {isLoading ? (
          <div className="loading">Loading agents...</div>
        ) : agents.length === 0 ? (
          <div className="empty-state">
            <p>No agents available.</p>
            <p>Create your first agent using the + button above.</p>
          </div>
        ) : (
          <div className="agent-items">
            {agents.map((agent) => (
              <div key={agent.id} className="agent-item">
                <div className="agent-checkbox-section">
                  <label className="agent-checkbox-label">
                    <input
                      type="checkbox"
                      checked={enabledAgents.has(agent.id)}
                      onChange={() => onToggleAgent(agent.id)}
                      className="agent-checkbox"
                    />
                    <span className="agent-name">{agent.name}</span>
                  </label>
                  <span className={`agent-type-badge ${agent.agent_type}`}>
                    {agent.agent_type}
                  </span>
                </div>
                <div className="agent-description">{agent.description}</div>
                <div className="agent-details">
                  <div className="agent-endpoint">
                    <strong>Endpoint:</strong> 
                    <span className="endpoint-url">{agent.mcp_connection.endpoint_url}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="enabled-summary">
        <div className="summary-text">
          {enabledAgents.size > 0 ? (
            <>
              <strong>{enabledAgents.size}</strong> of <strong>{agents.length}</strong> agents enabled
            </>
          ) : (
            <>No agents enabled</>
          )}
        </div>
        {enabledAgents.size > 0 && (
          <button 
            className="clear-all-button"
            onClick={() => enabledAgents.forEach(id => onToggleAgent(id))}
          >
            Clear All
          </button>
        )}
      </div>
    </div>
  );
}