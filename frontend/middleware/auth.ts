export default defineNuxtRouteMiddleware(() => {
  const { loadToken } = useAuth()
  if (import.meta.server) return
  const token = loadToken()
  if (!token) {
    return navigateTo('/login')
  }
})
