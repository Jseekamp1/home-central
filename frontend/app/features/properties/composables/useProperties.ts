import { computed, ref } from 'vue'
import { useApi, type ApiResult } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

type Property = Schemas['PropertyRead']
type PropertyCreate = Schemas['PropertyCreate']
type PropertyUpdate = Schemas['PropertyUpdate']

interface Api {
  request<T>(path: string, init?: RequestInit): Promise<ApiResult<T>>
}

export interface KeyValueStorage {
  get(key: string): string | null
  set(key: string, value: string): void
  remove(key: string): void
}

const CURRENT_KEY = 'home-central:current-property'

function byName(a: Property, b: Property) {
  return a.name.localeCompare(b.name)
}

// The current property is a per-device convenience, so storage failures
// (private browsing, blocked storage) must never break the app.
export function browserStorage(): KeyValueStorage {
  return {
    get(key) {
      try { return localStorage.getItem(key) }
      catch { return null }
    },
    set(key, value) {
      try { localStorage.setItem(key, value) }
      catch { /* storage unavailable: the choice just isn't remembered */ }
    },
    remove(key) {
      try { localStorage.removeItem(key) }
      catch { /* storage unavailable */ }
    },
  }
}

export function createPropertiesStore(api: Api, storage: KeyValueStorage) {
  const properties = ref<Property[]>([])
  const currentId = ref<string | null>(null)
  const loaded = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const current = computed(() => properties.value.find(p => p.id === currentId.value) ?? null)
  const needsSetup = computed(() => loaded.value && properties.value.length === 0)

  function select(id: string | null) {
    currentId.value = id
    if (id) storage.set(CURRENT_KEY, id)
    else storage.remove(CURRENT_KEY)
  }

  function selectRememberedOrFirst() {
    const remembered = storage.get(CURRENT_KEY)
    const match = properties.value.find(p => p.id === remembered)
    select(match?.id ?? properties.value[0]?.id ?? null)
  }

  async function load() {
    loading.value = true
    error.value = null
    const result = await api.request<Property[]>('/properties')
    loading.value = false
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not load properties'
      return
    }
    properties.value = result.data
    loaded.value = true
    selectRememberedOrFirst()
  }

  async function create(body: PropertyCreate): Promise<Property | null> {
    error.value = null
    const result = await api.request<Property>('/properties', { method: 'POST', body: JSON.stringify(body) })
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not create the property'
      return null
    }
    properties.value = [...properties.value, result.data].sort(byName)
    select(result.data.id)
    return result.data
  }

  async function update(id: string, body: PropertyUpdate): Promise<Property | null> {
    error.value = null
    const result = await api.request<Property>(`/properties/${id}`, { method: 'PATCH', body: JSON.stringify(body) })
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not save the property'
      return null
    }
    const saved = result.data
    properties.value = properties.value.map(p => (p.id === id ? saved : p)).sort(byName)
    return saved
  }

  async function remove(id: string): Promise<boolean> {
    error.value = null
    const result = await api.request<null>(`/properties/${id}`, { method: 'DELETE' })
    if (result.error) {
      error.value = result.error
      return false
    }
    properties.value = properties.value.filter(p => p.id !== id)
    if (currentId.value === id) select(properties.value[0]?.id ?? null)
    return true
  }

  return { properties, current, loaded, loading, error, needsSetup, load, select, create, update, remove }
}

let appStore: ReturnType<typeof createPropertiesStore> | null = null

/** The app-wide properties store, shared by the switcher and every page. */
export function useProperties() {
  appStore ??= createPropertiesStore(useApi(), browserStorage())
  return appStore
}
