<template>
  <div class="login-wrap">
    <form class="card login-card" @submit.prevent="onSubmit">
      <p class="eyebrow">ClinicCare Mini EMR</p>
      <h1>Doctor sign in</h1>
      <p class="sub">Use your clinic credentials to manage consultation notes.</p>

      <div class="field">
        <label for="email">Email</label>
        <input id="email" v-model="email" type="email" required autocomplete="username" />
      </div>
      <div class="field">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" required autocomplete="current-password" />
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <button class="btn" type="submit" :disabled="loading">
        {{ loading ? 'Signing in…' : 'Sign in' }}
      </button>
      <p class="demo">Demo: doctor@clinic.care / password123</p>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })

const { login } = useApi()
const { setToken, loadToken, isAuthenticated } = useAuth()

const email = ref('doctor@clinic.care')
const password = ref('password123')
const error = ref('')
const loading = ref(false)

onMounted(() => {
  loadToken()
  if (isAuthenticated.value) navigateTo('/consultations')
})

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    const res = await login(email.value.trim(), password.value)
    setToken(res.access_token)
    await navigateTo('/consultations')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
}

.login-card {
  width: min(420px, 100%);
}

.eyebrow {
  margin: 0;
  color: var(--accent);
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-size: 0.8rem;
}

h1 {
  font-family: var(--display);
  margin: 0.35rem 0 0.5rem;
}

.sub,
.demo {
  color: var(--muted);
}

.demo {
  margin-top: 1rem;
  font-size: 0.85rem;
}

.btn {
  width: 100%;
}
</style>
