import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useApi } from '../useApi'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

function jsonResponse(status: number, body: unknown) {
  return { ok: status >= 200 && status < 300, status, json: async () => body }
}

describe('useApi', () => {
  beforeEach(() => mockFetch.mockReset())

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

  it('reports an unreachable server instead of throwing', async () => {
    mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'))

    const { request } = useApi('http://api.test')
    const result = await request('/me')

    expect(result).toEqual({ data: null, error: 'Could not reach the server', status: 0 })
  })
})
