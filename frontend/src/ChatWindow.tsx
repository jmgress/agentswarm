import React, { useState } from 'react'
import './ChatWindow.css'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

interface ChatWindowProps {
  messages: ChatMessage[]
  onSend: (content: string) => void
}

export function ChatWindow({ messages, onSend }: ChatWindowProps) {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const text = input.trim()
    if (!text) return
    onSend(text)
    setInput('')
  }

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((m, idx) => (
          <div key={idx} className={`message ${m.role}`}>{m.content}</div>
        ))}
      </div>
      <form className="prompt-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}
