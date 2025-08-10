"""
Horizontal Three-Phase Separator Sizing Calculator

This module provides functions for sizing horizontal three-phase separators
using the Rule-of-Thumb method based on liquid flow rates and design parameters.
"""

import json
import math
from typing import Dict, Any, Union
from pydantic import BaseModel, field_validator


class SeparatorInput(BaseModel):
    """Input parameters for separator sizing calculations."""
    
    oil_flow_m3h: float
    water_flow_m3h: float
    allowable_liquid_velocity_m_s: float
    L_over_D_ratio: float
    
    @field_validator('oil_flow_m3h', 'water_flow_m3h', 'allowable_liquid_velocity_m_s', 'L_over_D_ratio')
    @classmethod
    def validate_positive_numbers(cls, v):
        """Validate that all input values are positive numbers."""
        if v <= 0:
            raise ValueError('All input values must be positive numbers')
        return v


class SeparatorOutput(BaseModel):
    """Output results from separator sizing calculations."""
    
    total_liquid_flow_m3h: float
    total_liquid_flow_m3s: float
    required_cross_sectional_area_m2: float
    internal_diameter_m: float
    separator_length_m: float
    input_parameters: SeparatorInput


def calculate_total_liquid_flow(oil_flow_m3h: float, water_flow_m3h: float) -> float:
    """
    Calculate total liquid flow rate.
    
    Args:
        oil_flow_m3h: Oil phase volumetric flow rate in m³/h
        water_flow_m3h: Water phase volumetric flow rate in m³/h
        
    Returns:
        Total liquid flow rate in m³/h
    """
    return oil_flow_m3h + water_flow_m3h


def convert_m3h_to_m3s(flow_m3h: float) -> float:
    """
    Convert flow rate from m³/h to m³/s.
    
    Args:
        flow_m3h: Flow rate in m³/h
        
    Returns:
        Flow rate in m³/s
    """
    return flow_m3h / 3600.0


def calculate_cross_sectional_area(flow_m3s: float, velocity_m_s: float) -> float:
    """
    Calculate required cross-sectional area for the separator.
    
    Args:
        flow_m3s: Total liquid flow rate in m³/s
        velocity_m_s: Allowable liquid velocity in m/s
        
    Returns:
        Required cross-sectional area in m²
    """
    return flow_m3s / velocity_m_s


def calculate_diameter_from_area(area_m2: float) -> float:
    """
    Calculate internal diameter from cross-sectional area.
    
    Args:
        area_m2: Cross-sectional area in m²
        
    Returns:
        Internal diameter in m
    """
    # A = π * (D/2)² = π * D²/4
    # D = √(4A/π)
    return math.sqrt((4 * area_m2) / math.pi)


def calculate_separator_length(diameter_m: float, l_over_d_ratio: float) -> float:
    """
    Calculate separator length using L/D ratio.
    
    Args:
        diameter_m: Internal diameter in m
        l_over_d_ratio: Length to diameter ratio
        
    Returns:
        Separator length in m
    """
    return diameter_m * l_over_d_ratio


def size_separator(input_data: SeparatorInput) -> SeparatorOutput:
    """
    Perform complete separator sizing calculations.
    
    Args:
        input_data: SeparatorInput object containing all input parameters
        
    Returns:
        SeparatorOutput object containing all calculation results
    """
    # Step 1: Calculate total liquid flow (m³/h)
    total_liquid_flow_m3h = calculate_total_liquid_flow(
        input_data.oil_flow_m3h, 
        input_data.water_flow_m3h
    )
    
    # Step 2: Convert to m³/s
    total_liquid_flow_m3s = convert_m3h_to_m3s(total_liquid_flow_m3h)
    
    # Step 3: Calculate required cross-sectional area (m²)
    required_cross_sectional_area_m2 = calculate_cross_sectional_area(
        total_liquid_flow_m3s, 
        input_data.allowable_liquid_velocity_m_s
    )
    
    # Step 4: Calculate internal diameter (m)
    internal_diameter_m = calculate_diameter_from_area(required_cross_sectional_area_m2)
    
    # Step 5: Calculate separator length (m)
    separator_length_m = calculate_separator_length(
        internal_diameter_m, 
        input_data.L_over_D_ratio
    )
    
    # Create and return output object
    return SeparatorOutput(
        total_liquid_flow_m3h=round(total_liquid_flow_m3h, 4),
        total_liquid_flow_m3s=round(total_liquid_flow_m3s, 4),
        required_cross_sectional_area_m2=round(required_cross_sectional_area_m2, 4),
        internal_diameter_m=round(internal_diameter_m, 3),
        separator_length_m=round(separator_length_m, 3),
        input_parameters=input_data
    )


def load_input_from_file(filename: str = "input.json") -> SeparatorInput:
    """
    Load input parameters from a JSON file.
    
    Args:
        filename: Name of the JSON file to load
        
    Returns:
        SeparatorInput object with loaded parameters
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return SeparatorInput(**data)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in '{filename}'")
    except Exception as e:
        raise ValueError(f"Error loading input data: {str(e)}")


def save_output_to_file(output_data: SeparatorOutput, filename: str = "output.json") -> None:
    """
    Save calculation results to a JSON file.
    
    Args:
        output_data: SeparatorOutput object containing results
        filename: Name of the output file to save
    """
    try:
        with open(filename, 'w') as file:
            json.dump(output_data.model_dump(), file, indent=4)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {str(e)}")


def main():
    """
    Main function to run calculations from input.json and save to output.json.
    """
    try:
        print("Loading input parameters...")
        input_data = load_input_from_file()
        
        print("Performing separator sizing calculations...")
        results = size_separator(input_data)
        
        print("Calculation Results:")
        print(f"  Total Liquid Flow: {results.total_liquid_flow_m3h} m³/h")
        print(f"  Total Liquid Flow: {results.total_liquid_flow_m3s} m³/s")
        print(f"  Required Cross-sectional Area: {results.required_cross_sectional_area_m2} m²")
        print(f"  Internal Diameter: {results.internal_diameter_m} m")
        print(f"  Separator Length: {results.separator_length_m} m")
        
        save_output_to_file(results)
        print("Calculations completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()