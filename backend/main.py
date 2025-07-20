from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Agent, AgentCreate, Chat, ChatCreate, Message, MessageCreate
import uuid
from datetime import datetime

app = FastAPI(title="AgentSwarm API", version="1.0.0")

# In-memory storage (in production, this would be a database)
agents_storage: List[Agent] = []
chats_storage: List[Chat] = []

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


# Agent endpoints
@app.post("/agents", response_model=Agent)
async def create_agent(agent_data: AgentCreate):
    """Create a new agent"""
    # Check if agent with same name already exists
    existing_agent = next((agent for agent in agents_storage if agent.name == agent_data.name), None)
    if existing_agent:
        raise HTTPException(status_code=400, detail="Agent with this name already exists")
    
    # Create new agent
    new_agent = Agent.from_create(agent_data)
    agents_storage.append(new_agent)
    
    return new_agent


@app.get("/agents", response_model=List[Agent])
async def get_agents():
    """Get all agents"""
    return agents_storage


# Chat endpoints
@app.post("/chats", response_model=Chat)
async def create_chat(chat_data: ChatCreate):
    """Create a new chat"""
    new_chat = Chat.from_create(chat_data)
    chats_storage.append(new_chat)
    return new_chat


@app.get("/chats", response_model=List[Chat])
async def get_chats():
    """Get all chats"""
    return sorted(chats_storage, key=lambda x: x.updated_at, reverse=True)


@app.get("/chats/{chat_id}", response_model=Chat)
async def get_chat(chat_id: str):
    """Get a specific chat by ID"""
    chat = next((chat for chat in chats_storage if chat.id == chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@app.post("/chats/{chat_id}/messages", response_model=Message)
async def add_message(chat_id: str, message_data: MessageCreate):
    """Add a message to a chat"""
    chat = next((chat for chat in chats_storage if chat.id == chat_id), None)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Create user message
    user_message = Message(
        id=str(uuid.uuid4()),
        content=message_data.content,
        sender="user",
        created_at=datetime.utcnow(),
        enabled_agents=message_data.enabled_agents
    )
    
    chat.messages.append(user_message)
    chat.updated_at = datetime.utcnow()
    
    # For now, create a simple assistant response
    # In the future, this would integrate with the enabled agents
    assistant_response = Message(
        id=str(uuid.uuid4()),
        content=f"I received your message: '{message_data.content}'. Enabled agents: {', '.join(message_data.enabled_agents) if message_data.enabled_agents else 'None'}",
        sender="assistant",
        created_at=datetime.utcnow(),
        enabled_agents=message_data.enabled_agents
    )
    
    chat.messages.append(assistant_response)
    chat.updated_at = datetime.utcnow()
    
    return user_message


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)