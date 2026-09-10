<template>
  <div>
    <header class="site-header" v-if="showNav">
      <div class="container header-inner">
        <NuxtLink to="/consultations" class="brand">ClinicCare</NuxtLink>
        <nav>
          <NuxtLink to="/consultations">Consultations</NuxtLink>
          <NuxtLink to="/consultations/new">New note</NuxtLink>
          <NuxtLink to="/search">Search</NuxtLink>
          <button class="btn-secondary btn logout" type="button" @click="logout">Log out</button>
        </nav>
      </div>
    </header>
    <main class="container main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { logout, isAuthenticated } = useAuth()

const showNav = computed(() => route.path !== '/login' && isAuthenticated.value)
</script>

<style scoped>
.site-header {
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
  gap: 1rem;
}

.brand {
  font-family: var(--display);
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--ink);
  text-decoration: none;
}

nav {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

nav a {
  color: var(--muted);
  font-weight: 600;
  text-decoration: none;
}

nav a.router-link-active {
  color: var(--accent);
}

.logout {
  padding: 0.4rem 0.75rem;
}

.main {
  padding: 1.75rem 0 3rem;
}

@media (max-width: 700px) {
  .header-inner {
    flex-direction: column;
    align-items: flex-start;
    padding: 0.75rem 0;
  }
}
</style>
