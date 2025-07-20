import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import App from '../App'

// Mock fetch globally
globalThis.fetch = vi.fn()

describe('App', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    vi.resetAllMocks()
  })

  it('renders without crashing', async () => {
    // Mock both chats and agents API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
    
    render(<App />)
    expect(screen.getByText('Chat History')).toBeInTheDocument()
    expect(screen.getByText('Agents')).toBeInTheDocument()
  })

  it('displays chat interface', async () => {
    // Mock successful API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

    render(<App />)
    expect(screen.getByText('Chat History')).toBeInTheDocument()
    expect(screen.getByText('+ New Chat')).toBeInTheDocument()
    expect(screen.getByText('Welcome to AgentSwarm')).toBeInTheDocument()
  })

  it('displays agent panel', async () => {
    // Mock API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      
    render(<App />)
    expect(screen.getByText('Agents')).toBeInTheDocument()
    expect(screen.getByText('+')).toBeInTheDocument()
    expect(screen.getByText('No agents enabled')).toBeInTheDocument()
  })

  it('displays empty states correctly', async () => {
    // Mock empty responses
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('No chats yet. Start a new conversation!')).toBeInTheDocument()
      expect(screen.getByText('No agents available.')).toBeInTheDocument()
    })
  })

  it('displays input interface', async () => {
    // Mock API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByPlaceholderText('Select agents from the panel to start chatting...')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: '→' })).toBeInTheDocument()
    })
  })
})