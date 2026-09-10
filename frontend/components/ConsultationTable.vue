<template>
  <div>
    <div v-if="!items.length" class="empty">{{ emptyMessage }}</div>
    <div v-else class="table-wrap card">
      <table class="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Diagnoses</th>
            <th>Notes</th>
            <th>Doctor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ formatDate(item.created_at) }}</td>
            <td>{{ item.patient_name }}</td>
            <td>
              <span v-for="dx in item.diagnoses" :key="dx.code" class="chip" :title="dx.description">
                {{ dx.code }}
              </span>
            </td>
            <td class="notes">{{ item.notes }}</td>
            <td>{{ item.doctor.full_name }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Consultation } from '~/composables/useApi'

defineProps<{
  items: Consultation[]
  emptyMessage?: string
}>()

function formatDate(value: string) {
  return new Date(value).toLocaleString()
}
</script>

<style scoped>
.table-wrap {
  overflow-x: auto;
  padding: 0.5rem 1rem 1rem;
}

.notes {
  max-width: 280px;
  white-space: pre-wrap;
}
</style>
