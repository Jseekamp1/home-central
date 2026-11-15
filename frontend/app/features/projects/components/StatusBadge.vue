<template>
  <span class="inline-flex shrink-0 items-center gap-1 rounded-md px-2 py-0.5 text-xs font-semibold" :class="classes[status]">
    <Check v-if="status === 'done'" class="size-3.5" aria-hidden="true" />
    {{ statusLabels[status] }}
  </span>
</template>

<script setup lang="ts">
import { Check } from 'lucide-vue-next'
import type { Schemas } from '~/shared/api/types'
import { statusLabels } from '../labels'

defineProps<{ status: Schemas['ProjectStatus'] }>()

const classes: Record<Schemas['ProjectStatus'], string> = {
  draft: 'bg-secondary text-foreground',
  ready: 'border border-project-time text-project-time-label',
  in_progress: 'bg-primary/15 text-project-time-label',
  done: 'bg-secondary text-muted-foreground',
  cancelled: 'bg-secondary text-muted-foreground line-through',
}
</script>
