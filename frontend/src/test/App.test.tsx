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
    // Mock both health and agents API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: false,
        json: async () => ({}),
        status: 500
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
    
    render(<App />)
    expect(screen.getByText('AgentSwarm - Agent Management')).toBeInTheDocument()
  })

  it('displays health check section', async () => {
    // Mock successful health check and empty agents list
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'ok' })
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

    render(<App />)
    expect(screen.getByText('Backend Health Status')).toBeInTheDocument()
    
    // Wait for the health check to complete and button text to update
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /check backend health/i })).toBeInTheDocument()
    })
  })

  it('displays counter functionality', async () => {
    // Mock failing health check and agents API
    vi.mocked(globalThis.fetch)
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)
      
    render(<App />)
    expect(screen.getByRole('button', { name: /count is 0/i })).toBeInTheDocument()
  })

  it('displays agent form', async () => {
    // Mock API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'ok' })
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

    render(<App />)
    
    // Check for agent form elements
    await waitFor(() => {
      expect(screen.getByText('Create New Agent')).toBeInTheDocument()
      expect(screen.getByLabelText(/agent name/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/agent type/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/description/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/mcp endpoint url/i)).toBeInTheDocument()
    })
  })

  it('displays agent list section', async () => {
    // Mock API calls
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: 'ok' })
      } as Response)
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      } as Response)

    render(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('Agents (0)')).toBeInTheDocument()
      expect(screen.getByText('No agents created yet. Create your first agent using the form above.')).toBeInTheDocument()
    })
  })
})