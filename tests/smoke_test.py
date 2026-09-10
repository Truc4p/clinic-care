import requests

BASE = "http://127.0.0.1:8000"


def smoke_test():
    # login
    resp = requests.post(f"{BASE}/auth/login", json={"email": "doctor@clinic.care", "password": "password123"})
    resp.raise_for_status()
    token = resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # create consultation
    payload = {
        "patient_name": "Test Patient",
        "notes": "Test notes",
        "diagnosis_codes": ["E11.9"]
    }
    r = requests.post(f"{BASE}/consultation", json=payload, headers=headers)
    r.raise_for_status()
    created = r.json()
    print("Created consultation ID:", created.get("id"))

    # list consultations
    r2 = requests.get(f"{BASE}/consultation", headers=headers)
    r2.raise_for_status()
    items = r2.json()
    print("Total consultations:", len(items))


if __name__ == "__main__":
    smoke_test()
