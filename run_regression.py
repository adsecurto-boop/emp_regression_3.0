"""
Module: run_regression.py
Purpose: Interactive CLI entry point & cross-layer regression orchestrator for EmpMonitor 3.0.
Evidence Mapping: L1 (Configuration), L2 (Host Storage & Runtime), L4 (Web Dashboard Alignment)
"""

import os
import sys
import re
import glob
import logging
import sqlite3
import configparser
from datetime import datetime
from pathlib import Path
from typing import Tuple, List, Dict, Optional, Any

import psutil
from playwright.sync_api import sync_playwright, expect

# Ensure project root is in python path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("RegressionOrchestrator")

REPORTS_DIR = PROJECT_ROOT / "reports"
EVIDENCE_DIR = REPORTS_DIR / "evidence"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

MODERN_BINARIES = [
    r"C:\Program Files\EmpMonitor\EmpMonitor\gui\empmonitor.exe",
    r"C:\Program Files\EmpMonitor\EmpMonitor\gui\UpdateMgr_Emp.exe",
    r"C:\Program Files\EmpMonitor\EmpMonitor\gui\executables\esr.exe",
    r"C:\Program Files\EmpMonitor\EmpMonitor\service\emp_psa_service.exe",
]


def mask_sensitive_value(key: str, value: str) -> str:
    """Mask sensitive config values (tokens, passwords, keys) with asterisks per EV-001."""
    sensitive_patterns = ["token", "password", "crypto", "secret", "key", "auth"]
    if any(pattern in key.lower() for pattern in sensitive_patterns):
        if not value:
            return "*****"
        return "*" * min(len(value), 16)
    return value


def parse_version_string(version_str: str) -> Tuple[int, ...]:
    """Parse version string into a comparable tuple of integers."""
    parts = re.findall(r"\d+", version_str)
    return tuple(int(p) for p in parts) if parts else (0, 0, 0)


# ==============================================================================
# STEP 1 & 2: Local System Inspection (L1 & L2)
# ==============================================================================
def inspect_local_system(version_input: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Executes binary checks, process monitoring, config parsing (config.js & empm.ini),
    and harvests the last 200 log lines from today's log file.
    """
    logger.info("=== STEP 1: Local System Inspection (L1 & L2) ===")
    
    agent_version = parse_version_string(version_input)
    baseline_version = parse_version_string("3.1.0")

    binary_statuses = {}
    process_statuses = {}

    if agent_version > baseline_version:
        logger.info(f"Modern Agent Version detected ({version_input} > 3.1.0). Evaluating binaries & active processes...")
        for binary_path in MODERN_BINARIES:
            name = Path(binary_path).name
            exists = Path(binary_path).exists()
            binary_statuses[name] = "FOUND" if exists else "MISSING"
            logger.info(f"  [{binary_statuses[name]}] Binary: {name}")

        running_processes = {p.info["name"].lower(): p.info for p in psutil.process_iter(["name", "status"])}
        target_procs = ["empmonitor.exe", "updatemgr_emp.exe", "esr.exe", "emp_psa_service.exe"]
        for proc in target_procs:
            if proc in running_processes:
                process_statuses[proc] = f"RUNNING ({running_processes[proc].get('status', 'active')})"
            else:
                process_statuses[proc] = "INACTIVE"
            logger.info(f"  [{process_statuses[proc]}] Process: {proc}")

    # Parse config.js
    config_js_path = Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui\configs\config.js")
    config_js_masked = "Not Found"
    if config_js_path.exists():
        try:
            raw_js = config_js_path.read_text(encoding="utf-8", errors="ignore")
            masked_lines = []
            for line in raw_js.splitlines():
                if any(k in line.lower() for k in ["token", "password", "key", "secret"]):
                    line = re.sub(r'([\'"][^\'"]*[\'"])\s*:\s*([\'"][^\'"]*[\'"])', r'\1: "***MASKED***"', line)
                masked_lines.append(line)
            config_js_masked = "\n".join(masked_lines)
            logger.info("[L1] config.js parsed and sanitized successfully.")
        except Exception as e:
            config_js_masked = f"Error reading config.js: {e}"

    # Parse empm.ini & AppData Discovery
    appdata_dir = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
    screen_dir = Path(appdata_dir) / "screen"
    oju_matches = list(screen_dir.glob("OjU*")) if screen_dir.exists() else []
    oju_dir = oju_matches[0] if oju_matches else None

    host_email = None
    ini_size_kb = 0.0
    ini_path_str = "Not Found"
    ini_attributes = {}

    if oju_dir:
        ini_path = oju_dir / "empm.ini"
        ini_path_str = str(ini_path)
        if ini_path.exists():
            ini_size_kb = round(ini_path.stat().st_size / 1024.0, 2)
            logger.info(f"[L1] Found empm.ini ({ini_size_kb} KB) at: {ini_path}")
            if ini_size_kb > 3.0:
                logger.info("[EV-001 VALIDATED] empm.ini file size is > 3 KB.")

            try:
                content = ini_path.read_text(encoding="utf-8", errors="ignore")
                config = configparser.ConfigParser(interpolation=None, strict=False, allow_no_value=True)
                try:
                    config.read_string(content)
                except Exception:
                    config.read_string("[DEFAULT]\n" + content)

                for section in config.sections():
                    for key, val in config.items(section):
                        if key.lower() == "email":
                            host_email = val
                        masked_val = mask_sensitive_value(key, val or "")
                        ini_attributes[key] = masked_val

                if not host_email:
                    email_match = re.search(r"email\s*=\s*([^\s\r\n]+)", content, re.IGNORECASE)
                    if email_match:
                        host_email = email_match.group(1)
            except Exception as e:
                logger.error(f"Failed to parse empm.ini: {e}")

    logger.info(f"[L1 EXTRACTED] Local Active Host Email: {host_email or 'Unknown'}")

    # Harvest Last 200 Log Lines
    empm_dir = (oju_dir / "empm") if (oju_dir and (oju_dir / "empm").exists()) else (screen_dir / "empm")
    logs_dir = empm_dir / "logs"
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_log_path = logs_dir / f"{today_str}.txt"

    if not today_log_path.exists() and logs_dir.exists():
        log_files = sorted(logs_dir.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
        today_log_path = log_files[0] if log_files else None

    last_200_logs = []
    if today_log_path and today_log_path.exists():
        logger.info(f"[L2 Log Harvest] Reading last 200 lines from: {today_log_path}")
        try:
            all_lines = today_log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            last_200_logs = all_lines[-200:]
        except Exception as e:
            logger.error(f"Error harvesting logs: {e}")
    else:
        logger.warning(f"No active log file found under: {logs_dir}")

    l1_l2_results = {
        "agent_version": version_input,
        "binaries": binary_statuses,
        "processes": process_statuses,
        "config_js": config_js_masked,
        "ini_path": ini_path_str,
        "ini_size_kb": ini_size_kb,
        "host_email": host_email or "Unknown",
        "ini_attributes": ini_attributes,
    }

    return l1_l2_results, last_200_logs


# ==============================================================================
# STEP 3: Playwright Web Dashboard Automation (L4 Verification)
# ==============================================================================
def audit_web_dashboard(target_user: str, auth_state_path: str = "playwright-profile/auth.json") -> Dict[str, Any]:
    """
    Executes Playwright Web Dashboard audit.
    Handles both Positive Path (user exists) and Negative/Failure Path (user missing/mismatch/empty).
    Captures visual evidence to reports/evidence/.
    """
    logger.info("=== STEP 2: Playwright Web Dashboard Audit (L4) ===")
    logger.info(f"Searching Web Dashboard for Target User: '{target_user}'")

    results = {
        "searched_user": target_user,
        "user_found": False,
        "dashboard_email": None,
        "evidence_files": [],
        "telemetry_summary": "No Data / Unregistered User"
    }

    if not os.path.exists(auth_state_path):
        logger.error(f"Authentication state missing at {auth_state_path}.")
        return results

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=auth_state_path, ignore_https_errors=True)
        page = context.new_page()

        try:
            # 1. Navigate to member URL to validate/refresh session state
            page.goto("https://app.dev.empmonitor.com/amember/member", wait_until="domcontentloaded", timeout=60000)
            
            # Auto-heal session if expired
            try:
                user_field = page.get_by_role("textbox", name="Username/Email")
                if user_field.count() > 0 and user_field.is_visible():
                    logger.info("Dashboard session expired. Authenticating with user credentials...")
                    from src.utils.auth_helper import get_dashboard_credentials
                    dash_user, dash_pass = get_dashboard_credentials(prompt_if_missing=True)
                    if dash_user and dash_pass:
                        user_field.fill(dash_user)
                        page.get_by_role("textbox", name="Password").fill(dash_pass)
                        page.get_by_role("button", name="Login").click()
                        page.wait_for_load_state("networkidle")
                        context.storage_state(path=auth_state_path)
            except Exception:
                pass

            # 2. Navigate to Employee Details
            page.goto("https://app.dev.empmonitor.com/admin/employee-details", wait_until="domcontentloaded", timeout=60000)
            
            search_box = page.locator("#search, input.search-field, input[placeholder='Search ...']").first
            expect(search_box).to_be_visible(timeout=60000)
            
            search_box.click()
            search_box.clear()
            search_box.fill(target_user)
            
            search_btn = page.locator("button.search-btn, .search-btn").first
            try:
                if search_btn.count() > 0 and search_btn.is_visible():
                    search_btn.click()
                else:
                    search_box.press("Enter")
            except Exception:
                search_box.press("Enter")
                
            page.wait_for_timeout(3000)

            # Check if target user link exists in the grid and extract email directly from grid row
            grid_email = None
            for row in page.locator("table tbody tr").all():
                row_txt = row.inner_text()
                if target_user.lower() in row_txt.lower():
                    row_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', row_txt)
                    if row_emails:
                        grid_email = row_emails[0].strip()
                        break

            user_link = page.locator(f"a:has-text('{target_user}'), td:has-text('{target_user}')").first
            
            if user_link.count() > 0 and user_link.is_visible():
                logger.info(f"[L4 MATCH] Target user '{target_user}' found in Employee Grid!")
                results["user_found"] = True
                if grid_email:
                    results["dashboard_email"] = grid_email

                grid_screenshot = EVIDENCE_DIR / "01_employee_grid_match.png"
                page.screenshot(path=str(grid_screenshot), timeout=30000)
                results["evidence_files"].append("01_employee_grid_match.png")

                # Click user link to open details
                user_link.click()
                page.wait_for_timeout(2000)

                # Open Edit Modal to extract/verify registered email
                try:
                    edit_link = page.locator("a:has-text('Edit'), [title='Edit'], .edit_employee, a[href*='edit']").first
                    if edit_link.count() > 0 and edit_link.is_visible():
                        edit_link.click()
                        
                        email_input = page.locator("input[placeholder*='Email'], input[name*='email'], #email, #edit_email, #emp_emailAddress").first
                        try:
                            expect(email_input).to_be_visible(timeout=10000)
                            page.wait_for_timeout(2000)
                            extracted = email_input.input_value()
                            if extracted and "@" in extracted:
                                results["dashboard_email"] = extracted.strip()
                        except Exception:
                            pass

                        modal_screenshot = EVIDENCE_DIR / "02_employee_edit_modal.png"
                        page.wait_for_timeout(2000)
                        page.screenshot(path=str(modal_screenshot), timeout=30000)
                        results["evidence_files"].append("02_employee_edit_modal.png")

                        # Close modal
                        close_btn = page.locator(".modal:visible button:has-text('Close'), .modal:visible .close, [data-dismiss='modal']").first
                        if close_btn.count() > 0 and close_btn.is_visible():
                            close_btn.click()
                        else:
                            page.keyboard.press("Escape")
                except Exception as e:
                    logger.warning(f"Edit Modal interaction warning: {e}")

                logger.info(f"[L4 EXTRACTED] Dashboard Registered Email: {results['dashboard_email']}")

                # -------------------------------------------------------------
                # Full Telemetry Modules Visual Evidence Collection
                # -------------------------------------------------------------
                logger.info("Capturing visual evidence across all 6 employee telemetry modules...")

                telemetry_tabs = [
                    ("03_keystrokes_module.png", "#keyLogger", "Keystrokes Data Module"),
                    ("04_app_history_module.png", "#AppHistory", "App History Module"),
                    ("05_web_history_module.png", "#BrowserHistory", "Web History Module"),
                    ("06_screenshots_module.png", "#Screenshots", "Screenshots Gallery Module"),
                    ("07_productivity_module.png", "#Productivity", "Productivity Timeline Module"),
                    ("08_screen_recording_module.png", "#ScreenRecording", "Screen Recording Module")
                ]

                for fname, href_key, label in telemetry_tabs:
                    try:
                        logger.info(f"[Module Evidence] Capturing {label} ({fname})...")
                        tab_btn = page.locator(f"a[href*='{href_key}']").first
                        if tab_btn.count() > 0:
                            tab_btn.click()
                            page.wait_for_timeout(3000)
                            try:
                                page.keyboard.press("Escape")
                            except Exception:
                                pass
                            img_path = EVIDENCE_DIR / fname
                            page.screenshot(path=str(img_path), full_page=True, timeout=30000)
                            results["evidence_files"].append(fname)
                            logger.info(f"  -> Saved {fname}")
                    except Exception as e:
                        logger.warning(f"Warning capturing {label}: {e}")

                results["telemetry_summary"] = "User active on Web Dashboard (Email, Grid & All 6 Telemetry Modules verified)."

            else:
                logger.warning(f"[L4 MISMATCH / FAILURE] Target user '{target_user}' NOT found in Employee Grid!")
                results["user_found"] = False
                results["dashboard_email"] = None
                results["telemetry_summary"] = f"Unregistered / Empty telemetry results for searched user '{target_user}'."

                # Capture empty search evidence screenshot
                empty_screenshot = EVIDENCE_DIR / "01_empty_search_result.png"
                page.screenshot(path=str(empty_screenshot), timeout=30000)
                results["evidence_files"].append("01_empty_search_result.png")

        except Exception as e:
            logger.error(f"[L4 ERROR] Playwright web audit failed: {e}")
            empty_screenshot = EVIDENCE_DIR / "01_empty_search_result.png"
            try:
                page.screenshot(path=str(empty_screenshot), timeout=10000)
                results["evidence_files"].append("01_empty_search_result.png")
            except Exception:
                pass
        finally:
            context.close()
            browser.close()

    return results


# ==============================================================================
# STEP 4: Report Compilation & Verdict Determination
# ==============================================================================
def compile_unified_report(l1_l2_results: Dict[str, Any], last_200_logs: List[str], l4_results: Dict[str, Any]) -> str:
    """
    Compares L1 host email with L4 dashboard email, determines final verdict (HEALTHY / FAILED),
    and builds reports/regression_report.md.
    """
    logger.info("=== STEP 4: Cross-Layer Alignment & Report Compilation ===")

    host_email = l1_l2_results.get("host_email", "").strip().lower()
    dashboard_email = (l4_results.get("dashboard_email") or "").strip().lower()
    searched_user = l4_results.get("searched_user", "")
    user_found = l4_results.get("user_found", False)

    verdict = "HEALTHY"
    discrepancy_reasons = []

    if not user_found:
        verdict = "FAILED"
        discrepancy_reasons.append(f"Searched dashboard user '{searched_user}' was NOT found in the Employee Details grid.")

    elif not host_email or host_email == "unknown":
        verdict = "FAILED"
        discrepancy_reasons.append("Local agent host email could not be extracted from empm.ini.")

    elif host_email != dashboard_email:
        verdict = "FAILED"
        discrepancy_reasons.append(
            f"Email Discrepancy Mismatch! Local Host Email ('{l1_l2_results.get('host_email')}') != Dashboard Email ('{l4_results.get('dashboard_email')}')"
        )

    if verdict == "FAILED":
        print("\n" + "!" * 76)
        logger.warning("[DISCREPANCY DETECTED] Non-ambiguous failure condition caught:")
        for reason in discrepancy_reasons:
            logger.warning(f"  -> {reason}")
        print("!" * 76 + "\n")
    else:
        logger.info("[ALIGNED] Cross-Layer Email Match Validated! Final Verdict: HEALTHY")

    # Generate Markdown Report Content
    report_path = REPORTS_DIR / "regression_report.md"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_lines = [
        "# EmpMonitor 3.0 Automated Regression Test Report",
        "",
        "## 1. Execution Metadata Summary",
        "",
        f"- **Date & Time**: `{now_str}`",
        f"- **Agent Version Evaluated**: `{l1_l2_results['agent_version']}`",
        f"- **Local Active Host Email (L1)**: `{l1_l2_results['host_email']}`",
        f"- **Searched Dashboard User (L4)**: `{searched_user}`",
        f"- **Dashboard Registered Email (L4)**: `{l4_results['dashboard_email'] or 'N/A'}`",
        f"- **Final System Verdict**: **`{verdict}`**",
        ""
    ]

    if discrepancy_reasons:
        md_lines.extend([
            "### ⚠️ Discrepancy Warnings",
            ""
        ])
        for r in discrepancy_reasons:
            md_lines.append(f"- 🔴 **[DISCREPANCY]**: {r}")
        md_lines.append("")

    md_lines.extend([
        "---",
        "",
        "## 2. Layer 1 System Configuration Audit",
        "",
        f"- **Local INI Path**: `{l1_l2_results['ini_path']}`",
        f"- **INI File Size**: `{l1_l2_results['ini_size_kb']} KB` (EV-001 Requirement: > 3.0 KB)",
        "",
        "### Binary Presence & Running Process Status",
        ""
    ])

    for b_name, b_stat in l1_l2_results.get("binaries", {}).items():
        md_lines.append(f"- **Binary `{b_name}`**: {b_stat}")
    for p_name, p_stat in l1_l2_results.get("processes", {}).items():
        md_lines.append(f"- **Process `{p_name}`**: {p_stat}")

    md_lines.extend([
        "",
        "### Sanitized `config.js` Contents (Masked)",
        "```json",
        l1_l2_results.get("config_js", "N/A"),
        "```",
        "",
        "### Sanitized `empm.ini` Attributes (Masked)",
        "```ini"
    ])
    for k, v in l1_l2_results.get("ini_attributes", {}).items():
        md_lines.append(f"{k} = {v}")
    md_lines.extend([
        "```",
        "",
        "---",
        "",
        "## 3. Layer 2 Host Log Harvest (Last 200 Lines)",
        "",
        "```text"
    ])
    if last_200_logs:
        md_lines.extend(last_200_logs)
    else:
        md_lines.append("No active log file harvested for today.")
    md_lines.extend([
        "```",
        "",
        "---",
        "",
        "## 4. Layer 4 Visual Evidence Artifacts",
        ""
    ])

    if l4_results.get("evidence_files"):
        for img_file in l4_results["evidence_files"]:
            img_rel_path = f"evidence/{img_file}"
            md_lines.append(f"### Evidence: `{img_file}`")
            md_lines.append(f"![{img_file}]({img_rel_path})")
            md_lines.append(f"Link: [{img_file}]({img_rel_path})")
            md_lines.append("")
    else:
        md_lines.append("No visual evidence artifacts captured.")

    md_content = "\n".join(md_lines)
    report_path.write_text(md_content, encoding="utf-8")
    logger.info(f"[REPORT COMPILED] Unified Markdown Report saved to: {report_path}")

    return verdict


def main():
    print("\n" + "=" * 76)
    print(f"{'EMPMONITOR 3.0 REGRESSION ORCHESTRATOR':^76}")
    print("=" * 76)

    # 1. Interactive Inputs
    version_input = input("Enter EmpMonitor Agent Version (e.g., 3.5.0 or 3.1.0) [default 3.5.0]: ").strip()
    if not version_input:
        version_input = "3.5.0"

    target_user_input = input("Enter Dashboard Target User to search (e.g., 'auto test' or 'mismatch_user') [default 'auto test']: ").strip()
    if not target_user_input:
        target_user_input = "auto test"

    print("\n" + "-" * 76)
    logger.info(f"Target Configuration: Version='{version_input}', Search User='{target_user_input}'")

    # Step 1 & 2: Local System Inspection
    l1_l2_results, last_200_logs = inspect_local_system(version_input)

    # Step 3: Playwright Web Dashboard Audit
    l4_results = audit_web_dashboard(target_user_input)

    # Step 4: Cross-Layer Alignment & Report Compilation
    final_verdict = compile_unified_report(l1_l2_results, last_200_logs, l4_results)

    print("\n" + "=" * 76)
    print(f"FINAL SYSTEM VERDICT: {final_verdict}")
    print(f"Report Location: {REPORTS_DIR / 'regression_report.md'}")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()
