<template>
  <div>
    <div class="page-head">
      <div>
        <h1>New consultation</h1>
        <p>Record patient notes and attach ICD-10 diagnosis codes.</p>
      </div>
      <NuxtLink class="btn btn-secondary" to="/consultations">Back to list</NuxtLink>
    </div>

    <form class="card form" @submit.prevent="onSubmit">
      <div class="field">
        <label for="patient">Patient name</label>
        <input id="patient" v-model="patientName" required maxlength="255" placeholder="Full name" />
      </div>

      <div class="field">
        <label for="notes">Treatment / consultation notes</label>
        <textarea id="notes" v-model="notes" rows="5" required placeholder="Clinical notes…" />
      </div>

      <div class="field">
        <label for="icd">Search ICD-10 diagnosis</label>
        <input
          id="icd"
          v-model="icdQuery"
          placeholder="Type code or description (e.g. diabetes, J06.9)"
          @input="onSearch"
        />
        <ul v-if="suggestions.length" class="suggestions">
          <li v-for="dx in suggestions" :key="dx.code">
            <button type="button" @click="addDiagnosis(dx)">
              <strong>{{ dx.code }}</strong> — {{ dx.description }}
            </button>
          </li>
        </ul>
      </div>

      <div class="selected" v-if="selected.length">
        <span v-for="dx in selected" :key="dx.code" class="chip">
          {{ dx.code }}
          <button type="button" aria-label="Remove" @click="removeDiagnosis(dx.code)">×</button>
        </span>
      </div>
      <p v-else class="hint">Select at least one diagnosis code.</p>

      <p v-if="error" class="error">{{ error }}</p>

      <button class="btn" type="submit" :disabled="saving">
        {{ saving ? 'Saving…' : 'Save consultation' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import type { Diagnosis } from '~/composables/useApi'

definePageMeta({ middleware: 'auth' })

const { searchDiagnosis, createConsultation } = useApi()

const patientName = ref('')
const notes = ref('')
const icdQuery = ref('')
const suggestions = ref<Diagnosis[]>([])
const selected = ref<Diagnosis[]>([])
const error = ref('')
const saving = ref(false)
let searchTimer: ReturnType<typeof setTimeout> | null = null

function onSearch() {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(async () => {
    const q = icdQuery.value.trim()
    if (!q) {
      suggestions.value = []
      return
    }
    try {
      const results = await searchDiagnosis(q)
      const selectedCodes = new Set(selected.value.map((d) => d.code))
      suggestions.value = results.filter((d) => !selectedCodes.has(d.code))
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Diagnosis search failed'
    }
  }, 250)
}

function addDiagnosis(dx: Diagnosis) {
  if (!selected.value.some((d) => d.code === dx.code)) {
    selected.value.push(dx)
  }
  suggestions.value = []
  icdQuery.value = ''
}

function removeDiagnosis(code: string) {
  selected.value = selected.value.filter((d) => d.code !== code)
}

async function onSubmit() {
  error.value = ''
  if (!selected.value.length) {
    error.value = 'Please select at least one diagnosis code.'
    return
  }
  saving.value = true
  try {
    await createConsultation({
      patient_name: patientName.value.trim(),
      notes: notes.value.trim(),
      diagnosis_codes: selected.value.map((d) => d.code),
    })
    await navigateTo('/consultations')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to save consultation'
  } finally {
    saving.value = false
  }
}
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

.form {
  max-width: 720px;
}

.suggestions {
  list-style: none;
  margin: 0.4rem 0 0;
  padding: 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}

.suggestions button {
  width: 100%;
  text-align: left;
  border: none;
  background: transparent;
  padding: 0.65rem 0.8rem;
  cursor: pointer;
  border-bottom: 1px solid var(--line);
}

.suggestions li:last-child button {
  border-bottom: none;
}

.suggestions button:hover {
  background: #eef6f3;
}

.selected {
  margin-bottom: 1rem;
}

.hint {
  margin: 0 0 1rem;
  color: var(--muted);
  font-size: 0.9rem;
}
</style>
