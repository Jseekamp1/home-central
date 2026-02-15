import { describe, it, expect, beforeEach, vi } from 'vitest'

// We'll test the auth composable's core logic as a standalone module
// (not inside a Vue component context) to keep tests fast and focused.

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

// Mock localStorage
const storage: Record<string, string> = {}
vi.stubGlobal('localStorage', {
  getItem: (key: string) => storage[key] ?? null,
  setItem: (key: string, value: string) => { storage[key] = value },
  removeItem: (key: string) => { delete storage[key] },
})

// Import after mocks are in place
import { useAuth } from '../composables/useAuth'

describe('useAuth', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    Object.keys(storage).forEach(key => delete storage[key])
  })

  describe('login', () => {
    it('sets user and token on successful login', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          user: { id: 'user-123', email: 'test@example.com' },
          session: { access_token: 'token-abc' },
        }),
      })

      const auth = useAuth('http://localhost:8000')
      await auth.login('test@example.com', 'password123')

      expect(auth.user.value).toEqual({ id: 'user-123', email: 'test@example.com' })
      expect(auth.token.value).toBe('token-abc')
      expect(auth.isAuthenticated.value).toBe(true)
      expect(storage['auth_token']).toBe('token-abc')
    })

    it('throws on failed login', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Invalid login credentials' }),
      })

      const auth = useAuth('http://localhost:8000')
      await expect(auth.login('test@example.com', 'wrong')).rejects.toThrow('Invalid login credentials')
      expect(auth.isAuthenticated.value).toBe(false)
    })
  })

  describe('signup', () => {
    it('sets user and token on successful signup', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          user: { id: 'user-456', email: 'new@example.com' },
          session: { access_token: 'token-def' },
        }),
      })

      const auth = useAuth('http://localhost:8000')
      await auth.signup('new@example.com', 'password123')

      expect(auth.user.value).toEqual({ id: 'user-456', email: 'new@example.com' })
      expect(auth.token.value).toBe('token-def')
      expect(auth.isAuthenticated.value).toBe(true)
    })
  })

  describe('logout', () => {
    it('clears user state and token', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          user: { id: 'user-123', email: 'test@example.com' },
          session: { access_token: 'token-abc' },
        }),
      })

      const auth = useAuth('http://localhost:8000')
      await auth.login('test@example.com', 'password123')
      auth.logout()

      expect(auth.user.value).toBeNull()
      expect(auth.token.value).toBeNull()
      expect(auth.isAuthenticated.value).toBe(false)
      expect(storage['auth_token']).toBeUndefined()
    })
  })

  describe('fetchUser', () => {
    it('fetches user data with stored token', async () => {
      storage['auth_token'] = 'stored-token'

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'user-123', email: 'test@example.com' }),
      })

      const auth = useAuth('http://localhost:8000')
      auth.token.value = 'stored-token'
      await auth.fetchUser()

      expect(auth.user.value).toEqual({ id: 'user-123', email: 'test@example.com' })
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/auth/me',
        expect.objectContaining({
          headers: { Authorization: 'Bearer stored-token' },
        }),
      )
    })

    it('clears state when token is invalid', async () => {
      mockFetch.mockResolvedValueOnce({ ok: false, json: async () => ({}) })

      const auth = useAuth('http://localhost:8000')
      auth.token.value = 'bad-token'
      await auth.fetchUser()

      expect(auth.user.value).toBeNull()
      expect(auth.token.value).toBeNull()
    })
  })

  describe('isAuthenticated', () => {
    it('returns false when no token', () => {
      const auth = useAuth('http://localhost:8000')
      expect(auth.isAuthenticated.value).toBe(false)
    })

    it('returns true when token exists', () => {
      const auth = useAuth('http://localhost:8000')
      auth.token.value = 'some-token'
      expect(auth.isAuthenticated.value).toBe(true)
    })
  })
})
