// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  // Client-only SPA: the app is a thin client of the API, which keeps it
  // portable to a PWA or Capacitor shell later.
  ssr: false,
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  typescript: { strict: true },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
    },
  },
})
