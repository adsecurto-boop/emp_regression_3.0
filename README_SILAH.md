# Silah Custom Regression Framework & Test Execution Guide

## Overview
This document provides instructions for executing automated regression tests and stealth security audits on the **`silah-custom-regression`** branch. The framework supports multi-tenant environment routing between the standard **Dev** environment and the live production **Silah TTS Dashboard** (`https://tts.silah.com.sa/admin-login`).

---

## 💻 Step-by-Step Shell Commands to Prepare & Run

Run the following commands in your PowerShell / Terminal:

### 1. Git Branch Setup
```powershell
# 1. Switch to parent custom agent branch
git checkout custom-agent-regression

# 2. Create and checkout your new Silah-specific branch
git checkout -b silah-custom-regression
```

### 2. Generate Authenticated Session Profile (`silah_live`)
```powershell
# Authenticate against Silah Live Dashboard and cache session state to auth_silah_live.json
python scripts/generate_auth_state.py --env silah_live
```

### 3. Run Consolidated Silah Pytest Regression Suite
```powershell
# Execute Tickets 2025, 2028, and 2029 regression tests against Silah Live
pytest tests/test_silah_regression.py --env=silah_live -v
```

### 4. Launch Interactive Custom Executable & Stealth Orchestrator
```powershell
# Runs L1 WinReg Stealth Audit, L2 Process & Binary Inspection (DisplayConfigManager.exe),
# L3 Windows Defender Firewall & Network Audit, and L4 Web Telemetry Capture
python run_custom_regression.py
```

---

## 📋 Ticket Assertions & Evidence Mapping

### 1. Ticket 2028: Auto Checkout & Permissions (L4 Web UI to L1 `empm.ini`)
- **L4 Web Assertion**: Verifies non-admin roles require explicit "Auto Checkout" permission in the Roles & Permissions grid to access/configure idle threshold limits in Monitoring Control.
- **L1 Host Assertion**: Asserts that when a Silah employee is idle, system configuration in `empm.ini` is set to pause tracking (`visibility=false` or idle pause flag).

### 2. Ticket 2025: Monthly Auto-Email Reports & Permissions
- **L4 Web Assertion**: Asserts that "Timeline (Silah PDF)" and "Task (Silah PDF)" checkmarks/options are active in Report Settings.
- **Permission Guard**: Verifies non-admin managers can enable/disable monthly email reports at client level *only* if proper permission toggle is enabled in the Roles & Permissions matrix.

### 3. Ticket 2029: Reseller Bulk ZIP & Pagination Audit (L4 Web UI to L1 PDF Layout)
- **L4 Web Assertion**: Navigates to Reseller Monthly Reports page, checks "Paginate by Employee", and initiates bulk ZIP package download.
- **L1 Layout Validation (`zipfile` + `pypdf`)**:
  - Programmatically unpacks ZIP archive.
  - Verifies zero Super Admin (Silah) reports exist in the package.
  - Inspects page breaks across employee PDF reports to assert each employee's data starts on a brand-new page (pagination compliance).

---

## 📁 Key File Locations

- **Environment Router**: [`config/environments.py`](file:///c:/Project/Emp_regression_3.0/emp-regression-suite/config/environments.py)
- **Settings & Config**: [`config/settings.py`](file:///c:/Project/Emp_regression_3.0/emp-regression-suite/config/settings.py)
- **Auth Generator**: [`scripts/generate_auth_state.py`](file:///c:/Project/Emp_regression_3.0/emp-regression-suite/scripts/generate_auth_state.py)
- **Pytest Fixtures**: [`tests/conftest.py`](file:///c:/Project/Emp_regression_3.0/emp-regression-suite/tests/conftest.py)
- **Silah Test Suite**: [`tests/test_silah_regression.py`](file:///c:/Project/Emp_regression_3.0/emp-regression-suite/tests/test_silah_regression.py)
- **Orchestrator**: [`run_custom_regression.py`](file:///c:/Project/Emp_regression_3.0/emp-regression-suite/run_custom_regression.py)
- **Auth Profile Target**: `playwright-profile/auth_silah_live.json`
