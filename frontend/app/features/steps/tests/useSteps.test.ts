import { describe, it, expect } from 'vitest'
import { createSteps } from '../composables/useSteps'
import type { ApiResult } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

type ProjectDetail = Schemas['ProjectDetail']

function detail(status: ProjectDetail['status']): ProjectDetail {
  return {
    id: 'p', property_id: 'prop', title: 'Replace faucet', description: null, status, priority: 'medium',
    due_date: null, completed_at: null, created_at: '', updated_at: '', my_role: 'owner',
    step_count: 1, done_step_count: 1, estimated_minutes: 15, unestimated_step_count: 0,
    steps: [{ id: 's1', position: 1, title: 'Turn off water', details: null, estimated_minutes: 15, wait_after_minutes: 0, keep_with_next: false, done_at: '2026-11-14T10:00:00Z' }],
  }
}

function fakeApi(response: ProjectDetail) {
  const calls: { path: string, method: string, body: unknown }[] = []
  async function request<T>(path: string, init: RequestInit = {}): Promise<ApiResult<T>> {
    calls.push({ path, method: init.method ?? 'GET', body: init.body ? JSON.parse(String(init.body)) : null })
    return { data: response as T, error: null, status: 200 }
  }
  return { request, calls }
}

describe('steps', () => {
  it('reports that checking off a step started the project', async () => {
    const api = fakeApi(detail('in_progress'))
    const steps = createSteps(api)

    const result = await steps.setDone(detail('draft'), 's1', true)

    expect(api.calls).toEqual([{ path: '/projects/p/steps/s1', method: 'PATCH', body: { done: true } }])
    expect(result?.started).toBe(true)
    expect(result?.project.status).toBe('in_progress')
  })

  it('does not report a start when the project was already under way', async () => {
    const steps = createSteps(fakeApi(detail('in_progress')))

    const result = await steps.setDone(detail('in_progress'), 's1', true)

    expect(result?.started).toBe(false)
  })

  it('moves a step by sending the full new order', async () => {
    const api = fakeApi(detail('draft'))
    const steps = createSteps(api)
    const project = { ...detail('draft'), steps: ['a', 'b', 'c'].map((id, i) => ({ ...detail('draft').steps[0]!, id, position: i + 1 })) }

    await steps.move(project, 'c', -1)

    expect(api.calls[0]).toEqual({ path: '/projects/p/steps/order', method: 'PUT', body: { step_ids: ['a', 'c', 'b'] } })
  })
})
