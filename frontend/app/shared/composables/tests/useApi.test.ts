import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useApi } from '../useApi'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

function jsonResponse(status: number, body: unknown) {
  return { ok: status >= 200 && status < 300, status, json: async () => body }
}

describe('useApi', () => {
  beforeEach(() => mockFetch.mockReset())

  it('returns parsed JSON from the API base URL', async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse(200, { id: '1', email: 'dev@example.com' }))

    const { request } = useApi('http://api.test')
    const result = await request<{ id: string }>('/me')

    expect(mockFetch).toHaveBeenCalledWith('http://api.test/me', expect.anything())
    expect(result).toEqual({ data: { id: '1', email: 'dev@example.com' }, error: null, status: 200 })
  })

  it('turns FastAPI validation errors into a readable message', async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse(422, {
      detail: [
        { loc: ['body', 'title'], msg: 'Field required', type: 'missing' },
        { loc: ['body', 'priority'], msg: "Input should be 'low' or 'high'", type: 'enum' },
      ],
    }))

    const { request } = useApi('http://api.test')
    const result = await request('/projects', { method: 'POST', body: '{}' })

    expect(result.data).toBeNull()
    expect(result.status).toBe(422)
    expect(result.error).toBe("title: Field required; priority: Input should be 'low' or 'high'")
  })

  it('passes through a plain error detail', async () => {
    mockFetch.mockResolvedValueOnce(jsonResponse(404, { detail: 'Project not found' }))

    const { request } = useApi('http://api.test')
    const result = await request('/projects/x')

    expect(result).toEqual({ data: null, error: 'Project not found', status: 404 })
  })

  it('reports an unreachable server instead of throwing', async () => {
    mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

    const { request } = useApi('http://api.test')
    const result = await request('/me')

    expect(result).toEqual({ data: null, error: 'Could not reach the server', status: 0 })
  })
})
