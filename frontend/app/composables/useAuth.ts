import { ref, computed } from 'vue'

interface User {
  id: string
  email: string
}

function getStoredToken(): string | null {
  if (typeof localStorage !== 'undefined') {
    return localStorage.getItem('auth_token')
  }
  return null
}

function setStoredToken(value: string) {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('auth_token', value)
  }
}

function removeStoredToken() {
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('auth_token')
  }
}

export function useAuth(apiBase?: string) {
  let base = apiBase ?? 'http://localhost:8000'

  // In Nuxt context, use runtime config if available
  if (!apiBase) {
    try {
      const config = useRuntimeConfig()
      if (config.public.apiBase) base = config.public.apiBase as string
    } catch {
      // Outside Nuxt context (tests) — use default
    }
  }

  const token = ref<string | null>(getStoredToken())
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const res = await fetch(`${base}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    token.value = data.session.access_token
    user.value = data.user
    setStoredToken(data.session.access_token)
  }

  async function signup(email: string, password: string) {
    const res = await fetch(`${base}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail)
    token.value = data.session.access_token
    user.value = data.user
    setStoredToken(data.session.access_token)
  }

  function logout() {
    token.value = null
    user.value = null
    removeStoredToken()
  }

  async function fetchUser() {
    if (!token.value) return
    const res = await fetch(`${base}/auth/me`, {
      headers: { Authorization: `Bearer ${token.value}` },
    })
    if (!res.ok) {
      token.value = null
      user.value = null
      removeStoredToken()
      return
    }
    user.value = await res.json()
  }

  return { token, user, isAuthenticated, login, signup, logout, fetchUser }
}
