<template>
  <section v-if="isAll" aria-labelledby="home-title" class="flex flex-col gap-5">
    <h1 id="home-title" class="text-3xl font-bold tracking-tight">All properties</h1>
    <ul class="flex flex-col gap-3">
      <li v-for="p in properties" :key="p.id">
        <button
          type="button"
          class="flex w-full items-center gap-3 rounded-xl border border-border bg-card p-4 text-left hover:bg-secondary focus-visible:outline-2 focus-visible:outline-ring"
          @click="select(p.id)"
        >
          <PropertyDot :color="p.my_color" />
          <span class="flex min-w-0 flex-1 flex-col">
            <span class="truncate font-semibold">{{ p.name }}</span>
            <span class="text-sm text-muted-foreground">{{ kindLabel(p.kind) }} · {{ roleLabel(p.my_role) }}</span>
          </span>
          <ChevronRight class="size-5 text-muted-foreground" aria-hidden="true" />
        </button>
      </li>
    </ul>
  </section>

  <section v-else-if="current" aria-labelledby="home-title" class="flex flex-col gap-5">
    <div class="flex items-baseline justify-between gap-3">
      <h1 id="home-title" class="flex items-center gap-3 text-3xl font-bold tracking-tight">
        <PropertyDot v-if="hasMultiple" :color="current.my_color" />
        {{ current.name }}
      </h1>
      <Button as-child variant="outline" size="sm">
        <NuxtLink to="/property">Settings</NuxtLink>
      </Button>
    </div>

    <dl class="grid grid-cols-2 gap-px overflow-hidden rounded-xl border border-border bg-border">
      <div class="flex flex-col gap-1 bg-card p-4">
        <dt class="text-sm text-muted-foreground">Kind</dt>
        <dd class="font-semibold">{{ kindLabel(current.kind) }}</dd>
      </div>
      <div class="flex flex-col gap-1 bg-card p-4">
        <dt class="text-sm text-muted-foreground">Your role</dt>
        <dd class="font-semibold">{{ roleLabel(current.my_role) }}</dd>
      </div>
      <div class="flex flex-col gap-1 bg-card p-4">
        <dt class="text-sm text-muted-foreground">Postal code</dt>
        <dd class="font-semibold">{{ current.postal_code }}</dd>
      </div>
      <div class="flex flex-col gap-1 bg-card p-4">
        <dt class="text-sm text-muted-foreground">Address</dt>
        <dd class="font-semibold">{{ current.address_line || '—' }}</dd>
      </div>
    </dl>

    <p v-if="current.notes" class="rounded-xl border border-border bg-card p-4 text-muted-foreground">{{ current.notes }}</p>
  </section>
</template>

<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
import { Button } from '~/shared/components/ui/button'
import PropertyDot from '~/features/properties/components/PropertyDot.vue'
import { useProperties } from '~/features/properties/composables/useProperties'
import { kindLabel, roleLabel } from '~/features/properties/kinds'

const { properties, current, isAll, hasMultiple, select } = useProperties()
</script>
