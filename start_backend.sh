#!/bin/bash
# Startup script for the Horizontal Three-Phase Separator Sizing Backend

echo "Starting Horizontal Three-Phase Separator Sizing Backend..."
echo "============================================================"

# Navigate to backend directory
cd backend

# Add local bin to PATH for uvicorn
export PATH="/home/ubuntu/.local/bin:$PATH"

# Check if dependencies are installed
if ! python3 -c "import fastapi, uvicorn, pydantic" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --break-system-packages -r requirements.txt
fi

echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation available at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload