import { useState, useRef, useEffect } from 'react'
import './ChatInterface.css'

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

interface ChatInterfaceProps {
  chat: Chat | null;
  onSendMessage: (content: string) => Promise<void>;
  enabledAgents: Set<string>;
}

export function ChatInterface({ chat, onSendMessage, enabledAgents }: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current && typeof messagesEndRef.current.scrollIntoView === 'function') {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat?.messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isSending) return;

    const messageContent = input.trim();
    setInput('');
    setIsSending(true);

    try {
      await onSendMessage(messageContent);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsSending(false);
    }
  };

  const formatMessageTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>{chat ? chat.title : 'Select a chat or start a new conversation'}</h2>
        {enabledAgents.size > 0 && (
          <div className="enabled-agents-indicator">
            {enabledAgents.size} agent{enabledAgents.size !== 1 ? 's' : ''} enabled
          </div>
        )}
      </div>

      <div className="messages-container">
        {chat ? (
          chat.messages.length === 0 ? (
            <div className="empty-chat">
              <div className="empty-chat-content">
                <h3>Start a conversation</h3>
                <p>Type your message below to begin chatting with the enabled agents.</p>
              </div>
            </div>
          ) : (
            chat.messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender}`}
              >
                <div className="message-content">
                  <div className="message-text">{message.content}</div>
                  <div className="message-meta">
                    <span className="message-time">{formatMessageTime(message.created_at)}</span>
                    {message.enabled_agents.length > 0 && (
                      <span className="message-agents">
                        {message.enabled_agents.length} agent{message.enabled_agents.length !== 1 ? 's' : ''}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )
        ) : (
          <div className="empty-chat">
            <div className="empty-chat-content">
              <h3>Welcome to AgentSwarm</h3>
              <p>Select a chat from the history or create a new one to start conversing with your agents.</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <form onSubmit={handleSubmit} className="message-form">
          <div className="input-wrapper">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={enabledAgents.size > 0 ? 
                `Message ${enabledAgents.size} enabled agent${enabledAgents.size !== 1 ? 's' : ''}...` : 
                'Select agents from the panel to start chatting...'
              }
              disabled={isSending}
              rows={1}
              className="message-input"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <button
              type="submit"
              disabled={!input.trim() || isSending}
              className="send-button"
            >
              {isSending ? '...' : '→'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}