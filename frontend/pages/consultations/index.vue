<template>
  <div>
    <div class="page-head">
      <div>
        <h1>Consultations</h1>
        <p>Past consultation notes recorded by clinic doctors.</p>
      </div>
      <NuxtLink class="btn" to="/consultations/new">New consultation</NuxtLink>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="pending" class="empty">Loading…</p>
    <ConsultationTable
      v-else
      :items="items"
      empty-message="No consultations yet. Create the first note."
    />
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { listConsultations } = useApi()
const items = ref<Awaited<ReturnType<typeof listConsultations>>>([])
const pending = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    items.value = await listConsultations()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load consultations'
  } finally {
    pending.value = false
  }
})
</script>

<style scoped>
.page-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

h1 {
  font-family: var(--display);
  margin: 0 0 0.35rem;
}

p {
  margin: 0;
  color: var(--muted);
}
</style>
