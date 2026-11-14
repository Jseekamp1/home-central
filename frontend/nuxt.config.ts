import tailwindcss from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  // Client-only SPA: the app is a thin client of the API, which keeps it
  // portable to a PWA or Capacitor shell later.
  ssr: false,
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    // Nuxt 4.3's bundled Vite plugin types disagree with @tailwindcss/vite's
    // (rollup `PluginContextMeta.viteVersion`); same Vite at runtime. Remove
    // this once the types line up — the directive will then error.
    // @ts-expect-error mismatched Vite plugin types across packages
    plugins: [tailwindcss()],
  },
  typescript: { strict: true },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
    },
  },
})
