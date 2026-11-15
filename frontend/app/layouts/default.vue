<template>
  <div class="min-h-dvh">
    <header class="mx-auto flex max-w-3xl items-center justify-between gap-2 px-4 pt-3 pb-1">
      <PropertySwitcher v-if="current || isAll" />
      <span v-else class="flex min-h-11 items-center font-display text-[17px] font-semibold">Home Central</span>
    </header>

    <div v-if="loadFailed" role="alert" class="mx-auto mt-2 flex max-w-3xl items-center justify-between gap-3 px-4">
      <span class="text-sm text-destructive">{{ error }}</span>
      <Button variant="outline" size="sm" @click="load">Try again</Button>
    </div>

    <main class="mx-auto max-w-3xl px-4 py-6">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Button } from '~/shared/components/ui/button'
import PropertySwitcher from '~/features/properties/components/PropertySwitcher.vue'
import { useProperties } from '~/features/properties/composables/useProperties'

const { current, isAll, error, loaded, load } = useProperties()
const loadFailed = computed(() => !loaded.value && !!error.value)
</script>
