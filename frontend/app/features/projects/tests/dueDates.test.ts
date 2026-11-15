import { describe, it, expect } from 'vitest'
import { dueLabel, localToday } from '../dueDates'

describe('dueLabel', () => {
  const today = '2026-11-14'

  it('flags an active project whose due date has passed', () => {
    expect(dueLabel('2026-11-10', today, true)).toEqual({ text: 'Overdue · Nov 10', overdue: true })
  })

  it('shows the weekday for dates later this year, without shifting the day', () => {
    // Nov 22, 2026 is a Sunday everywhere; a time zone conversion would make it Saturday the 21st.
    expect(dueLabel('2026-11-22', today, true)).toEqual({ text: 'Due Sun, Nov 22', overdue: false })
  })

  it('never calls finished or cancelled projects overdue', () => {
    expect(dueLabel('2026-11-10', today, false)).toEqual({ text: 'Was due Nov 10', overdue: false })
  })
})

describe('localToday', () => {
  it("uses the device's own calendar date, not UTC", () => {
    // 11:30 PM on Nov 14 local time is already Nov 15 in UTC for anyone west of Greenwich.
    expect(localToday(new Date(2026, 10, 14, 23, 30))).toBe('2026-11-14')
  })
})
