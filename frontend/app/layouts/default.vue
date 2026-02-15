<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <NuxtLink to="/" class="text-xl font-bold text-gray-900">Home Central</NuxtLink>
        <div class="flex gap-4 items-center">
          <template v-if="isAuthenticated">
            <NuxtLink to="/dashboard" class="text-gray-600 hover:text-gray-900">Dashboard</NuxtLink>
            <button
              class="text-sm text-gray-500 hover:text-gray-700"
              @click="handleLogout"
            >
              Log out
            </button>
          </template>
          <template v-else>
            <NuxtLink to="/login" class="text-gray-600 hover:text-gray-900">Log in</NuxtLink>
            <NuxtLink to="/signup" class="bg-green-600 text-white px-3 py-1.5 rounded text-sm hover:bg-green-700">Sign up</NuxtLink>
          </template>
        </div>
      </div>
    </nav>
    <main class="max-w-4xl mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/features/auth/composables/useAuth'

const { isAuthenticated, logout } = useAuth()

function handleLogout() {
  logout()
  navigateTo('/login')
}
</script>
