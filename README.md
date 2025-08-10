# Horizontal Three-Phase Separator Sizer

A minimal full-stack application (FastAPI + Vanilla JS) that sizes a horizontal three-phase separator using a Rule-of-Thumb approach.

---

## Project Structure

```
backend/
  ├── main.py           # FastAPI app & calculation logic
  ├── requirements.txt  # Python dependencies
  ├── input.json        # Example input data
  └── output.json       # Generated after running main.py
frontend/
  ├── index.html        # UI
  ├── styles.css        # Styling
  └── script.js         # Front-end logic
```

---

## Backend

1. **Install dependencies (preferably in a virtual environment):**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. **Run the API using Uvicorn:**

```bash
uvicorn main:app --reload
```

   The service will be available at `http://localhost:8000` and automatically reload on code changes.

3. **Manual calculation via CLI:**

   Edit `input.json` with your process data, then run:

```bash
python main.py
```

   Results will be saved to `output.json`.

---

## Frontend

Simply open `frontend/index.html` in any modern browser. Ensure the backend is running on `http://localhost:8000` (default FastAPI host/port). The UI will POST to `/api/size` and display the results.

- **Mobile-friendly:** The layout is responsive.
- **Validation:** The form checks that all inputs are positive numbers before sending.

---

## Example

Input:
```json
{
  "oil_flow_m3h": 36,
  "water_flow_m3h": 14,
  "allowable_liquid_velocity_m_s": 0.3,
  "L_over_D_ratio": 3
}
```

Output:
```json
{
    "oil_flow_m3h": 36.0,
    "water_flow_m3h": 14.0,
    "allowable_liquid_velocity_m_s": 0.3,
    "L_over_D_ratio": 3.0,
    "total_liquid_flow_m3h": 50.0,
    "total_liquid_flow_m3s": 0.013889,
    "required_area_m2": 0.0463,
    "diameter_m": 0.243,
    "length_m": 0.729
}
```

---

## Notes

- The sizing method is a simplified Rule-of-Thumb calculation. For detailed design, consult comprehensive separator design standards.
- Adjust CORS, authentication, or deployment configurations as needed for production environments.