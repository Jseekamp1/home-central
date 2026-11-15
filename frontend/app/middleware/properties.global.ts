import { useProperties } from '~/features/properties/composables/useProperties'

// Load the user's properties once, and send anyone without a property to setup.
export default defineNuxtRouteMiddleware(async (to) => {
  const store = useProperties()
  if (!store.loaded.value && !store.loading.value) await store.load()
  if (store.needsSetup.value && to.path !== '/setup') return navigateTo('/setup')
})
