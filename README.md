# Horizontal Three-Phase Separator Sizing Calculator

A full-stack web application for sizing horizontal three-phase separators using the Rule-of-Thumb method.

## Features

- **Backend**: FastAPI-based REST API for separator sizing calculations
- **Frontend**: Clean, responsive web interface for input and results display
- **Calculations**: Automatic computation of separator dimensions based on flow rates and design parameters

## Project Structure

```
├── backend/
│   ├── main.py
│   ├── separator_calculator.py
│   ├── input.json
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
```

## Backend Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Or for production:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. The API will be available at `http://localhost:8000`

### API Endpoints

- **POST** `/api/size` - Calculate separator dimensions
- **GET** `/docs` - Interactive API documentation (Swagger UI)

### Running Calculations Locally

You can also run calculations directly from the command line:
```bash
cd backend
python separator_calculator.py
```

This will read from `input.json` and save results to `output.json`.

## Frontend Setup

1. Open `frontend/index.html` in your web browser
2. Ensure the backend is running on `http://localhost:8000`
3. Enter your process parameters and click "Calculate"

## Input Parameters

- **Oil Flow (m³/h)**: Oil phase volumetric flow rate
- **Water Flow (m³/h)**: Water phase volumetric flow rate  
- **Allowable Liquid Velocity (m/s)**: Maximum allowed liquid velocity in separator
- **L/D Ratio**: Length to diameter ratio for separator design

## Calculation Method

The application uses the Rule-of-Thumb method:

1. **Total Liquid Flow**: Sum of oil and water flows
2. **Cross-sectional Area**: Total flow rate divided by allowable velocity
3. **Diameter**: Calculated from circular area formula
4. **Length**: Diameter multiplied by L/D ratio

## Example Input

```json
{
  "oil_flow_m3h": 36,
  "water_flow_m3h": 14,
  "allowable_liquid_velocity_m_s": 0.3,
  "L_over_D_ratio": 3
}
```

## Output Format

```json
{
  "total_liquid_flow_m3h": 50.0,
  "total_liquid_flow_m3s": 0.0139,
  "required_cross_sectional_area_m2": 0.0463,
  "internal_diameter_m": 0.243,
  "separator_length_m": 0.729,
  "input_parameters": {
    "oil_flow_m3h": 36,
    "water_flow_m3h": 14,
    "allowable_liquid_velocity_m_s": 0.3,
    "L_over_D_ratio": 3
  }
}
```

## Development

- Backend follows PEP8 Python coding standards
- Frontend uses vanilla JavaScript for simplicity
- API responses include input validation and error handling
- Responsive design for mobile and desktop use

## Troubleshooting

- Ensure backend is running before using frontend
- Check that all input values are positive numbers
- Verify API endpoint is accessible at `http://localhost:8000`
- Check browser console for any JavaScript errors