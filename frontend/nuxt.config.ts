// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000',
    },
  },
  app: {
    head: {
      title: 'ClinicCare Mini EMR',
      meta: [
        { name: 'description', content: 'Minimal EMR for consultation notes and ICD-10 codes' },
      ],
    },
  },
  css: ['~/assets/css/main.css'],
})
