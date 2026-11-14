<template>
  <div class="min-h-screen bg-background">
    <header class="border-b bg-card">
      <nav aria-label="Main" class="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
        <NuxtLink to="/" class="flex items-center gap-2 text-lg font-semibold">
          <House class="size-5 text-primary" aria-hidden="true" />
          Home Central
        </NuxtLink>
        <Button as-child variant="ghost" size="sm">
          <NuxtLink to="/">Dashboard</NuxtLink>
        </Button>
      </nav>
    </header>
    <main class="mx-auto max-w-4xl px-4 py-6 sm:py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { House } from 'lucide-vue-next'
import { Button } from '~/shared/components/ui/button'
</script>
