<template>
  <div>
    <div class="page-head">
      <div>
        <h1>Search notes</h1>
        <p>Find past consultations by patient name or diagnosis code.</p>
      </div>
    </div>

    <form class="card filters" @submit.prevent="onSearch">
      <div class="grid">
        <div class="field">
          <label for="patient">Patient name</label>
          <input id="patient" v-model="patient" placeholder="e.g. Jane" />
        </div>
        <div class="field">
          <label for="diagnosis">Diagnosis code or description</label>
          <input id="diagnosis" v-model="diagnosis" placeholder="e.g. E11.9 or diabetes" />
        </div>
      </div>
      <div class="actions">
        <button class="btn" type="submit" :disabled="pending">
          {{ pending ? 'Searching…' : 'Search' }}
        </button>
        <button class="btn btn-secondary" type="button" @click="onClear">Clear</button>
      </div>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <ConsultationTable
      v-if="searched"
      :items="items"
      empty-message="No matching consultation notes."
    />
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { listConsultations } = useApi()

const patient = ref('')
const diagnosis = ref('')
const items = ref<Awaited<ReturnType<typeof listConsultations>>>([])
const pending = ref(false)
const error = ref('')
const searched = ref(false)

async function onSearch() {
  error.value = ''
  pending.value = true
  searched.value = true
  try {
    items.value = await listConsultations({
      patient: patient.value.trim() || undefined,
      diagnosis: diagnosis.value.trim() || undefined,
    })
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Search failed'
    items.value = []
  } finally {
    pending.value = false
  }
}

function onClear() {
  patient.value = ''
  diagnosis.value = ''
  items.value = []
  searched.value = false
  error.value = ''
}
</script>

<style scoped>
.page-head {
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

.filters {
  margin-bottom: 1.25rem;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.actions {
  display: flex;
  gap: 0.75rem;
}

@media (max-width: 700px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
