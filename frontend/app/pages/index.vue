<template>
  <section aria-labelledby="dashboard-title">
    <h1 id="dashboard-title" class="text-2xl font-bold mb-4">Dashboard</h1>

    <p v-if="error" role="alert" class="text-red-600">{{ error }}</p>

    <div v-else-if="user" class="bg-white rounded-lg shadow p-6">
      <p class="text-gray-600">Signed in as</p>
      <p class="text-lg font-medium">{{ user.display_name }}</p>
      <p class="text-sm text-gray-500">{{ user.email }}</p>
    </div>

    <p v-else class="text-gray-500" aria-live="polite">Loading…</p>
  </section>
</template>

<script setup lang="ts">
import { useApi } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'

const { request } = useApi()

const user = ref<Schemas['UserRead'] | null>(null)
const error = ref<string | null>(null)

onMounted(async () => {
  const result = await request<Schemas['UserRead']>('/me')
  user.value = result.data
  error.value = result.error
})
</script>
