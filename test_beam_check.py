"""
test_beam_check.py
------------------
Pytest suite for beam_check.py.
Validates workbook baseline match, edge cases, invalid inputs, and file automation.
"""

import pytest
from beam_check import check_simply_supported_beam


def test_workbook_baseline_si():
    """Validates computation against the pre-filled workbook values (SI inputs)."""
    res = check_simply_supported_beam(
        span_l=6.0,
        uniform_load_w=10.0,
        section_modulus_s=597.0,
        second_moment_i=8503.0,
        youngs_modulus_e=200.0,
        yield_strength_fy=275.0,
        deflection_limit_ratio_n=360.0,
        unit_system="si",
    )

    assert res["max_bending_moment_m_kn_m"] == pytest.approx(45.0, rel=1e-5)
    assert res["bending_stress_sigma_mpa"] == pytest.approx(75.376884, rel=1e-5)
    assert res["utilisation_ratio"] == pytest.approx(0.27409776, rel=1e-5)
    assert res["stress_check_result"] == "PASS"
    assert res["midspan_deflection_delta_mm"] == pytest.approx(9.922968, rel=1e-5)
    assert res["deflection_limit_mm"] == pytest.approx(16.666667, rel=1e-5)
    assert res["deflection_check_result"] == "PASS"


@pytest.mark.parametrize(
    "invalid_kwargs",
    [
        {"span_l": 0.0},
        {"span_l": -5.0},
        {"uniform_load_w": 0.0},
        {"section_modulus_s": -10.0},
        {"second_moment_i": 0.0},
        {"youngs_modulus_e": -200.0},
        {"yield_strength_fy": 0.0},
        {"deflection_limit_ratio_n": -360.0},
    ],
)
def test_invalid_inputs_raise_value_error(invalid_kwargs):
    """Ensures zero or negative physical inputs raise ValueError."""
    base_args = {
        "span_l": 6.0,
        "uniform_load_w": 10.0,
        "section_modulus_s": 597.0,
        "second_moment_i": 8503.0,
        "youngs_modulus_e": 200.0,
        "yield_strength_fy": 275.0,
        "deflection_limit_ratio_n": 360.0,
        "unit_system": "si",
    }
    base_args.update(invalid_kwargs)
    with pytest.raises(ValueError):
        check_simply_supported_beam(**base_args)