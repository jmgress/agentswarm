import type { Agent } from './AgentForm'
import './AgentList.css'

interface AgentListProps {
  agents: Agent[]
  isLoading: boolean
}

export function AgentList({ agents, isLoading }: AgentListProps) {
  if (isLoading) {
    return (
      <div className="agent-list-container">
        <h2>Agents</h2>
        <div className="loading">Loading agents...</div>
      </div>
    )
  }

  return (
    <div className="agent-list-container">
      <h2>Agents ({agents.length})</h2>
      {agents.length === 0 ? (
        <div className="empty-state">
          No agents created yet. Create your first agent using the form above.
        </div>
      ) : (
        <div className="agent-list">
          {agents.map((agent) => (
            <div key={agent.id} className="agent-card">
              <div className="agent-header">
                <h3>{agent.name}</h3>
                <span className={`agent-type ${agent.agent_type}`}>
                  {agent.agent_type}
                </span>
              </div>
              <p className="agent-description">{agent.description}</p>
              <div className="agent-mcp">
                <strong>MCP Endpoint:</strong> {agent.mcp_connection.endpoint_url}
                {agent.mcp_connection.metadata && (
                  <details className="metadata-details">
                    <summary>Metadata</summary>
                    <pre>{JSON.stringify(agent.mcp_connection.metadata, null, 2)}</pre>
                  </details>
                )}
              </div>
              
              {agent.provider_config && (
                <div className="agent-provider">
                  <strong>AI Provider:</strong> {agent.provider_config.provider_id} ({agent.provider_config.provider_type})
                  <br />
                  <strong>Model:</strong> {agent.provider_config.model}
                  {agent.provider_config.fallback_providers && agent.provider_config.fallback_providers.length > 0 && (
                    <div className="fallback-providers">
                      <strong>Fallback providers:</strong> {agent.provider_config.fallback_providers.join(', ')}
                    </div>
                  )}
                </div>
              )}
              <div className="agent-created">
                Created: {new Date(agent.created_at).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}