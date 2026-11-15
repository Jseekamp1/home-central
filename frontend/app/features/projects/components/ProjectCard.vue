<template>
  <NuxtLink
    :to="`/projects/${project.id}`"
    class="flex flex-col gap-2.5 rounded-xl border border-border bg-card p-4 hover:bg-secondary focus-visible:outline-2 focus-visible:outline-ring"
  >
    <span class="flex items-start justify-between gap-3">
      <span class="text-base leading-snug font-semibold">{{ project.title }}</span>
      <StatusBadge :status="project.status" />
    </span>
    <span class="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-sm text-muted-foreground">
      <span v-if="property" class="flex items-center gap-1.5 text-foreground">
        <PropertyDot :color="property.my_color" size="sm" />
        {{ property.name }}
      </span>
      <PriorityLabel :priority="project.priority" />
      <span v-if="due" :class="{ 'font-semibold text-attention': due.overdue }">{{ due.text }}</span>
    </span>
  </NuxtLink>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Schemas } from '~/shared/api/types'
import PropertyDot from '~/features/properties/components/PropertyDot.vue'
import { dueLabel, localToday } from '../dueDates'
import { viewOf } from '../composables/useProjects'
import PriorityLabel from './PriorityLabel.vue'
import StatusBadge from './StatusBadge.vue'

const props = defineProps<{
  project: Schemas['ProjectRead']
  /** Shown in All properties, so each card says where it belongs. */
  property?: Schemas['PropertyRead'] | null
}>()

const due = computed(() => dueLabel(props.project.due_date, localToday(), viewOf(props.project.status) === 'active'))
</script>
