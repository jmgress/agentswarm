import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { AgentForm, type AgentFormData, type Agent } from './AgentForm'
import { AgentList } from './AgentList'

interface HealthStatus {
  status: string;
}

function App() {
  const [count, setCount] = useState(0)
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)
  const [isLoadingHealth, setIsLoadingHealth] = useState(false)
  
  // Agent-related state
  const [agents, setAgents] = useState<Agent[]>([])
  const [isCreatingAgent, setIsCreatingAgent] = useState(false)
  const [isLoadingAgents, setIsLoadingAgents] = useState(false)
  const [agentMessage, setAgentMessage] = useState<{type: 'success' | 'error', text: string} | null>(null)

  const checkBackendHealth = async () => {
    setIsLoadingHealth(true)
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
      setIsLoadingHealth(false)
    }
  }

  const loadAgents = async () => {
    setIsLoadingAgents(true)
    try {
      const response = await fetch('http://localhost:8000/agents')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: Agent[] = await response.json()
      setAgents(data)
    } catch (error) {
      console.error('Failed to load agents:', error)
    } finally {
      setIsLoadingAgents(false)
    }
  }

  const createAgent = async (agentData: AgentFormData) => {
    setIsCreatingAgent(true)
    setAgentMessage(null)
    
    try {
      const response = await fetch('http://localhost:8000/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(agentData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create agent')
      }

      const newAgent: Agent = await response.json()
      setAgents(prev => [...prev, newAgent])
      setAgentMessage({ type: 'success', text: `Agent "${newAgent.name}" created successfully!` })
      
      // Clear success message after 5 seconds
      setTimeout(() => setAgentMessage(null), 5000)
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create agent'
      setAgentMessage({ type: 'error', text: errorMessage })
    } finally {
      setIsCreatingAgent(false)
    }
  }

  useEffect(() => {
    checkBackendHealth()
    loadAgents()
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
      <h1>AgentSwarm - Agent Management</h1>
      
      <div className="card">
        <h2>Backend Health Status</h2>
        <button onClick={checkBackendHealth} disabled={isLoadingHealth}>
          {isLoadingHealth ? 'Checking...' : 'Check Backend Health'}
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

      {/* Agent Management Section */}
      <div className="agent-management">
        {agentMessage && (
          <div 
            className={`message ${agentMessage.type}`}
            style={{
              margin: '20px auto',
              padding: '10px',
              maxWidth: '600px',
              borderRadius: '4px',
              backgroundColor: agentMessage.type === 'success' ? '#d4edda' : '#f8d7da',
              border: `1px solid ${agentMessage.type === 'success' ? '#c3e6cb' : '#f5c6cb'}`,
              color: agentMessage.type === 'success' ? '#155724' : '#721c24'
            }}
          >
            {agentMessage.type === 'success' ? '✅' : '❌'} {agentMessage.text}
          </div>
        )}
        
        <AgentForm onSubmit={createAgent} isLoading={isCreatingAgent} />
        <AgentList agents={agents} isLoading={isLoadingAgents} />
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
