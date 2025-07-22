from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
from models import Agent, AgentCreate
from providers.registry import provider_registry
from providers.base import ProviderType, ChatCompletionRequest, ChatMessage
from providers.models import (
    ProviderCreate, 
    ProviderInfo, 
    ProviderListResponse, 
    ProviderHealthResponse,
    ChatRequest
)
from providers.ollama import OllamaProvider
from providers.openai import OpenAIProvider
from providers.gemini import GeminiProvider
import json

app = FastAPI(title="AgentSwarm API", version="1.0.0")

# In-memory storage for agents (in production, this would be a database)
agents_storage: List[Agent] = []

# Register provider classes
provider_registry.register_provider_class(ProviderType.OLLAMA, OllamaProvider)
provider_registry.register_provider_class(ProviderType.OPENAI, OpenAIProvider)
provider_registry.register_provider_class(ProviderType.GEMINI, GeminiProvider)

# Initialize default providers
default_providers = [
    {
        "provider_id": "default_ollama",
        "provider_type": ProviderType.OLLAMA,
        "name": "Default Ollama",
        "description": "Local Ollama instance",
        "config": {"base_url": "http://localhost:11434", "default_model": "llama2"}
    },
    {
        "provider_id": "default_openai",
        "provider_type": ProviderType.OPENAI,
        "name": "Default OpenAI",
        "description": "OpenAI GPT models",
        "config": {"api_key": None, "default_model": "gpt-3.5-turbo"}
    },
    {
        "provider_id": "default_gemini",
        "provider_type": ProviderType.GEMINI,
        "name": "Default Gemini",
        "description": "Google Gemini models",
        "config": {"api_key": None, "default_model": "gemini-pro"}
    }
]

# Create default providers
for provider_data in default_providers:
    try:
        provider_registry.create_provider(
            provider_data["provider_id"],
            provider_data["provider_type"],
            provider_data["config"]
        )
    except Exception:
        pass  # Ignore errors during default provider creation

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


# Provider endpoints
@app.get("/providers", response_model=ProviderListResponse)
async def list_providers():
    """List all registered providers"""
    providers = []
    for provider_id in provider_registry.list_providers():
        provider = provider_registry.get_provider(provider_id)
        if provider:
            providers.append(ProviderInfo(
                provider_id=provider_id,
                provider_type=provider.provider_type,
                name=provider.config.get("name", provider_id),
                description=provider.config.get("description", ""),
                config=provider.config,
                default_model=provider.get_default_model()
            ))
    
    return ProviderListResponse(providers=providers, total=len(providers))


@app.post("/providers", response_model=ProviderInfo)
async def create_provider(provider_data: ProviderCreate):
    """Create a new provider instance"""
    # Check if provider_id already exists
    if provider_registry.get_provider(provider_data.provider_id):
        raise HTTPException(status_code=400, detail="Provider with this ID already exists")
    
    try:
        provider = provider_registry.create_provider(
            provider_data.provider_id,
            provider_data.provider_type,
            provider_data.config
        )
        
        return ProviderInfo(
            provider_id=provider_data.provider_id,
            provider_type=provider.provider_type,
            name=provider_data.name,
            description=provider_data.description,
            config=provider.config,
            default_model=provider.get_default_model()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/providers/{provider_id}")
async def delete_provider(provider_id: str):
    """Delete a provider instance"""
    if not provider_registry.remove_provider(provider_id):
        raise HTTPException(status_code=404, detail="Provider not found")
    
    return {"message": f"Provider {provider_id} deleted successfully"}


@app.get("/providers/{provider_id}/health", response_model=ProviderHealthResponse)
async def check_provider_health(provider_id: str):
    """Check health status of a specific provider"""
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    status = await provider.health_check()
    return ProviderHealthResponse(provider_id=provider_id, status=status)


@app.get("/providers/{provider_id}/models")
async def get_provider_models(provider_id: str):
    """Get available models for a provider"""
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    try:
        models = await provider.get_available_models()
        return {"provider_id": provider_id, "models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/providers/{provider_id}/chat")
async def chat_with_provider(provider_id: str, chat_request: ChatRequest):
    """Chat with a specific provider"""
    provider = provider_registry.get_provider(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    # Convert messages to ChatMessage format
    messages = []
    for msg in chat_request.messages:
        messages.append(ChatMessage(
            role=msg.get("role", "user"),
            content=msg.get("content", "")
        ))
    
    # Create request
    request = ChatCompletionRequest(
        messages=messages,
        model=chat_request.model or provider.get_default_model() or "default",
        max_tokens=chat_request.max_tokens,
        temperature=chat_request.temperature,
        stream=chat_request.stream
    )
    
    try:
        if chat_request.stream:
            # Return streaming response
            async def generate():
                async for chunk in provider.stream_completion(request):
                    yield f"data: {json.dumps({'content': chunk})}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            # Return regular response
            response = await provider.chat_completion(request)
            return {
                "message": response.message.dict(),
                "model": response.model,
                "usage": response.usage,
                "metadata": response.metadata
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/providers/health")
async def check_all_providers_health():
    """Check health status of all providers"""
    health_results = await provider_registry.health_check_all()
    return {"providers": health_results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)