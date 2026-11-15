import type { Schemas } from '~/shared/api/types'

type ProjectStatus = Schemas['ProjectStatus']
type ProjectPriority = Schemas['ProjectPriority']

export const statusLabels: Record<ProjectStatus, string> = {
  draft: 'Draft',
  ready: 'Ready',
  in_progress: 'In progress',
  done: 'Done',
  cancelled: 'Cancelled',
}

export const priorityOptions: { value: ProjectPriority, label: string }[] = [
  { value: 'urgent', label: 'Urgent' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
]

export function priorityLabel(priority: ProjectPriority): string {
  return priorityOptions.find(o => o.value === priority)?.label ?? priority
}
