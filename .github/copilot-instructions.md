# GitHub Copilot Instructions for AgentSwarm

## Project Overview
AgentSwarm is a full-stack application designed as a generative AI system to build an agent swarm for task and problem solving. The project consists of:
- **Backend**: FastAPI application with Python
- **Frontend**: React application with TypeScript and Vite

## Code Style and Conventions

### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Prefer async/await for asynchronous operations when using FastAPI
- Use descriptive variable and function names
- Add docstrings for all public functions and classes
- Keep functions focused and single-purpose

### TypeScript/React (Frontend)
- Use TypeScript for all new files
- Follow React functional component patterns with hooks
- Use descriptive component and variable names in PascalCase for components, camelCase for variables
- Prefer const over let when variables won't be reassigned
- Use interfaces for type definitions
- Keep components focused and reusable

### File Organization
- Backend code goes in the `backend/` directory
- Frontend code goes in the `frontend/src/` directory
- Keep related functionality grouped together
- Use clear, descriptive file names

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Python 3.8+**: Runtime environment
- Consider using Pydantic models for request/response validation

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **Modern React patterns**: Functional components, hooks, context when needed

## Development Guidelines

### API Development
- Use RESTful conventions for endpoints
- Include proper error handling and status codes
- Add CORS configuration for frontend communication
- Document endpoints with FastAPI's automatic OpenAPI documentation
- Use Pydantic models for request/response validation

### Frontend Development
- Create reusable components
- Use proper error boundaries for error handling
- Implement loading states for async operations
- Follow React best practices for state management
- Use TypeScript interfaces for API responses

### Error Handling
- Backend: Use FastAPI's HTTPException for API errors
- Frontend: Implement try-catch blocks for API calls and show user-friendly error messages
- Log errors appropriately without exposing sensitive information

## Testing
- Write unit tests for backend endpoints
- Consider integration tests for full-stack functionality
- Use appropriate testing frameworks (pytest for Python, Jest/Vitest for frontend)

## Security Considerations
- Validate all inputs on the backend
- Use environment variables for sensitive configuration
- Implement proper CORS policies
- Don't commit secrets or sensitive data

## Performance
- Use async/await patterns in FastAPI for I/O operations
- Optimize React components with proper use of useMemo and useCallback when needed
- Consider pagination for large data sets
- Implement proper caching strategies

## Agent Swarm Specific Context
- This project is focused on building AI agent systems
- Consider scalability when designing agent management features
- Think about task distribution and coordination between agents
- Plan for real-time communication and status updates
- Design with modularity in mind for different agent types and capabilities