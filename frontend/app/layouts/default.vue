<template>
  <div class="min-h-dvh" :class="{ 'lg:grid lg:grid-cols-[15rem_minmax(0,1fr)]': showNav }">
    <!-- Desktop: sidebar with the property switcher and navigation. -->
    <aside v-if="showNav" class="sticky top-0 hidden h-dvh flex-col gap-5 border-r border-border bg-sidebar px-3 py-4 lg:flex">
      <PropertySwitcher />
      <nav aria-label="Main">
        <ul class="flex flex-col gap-1">
          <li v-for="item in items" :key="item.to">
            <NuxtLink
              :to="item.to"
              :aria-current="item.active ? 'page' : undefined"
              class="flex h-10 items-center gap-3 rounded-md border-l-2 px-3 text-sm focus-visible:outline-2 focus-visible:outline-ring"
              :class="item.active ? 'border-primary bg-secondary font-semibold text-foreground' : 'border-transparent font-medium text-muted-foreground hover:bg-secondary hover:text-foreground'"
            >
              <component :is="item.icon" class="size-5" aria-hidden="true" />
              {{ item.label }}
            </NuxtLink>
          </li>
        </ul>
      </nav>
    </aside>

    <div class="flex min-w-0 flex-col">
      <header class="mx-auto flex w-full max-w-3xl items-center justify-between gap-2 px-4 pt-3 pb-1" :class="{ 'lg:hidden': showNav }">
        <PropertySwitcher v-if="showNav" />
        <span v-else class="flex min-h-11 items-center font-display text-[17px] font-semibold">Home Central</span>
      </header>

      <div v-if="loadFailed" role="alert" class="mx-auto mt-2 flex w-full max-w-3xl items-center justify-between gap-3 px-4">
        <span class="text-sm text-destructive">{{ error }}</span>
        <Button variant="outline" size="sm" @click="load">Try again</Button>
      </div>

      <!-- Bottom padding keeps content clear of the phone's bottom bar. -->
      <main class="mx-auto w-full max-w-3xl px-4 pt-6 lg:px-8 lg:pt-10 lg:pb-10" :class="showNav ? 'pb-28' : 'pb-10'">
        <slot />
      </main>
    </div>

    <!-- Phone: bottom bar, padded clear of the home indicator. -->
    <nav
      v-if="showNav"
      aria-label="Main"
      class="fixed inset-x-0 bottom-0 border-t border-border bg-sidebar px-2 pt-1 lg:hidden"
      style="padding-bottom: max(0.5rem, env(safe-area-inset-bottom, 0px))"
    >
      <ul class="mx-auto grid max-w-md grid-cols-2">
        <li v-for="item in items" :key="item.to">
          <NuxtLink
            :to="item.to"
            :aria-current="item.active ? 'page' : undefined"
            class="flex h-12 flex-col items-center justify-center gap-0.5 rounded-md text-xs focus-visible:outline-2 focus-visible:outline-ring"
            :class="item.active ? 'font-semibold text-primary' : 'font-medium text-muted-foreground'"
          >
            <!-- The bar above the icon marks the current page without relying on color alone. -->
            <span aria-hidden="true" class="h-0.5 w-6 rounded-full" :class="item.active ? 'bg-primary' : 'bg-transparent'" />
            <component :is="item.icon" class="size-5" aria-hidden="true" />
            {{ item.label }}
          </NuxtLink>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ClipboardList, Ellipsis } from 'lucide-vue-next'
import { Button } from '~/shared/components/ui/button'
import PropertySwitcher from '~/features/properties/components/PropertySwitcher.vue'
import { useProperties } from '~/features/properties/composables/useProperties'

const route = useRoute()
const { current, isAll, error, loaded, load } = useProperties()

const loadFailed = computed(() => !loaded.value && !!error.value)
// No navigation until there's a property to navigate (first-run setup).
const showNav = computed(() => !!current.value || isAll.value)

// Items appear as their milestones ship: Week, Talk and Shop come later.
const items = computed(() => {
  const path = route.path
  return [
    { to: '/', label: 'Projects', icon: ClipboardList, active: path === '/' || path.startsWith('/projects') },
    { to: '/more', label: 'More', icon: Ellipsis, active: ['/more', '/property', '/setup'].includes(path) },
  ]
})
</script>
