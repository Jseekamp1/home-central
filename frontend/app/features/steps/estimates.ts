/** "15 min", "1 h", "1 h 30". */
export function formatMinutes(minutes: number): string {
  if (minutes < 60) return `${minutes} min`
  const hours = Math.floor(minutes / 60)
  const rest = minutes % 60
  return rest ? `${hours} h ${rest}` : `${hours} h`
}

/** Quick picks offered when estimating a step; null means "decide later". */
export const estimatePicks: { minutes: number | null, label: string }[] = [
  { minutes: 15, label: '15 min' },
  { minutes: 30, label: '30 min' },
  { minutes: 60, label: '1 h' },
  { minutes: 120, label: '2 h' },
  { minutes: 240, label: '4 h' },
  { minutes: null, label: 'Later' },
]

/**
 * Why a project can't be marked ready yet, or null if it can. Mirrors the
 * backend rule so the control can be disabled with the reason shown.
 */
export function readyBlocker(summary: { step_count: number, unestimated_step_count: number }): string | null {
  if (summary.step_count === 0) return 'Add a step with a time estimate first.'
  const missing = summary.unestimated_step_count
  if (missing === 0) return null
  return missing === 1 ? '1 step needs a time estimate.' : `${missing} steps need a time estimate.`
}
