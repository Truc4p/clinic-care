# ClinicCare Mini EMR

Minimal, secure web app for clinic consultation notes with ICD-10 diagnosis codes.

Doctors can search ICD-10 codes, record consultation notes with selected diagnoses, list past notes, and search by patient or diagnosis.

## Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy, SQLite, Pydantic, JWT |
| Frontend | Nuxt 3 (Vue 3) |
| Data | ~100 ICD-10-CM codes seeded from categories on [icd10data.com](https://www.icd10data.com/ICD10CM/Codes) |

## Project structure

```
```

### Run with Docker

Build and run backend + frontend with Docker Compose:

```bash
docker compose up --build
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

ClinicCare/
├── backend/
│   ├── app/                 # FastAPI application
│   ├── sql/seed_icd10.sql   # 100 ICD-10 diagnosis inserts
│   └── requirements.txt
├── frontend/                # Nuxt 3 app
└── README.md
```

## Setup and run

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# set required env vars (example)
export SECRET_KEY='replace-me-with-random-secret'
export DATABASE_URL='sqlite:///./cliniccare.db'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

On startup the app creates SQLite tables (`cliniccare.db`), loads ICD-10 codes if empty, and seeds a demo doctor.

### Environment variables

- `CLINICCARE_SECRET_KEY` — JWT secret (set to a strong random value in production)
- `DATABASE_URL` — SQLAlchemy database URL (defaults to local SQLite if unset)
- `CLINICCARE_FRONTEND_URL` — deployed frontend origin, for example `https://clinic-care-tau.vercel.app`. Multiple origins may be separated by commas.

For production, configure these variables on the backend host. A PostgreSQL URL
should use the `postgresql+psycopg://` scheme. See `backend/.env.example` for
the expected format. Configure the frontend separately in Vercel with:

On Render, set this backend variable exactly, without a trailing slash, then redeploy:

```bash
CLINICCARE_FRONTEND_URL=https://clinic-care-tau.vercel.app
```

```bash
NUXT_PUBLIC_API_BASE=https://your-backend-domain.com
```

To run the local smoke test (backend must be running):

```bash
python3 tests/smoke_test.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:3000

Optional API base override:

```bash
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000 npm run dev
```

## Demo login

| Field | Value |
|-------|-------|
| Email | `doctor@clinic.care` |
| Password | `password123` |

## API summary

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/login` | No | JSON `{ "email", "password" }` → JWT |
| `GET` | `/diagnosis?search=<term>` | No | Search local ICD-10 table |
| `POST` | `/consultation` | Bearer JWT | Create note with diagnosis codes |
| `GET` | `/consultation` | Bearer JWT | List notes; optional `patient`, `diagnosis` filters |
| `GET` | `/health` | No | Health check |
| `GET` | `/auth/me` | Bearer JWT | Return current authenticated doctor profile |

### Example requests

```bash
# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"doctor@clinic.care","password":"password123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Search diagnoses
curl "http://127.0.0.1:8000/diagnosis?search=diabetes"

# Create consultation
curl -X POST http://127.0.0.1:8000/consultation \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"patient_name":"Jane Doe","notes":"Follow-up","diagnosis_codes":["E11.9"]}'

# List / filter
curl "http://127.0.0.1:8000/consultation?patient=Jane" \
  -H "Authorization: Bearer $TOKEN"
curl "http://127.0.0.1:8000/consultation?diagnosis=E11.9" \
  -H "Authorization: Bearer $TOKEN"

# Get current doctor
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/auth/me
```

## Frontend pages

| Route | Purpose |
|-------|---------|
| `/login` | Doctor JWT login |
| `/consultations` | Table of past consultations |
| `/consultations/new` | New consultation form with ICD typeahead |
| `/search` | Search notes by patient or diagnosis |

## Features

- Pydantic validation on request bodies
- HTTP error responses for unknown diagnosis codes, auth failures, and bad input
- JWT-protected consultation create/list
- CORS enabled for local Nuxt (`localhost:3000`)

## License

Educational / assignment use.
