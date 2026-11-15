<template>
  <section aria-labelledby="setup-title" class="mx-auto flex max-w-lg flex-col gap-6">
    <div class="flex flex-col gap-2">
      <h1 id="setup-title" class="text-3xl font-bold tracking-tight">{{ firstRun ? 'Set up your first property' : 'Add a property' }}</h1>
      <p class="text-muted-foreground">
        A property is any place you look after: your home, a rental, a family member's place, or somewhere like your church.
      </p>
    </div>

    <div class="rounded-xl border border-border bg-card p-5">
      <PropertyForm
        submit-label="Create property"
        :busy="busy"
        :error="formError"
        :cancel-to="firstRun ? undefined : '/'"
        @submit="onSubmit"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import PropertyForm from '~/features/properties/components/PropertyForm.vue'
import { useProperties } from '~/features/properties/composables/useProperties'
import type { Schemas } from '~/shared/api/types'

const { properties, create, error } = useProperties()

const firstRun = computed(() => properties.value.length === 0)
const busy = ref(false)
const formError = ref<string | null>(null)

async function onSubmit(values: Schemas['PropertyCreate']) {
  busy.value = true
  formError.value = null
  const created = await create(values)
  busy.value = false
  if (!created) {
    formError.value = error.value
    return
  }
  await navigateTo('/')
}
</script>
