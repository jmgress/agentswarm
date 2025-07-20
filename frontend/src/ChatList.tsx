import React from 'react'
import './ChatList.css'

export interface ChatSummary {
  id: number
  title: string
}

interface ChatListProps {
  chats: ChatSummary[]
  activeChatId: number
  onSelect: (id: number) => void
  onAddChat: () => void
}

export function ChatList({ chats, activeChatId, onSelect, onAddChat }: ChatListProps) {
  return (
    <div className="chat-list">
      <button className="add-chat" onClick={onAddChat}>+ New Chat</button>
      <ul>
        {chats.map(chat => (
          <li
            key={chat.id}
            className={chat.id === activeChatId ? 'active' : ''}
            onClick={() => onSelect(chat.id)}
          >
            {chat.title}
          </li>
        ))}
      </ul>
    </div>
  )
}
