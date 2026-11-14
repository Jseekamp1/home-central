<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <nav aria-label="Main" class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
        <NuxtLink to="/" class="text-xl font-bold text-gray-900">Home Central</NuxtLink>
        <NuxtLink to="/" class="text-gray-600 hover:text-gray-900">Dashboard</NuxtLink>
      </nav>
    </header>
    <main class="max-w-4xl mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>
