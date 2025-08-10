#!/bin/bash
# Startup script for the Horizontal Three-Phase Separator Sizing Frontend

echo "Starting Horizontal Three-Phase Separator Sizing Frontend..."
echo "============================================================"

# Navigate to frontend directory
cd frontend

echo "Starting HTTP server on http://localhost:3000"
echo "Make sure the backend is running on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the frontend server
python3 -m http.server 3000