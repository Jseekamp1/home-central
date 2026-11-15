import { ref } from 'vue'
import { useApi, type ApiResult } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

type Project = Schemas['ProjectRead']
type ProjectDetail = Schemas['ProjectDetail']
type ProjectCreate = Schemas['ProjectCreate']
type ProjectUpdate = Schemas['ProjectUpdate']
export type ProjectView = Schemas['ProjectView']

interface Api {
  request<T>(path: string, init?: RequestInit): Promise<ApiResult<T>>
}

/** Which projects to show: one property's, or every property's together. */
export type ProjectScope = { propertyId: string } | { all: true }

const VIEW_OF_STATUS: Record<Project['status'], ProjectView> = {
  draft: 'active',
  ready: 'active',
  in_progress: 'active',
  done: 'done',
  cancelled: 'cancelled',
}

export function viewOf(status: Project['status']): ProjectView {
  return VIEW_OF_STATUS[status]
}

export function createProjectsStore(api: Api) {
  const projects = ref<Project[]>([])
  const view = ref<ProjectView>('active')
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function load(scope: ProjectScope, nextView: ProjectView) {
    view.value = nextView
    loading.value = true
    error.value = null
    const path = 'all' in scope ? '/projects' : `/properties/${scope.propertyId}/projects`
    const result = await api.request<Project[]>(`${path}?view=${nextView}`)
    loading.value = false
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not load projects'
      return
    }
    projects.value = result.data
  }

  async function get(id: string): Promise<ProjectDetail | null> {
    error.value = null
    const result = await api.request<ProjectDetail>(`/projects/${id}`)
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not load the project'
      return null
    }
    return result.data
  }

  async function create(propertyId: string, body: ProjectCreate): Promise<Project | null> {
    error.value = null
    const result = await api.request<Project>(`/properties/${propertyId}/projects`, { method: 'POST', body: JSON.stringify(body) })
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not create the project'
      return null
    }
    return result.data
  }

  async function update(id: string, body: ProjectUpdate): Promise<ProjectDetail | null> {
    error.value = null
    const result = await api.request<ProjectDetail>(`/projects/${id}`, { method: 'PATCH', body: JSON.stringify(body) })
    if (result.error || !result.data) {
      error.value = result.error ?? 'Could not save the project'
      return null
    }
    const saved = result.data
    // A project whose new status belongs to another tab leaves this list.
    projects.value = viewOf(saved.status) === view.value
      ? projects.value.map(p => (p.id === id ? saved : p))
      : projects.value.filter(p => p.id !== id)
    return saved
  }

  async function remove(id: string): Promise<boolean> {
    error.value = null
    const result = await api.request<null>(`/projects/${id}`, { method: 'DELETE' })
    if (result.error) {
      error.value = result.error
      return false
    }
    projects.value = projects.value.filter(p => p.id !== id)
    return true
  }

  return { projects, view, loading, error, load, get, create, update, remove }
}

let appStore: ReturnType<typeof createProjectsStore> | null = null

export function useProjects() {
  appStore ??= createProjectsStore(useApi())
  return appStore
}
