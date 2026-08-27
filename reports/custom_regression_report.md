# Custom Agent Stealth & Security Regression Report

> **Generated On**: `2026-08-27 08:58:45`  
> **Target Environment**: `DEV` (`https://app.dev.empmonitor.com`)  
> **Agent Version Evaluated**: `3.5.0`

---

## 1. Executive Summary & Verdicts

| Audit Dimension | Evaluation Result | Status |
| :--- | :--- | :--- |
| **Final Report Verdict** | **`HEALTHY`** | ✅ PASS |
| **Covert Cloaking Verdict** | **`SECURE (Hidden from Control Panel)`** | 🛡️ SECURE |
| **Dashboard Visibility Setting** | `Stealth` (Expected: Stealth) | ✅ ALIGNED |
| **Target Dashboard User** | `auto test` | ✅ FOUND |
| **Host INI Visibility Flag** | `INI FILE NOT FOUND` | ⚠️ AUDIT |
| **Screencast Stream Status** | `STANDBY` | ⚪ STANDBY |

---

## 2. Custom Binary & Process Mapping

| Executable Role | Configured Process Name | Disk Binary Status | Host Process Runtime Status |
| :--- | :--- | :--- | :--- |
| **Main Agent** | `DisplayConfigManager.exe` | `NOT DETECTED ON DISK` | `INACTIVE` |
| **Watchdog / Service** | `UpdateMgr_Emp.exe` | `NOT DETECTED ON DISK` | `INACTIVE` |
| **Screencast / Helper** | `esr.exe` | `NOT DETECTED ON DISK` | `INACTIVE` |
| **Helper Service** | `emp_psa_service.exe` | `NOT DETECTED ON DISK` | `INACTIVE` |

---

## 3. Windows Control Panel Visibility Audit (winreg)

To verify that the custom stealth agent is invisible to host users in the Windows Control Panel (Add/Remove Programs), the three primary Windows uninstallation registry hives were audited:

| Scanned Registry Pathway | Scope / Architecture | Subkeys Audited | Cloaking Status |
| :--- | :--- | :---: | :--- |
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall (64-bit)` | 64-bit System Applications (HKLM) | 52 | **SECURE (0 traces found)** |
| `HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall (32-bit)` | 32-bit Applications on 64-bit OS (HKLM Wow6432Node) | 46 | **SECURE (0 traces found)** |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall` | Current User Scope Applications (HKCU) | 11 | **SECURE (0 traces found)** |

> **Stealth Assertion Passed**: No subkeys or values containing `EmpMonitor` or custom binary names were discovered in `HKEY_LOCAL_MACHINE` (64-bit/32-bit Wow6432Node) or `HKEY_CURRENT_USER` uninstallation keys.

---

## 4. Host Configuration & Storage Diagnostics (L1 / L2)

- **Local INI Path**: `Not Found`
- **INI File Size**: `0.0 KB` (EV-001 Requirement: > 3.0 KB)
- **Local Active Host Email**: `Unknown`
- **Visibility Flag in INI**: `N/A` (INI FILE NOT FOUND)

### Sanitized `config.js` Contents (Masked)
```json
Not Found
```

### Sanitized `empm.ini` Attributes (Masked)
```ini
```

---

## 5. Host Log Harvest (Last 200 Lines)

```text
No active host log file harvested for today.
```

---

## 6. Layer 4 Visual Evidence Artifacts

### Evidence: `01_employee_grid_match.png`
![01_employee_grid_match.png](evidence/01_employee_grid_match.png)
Link: [01_employee_grid_match.png](evidence/01_employee_grid_match.png)

### Evidence: `02_user_tracking_settings.png`
![02_user_tracking_settings.png](evidence/02_user_tracking_settings.png)
Link: [02_user_tracking_settings.png](evidence/02_user_tracking_settings.png)
