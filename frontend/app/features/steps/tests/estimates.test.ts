import { describe, it, expect } from 'vitest'
import { readyBlocker } from '../estimates'

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
