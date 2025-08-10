# Horizontal Three-Phase Separator Sizing Application

A complete full-stack application for sizing horizontal three-phase separators using the Rule-of-Thumb method. This application calculates the required dimensions based on oil and water flow rates, allowable liquid velocity, and L/D ratio.

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── input.json          # Example input data
│   └── output.json         # Generated output (created after calculation)
├── frontend/
│   ├── index.html          # Main HTML interface
│   ├── styles.css          # CSS styling
│   └── script.js           # JavaScript functionality
├── start_backend.sh        # Backend startup script
├── start_frontend.sh       # Frontend startup script
└── README.md               # This file
```

## Features

### Backend (Python + FastAPI)
- **Calculation Engine**: Implements Rule-of-Thumb method for separator sizing
- **REST API**: POST endpoint `/api/size` for calculations
- **Input Validation**: Ensures all inputs are positive numbers
- **File I/O**: Reads from `input.json` and saves results to `output.json`
- **Error Handling**: Comprehensive error handling with meaningful messages

### Frontend (HTML + CSS + JavaScript)
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Validation**: Client-side input validation
- **Modern UI**: Clean, professional interface with gradient backgrounds
- **API Integration**: Communicates with backend via fetch API
- **Loading States**: Visual feedback during calculations

## Quick Start

1. **Start the backend server:**
   ```bash
   ./start_backend.sh
   ```

2. **In a new terminal, start the frontend:**
   ```bash
   ./start_frontend.sh
   ```

3. **Open your browser and go to:** `http://localhost:3000`

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- Modern web browser

### Backend Setup

#### Quick Start (Recommended)
```bash
./start_backend.sh
```

#### Manual Setup
1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install --break-system-packages -r requirements.txt
   ```

3. **Run the FastAPI server:**
   ```bash
   export PATH="/home/ubuntu/.local/bin:$PATH"
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: `http://localhost:8000`
   
   API documentation (Swagger UI): `http://localhost:8000/docs`

### Frontend Setup

#### Quick Start (Recommended)
```bash
./start_frontend.sh
```

#### Manual Setup
1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Open the frontend in a web browser:**
   - **Option 1**: Open `index.html` directly in your browser
   - **Option 2**: Use a simple HTTP server (recommended):
     ```bash
     # Using Python
     python3 -m http.server 3000
     
     # Using Node.js (if available)
     npx serve .
     ```

3. **Access the application:**
   - If using a server: `http://localhost:3000`
   - If opening directly: `file:///path/to/frontend/index.html`

## Usage

### Using the Web Interface

1. **Start the backend server** (see Backend Setup above)
2. **Open the frontend** in your web browser
3. **Enter the input parameters:**
   - Oil Flow Rate (m³/h)
   - Water Flow Rate (m³/h)
   - Allowable Liquid Velocity (m/s)
   - L/D Ratio
4. **Click "Calculate Separator Dimensions"**
5. **View the results** displayed in the results section

### Using the Backend Directly

#### Command Line Calculation
```bash
cd backend
python main.py
```
This will read from `input.json` and save results to `output.json`.

#### API Endpoint
```bash
curl -X POST "http://localhost:8000/api/size" \
     -H "Content-Type: application/json" \
     -d '{
       "oil_flow_m3h": 36,
       "water_flow_m3h": 14,
       "allowable_liquid_velocity_m_s": 0.3,
       "L_over_D_ratio": 3
     }'
```

## Calculation Method

The application uses the Rule-of-Thumb method for horizontal three-phase separator sizing:

1. **Total Liquid Flow**: Sum of oil and water flow rates
2. **Flow Rate Conversion**: Convert from m³/h to m³/s
3. **Cross-Sectional Area**: Calculate using Area = Flow / Velocity
4. **Internal Diameter**: Calculate using circular area formula: D = √(4 × Area / π)
5. **Separator Length**: Calculate using L = L/D ratio × Diameter

## Input Parameters

| Parameter | Unit | Description |
|-----------|------|-------------|
| Oil Flow Rate | m³/h | Volumetric flow rate of oil phase |
| Water Flow Rate | m³/h | Volumetric flow rate of water phase |
| Allowable Liquid Velocity | m/s | Maximum allowable liquid velocity in separator |
| L/D Ratio | - | Length to diameter ratio (typically 3-5) |

## Output Results

| Result | Unit | Description |
|--------|------|-------------|
| Total Liquid Flow | m³/h, m³/s | Combined oil and water flow rates |
| Required Cross-Sectional Area | m² | Minimum cross-sectional area needed |
| Internal Diameter | m | Required internal diameter of separator |
| Separator Length | m | Required length of separator |

## Example

### Input
```json
{
  "oil_flow_m3h": 36,
  "water_flow_m3h": 14,
  "allowable_liquid_velocity_m_s": 0.3,
  "L_over_D_ratio": 3
}
```

### Output
```json
{
  "total_liquid_flow_m3h": 50.0,
  "total_liquid_flow_m3s": 0.013889,
  "required_cross_sectional_area_m2": 0.046296,
  "internal_diameter_m": 0.2428,
  "separator_length_m": 0.7284
}
```

## Development

### Backend Development
- The main application is in `backend/main.py`
- Uses FastAPI with Pydantic for data validation
- Includes comprehensive docstrings and comments
- Follows PEP8 coding standards

### Frontend Development
- Vanilla JavaScript (no frameworks required)
- Responsive CSS with modern design
- Client-side validation
- Error handling and loading states

### API Documentation
When the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Troubleshooting

### Common Issues

1. **"Unable to connect to backend server"**
   - Ensure the FastAPI server is running on port 8000
   - Check that CORS is properly configured

2. **"Module not found" errors**
   - Install required Python packages: `pip install -r requirements.txt`

3. **Input validation errors**
   - Ensure all inputs are positive numbers
   - Check that decimal separator is correct for your locale

### CORS Issues
If you encounter CORS issues when running the frontend:
- Use a local HTTP server instead of opening HTML files directly
- Ensure the backend CORS middleware is properly configured

## License

This project is provided as-is for educational and engineering purposes.