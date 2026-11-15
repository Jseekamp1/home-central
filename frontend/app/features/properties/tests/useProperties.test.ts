import { describe, it, expect } from 'vitest'
import { createPropertiesStore, type KeyValueStorage } from '../composables/useProperties'
import type { ApiResult } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

type Property = Schemas['PropertyRead']

function property(id: string, name: string): Property {
  return { id, name, kind: 'home', postal_code: '55401', address_line: null, notes: null, my_role: 'owner' }
}

// A small in-memory stand-in for the backend's /properties endpoints.
function fakeApi(initial: Property[]) {
  const rows = [...initial]
  let nextId = 100
  async function request<T>(path: string, init: RequestInit = {}): Promise<ApiResult<T>> {
    const method = init.method ?? 'GET'
    if (path === '/properties' && method === 'GET') {
      const sorted = [...rows].sort((a, b) => a.name.localeCompare(b.name))
      return { data: sorted as T, error: null, status: 200 }
    }
    if (path === '/properties' && method === 'POST') {
      const body = JSON.parse(String(init.body))
      const created = { ...property(String(nextId++), body.name), ...body, my_role: 'owner' }
      rows.push(created)
      return { data: created as T, error: null, status: 201 }
    }
    const id = path.split('/')[2]
    if (method === 'DELETE') {
      rows.splice(rows.findIndex(r => r.id === id), 1)
      return { data: null, error: null, status: 204 }
    }
    return { data: null, error: 'Not found', status: 404 }
  }
  return { request }
}

function memoryStorage(initial: Record<string, string> = {}): KeyValueStorage & { data: Record<string, string> } {
  const data = { ...initial }
  return {
    data,
    get: key => data[key] ?? null,
    set: (key, value) => { data[key] = value },
    remove: (key) => { delete data[key] },
  }
}

const KEY = 'home-central:current-property'

describe('properties store', () => {
  it('reopens the property remembered on this device', async () => {
    const store = createPropertiesStore(
      fakeApi([property('1', 'Our House'), property('2', "Mom's House")]),
      memoryStorage({ [KEY]: '2' }),
    )

    await store.load()

    expect(store.current.value?.name).toBe("Mom's House")
  })

  it('falls back to the first property when the remembered one is gone', async () => {
    const storage = memoryStorage({ [KEY]: 'deleted-elsewhere' })
    const store = createPropertiesStore(fakeApi([property('1', 'Our House'), property('2', 'Cabin')]), storage)

    await store.load()

    expect(store.current.value?.name).toBe('Cabin')
    expect(storage.data[KEY]).toBe('2')
  })

  it('needs setup only after loading shows no properties', async () => {
    const store = createPropertiesStore(fakeApi([]), memoryStorage())
    expect(store.needsSetup.value).toBe(false)

    await store.load()

    expect(store.needsSetup.value).toBe(true)
    expect(store.current.value).toBeNull()
  })

  it('selects a property right after creating it', async () => {
    const store = createPropertiesStore(fakeApi([property('1', 'Our House')]), memoryStorage())
    await store.load()

    const created = await store.create({ name: 'Grace Church', kind: 'organization', postal_code: '55402' })

    expect(created?.name).toBe('Grace Church')
    expect(store.current.value?.name).toBe('Grace Church')
    expect(store.properties.value.map(p => p.name)).toEqual(['Grace Church', 'Our House'])
  })

  it('moves to another property when the current one is deleted', async () => {
    const storage = memoryStorage({ [KEY]: '1' })
    const store = createPropertiesStore(fakeApi([property('1', 'Our House'), property('2', 'Cabin')]), storage)
    await store.load()

    await store.remove('1')

    expect(store.current.value?.name).toBe('Cabin')
    expect(storage.data[KEY]).toBe('2')

    await store.remove('2')

    expect(store.current.value).toBeNull()
    expect(store.needsSetup.value).toBe(true)
    expect(storage.data[KEY]).toBeUndefined()
  })
})
