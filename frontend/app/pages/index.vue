<template>
  <section aria-labelledby="dashboard-title" class="space-y-4">
    <h1 id="dashboard-title" class="text-2xl font-bold">Dashboard</h1>

    <p v-if="error" role="alert" class="text-destructive">{{ error }}</p>

    <Card v-else-if="user">
      <CardHeader>
        <CardDescription>Signed in as</CardDescription>
        <CardTitle class="text-lg">{{ user.display_name }}</CardTitle>
      </CardHeader>
      <CardContent class="text-sm text-muted-foreground">{{ user.email }}</CardContent>
    </Card>

    <p v-else class="text-muted-foreground" aria-live="polite">Loading…</p>
  </section>
</template>

<script setup lang="ts">
import { useApi } from '~/shared/composables/useApi'
import type { Schemas } from '~/shared/api/types'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/shared/components/ui/card'

const { request } = useApi()

const user = ref<Schemas['UserRead'] | null>(null)
const error = ref<string | null>(null)

onMounted(async () => {
  const result = await request<Schemas['UserRead']>('/me')
  user.value = result.data
  error.value = result.error
})
</script>
