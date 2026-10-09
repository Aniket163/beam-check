# Simply Supported Beam Checker (`simply-supported-beam-checker`)

An automated engineering calculation pipeline that converts spreadsheet structural calculations for a simply-supported steel beam under a uniform load into verified, production-grade Python code.

## 🚀 Features
* **Core Calculation Module (`beam_check.py`)**: Computes maximum bending moment ($M$), bending stress ($\sigma$), utilisation ratios ($\sigma/f_y$), midspan deflection ($\delta$), and pass/fail criteria according to standard textbook formulations.
* **Dual-Unit Support**: Accepts SI inputs by default with optional Imperial unit boundaries (`ft`, `kip/ft`, `in³`, `in⁴`, `ksi`) with automatic conversion.
* **Excel Integration**: Automatically reads beam parameters from `source_.xlsx` (Inputs sheet) and writes calculated verification results back to the Calculation sheet.
* **Rigorous Testing (`test_beam_check.py`)**: Comprehensive `pytest` suite ensuring baseline matching against workbook values and robust input error handling (`ValueError` on zero/negative values).
* **Verification & Validation (`VV.md`)**: Complete V&V report documenting governing formulas (*Roark's / Timoshenko*), boundary assumptions, and the discovered hard-coded unit multiplier (`E2 = 100,000.0`).

---

## 🛠️ Installation & Usage

### 1. Prerequisites
Ensure you have Python installed along with the required libraries:
```bash
pip install pandas openpyxl pytest
