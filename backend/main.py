"""
FastAPI application for Horizontal Three-Phase Separator Sizing Calculator

This module provides a REST API endpoint for performing separator sizing calculations
using the Rule-of-Thumb method.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

from separator_calculator import SeparatorInput, SeparatorOutput, size_separator

# Create FastAPI application instance
app = FastAPI(
    title="Separator Sizing Calculator",
    description="API for sizing horizontal three-phase separators using Rule-of-Thumb method",
    version="1.0.0"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint providing basic API information."""
    return {
        "message": "Horizontal Three-Phase Separator Sizing Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/size": "Calculate separator dimensions",
            "GET /docs": "Interactive API documentation"
        }
    }


@app.post("/api/size", response_model=SeparatorOutput)
async def calculate_separator_size(input_data: SeparatorInput) -> SeparatorOutput:
    """
    Calculate separator dimensions based on input parameters.
    
    This endpoint performs the complete separator sizing calculation using the Rule-of-Thumb method:
    1. Calculate total liquid flow (m³/h)
    2. Convert to m³/s
    3. Calculate required cross-sectional area (m²)
    4. Calculate internal diameter (m)
    5. Calculate separator length (m)
    
    Args:
        input_data: SeparatorInput object containing:
            - oil_flow_m3h: Oil phase volumetric flow rate in m³/h
            - water_flow_m3h: Water phase volumetric flow rate in m³/h
            - allowable_liquid_velocity_m_s: Maximum allowed liquid velocity in m/s
            - L_over_D_ratio: Length to diameter ratio for separator design
    
    Returns:
        SeparatorOutput object containing all calculation results
        
    Raises:
        HTTPException: If input validation fails or calculation errors occur
    """
    try:
        # Perform separator sizing calculations
        results = size_separator(input_data)
        return results
        
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "separator-calculator"}


if __name__ == "__main__":
    import uvicorn
    
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )