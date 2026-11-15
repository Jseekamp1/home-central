import { describe, it, expect } from 'vitest'
import { formatMinutes, readyBlocker } from '../estimates'

describe('formatMinutes', () => {
  it.each([
    [15, '15 min'],
    [60, '1 h'],
    [90, '1 h 30'],
    [245, '4 h 5'],
    [0, '0 min'],
  ])('%i minutes reads as "%s"', (minutes, text) => {
    expect(formatMinutes(minutes)).toBe(text)
  })
})

describe('readyBlocker', () => {
  it('asks for a first step when there are none', () => {
    expect(readyBlocker({ step_count: 0, unestimated_step_count: 0 })).toBe('Add a step with a time estimate first.')
  })

  it('counts the steps still missing an estimate', () => {
    expect(readyBlocker({ step_count: 3, unestimated_step_count: 1 })).toBe('1 step needs a time estimate.')
    expect(readyBlocker({ step_count: 3, unestimated_step_count: 2 })).toBe('2 steps need a time estimate.')
  })

  it('has nothing to say once every step is estimated', () => {
    expect(readyBlocker({ step_count: 3, unestimated_step_count: 0 })).toBeNull()
  })
})
