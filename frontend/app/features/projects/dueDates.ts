/**
 * Due dates are calendar dates ("2026-11-22"), not instants. They're kept as
 * ISO date strings, compared as strings (ISO dates sort correctly), and only
 * turned into a Date for formatting — in UTC on both sides, so the shown day
 * can never drift to the day before for someone west of Greenwich.
 *
 * Modern Web Guidance recommends Temporal.PlainDate for this; it isn't in
 * Safari yet and would need a polyfill dependency, so this stays dependency-free.
 */

export interface DueLabel {
  text: string
  overdue: boolean
}

/** Today's date on this device's own calendar, as "YYYY-MM-DD". */
export function localToday(now: Date = new Date()): string {
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

function format(iso: string, options: Intl.DateTimeFormatOptions): string {
  const [y, m, d] = iso.split('-').map(Number)
  const utcMidnight = new Date(Date.UTC(y!, m! - 1, d!))
  return new Intl.DateTimeFormat('en-US', { ...options, timeZone: 'UTC' }).format(utcMidnight)
}

export function dueLabel(due: string | null, today: string, active: boolean): DueLabel | null {
  if (!due) return null

  const sameYear = due.slice(0, 4) === today.slice(0, 4)
  const short = format(due, sameYear ? { month: 'short', day: 'numeric' } : { month: 'short', day: 'numeric', year: 'numeric' })

  if (!active) return { text: `Was due ${short}`, overdue: false }
  if (due < today) return { text: `Overdue · ${short}`, overdue: true }
  if (due === today) return { text: 'Due today', overdue: false }

  const withWeekday = sameYear ? format(due, { weekday: 'short', month: 'short', day: 'numeric' }) : short
  return { text: `Due ${withWeekday}`, overdue: false }
}
