"""
Horizontal Three-Phase Separator Sizing Application
Using Rule-of-Thumb method

This application calculates the required dimensions for a horizontal
three-phase separator based on input flow rates and design parameters.
"""

import json
import math
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator


class SeparatorInput(BaseModel):
    """Input model for separator sizing calculations."""
    oil_flow_m3h: float
    water_flow_m3h: float
    allowable_liquid_velocity_m_s: float
    L_over_D_ratio: float

    @field_validator('oil_flow_m3h', 'water_flow_m3h', 'allowable_liquid_velocity_m_s', 'L_over_D_ratio')
    @classmethod
    def validate_positive(cls, v):
        """Validate that all inputs are positive numbers."""
        if v <= 0:
            raise ValueError('All inputs must be positive numbers')
        return v


class SeparatorOutput(BaseModel):
    """Output model for separator sizing results."""
    total_liquid_flow_m3h: float
    total_liquid_flow_m3s: float
    required_cross_sectional_area_m2: float
    internal_diameter_m: float
    separator_length_m: float


app = FastAPI(
    title="Horizontal Three-Phase Separator Sizing",
    description="Calculate separator dimensions using Rule-of-Thumb method",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_separator_dimensions(
    oil_flow_m3h: float,
    water_flow_m3h: float,
    allowable_liquid_velocity_m_s: float,
    L_over_D_ratio: float
) -> Dict[str, float]:
    """
    Calculate horizontal three-phase separator dimensions using Rule-of-Thumb method.
    
    Args:
        oil_flow_m3h: Oil flow rate in m³/h
        water_flow_m3h: Water flow rate in m³/h
        allowable_liquid_velocity_m_s: Maximum allowable liquid velocity in m/s
        L_over_D_ratio: Length to diameter ratio
    
    Returns:
        Dictionary containing calculated dimensions
    """
    # Step 1: Calculate total liquid flow (m³/h)
    total_liquid_flow_m3h = oil_flow_m3h + water_flow_m3h
    
    # Step 2: Convert to m³/s
    total_liquid_flow_m3s = total_liquid_flow_m3h / 3600
    
    # Step 3: Calculate required cross-sectional area (m²)
    # Using: Area = Flow / Velocity
    required_cross_sectional_area_m2 = total_liquid_flow_m3s / allowable_liquid_velocity_m_s
    
    # Step 4: Calculate internal diameter (m) using circular area formula
    # Area = π * D² / 4, therefore D = sqrt(4 * Area / π)
    internal_diameter_m = math.sqrt(4 * required_cross_sectional_area_m2 / math.pi)
    
    # Step 5: Calculate separator length (m) using L/D ratio
    separator_length_m = L_over_D_ratio * internal_diameter_m
    
    return {
        "total_liquid_flow_m3h": round(total_liquid_flow_m3h, 4),
        "total_liquid_flow_m3s": round(total_liquid_flow_m3s, 6),
        "required_cross_sectional_area_m2": round(required_cross_sectional_area_m2, 6),
        "internal_diameter_m": round(internal_diameter_m, 4),
        "separator_length_m": round(separator_length_m, 4)
    }


def save_results_to_file(results: Dict[str, float], filename: str = "output.json") -> None:
    """
    Save calculation results to a JSON file.
    
    Args:
        results: Dictionary containing calculation results
        filename: Output filename (default: output.json)
    """
    filepath = Path(__file__).parent / filename
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)


def load_input_from_file(filename: str = "input.json") -> Dict[str, float]:
    """
    Load input data from a JSON file.
    
    Args:
        filename: Input filename (default: input.json)
    
    Returns:
        Dictionary containing input parameters
    """
    filepath = Path(__file__).parent / filename
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file {filename} not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {filename}")


@app.post("/api/size", response_model=SeparatorOutput)
async def size_separator(input_data: SeparatorInput) -> SeparatorOutput:
    """
    Calculate separator dimensions based on input parameters.
    
    Args:
        input_data: Separator input parameters
    
    Returns:
        Calculated separator dimensions
    """
    try:
        results = calculate_separator_dimensions(
            oil_flow_m3h=input_data.oil_flow_m3h,
            water_flow_m3h=input_data.water_flow_m3h,
            allowable_liquid_velocity_m_s=input_data.allowable_liquid_velocity_m_s,
            L_over_D_ratio=input_data.L_over_D_ratio
        )
        
        # Save results to output.json
        save_results_to_file(results)
        
        return SeparatorOutput(**results)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Horizontal Three-Phase Separator Sizing API",
        "endpoints": {
            "POST /api/size": "Calculate separator dimensions"
        }
    }


if __name__ == "__main__":
    """
    Main execution block for testing calculations from input.json file.
    
    To run this script directly:
    python main.py
    
    To run the FastAPI server:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
    try:
        # Load input data from file
        input_data = load_input_from_file()
        print("Loaded input data:")
        print(json.dumps(input_data, indent=2))
        
        # Validate input data
        separator_input = SeparatorInput(**input_data)
        
        # Perform calculations
        results = calculate_separator_dimensions(
            oil_flow_m3h=separator_input.oil_flow_m3h,
            water_flow_m3h=separator_input.water_flow_m3h,
            allowable_liquid_velocity_m_s=separator_input.allowable_liquid_velocity_m_s,
            L_over_D_ratio=separator_input.L_over_D_ratio
        )
        
        # Save results to output.json
        save_results_to_file(results)
        
        print("\nCalculation Results:")
        print(json.dumps(results, indent=2))
        print(f"\nResults saved to output.json")
        
    except Exception as e:
        print(f"Error: {e}")