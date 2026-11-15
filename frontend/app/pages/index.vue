<template>
  <section v-if="current" aria-labelledby="home-title" class="flex flex-col gap-5">
    <div class="flex items-baseline justify-between gap-3">
      <h1 id="home-title" class="text-3xl font-bold tracking-tight">{{ current.name }}</h1>
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
import { Button } from '~/shared/components/ui/button'
import { useProperties } from '~/features/properties/composables/useProperties'
import { kindLabel, roleLabel } from '~/features/properties/kinds'

const { current } = useProperties()
</script>
