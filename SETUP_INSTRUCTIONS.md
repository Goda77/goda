# Quick Setup Guide

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be available at: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Frontend Setup

1. **Open the frontend in your browser:**
   - Navigate to `frontend/index.html`
   - Or serve it with a simple HTTP server:
     ```bash
     cd frontend
     python3 -m http.server 8080
     ```
   - Then open: http://localhost:8080

2. **Ensure the backend is running** before using the frontend

## Testing

1. **Test the backend directly:**
   ```bash
   cd backend
   source venv/bin/activate
   python3 separator_calculator.py
   ```

2. **Test the API:**
   ```bash
   curl -X POST http://localhost:8000/api/size \
     -H "Content-Type: application/json" \
     -d '{"oil_flow_m3h": 36, "water_flow_m3h": 14, "allowable_liquid_velocity_m_s": 0.3, "L_over_D_ratio": 3}'
   ```

## Example Calculation

**Input:**
- Oil Flow: 36 m³/h
- Water Flow: 14 m³/h  
- Allowable Liquid Velocity: 0.3 m/s
- L/D Ratio: 3

**Output:**
- Total Liquid Flow: 50.0 m³/h
- Total Liquid Flow: 0.0139 m³/s
- Cross-sectional Area: 0.0463 m²
- Internal Diameter: 0.243 m
- Separator Length: 0.728 m

## Troubleshooting

- **Backend won't start:** Check if port 8000 is available
- **Frontend can't connect:** Ensure backend is running on http://localhost:8000
- **Calculation errors:** Verify all input values are positive numbers
- **Import errors:** Make sure virtual environment is activated and dependencies are installed