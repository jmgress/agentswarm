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

  it('renders without crashing', () => {
    // Mock a failing fetch to avoid loading state
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error('Network error'))
    render(<App />)
    expect(screen.getByText('AgentSwarm - Frontend')).toBeInTheDocument()
  })

  it('displays health check section', async () => {
    // Mock a successful fetch response
    vi.mocked(globalThis.fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'ok' })
    } as Response)

    render(<App />)
    expect(screen.getByText('Backend Health Status')).toBeInTheDocument()
    
    // Wait for the loading to complete and button text to update
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /check backend health/i })).toBeInTheDocument()
    })
  })

  it('displays counter functionality', () => {
    // Mock a failing fetch to avoid loading state
    vi.mocked(globalThis.fetch).mockRejectedValue(new Error('Network error'))
    render(<App />)
    expect(screen.getByRole('button', { name: /count is 0/i })).toBeInTheDocument()
  })
})