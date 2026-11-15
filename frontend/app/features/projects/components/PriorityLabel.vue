<template>
  <span
    v-if="priority === 'urgent'"
    class="rounded-md bg-urgent px-1.5 py-0.5 text-xs font-bold text-urgent-foreground"
  >Urgent</span>
  <span v-else :class="priority === 'high' ? 'font-semibold text-attention' : 'text-muted-foreground'">
    {{ priorityLabel(priority) }}
  </span>
</template>

<script setup lang="ts">
import type { Schemas } from '~/shared/api/types'
import { priorityLabel } from '../labels'

defineProps<{ priority: Schemas['ProjectPriority'] }>()
</script>
