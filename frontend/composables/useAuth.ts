const TOKEN_KEY = 'cliniccare_token'

export function useAuth() {
  const token = useState<string | null>('auth_token', () => null)

  const loadToken = () => {
    if (import.meta.client && !token.value) {
      token.value = localStorage.getItem(TOKEN_KEY)
    }
    return token.value
  }

  const setToken = (value: string | null) => {
    token.value = value
    if (import.meta.client) {
      if (value) localStorage.setItem(TOKEN_KEY, value)
      else localStorage.removeItem(TOKEN_KEY)
    }
  }

  const isAuthenticated = computed(() => Boolean(loadToken()))

  const logout = () => {
    setToken(null)
    navigateTo('/login')
  }

  return { token, loadToken, setToken, isAuthenticated, logout }
}
