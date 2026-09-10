<template>
  <div class="home card">
    <h1>ClinicCare Mini EMR</h1>
    <p>Manage consultation notes and ICD-10 diagnosis codes.</p>
    <NuxtLink class="btn" to="/login">Sign in</NuxtLink>
  </div>
</template>

<script setup lang="ts">
const { isAuthenticated, loadToken } = useAuth()
onMounted(() => {
  loadToken()
  if (isAuthenticated.value) navigateTo('/consultations')
})
</script>

<style scoped>
.home {
  margin-top: 4rem;
  max-width: 520px;
}

h1 {
  font-family: var(--display);
  margin-top: 0;
}

p {
  color: var(--muted);
}
</style>
