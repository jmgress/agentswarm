# Provider Configuration Guide

## Overview

AgentSwarm now supports a unified provider interface for integrating different AI models. This allows you to easily switch between AI providers (Ollama, OpenAI, and Gemini) without changing the core agent logic.

## Supported Providers

### Ollama Provider
- **Type**: `ollama`
- **Use Case**: Local AI model inference
- **Configuration**:
  ```json
  {
    "base_url": "http://localhost:11434",
    "timeout": 30.0,
    "default_model": "llama2"
  }
  ```
- **Requirements**: Ollama server running locally
- **Models**: Any model supported by your Ollama installation

### OpenAI Provider
- **Type**: `openai`
- **Use Case**: GPT models through OpenAI API
- **Configuration**:
  ```json
  {
    "api_key": "your-openai-api-key",
    "base_url": "https://api.openai.com/v1",
    "timeout": 30.0,
    "default_model": "gpt-3.5-turbo"
  }
  ```
- **Requirements**: Valid OpenAI API key
- **Models**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, etc.

### Gemini Provider
- **Type**: `gemini`
- **Use Case**: Google's Gemini models
- **Configuration**:
  ```json
  {
    "api_key": "your-gemini-api-key",
    "base_url": "https://generativelanguage.googleapis.com/v1",
    "timeout": 30.0,
    "default_model": "gemini-pro",
    "safety_settings": {}
  }
  ```
- **Requirements**: Valid Google AI API key
- **Models**: `gemini-pro`, `gemini-pro-vision`

## Environment Variables

Set these environment variables for automatic provider configuration:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Gemini Configuration  
GEMINI_API_KEY=your-gemini-api-key

# Ollama Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
```

## API Endpoints

### Provider Management

- `GET /providers` - List all registered providers
- `POST /providers` - Create a new provider instance
- `DELETE /providers/{provider_id}` - Delete a provider
- `GET /providers/{provider_id}/health` - Check provider health
- `GET /providers/{provider_id}/models` - Get available models
- `POST /providers/{provider_id}/chat` - Chat with a provider
- `GET /providers/health` - Check all providers health

### Example: Create a Provider

```bash
curl -X POST http://localhost:8000/providers \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": "my_openai",
    "provider_type": "openai",
    "name": "My OpenAI Instance",
    "description": "OpenAI GPT models",
    "config": {
      "api_key": "your-api-key",
      "default_model": "gpt-3.5-turbo"
    }
  }'
```

### Example: Chat with a Provider

```bash
curl -X POST http://localhost:8000/providers/my_openai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  }'
```

## Agent Configuration

When creating agents, you can now specify which AI provider to use:

```json
{
  "name": "My Chat Agent",
  "agent_type": "utility",
  "description": "AI chat agent",
  "mcp_connection": {
    "endpoint_url": "http://localhost:8080/mcp"
  },
  "provider_config": {
    "provider_id": "my_openai",
    "provider_type": "openai",
    "model": "gpt-3.5-turbo",
    "config": {
      "temperature": 0.7
    },
    "fallback_providers": ["my_ollama"]
  }
}
```

## Health Monitoring

Check the health of all providers:

```bash
curl http://localhost:8000/providers/health
```

Response:
```json
{
  "providers": {
    "default_ollama": {
      "available": false,
      "error": "Connection error: All connection attempts failed",
      "models": [],
      "capabilities": []
    },
    "my_openai": {
      "available": true,
      "models": ["gpt-4", "gpt-3.5-turbo"],
      "capabilities": ["chat_completion", "streaming", "function_calling", "tool_use"]
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama is running: `ollama serve`
   - Check if models are installed: `ollama list`
   - Verify the base URL is correct

2. **OpenAI Authentication Error**
   - Verify your API key is valid
   - Check your OpenAI account has sufficient credits
   - Ensure the API key has proper permissions

3. **Gemini API Error**
   - Verify your Google AI API key is valid
   - Check your quota limits in Google Cloud Console
   - Ensure the Gemini API is enabled in your project

4. **Agent Creation Failed**
   - Ensure the provider_id exists in the provider registry
   - Verify the model name is supported by the provider
   - Check the provider health status

### Debug Commands

```bash
# List all providers
curl http://localhost:8000/providers

# Check specific provider health
curl http://localhost:8000/providers/default_ollama/health

# Get available models for a provider
curl http://localhost:8000/providers/default_ollama/models

# Test chat with a provider
curl -X POST http://localhost:8000/providers/default_ollama/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "test"}], "model": "llama2"}'
```

## Adding New Providers

To add support for a new AI provider:

1. Create a new provider class extending `BaseProvider`
2. Implement all abstract methods
3. Register the provider class in the registry
4. Add configuration documentation
5. Add tests for the new provider

See the existing provider implementations (`ollama.py`, `openai.py`, `gemini.py`) for examples.