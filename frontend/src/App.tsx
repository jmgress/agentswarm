import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

interface HealthStatus {
  status: string;
}

function App() {
  const [count, setCount] = useState(0)
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

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

  useEffect(() => {
    checkBackendHealth()
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
