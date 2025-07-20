import './ChatHistory.css'

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

interface ChatHistoryProps {
  chats: Chat[];
  currentChat: Chat | null;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => Promise<Chat>;
  isLoading: boolean;
}

export function ChatHistory({ chats, currentChat, onSelectChat, onNewChat, isLoading }: ChatHistoryProps) {
  const handleNewChat = async () => {
    try {
      await onNewChat();
    } catch (error) {
      console.error('Failed to create new chat:', error);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays < 7) {
      return date.toLocaleDateString([], { weekday: 'short' });
    } else {
      return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  return (
    <div className="chat-history">
      <div className="chat-history-header">
        <h2>Chat History</h2>
        <button 
          className="new-chat-button"
          onClick={handleNewChat}
        >
          + New Chat
        </button>
      </div>
      
      <div className="chat-list">
        {isLoading ? (
          <div className="loading">Loading chats...</div>
        ) : chats.length === 0 ? (
          <div className="empty-state">
            No chats yet. Start a new conversation!
          </div>
        ) : (
          chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${currentChat?.id === chat.id ? 'active' : ''}`}
              onClick={() => onSelectChat(chat.id)}
            >
              <div className="chat-title">{chat.title}</div>
              <div className="chat-meta">
                <span className="chat-date">{formatDate(chat.updated_at)}</span>
                <span className="message-count">{chat.messages.length} msgs</span>
              </div>
              {chat.messages.length > 0 && (
                <div className="chat-preview">
                  {chat.messages[chat.messages.length - 1].content.substring(0, 50)}
                  {chat.messages[chat.messages.length - 1].content.length > 50 ? '...' : ''}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}