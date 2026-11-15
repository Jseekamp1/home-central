import type { Schemas } from '~/shared/api/types'

type PropertyColor = Schemas['PropertyColor']

export const colorOptions: { value: PropertyColor, label: string }[] = [
  { value: 'sky', label: 'Sky' },
  { value: 'teal', label: 'Teal' },
  { value: 'lime', label: 'Lime' },
  { value: 'violet', label: 'Violet' },
  { value: 'pink', label: 'Pink' },
  { value: 'coral', label: 'Coral' },
  { value: 'sand', label: 'Sand' },
  { value: 'slate', label: 'Slate' },
]

/** CSS value for a property color; the hex values live in main.css. */
export function colorVar(color: PropertyColor): string {
  return `var(--property-${color})`
}
