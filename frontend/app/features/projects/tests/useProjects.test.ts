import { describe, it, expect } from 'vitest'
import { createProjectsStore } from '../composables/useProjects'
import type { ApiResult } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

type Project = Schemas['ProjectRead']

function project(id: string, title: string, status: Project['status'] = 'draft'): Project {
  return {
    id, title, status, property_id: 'p1', description: null, priority: 'medium', due_date: null,
    completed_at: null, created_at: '2026-11-14T00:00:00Z', updated_at: '2026-11-14T00:00:00Z', my_role: 'owner',
    step_count: 0, done_step_count: 0, estimated_minutes: 0, unestimated_step_count: 0,
  }
}

// Records every request and answers from a small in-memory list.
function fakeApi(rows: Project[]) {
  const calls: string[] = []
  async function request<T>(path: string, init: RequestInit = {}): Promise<ApiResult<T>> {
    const method = init.method ?? 'GET'
    calls.push(`${method} ${path}`)
    if (method === 'GET') return { data: rows as T, error: null, status: 200 }
    if (method === 'PATCH') {
      const id = path.split('/')[2]
      const row = { ...rows.find(r => r.id === id)!, ...JSON.parse(String(init.body)) }
      return { data: row as T, error: null, status: 200 }
    }
    if (method === 'POST') {
      return { data: project('new', JSON.parse(String(init.body)).title) as T, error: null, status: 201 }
    }
    return { data: null, error: null, status: 204 }
  }
  return { request, calls }
}

describe('projects store', () => {
  it("loads one property's projects for the chosen view", async () => {
    const api = fakeApi([project('1', 'Replace faucet')])
    const store = createProjectsStore(api)

    await store.load({ propertyId: 'p1' }, 'done')

    expect(api.calls).toEqual(['GET /properties/p1/projects?view=done'])
    expect(store.projects.value.map(p => p.title)).toEqual(['Replace faucet'])
  })

  it('loads every property together for All properties', async () => {
    const api = fakeApi([])
    const store = createProjectsStore(api)

    await store.load({ all: true }, 'active')

    expect(api.calls).toEqual(['GET /projects?view=active'])
  })

  it('drops a project from the list when its new status belongs to another view', async () => {
    const store = createProjectsStore(fakeApi([project('1', 'Replace faucet'), project('2', 'Clean gutters')]))
    await store.load({ propertyId: 'p1' }, 'active')

    await store.update('1', { status: 'cancelled' })

    expect(store.projects.value.map(p => p.title)).toEqual(['Clean gutters'])
  })

  it('keeps a project in the list when it stays in the same view', async () => {
    const store = createProjectsStore(fakeApi([project('1', 'Replace faucet')]))
    await store.load({ propertyId: 'p1' }, 'active')

    await store.update('1', { status: 'in_progress' })

    expect(store.projects.value[0]?.status).toBe('in_progress')
  })
})
