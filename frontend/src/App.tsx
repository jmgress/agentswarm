import { useState, useEffect, FormEvent } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

interface HealthStatus {
  status: string;
}

interface Agent {
  id: number
  name: string
  agent_type: string
  description?: string
  mcp_url?: string
}

function App() {
  const [count, setCount] = useState(0)
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [agents, setAgents] = useState<Agent[]>([])
  const [name, setName] = useState('')
  const [agentType, setAgentType] = useState('utility')
  const [description, setDescription] = useState('')
  const [mcpUrl, setMcpUrl] = useState('')
  const [formMessage, setFormMessage] = useState<string | null>(null)

  const checkBackendHealth = async () => {
    setIsLoading(true)
    setHealthError(null)
    try {
      const response = await fetch('http://localhost:8000/health')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: HealthStatus = await response.json()
      setHealthStatus(data)
    } catch (error) {
      setHealthError(error instanceof Error ? error.message : 'Failed to connect to backend')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchAgents = async () => {
    const resp = await fetch('http://localhost:8000/agents')
    if (resp.ok) {
      const data: Agent[] = await resp.json()
      setAgents(data)
    }
  }

  const handleCreateAgent = async (e: FormEvent) => {
    e.preventDefault()
    setFormMessage(null)
    const resp = await fetch('http://localhost:8000/agents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        agent_type: agentType,
        description,
        mcp_url: mcpUrl,
      }),
    })
    if (resp.ok) {
      setName('')
      setAgentType('utility')
      setDescription('')
      setMcpUrl('')
      setFormMessage('Agent created!')
      fetchAgents()
    } else {
      setFormMessage('Failed to create agent')
    }
  }

  useEffect(() => {
    checkBackendHealth()
    fetchAgents()
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>AgentSwarm - Frontend</h1>
      
      <div className="card">
        <h2>Backend Health Status</h2>
        <button onClick={checkBackendHealth} disabled={isLoading}>
          {isLoading ? 'Checking...' : 'Check Backend Health'}
        </button>
        
        {healthStatus && (
          <div style={{ marginTop: '10px', padding: '10px', backgroundColor: '#d4edda', border: '1px solid #c3e6cb', borderRadius: '4px' }}>
            ✅ Backend Status: <strong>{healthStatus.status}</strong>
          </div>
        )}
        
        {healthError && (
          <div style={{ marginTop: '10px', padding: '10px', backgroundColor: '#f8d7da', border: '1px solid #f5c6cb', borderRadius: '4px' }}>
            ❌ Error: {healthError}
          </div>
        )}
      </div>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Create Agent</h2>
        <form onSubmit={handleCreateAgent} data-testid="agent-form">
          <div>
            <label>
              Agent Name
              <input value={name} onChange={e => setName(e.target.value)} />
            </label>
          </div>
          <div>
            <label>
              Agent Type
              <select value={agentType} onChange={e => setAgentType(e.target.value)}>
                <option value="utility">utility</option>
                <option value="task">task</option>
                <option value="orchestration">orchestration</option>
              </select>
            </label>
          </div>
          <div>
            <label>
              Description
              <input value={description} onChange={e => setDescription(e.target.value)} />
            </label>
          </div>
          <div>
            <label>
              MCP URL
              <input value={mcpUrl} onChange={e => setMcpUrl(e.target.value)} />
            </label>
          </div>
          <button type="submit">Create</button>
        </form>
        {formMessage && <p>{formMessage}</p>}
      </div>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Agents</h2>
        <ul>
          {agents.map(a => (
            <li key={a.id}>{a.name} - {a.agent_type}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
