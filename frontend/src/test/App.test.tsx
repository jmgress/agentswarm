import { render, screen, act } from '@testing-library/react'
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
    // Mock a failing fetch to avoid loading state
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error('Network error'))
    
    await act(async () => {
      render(<App />)
    })
    
    expect(screen.getByText('AgentSwarm')).toBeInTheDocument()
  })

  it('displays agent creation form', async () => {
    // Mock a successful fetch response for agents
    vi.mocked(globalThis.fetch).mockResolvedValue({
      ok: true,
      json: async () => ([])
    } as Response)

    await act(async () => {
      render(<App />)
    })
    
    expect(screen.getByText('Create New Agent')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /create agent/i })).toBeInTheDocument()
  })

  it('displays agents list section', async () => {
    // Mock a failing fetch to avoid loading state
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error('Network error'))
    
    await act(async () => {
      render(<App />)
    })
    
    expect(screen.getByText('Available Agents')).toBeInTheDocument()
    expect(screen.getByText('No agents created yet.')).toBeInTheDocument()
  })
})