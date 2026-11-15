import { ref } from 'vue'
import { useApi, type ApiResult } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

type ProjectDetail = Schemas['ProjectDetail']
type StepCreate = Schemas['StepCreate']
type StepUpdate = Schemas['StepUpdate']

interface Api {
  request<T>(path: string, init?: RequestInit): Promise<ApiResult<T>>
}

const NOT_STARTED: ProjectDetail['status'][] = ['draft', 'ready']

/**
 * Step changes. Each call returns the whole updated project from the server, so
 * positions, the summary and any status change all arrive together.
 */
export function createSteps(api: Api) {
  const error = ref<string | null>(null)

  async function send(path: string, method: string, body?: unknown): Promise<ProjectDetail | null> {
    error.value = null
    const result = await api.request<ProjectDetail>(path, { method, body: body === undefined ? undefined : JSON.stringify(body) })
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not save the step'
      return null
    }
    return result.data
  }

  function add(project: ProjectDetail, body: StepCreate) {
    return send(`/projects/${project.id}/steps`, 'POST', body)
  }

  function update(project: ProjectDetail, stepId: string, body: StepUpdate) {
    return send(`/projects/${project.id}/steps/${stepId}`, 'PATCH', body)
  }

  /** Check a step off (or back on). `started` says whether that started the project. */
  async function setDone(project: ProjectDetail, stepId: string, done: boolean) {
    const saved = await update(project, stepId, { done })
    if (!saved) return null
    return { project: saved, started: NOT_STARTED.includes(project.status) && saved.status === 'in_progress' }
  }

  function remove(project: ProjectDetail, stepId: string) {
    return send(`/projects/${project.id}/steps/${stepId}`, 'DELETE')
  }

  function reorder(project: ProjectDetail, stepIds: string[]) {
    return send(`/projects/${project.id}/steps/order`, 'PUT', { step_ids: stepIds })
  }

  /** Move a step up (-1) or down (+1) by sending the whole new order. */
  function move(project: ProjectDetail, stepId: string, delta: -1 | 1) {
    const ids = project.steps.map(s => s.id)
    const from = ids.indexOf(stepId)
    const to = from + delta
    if (from < 0 || to < 0 || to >= ids.length) return Promise.resolve(null)
    ids.splice(to, 0, ...ids.splice(from, 1))
    return reorder(project, ids)
  }

  return { error, add, update, setDone, remove, reorder, move }
}

export function useSteps() {
  return createSteps(useApi())
}
