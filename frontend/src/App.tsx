import { useEffect, useState } from 'react'
import './App.css'
import { AgentForm, type AgentFormData, type Agent } from './AgentForm'
import { AgentList } from './AgentList'
import { ChatList, ChatSummary } from './ChatList'
import { ChatWindow, ChatMessage } from './ChatWindow'

interface HealthStatus {
  status: string
}

interface Chat {
  id: number
  messages: ChatMessage[]
}

function App() {
  // Health check (retain existing logic)
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)
  const [isLoadingHealth, setIsLoadingHealth] = useState(false)

  // Agents
  const [agents, setAgents] = useState<Agent[]>([])
  const [isCreatingAgent, setIsCreatingAgent] = useState(false)
  const [isLoadingAgents, setIsLoadingAgents] = useState(false)
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([])

  // Chats
  const [chats, setChats] = useState<Chat[]>([{ id: 1, messages: [] }])
  const [activeChatId, setActiveChatId] = useState(1)

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
      setHealthError(
        error instanceof Error ? error.message : 'Failed to connect to backend'
      )
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
    try {
      const response = await fetch('http://localhost:8000/agents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(agentData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create agent')
      }

      const newAgent: Agent = await response.json()
      setAgents(prev => [...prev, newAgent])
    } catch (error) {
      console.error('Failed to create agent:', error)
    } finally {
      setIsCreatingAgent(false)
    }
  }

  const toggleAgent = (id: string) => {
    setSelectedAgentIds(prev =>
      prev.includes(id) ? prev.filter(a => a !== id) : [...prev, id]
    )
  }

  const addChat = () => {
    const newId = chats.length ? chats[chats.length - 1].id + 1 : 1
    setChats([...chats, { id: newId, messages: [] }])
    setActiveChatId(newId)
  }

  const sendMessage = (content: string) => {
    setChats(prev =>
      prev.map(chat =>
        chat.id === activeChatId
          ? {
              ...chat,
              messages: [
                ...chat.messages,
                { role: 'user', content },
                { role: 'assistant', content: 'This is a placeholder response.' }
              ]
            }
          : chat
      )
    )
  }

  useEffect(() => {
    checkBackendHealth()
    loadAgents()
  }, [])

  const chatSummaries: ChatSummary[] = chats.map(c => ({
    id: c.id,
    title: `Chat ${c.id}`
  }))
  const activeMessages = chats.find(c => c.id === activeChatId)?.messages ?? []

  return (
    <div className="app-container">
      <aside className="sidebar-left">
        <ChatList
          chats={chatSummaries}
          activeChatId={activeChatId}
          onSelect={setActiveChatId}
          onAddChat={addChat}
        />
      </aside>
      <main className="main-content">
        <div className="health-section">
          <button onClick={checkBackendHealth} disabled={isLoadingHealth}>
            {isLoadingHealth ? 'Checking...' : 'Check Backend Health'}
          </button>
          {healthStatus && <div>Backend: {healthStatus.status}</div>}
          {healthError && <div>Error: {healthError}</div>}
        </div>
        <ChatWindow messages={activeMessages} onSend={sendMessage} />
      </main>
      <aside className="agent-sidebar">
        <AgentForm onSubmit={createAgent} isLoading={isCreatingAgent} />
        <AgentList
          agents={agents}
          isLoading={isLoadingAgents}
          selectedAgentIds={selectedAgentIds}
          onToggleAgent={toggleAgent}
        />
      </aside>
    </div>
  )
}

export default App
