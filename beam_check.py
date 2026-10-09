"""
beam_check.py
-------------
Software Engineer I - Take-home Task: Simply-Supported Steel Beam Calculation Module.

This module evaluates a simply-supported steel beam under a uniform load, performing
both a bending-stress check and a midspan-deflection check according to standard textbook
engineering formulations (derived from Roark's Formulas for Stress and Strain / Timoshenko).

It also includes file automation to read inputs from 'source_.xlsx' and write outputs
back to the Calculation sheet.
"""

from typing import Dict, Union
import pandas as pd


def check_simply_supported_beam(
    span_l: float,
    uniform_load_w: float,
    section_modulus_s: float,
    second_moment_i: float,
    youngs_modulus_e: float,
    yield_strength_fy: float,
    deflection_limit_ratio_n: float = 360.0,
    unit_system: str = "si",
) -> Dict[str, Union[float, str]]:
    """Evaluates bending moment, bending stress, utilisation, midspan deflection,

    and engineering pass/fail checks for a simply-supported steel beam under uniform load.
    """
    # 1. Input Validation: Zero or negative values are invalid for physical beam properties.
    if span_l <= 0:
        raise ValueError(f"Span length (span_l) must be positive, got {span_l}.")
    if uniform_load_w <= 0:
        raise ValueError(
            f"Uniform load (uniform_load_w) must be positive, got {uniform_load_w}."
        )
    if section_modulus_s <= 0:
        raise ValueError(
            f"Section modulus (section_modulus_s) must be positive, got {section_modulus_s}."
        )
    if second_moment_i <= 0:
        raise ValueError(
            f"Second moment of area (second_moment_i) must be positive, got {second_moment_i}."
        )
    if youngs_modulus_e <= 0:
        raise ValueError(
            f"Young's modulus (youngs_modulus_e) must be positive, got {youngs_modulus_e}."
        )
    if yield_strength_fy <= 0:
        raise ValueError(
            f"Yield strength (yield_strength_fy) must be positive, got {yield_strength_fy}."
        )
    if deflection_limit_ratio_n <= 0:
        raise ValueError(
            f"Deflection limit ratio (deflection_limit_ratio_n) must be positive, got {deflection_limit_ratio_n}."
        )

    sys_lower = unit_system.strip().lower()
    if sys_lower not in ("si", "imperial"):
        raise ValueError(
            f"Invalid unit_system '{unit_system}'. Must be 'si' or 'imperial'."
        )

    # Conversion Constants
    FT_TO_M = 0.3048
    KIP_FT_TO_KN_M = 14.59390293720636
    IN3_TO_CM3 = 16.387064
    IN4_TO_CM4 = 41.62314256
    KSI_TO_GPA = 0.006894757293168361
    KSI_TO_MPA = 6.894757293168361
    IN_TO_MM = 25.4

    # Boundary Conversion to SI Base Units
    if sys_lower == "imperial":
        L_m = span_l * FT_TO_M
        w_kn_m = uniform_load_w * KIP_FT_TO_KN_M
        S_cm3 = section_modulus_s * IN3_TO_CM3
        I_cm4 = second_moment_i * IN4_TO_CM4
        E_gpa = youngs_modulus_e * KSI_TO_GPA
        fy_mpa = yield_strength_fy * KSI_TO_MPA
    else:
        L_m = float(span_l)
        w_kn_m = float(uniform_load_w)
        S_cm3 = float(section_modulus_s)
        I_cm4 = float(second_moment_i)
        E_gpa = float(youngs_modulus_e)
        fy_mpa = float(yield_strength_fy)

    n_ratio = float(deflection_limit_ratio_n)

    # Core Engineering Calculations (SI Units)
    M_kn_m = w_kn_m * (L_m**2) / 8.0
    sigma_mpa = (M_kn_m * 1000.0) / S_cm3
    utilisation = sigma_mpa / fy_mpa
    stress_status = "PASS" if utilisation <= 1.0 else "FAIL"

    E2_CONSTANT = 100000.0
    delta_mm = (
        (5.0 * w_kn_m * (L_m**4)) / (384.0 * E_gpa * I_cm4)
    ) * E2_CONSTANT
    deflection_limit_mm = (L_m * 1000.0) / n_ratio
    deflection_status = "PASS" if delta_mm <= deflection_limit_mm else "FAIL"

    # Dual-Unit Reporting Conversions
    results = {
        "span_l_m": L_m,
        "uniform_load_w_kn_per_m": w_kn_m,
        "section_modulus_s_cm3": S_cm3,
        "second_moment_i_cm4": I_cm4,
        "youngs_modulus_e_gpa": E_gpa,
        "yield_strength_fy_mpa": fy_mpa,
        "deflection_limit_ratio_n": n_ratio,
        "max_bending_moment_m_kn_m": M_kn_m,
        "bending_stress_sigma_mpa": sigma_mpa,
        "utilisation_ratio": utilisation,
        "stress_check_result": stress_status,
        "midspan_deflection_delta_mm": delta_mm,
        "deflection_limit_mm": deflection_limit_mm,
        "deflection_check_result": deflection_status,
    }

    return results


def process_beam_spreadsheet(file_path: str = r"D:\maha\source_.xlsx") -> None:
    """Reads inputs from Excel, calculates results using check_simply_supported_beam,

    and writes them back to the Calculation sheet.
    """
    df_inputs = pd.read_excel(file_path, sheet_name="Inputs")
    inputs_dict = dict(zip(df_inputs["Input"], df_inputs["Value"]))

    # Extract inputs with workbook defaults
    span = float(inputs_dict.get("Span, L", 6.0))
    load = float(inputs_dict.get("Uniform load, w", 10.0))
    s_mod = float(inputs_dict.get("Section modulus, S", 597.0))
    moment_i = float(inputs_dict.get("Second moment of area, I", 8503.0))
    youngs_e = float(inputs_dict.get("Young's modulus, E", 200.0))
    yield_f = float(inputs_dict.get("Yield strength, fy", 275.0))
    n_lim = float(
        inputs_dict.get("Deflection limit ratio, n (limit = L/n)", 360.0)
    )

    # Compute using core function
    res = check_simply_supported_beam(
        span_l=span,
        uniform_load_w=load,
        section_modulus_s=s_mod,
        second_moment_i=moment_i,
        youngs_modulus_e=youngs_e,
        yield_strength_fy=yield_f,
        deflection_limit_ratio_n=n_lim,
        unit_system="si",
    )

    # Format output table matching spreadsheet layout
    calc_data = [
        {"Quantity": "Max bending moment, M", "Value": res["max_bending_moment_m_kn_m"], "Unit": "kN·m"},
        {"Quantity": "Bending stress, sigma", "Value": res["bending_stress_sigma_mpa"], "Unit": "MPa"},
        {"Quantity": "Utilisation, sigma/fy", "Value": res["utilisation_ratio"], "Unit": "-"},
        {"Quantity": "Stress check", "Value": res["stress_check_result"], "Unit": "-"},
        {"Quantity": "Midspan deflection, delta", "Value": res["midspan_deflection_delta_mm"], "Unit": "mm"},
        {"Quantity": "Deflection limit, L/n", "Value": res["deflection_limit_mm"], "Unit": "mm"},
        {"Quantity": "Deflection check", "Value": res["deflection_check_result"], "Unit": "-"},
    ]

    df_calc = pd.DataFrame(calc_data)

    # Write back to Excel workbook
    with pd.ExcelWriter(
        file_path, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        df_inputs.to_excel(writer, sheet_name="Inputs", index=False)
        df_calc.to_excel(writer, sheet_name="Calculation", index=False)

    print(f"Successfully processed and updated '{file_path}'!")
    print(df_calc.to_string(index=False))


if __name__ == "__main__":
    process_beam_spreadsheet()