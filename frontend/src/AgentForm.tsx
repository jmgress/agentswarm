import { useState } from 'react'
import './AgentForm.css'

export interface MCPConnectionInfo {
  endpoint_url: string
  metadata?: Record<string, any>
}

export interface AgentFormData {
  name: string
  agent_type: 'utility' | 'task' | 'orchestration'
  description: string
  mcp_connection: MCPConnectionInfo
}

export interface Agent extends AgentFormData {
  id: string
  created_at: string
}

interface AgentFormProps {
  onSubmit: (agent: AgentFormData) => Promise<void>
  isLoading: boolean
}

export function AgentForm({ onSubmit, isLoading }: AgentFormProps) {
  const [formData, setFormData] = useState<AgentFormData>({
    name: '',
    agent_type: 'utility',
    description: '',
    mcp_connection: {
      endpoint_url: '',
      metadata: {}
    }
  })

  const [metadataText, setMetadataText] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Parse metadata if provided
    let metadata = {}
    if (metadataText.trim()) {
      try {
        metadata = JSON.parse(metadataText)
      } catch (error) {
        alert('Invalid JSON in metadata field')
        return
      }
    }

    const agentData = {
      ...formData,
      mcp_connection: {
        endpoint_url: formData.mcp_connection.endpoint_url,
        metadata: Object.keys(metadata).length > 0 ? metadata : undefined
      }
    }

    await onSubmit(agentData)
    
    // Reset form on successful submission
    setFormData({
      name: '',
      agent_type: 'utility',
      description: '',
      mcp_connection: { endpoint_url: '', metadata: {} }
    })
    setMetadataText('')
  }

  const handleInputChange = (field: keyof AgentFormData, value: string) => {
    if (field === 'mcp_connection') {
      setFormData(prev => ({
        ...prev,
        mcp_connection: { ...prev.mcp_connection, endpoint_url: value }
      }))
    } else {
      setFormData(prev => ({ ...prev, [field]: value }))
    }
  }

  return (
    <div className="agent-form-container">
      <h2>Create New Agent</h2>
      <form onSubmit={handleSubmit} className="agent-form">
        <div className="form-group">
          <label htmlFor="name">Agent Name *</label>
          <input
            type="text"
            id="name"
            value={formData.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            required
            disabled={isLoading}
            placeholder="Enter agent name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="agent_type">Agent Type *</label>
          <select
            id="agent_type"
            value={formData.agent_type}
            onChange={(e) => handleInputChange('agent_type', e.target.value as AgentFormData['agent_type'])}
            required
            disabled={isLoading}
          >
            <option value="utility">Utility</option>
            <option value="task">Task</option>
            <option value="orchestration">Orchestration</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            required
            disabled={isLoading}
            placeholder="Describe the agent's purpose and capabilities"
            rows={3}
          />
        </div>

        <div className="form-group">
          <label htmlFor="endpoint_url">MCP Endpoint URL *</label>
          <input
            type="url"
            id="endpoint_url"
            value={formData.mcp_connection.endpoint_url}
            onChange={(e) => handleInputChange('mcp_connection', e.target.value)}
            required
            disabled={isLoading}
            placeholder="http://localhost:8080/mcp"
          />
        </div>

        <div className="form-group">
          <label htmlFor="metadata">MCP Metadata (JSON, optional)</label>
          <textarea
            id="metadata"
            value={metadataText}
            onChange={(e) => setMetadataText(e.target.value)}
            disabled={isLoading}
            placeholder='{"version": "1.0", "protocol": "http"}'
            rows={3}
          />
          <small>Enter valid JSON for additional MCP connection metadata</small>
        </div>

        <button type="submit" disabled={isLoading} className="submit-button">
          {isLoading ? 'Creating Agent...' : 'Create Agent'}
        </button>
      </form>
    </div>
  )
}