import { useState, useEffect } from 'react'
import './App.css'
import { ChatHistory } from './ChatHistory'
import { ChatInterface } from './ChatInterface'
import { AgentPanel } from './AgentPanel'
import type { Agent } from './AgentForm'

interface Chat {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  created_at: string;
  enabled_agents: string[];
}

function App() {
  // Agent-related state
  const [agents, setAgents] = useState<Agent[]>([])
  const [isLoadingAgents, setIsLoadingAgents] = useState(false)
  
  // Chat-related state
  const [chats, setChats] = useState<Chat[]>([])
  const [currentChat, setCurrentChat] = useState<Chat | null>(null)
  const [isLoadingChats, setIsLoadingChats] = useState(false)
  
  // Agent selection state
  const [enabledAgents, setEnabledAgents] = useState<Set<string>>(new Set())

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

  const loadChats = async () => {
    setIsLoadingChats(true)
    try {
      const response = await fetch('http://localhost:8000/chats')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: Chat[] = await response.json()
      setChats(data)
    } catch (error) {
      console.error('Failed to load chats:', error)
    } finally {
      setIsLoadingChats(false)
    }
  }

  const createNewChat = async (title?: string) => {
    try {
      const response = await fetch('http://localhost:8000/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const newChat: Chat = await response.json()
      setChats(prev => [newChat, ...prev])
      setCurrentChat(newChat)
      return newChat
    } catch (error) {
      console.error('Failed to create chat:', error)
      throw error
    }
  }

  const selectChat = async (chatId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/chats/${chatId}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const chat: Chat = await response.json()
      setCurrentChat(chat)
    } catch (error) {
      console.error('Failed to load chat:', error)
    }
  }

  const sendMessage = async (content: string) => {
    if (!currentChat) {
      // Create a new chat if none exists
      await createNewChat()
      if (!currentChat) return
    }

    try {
      const response = await fetch(`http://localhost:8000/chats/${currentChat.id}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          enabled_agents: Array.from(enabledAgents)
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Reload the current chat to get updated messages
      await selectChat(currentChat.id)
      // Also reload chats list to update timestamps
      await loadChats()
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  const toggleAgent = (agentId: string) => {
    setEnabledAgents(prev => {
      const newSet = new Set(prev)
      if (newSet.has(agentId)) {
        newSet.delete(agentId)
      } else {
        newSet.add(agentId)
      }
      return newSet
    })
  }

  useEffect(() => {
    loadAgents()
    loadChats()
  }, [])

  return (
    <div className="app-container">
      <ChatHistory 
        chats={chats}
        currentChat={currentChat}
        onSelectChat={selectChat}
        onNewChat={createNewChat}
        isLoading={isLoadingChats}
      />
      
      <ChatInterface 
        chat={currentChat}
        onSendMessage={sendMessage}
        enabledAgents={enabledAgents}
      />
      
      <AgentPanel 
        agents={agents}
        enabledAgents={enabledAgents}
        onToggleAgent={toggleAgent}
        onAgentsUpdated={loadAgents}
        isLoading={isLoadingAgents}
      />
    </div>
  )
}

export default App
