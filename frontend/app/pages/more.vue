<template>
  <section aria-labelledby="more-title" class="mx-auto flex max-w-lg flex-col gap-5">
    <h1 id="more-title" class="text-3xl font-bold tracking-tight">More</h1>

    <ul class="flex flex-col divide-y divide-border rounded-xl border border-border bg-card">
      <li v-for="p in settingsFor" :key="p.id">
        <button type="button" :class="rowClass" @click="openSettings(p.id)">
          <Settings class="size-5 text-muted-foreground" aria-hidden="true" />
          <span class="flex min-w-0 flex-1 items-center gap-2">
            <PropertyDot v-if="hasMultiple" :color="p.my_color" size="sm" />
            <span class="truncate">{{ p.name }} settings</span>
          </span>
          <ChevronRight class="size-5 text-muted-foreground" aria-hidden="true" />
        </button>
      </li>
      <li>
        <NuxtLink to="/setup" :class="rowClass">
          <Plus class="size-5 text-muted-foreground" aria-hidden="true" />
          <span class="flex-1">Add a property</span>
          <ChevronRight class="size-5 text-muted-foreground" aria-hidden="true" />
        </NuxtLink>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ChevronRight, Plus, Settings } from 'lucide-vue-next'
import PropertyDot from '~/features/properties/components/PropertyDot.vue'
import { useProperties } from '~/features/properties/composables/useProperties'

const { properties, current, hasMultiple, select } = useProperties()

const rowClass = 'flex min-h-14 w-full items-center gap-3 px-4 text-left font-medium hover:bg-secondary focus-visible:outline-2 focus-visible:outline-ring'

// One property selected: its settings. All properties: a settings row for each.
const settingsFor = computed(() => (current.value ? [current.value] : properties.value))

async function openSettings(id: string) {
  select(id)
  await navigateTo('/property')
}
</script>
