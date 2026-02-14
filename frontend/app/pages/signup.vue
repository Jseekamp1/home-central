<template>
  <div class="max-w-sm mx-auto mt-16">
    <h1 class="text-2xl font-bold mb-6">Sign up</h1>
    <form class="space-y-4" @submit.prevent="handleSignup">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          class="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 px-3 py-2 border"
        />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          minlength="6"
          class="mt-1 block w-full rounded border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 px-3 py-2 border"
        />
      </div>
      <p v-if="error" class="text-red-600 text-sm">{{ error }}</p>
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 disabled:opacity-50"
      >
        {{ loading ? 'Creating account...' : 'Sign up' }}
      </button>
    </form>
    <p class="mt-4 text-sm text-gray-600">
      Already have an account?
      <NuxtLink to="/login" class="text-green-600 hover:underline">Log in</NuxtLink>
    </p>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth'

const { signup } = useAuth()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSignup() {
  error.value = ''
  loading.value = true
  try {
    await signup(email.value, password.value)
    navigateTo('/dashboard')
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>
