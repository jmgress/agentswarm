import { useState, useEffect, type FormEvent } from 'react'
import './AgentForm.css'

export interface MCPConnectionInfo {
  endpoint_url: string
  metadata?: Record<string, unknown>
}

export interface ProviderConfig {
  provider_id: string
  provider_type: 'ollama' | 'openai' | 'gemini'
  model: string
  config?: Record<string, unknown>
  fallback_providers?: string[]
}

export interface AgentFormData {
  name: string
  agent_type: 'utility' | 'task' | 'orchestration'
  description: string
  mcp_connection: MCPConnectionInfo
  provider_config?: ProviderConfig
}

export interface Agent extends AgentFormData {
  id: string
  created_at: string
}

export interface Provider {
  provider_id: string
  provider_type: 'ollama' | 'openai' | 'gemini'
  name: string
  description: string
  config: Record<string, unknown>
  default_model: string | null
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
  const [providers, setProviders] = useState<Provider[]>([])
  const [showProviderConfig, setShowProviderConfig] = useState(false)
  
  // Load providers on component mount
  useEffect(() => {
    const loadProviders = async () => {
      try {
        const response = await fetch('http://localhost:8000/providers')
        if (response.ok) {
          const data = await response.json()
          setProviders(data.providers)
        }
      } catch (error) {
        console.error('Failed to load providers:', error)
      }
    }
    loadProviders()
  }, [])

  const handleSubmit = async (e: FormEvent) => {
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

    const agentData: AgentFormData = {
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
    setShowProviderConfig(false)
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

  const handleProviderConfigChange = (field: keyof ProviderConfig, value: any) => {
    setFormData(prev => ({
      ...prev,
      provider_config: {
        ...prev.provider_config,
        provider_id: prev.provider_config?.provider_id || '',
        provider_type: prev.provider_config?.provider_type || 'ollama',
        model: prev.provider_config?.model || '',
        [field]: value
      } as ProviderConfig
    }))
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

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={showProviderConfig}
              onChange={(e) => setShowProviderConfig(e.target.checked)}
              disabled={isLoading}
            />
            Configure AI Provider (optional)
          </label>
        </div>

        {showProviderConfig && (
          <div className="provider-config-section">
            <h3>AI Provider Configuration</h3>
            
            <div className="form-group">
              <label htmlFor="provider_id">Provider</label>
              <select
                id="provider_id"
                value={formData.provider_config?.provider_id || ''}
                onChange={(e) => handleProviderConfigChange('provider_id', e.target.value)}
                disabled={isLoading}
              >
                <option value="">Select a provider</option>
                {providers.map(provider => (
                  <option key={provider.provider_id} value={provider.provider_id}>
                    {provider.name} ({provider.provider_type})
                  </option>
                ))}
              </select>
            </div>

            {formData.provider_config?.provider_id && (
              <>
                <div className="form-group">
                  <label htmlFor="provider_model">Model</label>
                  <input
                    type="text"
                    id="provider_model"
                    value={formData.provider_config?.model || ''}
                    onChange={(e) => handleProviderConfigChange('model', e.target.value)}
                    disabled={isLoading}
                    placeholder="e.g., llama2, gpt-3.5-turbo, gemini-pro"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="provider_type">Provider Type</label>
                  <select
                    id="provider_type"
                    value={formData.provider_config?.provider_type || 'ollama'}
                    onChange={(e) => handleProviderConfigChange('provider_type', e.target.value as ProviderConfig['provider_type'])}
                    disabled={isLoading}
                  >
                    <option value="ollama">Ollama</option>
                    <option value="openai">OpenAI</option>
                    <option value="gemini">Gemini</option>
                  </select>
                </div>
              </>
            )}
          </div>
        )}

        <button type="submit" disabled={isLoading} className="submit-button">
          {isLoading ? 'Creating Agent...' : 'Create Agent'}
        </button>
      </form>
    </div>
  )
}