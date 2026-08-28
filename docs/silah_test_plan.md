# Silah Custom Regression Master Test Plan & Strategy

> **Branch Target**: `silah-custom-regression` (derived from `custom-agent-regression`)  
> **Document Status**: Single Source of Truth for Test Objectives, Risk Register & Execution Scheduling  
> **Role & Authority**: Principal Software Quality Assurance (QA) Architect & Lead SDET  

---

## SECTION 1: Test Objectives & Scope

### 1.1 Ticket-Specific Quality Objectives

#### Ticket 2025: Auto Email Productivity Reports (Company Manager Role)
* **Objective 1.1.1 (PDF Naming Compliance)**: Verify that generated monthly productivity reports strictly comply with the mandatory naming schema:  
  `[Company Name] – Monthly Report – [Month] [Year]` (e.g., `Silah Tech – Monthly Report – August 2026`).
* **Objective 1.1.2 (Reseller Client Toggle)**: Validate that an Enable/Disable toggle is exposed in the Reseller Client Management page to control auto-email generation for Company Managers at the individual client level.
* **Objective 1.1.3 (Roles & Permissions Guard)**: Assert that non-admin users (e.g., Company Managers) can access and toggle the client-level report setting *only* when the "Monthly Auto-Email Reports" permission is explicitly active in the Roles & Permissions matrix.

#### Ticket 2028: Time Tracking Pause & Auto Checkout (Exclusive to Silah)
* **Objective 1.2.1 (Idle Threshold Configuration)**: Verify that when an employee exceeds the defined idle threshold under Monitoring Control, time tracking automatically pauses or checks out the user.
* **Objective 1.2.2 (Roles & Permissions Access Control)**: Assert that non-admin roles require the explicit "Auto Checkout" permission in the Roles & Permissions grid to view or modify idle threshold parameters in Monitoring Control.
* **Objective 1.2.3 (Host INI Alignment - L1)**: Assert that local system configuration inside `empm.ini` dynamically reflects idle pause behavior (`visibility=false` / idle pause flag active).

#### Ticket 2029: Bulk Reseller PDF Downloads & Pagination
* **Objective 1.3.1 (Bulk ZIP Archive Extraction)**: Verify that Resellers can trigger bulk ZIP downloads containing Timeline (Silah PDF) and Task Details (Silah PDF) reports for all client companies under their reseller account for a selected month.
* **Objective 1.3.2 (Super Admin Filtering Integrity)**: Assert that Silah Super Admin account records and reports are 100% excluded from the generated bulk ZIP archive.
* **Objective 1.3.3 (Employee Pagination Compliance - L1)**: Programmatically unpack the downloaded ZIP using Python `zipfile` and `pypdf` to verify that selecting "Paginate by Employee" ensures each employee's metrics start on a brand-new page.

---

### 1.2 The 4-Layer Validation Model

The test framework enforces cross-layer boundary validation across four distinct system operational tiers:

```
+-------------------------------------------------------------------------------+
|                        4-LAYER VALIDATION ARCHITECTURE                        |
+-------------------------------------------------------------------------------+
|  LAYER 4: Web UI Automation (Playwright Browser Contexts & POMs)              |
|  - Roles Grid, Monitoring Control, Client Management, Reseller Bulk Export    |
+-------------------------------------------------------------------------------+
|  LAYER 3: Outbound API Routing & Firewall Audit (NetworkAuditor)             |
|  - DNS/TCP Handshakes, Windows Defender Firewall Rules, Zero Cross-Leak Check |
+-------------------------------------------------------------------------------+
|  LAYER 2: Host Process & Custom Executable Inspection (psutil)                |
|  - DisplayConfigManager.exe, UpdateMgr_Emp.exe, esr.exe, emp_psa_service.exe  |
+-------------------------------------------------------------------------------+
|  LAYER 1: System Storage & File Structural Verification (winreg & pypdf)       |
|  - WinReg Cloaking, empm.ini Attributes (>3KB), PDF Stream Pagination Audit   |
+-------------------------------------------------------------------------------+
```

1. **Layer 1 (L1 - System Storage & Structural Layout)**:
   - Registry Stealth: Verify HKLM/HKCU uninstallation keys contain zero traces of `EmpMonitor` or custom executable names.
   - Host Configuration: Inspect `empm.ini` size (> 3.0 KB) and verify local stealth flags (`visibility=false`).
   - PDF Layout Inspection: Use `pypdf` to parse page boundaries, headers, and text streams in generated PDF artifacts.
2. **Layer 2 (L2 - Host Executable Runtime)**:
   - Inspect active running processes via `psutil` targeting Silah custom executable names on the host machine.
3. **Layer 3 (L3 - Outbound API Routing & Firewall Security)**:
   - Audit Windows Defender Firewall outbound rules via `netsh`.
   - Verify TCP/DNS connectivity matrix to target backend endpoints and enforce zero cross-environment data leakage.
4. **Layer 4 (L4 - Playwright Web UI Automation)**:
   - Automated end-to-end browser interactions targeting pre-authenticated Playwright storage states (`auth_silah_live.json` / `auth.json`).

---

### 1.3 Target Environments & Custom Executable Mappings

#### Target Environments
| Environment Key | Base URL | Login Endpoint | Session Auth Profile |
| :--- | :--- | :--- | :--- |
| **`dev`** | `https://app.dev.empmonitor.com` | `https://app.dev.empmonitor.com/amember/member` | `playwright-profile/auth.json` |
| **`silah_live`** | `https://tts.silah.com.sa` | `https://tts.silah.com.sa/admin-login` | `playwright-profile/auth_silah_live.json` |

#### Custom Executable Name Mapping (Silah Agent)
| Functional Role | Standard Name | Silah Custom Agent Name | Host Inspection Status |
| :--- | :--- | :--- | :--- |
| **Main Agent Process** | `empmonitor.exe` | `DisplayConfigManager.exe` | Monitored via `psutil` & disk binary check |
| **Watchdog / Service** | `UpdateMgr_Emp.exe` | `UpdateMgr_Emp.exe` | Monitored via `psutil` & disk binary check |
| **Screencast / Helper** | `esr.exe` | `esr.exe` | Monitored via `psutil` & disk binary check |
| **Helper Service** | `emp_psa_service.exe` | `emp_psa_service.exe` | Monitored via `psutil` & disk binary check |

---

## SECTION 2: Comprehensive Risk Register

| Risk ID | Risk Description | Severity / Impact | Technical Mitigation Strategy | Operational Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **R-001** | **L1 Configuration Sync Delay**: Local `empm.ini` on host machine does not update immediately following Web Dashboard setting changes. | **HIGH** | Implement fast-sync agent process restart (`fast_sync_agent_restart`) inside `sync_helper.py` to kill and relaunch `DisplayConfigManager.exe`, forcing immediate fetch from `/api/v3/user/config`. | If sync lags after restart, prompt operator via `prompt_conflict_resolution` to document tolerated conflict in final report. |
| **R-002** | **SMTP / Inbox Verification Constraints**: Live auto-email report delivery to external inbox cannot be verified via POP3/IMAP in isolated test runner environment. | **MEDIUM** | Validate the trigger condition at L4 (assert success alert & email dispatch queue entry in DB/UI) combined with PDF generator stream verification. | Use mock SMTP handler or UI status assertion ("Email Dispatched Successfully") for automated pass criteria. |
| **R-003** | **PDF Structural Verification Layout Drift**: Downloaded PDF reports alter page stream format or text formatting across versions, breaking layout assertion. | **HIGH** | Use robust PDF parsing via `pypdf.PdfReader` inspecting logical page boundaries and regex header patterns (`[Company] – Monthly Report`) rather than fixed pixel coordinates. | Fall back to fallback synthetic PDF stream generator (`_generate_sample_pdf_bytes`) for offline/staging testing. |
| **R-004** | **Authentication Cookie / Token Expiration**: Stale `auth_silah_live.json` session causes Playwright tests to redirect to `/admin-login` mid-suite execution. | **HIGH** | Implement automated session auto-healing inside `authenticated_context` fixture in `tests/conftest.py`. | Detect login input field presence; auto-fill credentials via `auth_helper.get_dashboard_credentials()` and update `auth_silah_live.json`. |
| **R-005** | **Silent Outbound Network / Firewall Blocking**: Host workstation firewall rules block TCP connection to Silah telemetry/update sockets without raising Python exceptions. | **MEDIUM** | Execute `NetworkAuditor.run_full_audit()` prior to web UI tests to query Windows Defender Firewall via `netsh` and test socket connection timeouts. | Surface explicit warnings in `custom_regression_report.md` outlining exact blocked domain/port combinations. |

---

## SECTION 3: Test Process Scheduling & Execution Sequence

The test execution roadmap is structured into five sequential phases to ensure complete framework reliability:

```
+-------------------------------------------------------------------------------+
|                         SEQUENTIAL TEST EXECUTION PHASES                       |
+-------------------------------------------------------------------------------+
| PHASE A: Test Analysis & Target Environment Mapping                          |
|   --> Audit client specifications, map URLs, establish silah-custom-regression |
+-------------------------------------------------------------------------------+
| PHASE B: Page Object Model (POM) Refactoring & Locators Mapping              |
|   --> Refactor BasePage, SettingsPage, and create Silah-specific POM components  |
+-------------------------------------------------------------------------------+
| PHASE C: Test Scripting & Verification Routine Development                    |
|   --> Implement Pytest suites for Tickets 2025, 2028, and 2029               |
+-------------------------------------------------------------------------------+
| PHASE D: Cross-Layer Network & PDF Audit Integration                          |
|   --> Integrate pypdf unpacker, NetworkAuditor L3 checks & winreg cloaking  |
+-------------------------------------------------------------------------------+
| PHASE E: Dry-Runs, Exception Checks, and Report Compilation                  |
|   --> Execute full test suite, verify auto-healing, compile Markdown report   |
+-------------------------------------------------------------------------------+
```

### Phase A: Test Analysis & Target Environment Mapping
- Analyze Silah client ticket requirements (Tickets 2025, 2028, 2029).
- Map environment URLs (`dev` vs `silah_live`).
- Establish `silah-custom-regression` branch and verify session profile paths (`auth_silah_live.json`).

### Phase B: Page Object Model (POM) Refactoring & Locators Mapping
- Refactor `BasePage` and `SettingsPage` to support multi-tenant selector fallbacks (EmpMonitor vs Silah TTS Admin).
- Map locators for Reseller Client Management, Roles & Permissions grid, Monitoring Control, and Reseller Reports.

### Phase C: Test Scripting & Verification Routine Development
- Author automated Playwright test scripts in `tests/test_silah_regression.py`.
- Enforce strict assertions for Auto Checkout permissions, Monthly Email Report toggles, and Reseller Bulk ZIP downloads.

### Phase D: Cross-Layer Network & PDF Audit Integration
- Integrate `pypdf` layout inspection to verify employee pagination and Super Admin exclusion in ZIP archives.
- Bind `NetworkAuditor` for L3 outbound firewall rule verification targeting `DisplayConfigManager.exe`.

### Phase E: Dry-Runs, Exception Checks, and Report Compilation
- Perform headless and headed test dry-runs against `silah_live` and `dev`.
- Verify session auto-healing on expired authentication state.
- Compile dynamic regression execution reports (`reports/custom_regression_report.md`).
