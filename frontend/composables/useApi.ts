export type Diagnosis = {
  code: string
  description: string
}

export type Doctor = {
  id: number
  email: string
  full_name: string
}

export type Consultation = {
  id: number
  patient_name: string
  notes: string
  created_at: string
  doctor: Doctor
  diagnoses: Diagnosis[]
}

export function useApi() {
  const config = useRuntimeConfig()
  const { loadToken, setToken } = useAuth()

  async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
    const headers = new Headers(options.headers || {})
    if (!headers.has('Content-Type') && options.body) {
      headers.set('Content-Type', 'application/json')
    }
    const token = loadToken()
    if (token) headers.set('Authorization', `Bearer ${token}`)

    const response = await fetch(`${config.public.apiBase}${path}`, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      setToken(null)
      if (import.meta.client && !path.includes('/auth/login')) {
        await navigateTo('/login')
      }
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      let detail = `Request failed (${response.status})`
      try {
        const data = await response.json()
        if (typeof data.detail === 'string') detail = data.detail
        else if (Array.isArray(data.detail)) {
          detail = data.detail.map((d: { msg?: string }) => d.msg || JSON.stringify(d)).join('; ')
        }
      } catch {
        /* ignore parse errors */
      }
      throw new Error(detail)
    }

    if (response.status === 204) return undefined as T
    return (await response.json()) as T
  }

  return {
    login: (email: string, password: string) =>
      api<{ access_token: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),
    searchDiagnosis: (search: string) =>
      api<Diagnosis[]>(`/diagnosis?search=${encodeURIComponent(search)}`),
    listConsultations: (params: { patient?: string; diagnosis?: string } = {}) => {
      const q = new URLSearchParams()
      if (params.patient) q.set('patient', params.patient)
      if (params.diagnosis) q.set('diagnosis', params.diagnosis)
      const qs = q.toString()
      return api<Consultation[]>(`/consultation${qs ? `?${qs}` : ''}`)
    },
    createConsultation: (payload: {
      patient_name: string
      notes: string
      diagnosis_codes: string[]
    }) =>
      api<Consultation>('/consultation', {
        method: 'POST',
        body: JSON.stringify(payload),
      }),
  }
}
