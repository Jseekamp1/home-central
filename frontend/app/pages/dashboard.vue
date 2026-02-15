<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
    <div v-if="user" class="bg-white rounded-lg shadow p-6">
      <p class="text-gray-600">Logged in as</p>
      <p class="text-lg font-medium">{{ user.email }}</p>
      <p class="text-sm text-gray-400 mt-1">ID: {{ user.id }}</p>
    </div>
    <div v-else class="text-gray-500">Loading user info...</div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/features/auth/composables/useAuth'

definePageMeta({
  middleware: 'auth',
})

const { user, fetchUser } = useAuth()

onMounted(() => {
  fetchUser()
})
</script>
