### Horizontal 3-Phase Separator Sizing (Rule-of-Thumb)

A minimal full-stack app to size a horizontal three-phase separator using the Rule-of-Thumb method.

- **Backend**: Python, FastAPI (`backend/`)
- **Frontend**: HTML/CSS/Vanilla JS (`frontend/`)

---

### Backend (FastAPI)

Requirements:
- Python 3.9+

Install dependencies:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API server (default: `http://127.0.0.1:8000`):

```bash
cd backend
uvicorn main:app --reload --port 8000
```

API endpoint:
- `POST /api/size`
  - Body JSON fields: `oil_flow_m3h`, `water_flow_m3h`, `allowable_liquid_velocity_m_s`, `L_over_D_ratio`
  - Returns calculation results as JSON

Example request:

```bash
curl -X POST \
  -H 'Content-Type: application/json' \
  -d '{
        "oil_flow_m3h": 36,
        "water_flow_m3h": 14,
        "allowable_liquid_velocity_m_s": 0.3,
        "L_over_D_ratio": 3
      }' \
  http://127.0.0.1:8000/api/size | jq
```

Batch calculation (reads `backend/input.json` and writes `backend/output.json`):

```bash
python3 backend/main.py
```

The results are saved in a human-readable `output.json` with `indent=4`.

---

### Frontend (HTML + CSS + JS)

You can open `frontend/index.html` directly in a browser, or run a small static server for better CORS behavior:

```bash
cd frontend
python3 -m http.server 5500
# open http://127.0.0.1:5500 in your browser
```

The frontend expects the backend at `http://127.0.0.1:8000` (configured in `frontend/app.js`). Ensure the backend is running, then use the form to submit inputs and view results.

Input validation ensures all values are positive numbers before sending to the API. Any API errors will be displayed on the page.

---

### Notes
- The backend enables permissive CORS for local development.
- Code follows PEP8 style and is organized into small, testable functions.
- To adjust formatting precision in the UI, change the `toFixed(6)` inside `frontend/app.js`.