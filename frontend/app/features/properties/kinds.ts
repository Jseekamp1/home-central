import type { Schemas } from '~/shared/api/types'

type PropertyKind = Schemas['PropertyKind']
type MemberRole = Schemas['MemberRole']

export const kindOptions: { value: PropertyKind, label: string }[] = [
  { value: 'home', label: 'Home' },
  { value: 'rental', label: 'Rental' },
  { value: 'family', label: "Family member's place" },
  { value: 'organization', label: 'Organization' },
  { value: 'other', label: 'Other' },
]

export function kindLabel(kind: PropertyKind): string {
  return kindOptions.find(o => o.value === kind)?.label ?? kind
}

export function roleLabel(role: MemberRole): string {
  return { owner: 'Owner', editor: 'Editor', viewer: 'View only' }[role]
}
