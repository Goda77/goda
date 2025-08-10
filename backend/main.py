"""FastAPI backend for sizing a horizontal three-phase separator using Rule-of-Thumb.

This module provides:
- Data model for inputs
- Validation for positive numeric inputs
- Calculation utilities (total flow, unit conversion, area, diameter, length)
- JSON IO helpers (read input.json, write output.json)
- FastAPI app with POST /api/size endpoint
- __main__ block to run calculations from input.json and save to output.json

Run the API locally (from the backend directory):
    uvicorn main:app --reload --port 8000
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# --------------------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------------------
class SeparatorInput(BaseModel):
    """Input schema for separator sizing.

    All fields must be positive numbers (> 0).
    """

    oil_flow_m3h: float = Field(..., description="Oil volumetric flow rate in m^3/h")
    water_flow_m3h: float = Field(..., description="Water volumetric flow rate in m^3/h")
    allowable_liquid_velocity_m_s: float = Field(
        ..., description="Allowable bulk liquid velocity in m/s"
    )
    L_over_D_ratio: float = Field(..., description="Length to Diameter ratio (L/D)")


class SeparatorResult(BaseModel):
    """Result schema for separator sizing."""

    oil_flow_m3h: float
    water_flow_m3h: float
    total_liquid_flow_m3h: float
    total_liquid_flow_m3s: float
    allowable_liquid_velocity_m_s: float
    required_cross_sectional_area_m2: float
    internal_diameter_m: float
    L_over_D_ratio: float
    separator_length_m: float


# --------------------------------------------------------------------------------------
# Utility paths
# --------------------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
INPUT_JSON_PATH = HERE / "input.json"
OUTPUT_JSON_PATH = HERE / "output.json"


# --------------------------------------------------------------------------------------
# Validation utilities
# --------------------------------------------------------------------------------------
def validate_positive_values(payload: Dict[str, Any]) -> None:
    """Validate that all required numeric inputs are present and positive.

    Raises:
        ValueError: if a field is missing or is not a positive number
    """
    required_fields = [
        "oil_flow_m3h",
        "water_flow_m3h",
        "allowable_liquid_velocity_m_s",
        "L_over_D_ratio",
    ]
    missing = [k for k in required_fields if k not in payload]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    for key in required_fields:
        value = payload[key]
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:  # noqa: PERF203
            raise ValueError(f"Field '{key}' must be a number") from exc
        if numeric_value <= 0:
            raise ValueError(f"Field '{key}' must be a positive number (> 0)")


# --------------------------------------------------------------------------------------
# Calculation utilities
# --------------------------------------------------------------------------------------
def calculate_total_liquid_flow_m3h(oil_flow_m3h: float, water_flow_m3h: float) -> float:
    """Return the total liquid flow in m^3/h by summing oil and water flows."""
    return oil_flow_m3h + water_flow_m3h


def convert_m3h_to_m3s(flow_m3h: float) -> float:
    """Convert volumetric flow from m^3/h to m^3/s."""
    return flow_m3h / 3600.0


def calculate_required_area_m2(flow_m3s: float, allowable_velocity_m_s: float) -> float:
    """Return required cross-sectional area A = Q / v."""
    return flow_m3s / allowable_velocity_m_s


def calculate_internal_diameter_m(area_m2: float) -> float:
    """Return internal diameter from circular area A = (pi/4) * D^2 => D = sqrt(4A/pi)."""
    if area_m2 <= 0:
        raise ValueError("Area must be positive")
    return math.sqrt(4.0 * area_m2 / math.pi)


def calculate_separator_length_m(diameter_m: float, L_over_D_ratio: float) -> float:
    """Return separator length from L/D ratio: L = (L/D) * D."""
    return L_over_D_ratio * diameter_m


def perform_sizing(payload: Dict[str, Any]) -> SeparatorResult:
    """Perform all sizing calculations and return a structured result.

    Args:
        payload: mapping with input fields

    Returns:
        SeparatorResult: structured results
    """
    validate_positive_values(payload)

    inputs = SeparatorInput(**payload)

    total_liq_m3h = calculate_total_liquid_flow_m3h(
        inputs.oil_flow_m3h, inputs.water_flow_m3h
    )
    total_liq_m3s = convert_m3h_to_m3s(total_liq_m3h)
    area_m2 = calculate_required_area_m2(
        total_liq_m3s, inputs.allowable_liquid_velocity_m_s
    )
    diameter_m = calculate_internal_diameter_m(area_m2)
    length_m = calculate_separator_length_m(diameter_m, inputs.L_over_D_ratio)

    result = SeparatorResult(
        oil_flow_m3h=inputs.oil_flow_m3h,
        water_flow_m3h=inputs.water_flow_m3h,
        total_liquid_flow_m3h=total_liq_m3h,
        total_liquid_flow_m3s=total_liq_m3s,
        allowable_liquid_velocity_m_s=inputs.allowable_liquid_velocity_m_s,
        required_cross_sectional_area_m2=area_m2,
        internal_diameter_m=diameter_m,
        L_over_D_ratio=inputs.L_over_D_ratio,
        separator_length_m=length_m,
    )
    return result


# --------------------------------------------------------------------------------------
# JSON IO helpers
# --------------------------------------------------------------------------------------
def read_input_json(path: Path = INPUT_JSON_PATH) -> Dict[str, Any]:
    """Read inputs from a JSON file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_output_json(result: SeparatorResult, path: Path = OUTPUT_JSON_PATH) -> None:
    """Write results to a JSON file in a human-readable format (indent=4)."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=4)


# --------------------------------------------------------------------------------------
# FastAPI application
# --------------------------------------------------------------------------------------
app = FastAPI(title="Separator Sizing API", version="1.0.0")

# Enable permissive CORS for local development and static frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/size", response_model=SeparatorResult)
async def size_separator(inputs: SeparatorInput) -> SeparatorResult:
    """POST endpoint to perform sizing given process inputs.

    Also writes the results to output.json on each request.
    """
    try:
        result = perform_sizing(inputs.dict())
    except ValueError as exc:  # validation errors
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    # Save to output.json
    try:
        write_output_json(result)
    except Exception as exc:  # noqa: BLE001
        # Do not fail the API response if file writing fails; include message instead
        raise HTTPException(status_code=500, detail=f"Failed to write output.json: {exc}")

    return result


# --------------------------------------------------------------------------------------
# __main__ runner
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Example batch run reading from input.json and writing output.json
    try:
        payload = read_input_json()
        result_obj = perform_sizing(payload)
        write_output_json(result_obj)
        print("Calculation complete. Results saved to:", OUTPUT_JSON_PATH)
        print(json.dumps(result_obj.model_dump(), indent=4))
    except FileNotFoundError:
        print(f"Input file not found at {INPUT_JSON_PATH}. Please create input.json.")
    except ValueError as ex:
        print(f"Validation error: {ex}")
    except Exception as ex:  # noqa: BLE001
        print(f"Unexpected error: {ex}")