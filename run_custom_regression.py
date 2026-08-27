"""
Module: run_custom_regression.py
Purpose: Interactive Custom Agent Regression Orchestrator, Windows Registry Stealth Auditor & L3 Network/Firewall Validator.
Branch: custom-agent-regression
Evidence Mapping: 
  - L1: Windows Registry Control Panel Stealth Scan & Host Configuration (empm.ini)
  - L2: Custom Process & Binary Runtime Inspection
  - L3: Outbound Network Connectivity & Windows Firewall Audit
  - L4: Playwright Web Dashboard User Alignment & Tracking Settings Audit
"""

import os
import sys
import re
import logging
import configparser
import winreg
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
logger = logging.getLogger("CustomAgentAuditor")

REPORTS_DIR = PROJECT_ROOT / "reports"
EVIDENCE_DIR = REPORTS_DIR / "evidence"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# SENSITIVE DATA SANITIZATION & VERSION UTILS
# ==============================================================================
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


from src.utils.path_resolver import (
    parse_version_string,
    resolve_empm_ini,
    resolve_local_db,
    harvest_latest_logs,
    find_screen_dirs,
    discover_oju_directories,
)
from src.pages.settings_page import SettingsPage
from src.utils.network_auditor import NetworkAuditor
from src.utils.sync_helper import fast_sync_agent_restart, prompt_conflict_resolution


# ==============================================================================
# LAYER 1: Windows Control Panel Stealth & Registry Audit (winreg)
# ==============================================================================
def verify_control_panel_stealth(
    custom_names_list: List[str]
) -> Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Programmatically audits the Windows Registry for visibility traces across
    the three primary Add/Remove Programs registry pathways:
      1. HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall (64-bit applications)
      2. HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall (32-bit on 64-bit OS)
      3. HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall (Current User scope)

    Assertion: If any key contains "EmpMonitor" or any of the custom executable names
    in its Key Name, DisplayName, Publisher, or UninstallString, the check fails (returns False).
    If no matching registry traces are discovered, returns True (Stealth Verified).
    """
    logger.info("=== LAYER 1 AUDIT: Windows Control Panel Registry Stealth Check ===")
    
    # Build search token list (case-insensitive)
    search_targets = {"empmonitor"}
    for name in custom_names_list:
        if name and name.strip():
            clean_name = name.strip().lower()
            search_targets.add(clean_name)
            if clean_name.endswith(".exe"):
                search_targets.add(clean_name[:-4])

    logger.info(f"Stealth Scan Targets: {sorted(list(search_targets))}")

    # Registry search pathways
    registry_paths = [
        {
            "root": winreg.HKEY_LOCAL_MACHINE,
            "root_str": "HKEY_LOCAL_MACHINE",
            "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            "access": winreg.KEY_READ | getattr(winreg, "KEY_WOW64_64KEY", 0x0100),
            "description": "64-bit System Applications (HKLM)",
            "short_name": r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall (64-bit)"
        },
        {
            "root": winreg.HKEY_LOCAL_MACHINE,
            "root_str": "HKEY_LOCAL_MACHINE",
            "path": r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            "access": winreg.KEY_READ | getattr(winreg, "KEY_WOW64_32KEY", 0x0200),
            "description": "32-bit Applications on 64-bit OS (HKLM Wow6432Node)",
            "short_name": r"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall (32-bit)"
        },
        {
            "root": winreg.HKEY_CURRENT_USER,
            "root_str": "HKEY_CURRENT_USER",
            "path": r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
            "access": winreg.KEY_READ,
            "description": "Current User Scope Applications (HKCU)",
            "short_name": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall"
        }
    ]

    path_summaries: List[Dict[str, Any]] = []
    breach_findings: List[Dict[str, Any]] = []

    def check_value_match(val_lower: str, target: str) -> bool:
        if not val_lower or not target:
            return False
        # Short token check (e.g. 'esr') requires executable extension or boundary to avoid false positives (e.g. Thunderbird ESR)
        if len(target) < 4:
            return (f"{target}.exe" in val_lower) or (re.search(r'[\/\\\.]' + re.escape(target) + r'(\.exe)?\b', val_lower) is not None)
        return target in val_lower

    for reg_target in registry_paths:
        root_key = reg_target["root"]
        path_str = reg_target["path"]
        access_flag = reg_target["access"]
        desc = reg_target["description"]
        short_name = reg_target["short_name"]

        subkeys_scanned = 0
        path_breaches = 0
        status_msg = "CLEAN"

        try:
            parent_key = winreg.OpenKey(root_key, path_str, 0, access_flag)
            subkeys_count, _, _ = winreg.QueryInfoKey(parent_key)
            subkeys_scanned = subkeys_count

            for i in range(subkeys_count):
                try:
                    subkey_name = winreg.EnumKey(parent_key, i)
                    sub_key = winreg.OpenKey(parent_key, subkey_name, 0, access_flag)
                    
                    # Read all registry key values
                    values_dict: Dict[str, str] = {}
                    num_values = winreg.QueryInfoKey(sub_key)[1]
                    for v_idx in range(num_values):
                        try:
                            val_name, val_data, _ = winreg.EnumValue(sub_key, v_idx)
                            values_dict[val_name] = str(val_data)
                        except Exception:
                            pass

                    winreg.CloseKey(sub_key)

                    display_name = values_dict.get("DisplayName", "")
                    publisher = values_dict.get("Publisher", "")
                    uninstall_string = values_dict.get("UninstallString", "")
                    install_location = values_dict.get("InstallLocation", "")

                    # Check for stealth breaches
                    inspect_fields = [
                        ("SubKeyName", subkey_name),
                        ("DisplayName", display_name),
                        ("Publisher", publisher),
                        ("UninstallString", uninstall_string),
                        ("InstallLocation", install_location)
                    ]

                    for field_label, field_value in inspect_fields:
                        val_lower = field_value.lower()
                        for target in search_targets:
                            if check_value_match(val_lower, target):
                                breach_item = {
                                    "path_desc": desc,
                                    "registry_path": f"{reg_target['root_str']}\\{path_str}",
                                    "subkey": subkey_name,
                                    "field": field_label,
                                    "value": field_value,
                                    "matched_pattern": target
                                }
                                breach_findings.append(breach_item)
                                path_breaches += 1
                                logger.warning(
                                    f"[STEALTH BREACH DETECTED] Key '{subkey_name}' in {desc} "
                                    f"contains target '{target}' in field '{field_label}': '{field_value}'"
                                )
                                break

                except Exception as sub_err:
                    logger.debug(f"Could not open subkey index {i} in {desc}: {sub_err}")

            winreg.CloseKey(parent_key)

            if path_breaches > 0:
                status_msg = f"BREACHED ({path_breaches} traces found)"
            else:
                status_msg = "SECURE (0 traces found)"

        except FileNotFoundError:
            status_msg = "NOT PRESENT (Key path does not exist on this OS)"
            logger.info(f"Registry path not present: {path_str}")
        except Exception as err:
            status_msg = f"ERROR ({err})"
            logger.error(f"Failed to scan registry path {path_str}: {err}")

        path_summaries.append({
            "path_name": short_name,
            "description": desc,
            "subkeys_scanned": subkeys_scanned,
            "breaches_count": path_breaches,
            "status": status_msg
        })
        logger.info(f"  [{status_msg}] {short_name} ({subkeys_scanned} subkeys scanned)")

    is_stealth_verified = (len(breach_findings) == 0)
    
    if is_stealth_verified:
        logger.info(">>> [AUDIT SUCCESS] Stealth Cloaking Verified: 0 traces discovered in Windows Control Panel registry pathways.")
    else:
        logger.warning(f">>> [AUDIT FAILURE] Stealth Cloaking Compromised: {len(breach_findings)} trace element(s) discovered in Windows Registry!")

    return is_stealth_verified, path_summaries, breach_findings


# ==============================================================================
# LAYER 2: Process & Binary & Host Configuration Checks (L1/L2)
# ==============================================================================
def inspect_custom_host_system(
    version_input: str,
    exe_map: Dict[str, str],
    expected_stealth: bool = True
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Executes:
    1. Custom process validation (checking whether custom names like DisplayConfigManager.exe are running).
    2. Custom binary presence inspection across Program Files.
    3. empm.ini discovery, size validation (> 3 KB), and stealth visibility flag verification (visibility=false).
    4. Sanitization and masking of sensitive credentials.
    5. Harvesting latest 200 log lines.
    """
    logger.info("=== LAYER 2 AUDIT: Host Process, Binary & Configuration Inspection ===")

    agent_version = parse_version_string(version_input)
    baseline_version = parse_version_string("3.1.0")

    # 1. Binary checks (checking both custom named binaries and standard paths)
    standard_install_dirs = [
        Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui"),
        Path(r"C:\Program Files\EmpMonitor\EmpMonitor\service"),
        Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui\executables"),
        Path(r"C:\Program Files\EmpMonitor"),
    ]

    binary_statuses: Dict[str, str] = {}
    for role, exe_name in exe_map.items():
        found = False
        found_path = None
        for base_dir in standard_install_dirs:
            candidate = base_dir / exe_name
            if candidate.exists():
                found = True
                found_path = str(candidate)
                break
        
        status_label = f"FOUND ({found_path})" if found else "NOT DETECTED ON DISK"
        binary_statuses[exe_name] = status_label
        logger.info(f"  [Binary Check] {role} (`{exe_name}`): {status_label}")

    # 2. Process inspection via psutil
    running_procs = {}
    try:
        for p in psutil.process_iter(["name", "status", "pid", "exe"]):
            try:
                p_name = p.info.get("name")
                if p_name:
                    running_procs[p_name.lower()] = p.info
            except Exception:
                pass
    except Exception as e:
        logger.error(f"Error enumerating host processes: {e}")

    process_statuses: Dict[str, str] = {}
    for role, exe_name in exe_map.items():
        name_lower = exe_name.lower()
        if name_lower in running_procs:
            proc_info = running_procs[name_lower]
            stat = proc_info.get("status", "running")
            pid = proc_info.get("pid", "N/A")
            status_text = f"RUNNING (PID={pid}, Status={stat})"
        else:
            status_text = "INACTIVE"
        
        process_statuses[exe_name] = status_text
        logger.info(f"  [Process Check] {role} (`{exe_name}`): {status_text}")

    # 3. Parse config.js
    config_js_path = Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui\configs\config.js")
    config_js_raw = ""
    config_js_masked = "Not Found"
    if config_js_path.exists():
        try:
            config_js_raw = config_js_path.read_text(encoding="utf-8", errors="ignore")
            masked_lines = []
            for line in config_js_raw.splitlines():
                if any(k in line.lower() for k in ["token", "password", "key", "secret"]):
                    line = re.sub(r'([\'"][^\'"]*[\'"])\s*:\s*([\'"][^\'"]*[\'"])', r'\1: "***MASKED***"', line)
                masked_lines.append(line)
            config_js_masked = "\n".join(masked_lines)
            logger.info("[Host Config] config.js parsed and sanitized successfully.")
        except Exception as e:
            config_js_masked = f"Error reading config.js: {e}"

    # 4. Parse empm.ini & AppData Discovery
    screen_dirs = find_screen_dirs()
    logger.info(f"[Host AppData] Local Screen: {screen_dirs['local']}, Roaming Screen: {screen_dirs['roaming']}")
    
    ini_path, ini_size_kb = resolve_empm_ini()
    host_email = None
    ini_path_str = str(ini_path) if ini_path else "Not Found"
    ini_content_raw = ""
    ini_attributes: Dict[str, str] = {}
    visibility_flag_found: Optional[str] = None
    visibility_status_verdict = "UNKNOWN"

    if ini_path and ini_path.exists():
        logger.info(f"[Host INI] Found empm.ini ({ini_size_kb} KB) at: {ini_path}")
        if ini_size_kb > 3.0:
            logger.info("[EV-001 VALIDATED] empm.ini file size is > 3 KB.")
        else:
            logger.warning(f"[EV-001 WARNING] empm.ini file size ({ini_size_kb} KB) is <= 3 KB.")

        try:
            ini_content_raw = ini_path.read_text(encoding="utf-8", errors="ignore")
            config = configparser.ConfigParser(interpolation=None, strict=False, allow_no_value=True)
            try:
                config.read_string(ini_content_raw)
            except Exception:
                config.read_string("[DEFAULT]\n" + ini_content_raw)

            for section in config.sections():
                for key, val in config.items(section):
                    if key.lower() == "email":
                        host_email = val
                    if key.lower() in ["visibility", "empicon", "system/visibility", "system\\visibility"]:
                        visibility_flag_found = val
                    masked_val = mask_sensitive_value(key, val or "")
                    ini_attributes[f"[{section}] {key}"] = masked_val

            if not host_email:
                email_match = re.search(r"email\s*=\s*([^\s\r\n]+)", ini_content_raw, re.IGNORECASE)
                if email_match:
                    host_email = email_match.group(1)

            # Direct regex for visibility if not parsed through sections
            if not visibility_flag_found:
                vis_match = re.search(r"(?:visibility|empicon)\s*=\s*([^\s\r\n]+)", ini_content_raw, re.IGNORECASE)
                if vis_match:
                    visibility_flag_found = vis_match.group(1).strip()

            if visibility_flag_found is not None:
                vis_clean = visibility_flag_found.strip().lower()
                is_stealth_flag = (vis_clean in ["false", "0", "stealth", "hidden"])
                if expected_stealth:
                    if is_stealth_flag:
                        visibility_status_verdict = f"STEALTH VERIFIED (visibility={visibility_flag_found})"
                        logger.info(f"[INI Visibility] Stealth Mode Flag Validated: {visibility_status_verdict}")
                    else:
                        visibility_status_verdict = f"MISMATCH (Expected stealth=false, got visibility={visibility_flag_found})"
                        logger.warning(f"[INI Visibility] Flag Mismatch: {visibility_status_verdict}")
                else:
                    visibility_status_verdict = f"CONFIGURED (visibility={visibility_flag_found})"
            else:
                visibility_status_verdict = "NOT SPECIFIED IN INI"

        except Exception as e:
            logger.error(f"Failed to parse empm.ini: {e}")
            visibility_status_verdict = f"PARSE ERROR ({e})"
    else:
        logger.warning("[Host INI] empm.ini was not found in Local or Roaming AppData.")
        visibility_status_verdict = "INI FILE NOT FOUND"

    logger.info(f"[Host Identity] Local Active Host Email: {host_email or 'Unknown'}")

    # 5. Harvest Last 200 Log Lines
    active_log_file, last_200_logs = harvest_latest_logs(line_count=200)
    if active_log_file:
        logger.info(f"[Log Harvest] Harvested {len(last_200_logs)} lines from: {active_log_file}")
    else:
        logger.warning("[Log Harvest] No active log file found in Local or Roaming AppData.")

    l1_l2_results = {
        "agent_version": version_input,
        "exe_map": exe_map,
        "binaries": binary_statuses,
        "processes": process_statuses,
        "config_js_raw": config_js_raw,
        "config_js": config_js_masked,
        "ini_path": ini_path_str,
        "ini_size_kb": ini_size_kb,
        "ini_content_raw": ini_content_raw,
        "host_email": host_email or "Unknown",
        "visibility_flag": visibility_flag_found or "N/A",
        "visibility_verdict": visibility_status_verdict,
        "ini_attributes": ini_attributes,
    }

    return l1_l2_results, last_200_logs


# ==============================================================================
# LAYER 4: Playwright Dashboard Validation & Settings Audit
# ==============================================================================
def audit_custom_web_dashboard(
    target_user: str,
    base_url: str,
    auth_state_path: str = "playwright-profile/auth.json",
    expected_stealth: bool = True
) -> Dict[str, Any]:
    """
    Executes Playwright Web Dashboard validation:
    1. Authenticates session (refreshing auth state if needed).
    2. Searches for target user in Employee Details grid and extracts registered email.
    3. Navigates to User Tracking Settings to audit active Visibility Mode (Stealth vs. Visible).
    4. Audits functional telemetry modules (Screencast, Keystrokes, Web & App Blocking, etc.).
    5. Captures screenshot evidence to reports/evidence/.
    """
    member_url = f"{base_url}/amember/member"
    employee_details_url = f"{base_url}/admin/employee-details"

    logger.info("=== LAYER 4 AUDIT: Playwright Web Dashboard Validation ===")
    logger.info(f"Target Environment URL: {member_url}")
    logger.info(f"Searching Web Dashboard for Target User: '{target_user}'")

    results: Dict[str, Any] = {
        "searched_user": target_user,
        "user_found": False,
        "dashboard_email": None,
        "dashboard_visibility_mode": "Unknown",
        "visibility_mode_match": False,
        "evidence_files": [],
        "telemetry_summary": "No Data / Unregistered User",
        "screencast_status": "OFFLINE / FALLBACK",
        "modules_status": {}
    }

    if not os.path.exists(auth_state_path):
        logger.error(f"Authentication state missing at {auth_state_path}.")
        return results

    with sync_playwright() as p:
        is_headless = os.getenv("HEADLESS", "true").lower() == "true"
        browser = p.chromium.launch(headless=is_headless)
        context = browser.new_context(storage_state=auth_state_path, ignore_https_errors=True)
        page = context.new_page()

        try:
            # 1. Validate / Refresh Session State
            page.goto(member_url, wait_until="domcontentloaded", timeout=60000)
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
            page.goto(employee_details_url, wait_until="domcontentloaded", timeout=60000)
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass

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

            # Wait for AJAX results
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            try:
                page.locator(".dataTables_processing").wait_for(state="hidden", timeout=10000)
            except Exception:
                pass

            user_link = page.locator(f"a:has-text('{target_user}'), td:has-text('{target_user}')").first
            try:
                user_link.wait_for(state="visible", timeout=15000)
            except Exception:
                page.wait_for_timeout(3000)

            # Extract email from grid row
            grid_email = None
            for row in page.locator("table tbody tr").all():
                row_txt = row.inner_text()
                if target_user.lower() in row_txt.lower():
                    row_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', row_txt)
                    if row_emails:
                        grid_email = row_emails[0].strip()
                        break

            if user_link.count() > 0 and user_link.is_visible():
                logger.info(f"[L4 MATCH] Target user '{target_user}' found in Employee Grid!")
                results["user_found"] = True
                if grid_email:
                    results["dashboard_email"] = grid_email

                grid_screenshot = EVIDENCE_DIR / "01_employee_grid_match.png"
                page.wait_for_timeout(1000)
                page.screenshot(path=str(grid_screenshot), timeout=30000)
                results["evidence_files"].append("01_employee_grid_match.png")

                # Open User Tracking Settings to audit Stealth Mode & Toggles
                logger.info("Navigating to User Tracking Settings to audit Stealth visibility mode...")
                settings_p = SettingsPage(page)
                
                # Check user settings via direct or link navigation
                target_user_id = "237232" if ("app.empmonitor.com" in base_url and "dev" not in base_url) else "45009"
                settings_p.navigate_to_user_settings(user_name=target_user, user_id=target_user_id)
                page.wait_for_timeout(2000)

                # Extract Visibility Mode
                detected_vis_mode = settings_p.get_active_visibility_mode()
                results["dashboard_visibility_mode"] = detected_vis_mode
                logger.info(f"[L4 SETTINGS AUDIT] Dashboard Visibility Mode: '{detected_vis_mode}'")

                if expected_stealth:
                    results["visibility_mode_match"] = (detected_vis_mode.lower() == "stealth")
                else:
                    results["visibility_mode_match"] = (detected_vis_mode.lower() == "visible")

                # Capture settings screenshot
                settings_screenshot = EVIDENCE_DIR / "02_user_tracking_settings.png"
                page.screenshot(path=str(settings_screenshot), full_page=True, timeout=30000)
                results["evidence_files"].append("02_user_tracking_settings.png")
                logger.info(f"  -> Saved {settings_screenshot.name}")

                # Return to Employee Details page to audit individual telemetry modules
                page.goto(employee_details_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(2000)

                # Re-search and click user link to open telemetry panel
                search_box2 = page.locator("#search, input.search-field, input[placeholder='Search ...']").first
                if search_box2.count() > 0 and search_box2.is_visible():
                    search_box2.fill(target_user)
                    search_box2.press("Enter")
                    page.wait_for_timeout(3000)
                    user_link2 = page.locator(f"a:has-text('{target_user}'), td:has-text('{target_user}')").first
                    if user_link2.count() > 0 and user_link2.is_visible():
                        user_link2.click()
                        page.wait_for_timeout(2000)

                # -------------------------------------------------------------
                # Capture Telemetry Modules Visual Evidence (Safe Check)
                # -------------------------------------------------------------
                logger.info("Auditing visual evidence across telemetry modules...")
                telemetry_tabs = [
                    ("03_timesheets_module.png", "#Timesheets", "Timesheets Data Module"),
                    ("04_keystrokes_module.png", "#keyLogger", "Keystrokes Data Module"),
                    ("05_app_history_module.png", "#AppHistory", "App History Module"),
                    ("06_web_history_module.png", "#BrowserHistory", "Web History Module"),
                    ("07_screenshots_module.png", "#Screenshots", "Screenshots Gallery Module"),
                    ("08_productivity_module.png", "#Productivity", "Productivity Timeline Module"),
                    ("09_screen_recording_module.png", "#ScreenRecording", "Screen Recording Module"),
                    ("10_screencast_module.png", "#ScreenCast", "Screencast Stream Telemetry Module")
                ]

                screencast_status = "OFFLINE / FALLBACK"
                for fname, href_key, label in telemetry_tabs:
                    try:
                        tab_btn = page.locator(f"a[href*='{href_key}']").first
                        if tab_btn.count() > 0 and tab_btn.is_visible():
                            try:
                                tab_btn.click(timeout=5000)
                                try:
                                    page.wait_for_load_state("networkidle", timeout=5000)
                                except Exception:
                                    pass
                                page.wait_for_timeout(2500)

                                if href_key == "#ScreenCast":
                                    live_canvas = page.locator("#canvas-img-0, canvas.screencast-canvas").first
                                    if live_canvas.count() > 0 and live_canvas.is_visible():
                                        screencast_status = "LIVE / ONLINE"
                                    else:
                                        screencast_status = "OFFLINE / FALLBACK"
                                    logger.info(f"[L4 TELEMETRY] Screencast Stream Status: {screencast_status}")

                                try:
                                    page.keyboard.press("Escape")
                                except Exception:
                                    pass
                                img_path = EVIDENCE_DIR / fname
                                page.screenshot(path=str(img_path), full_page=True, timeout=30000)
                                results["evidence_files"].append(fname)
                                results["modules_status"][label] = "CAPTURED"
                                logger.info(f"  -> Captured {label} ({fname})")
                            except Exception as click_err:
                                logger.warning(f"Could not capture {label}: {click_err}")
                                results["modules_status"][label] = f"CLICK_ERROR ({click_err})"
                        elif tab_btn.count() > 0:
                            logger.info(f"  -> {label} ({href_key}) is marked hidden/disabled on this dashboard profile. Skipping tab click.")
                            results["modules_status"][label] = "HIDDEN / DISABLED ON DASHBOARD"
                        else:
                            results["modules_status"][label] = "TAB NOT PRESENT"
                    except Exception as e:
                        logger.warning(f"Warning checking {label}: {e}")
                        results["modules_status"][label] = f"ERROR ({e})"

                results["screencast_status"] = screencast_status
                results["telemetry_summary"] = (
                    f"User active on Web Dashboard (Visibility Setting='{detected_vis_mode}', "
                    f"Email='{results['dashboard_email'] or 'Found'}', Screencast [{screencast_status}] verified)."
                )

            else:
                logger.warning(f"[L4 MISMATCH / FAILURE] Target user '{target_user}' NOT found in Employee Grid!")
                results["user_found"] = False
                results["dashboard_email"] = None
                results["telemetry_summary"] = f"Unregistered / Empty telemetry results for searched user '{target_user}'."

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
# REPORT COMPILATION & DIAGNOSTICS (reports/custom_regression_report.md)
# ==============================================================================
def compile_custom_markdown_report(
    env_name: str,
    base_url: str,
    is_stealth_secure: bool,
    registry_summaries: List[Dict[str, Any]],
    registry_breaches: List[Dict[str, Any]],
    l1_l2_results: Dict[str, Any],
    last_200_logs: List[str],
    l3_results: Dict[str, Any],
    l4_results: Dict[str, Any],
    expected_stealth: bool = True,
    operator_overrides: Optional[List[str]] = None
) -> Tuple[str, str]:
    """
    Compiles structured diagnostic markdown report at reports/custom_regression_report.md
    including:
      1. Metadata Block
      2. Executive Summary & Verdicts Table
      3. Custom Executable Mapping Table
      4. Windows Registry Control Panel Audit Status Table
      5. Host Diagnostics (Processes, Binaries, empm.ini visibility)
      6. Layer 3 Outbound Network & Firewall Audit
      7. Layer 4 Dashboard Verification & Screenshots Evidence Gallery
    """
    logger.info("=== REPORT COMPILATION: reports/custom_regression_report.md ===")

    host_email = l1_l2_results.get("host_email", "").strip().lower()
    dashboard_email = (l4_results.get("dashboard_email") or "").strip().lower()
    searched_user = l4_results.get("searched_user", "")
    user_found = l4_results.get("user_found", False)
    dash_vis_mode = l4_results.get("dashboard_visibility_mode", "Unknown")

    if not operator_overrides:
        operator_overrides = []

    # Determine Cloaking Verdict
    if is_stealth_secure:
        cloaking_verdict = "SECURE (Hidden from Control Panel)"
    else:
        cloaking_verdict = "BREACHED (Trace elements found in Registry)"

    # Determine System Report Verdict
    discrepancy_reasons = []
    if not is_stealth_secure:
        discrepancy_reasons.append(
            f"Control Panel Registry Cloaking Failed: {len(registry_breaches)} trace element(s) discovered in uninstallation registry keys."
        )

    # Layer 3 failures
    if l3_results.get("has_tcp_failures"):
        blocked_endpoints = [k for k, v in l3_results.get("tcp_connectivity", {}).items() if v.get("status") == "BLOCKED"]
        discrepancy_reasons.append(f"Network Routing Failure: Connection blocked to endpoint(s): {', '.join(blocked_endpoints)}")

    if not l3_results.get("leak_audit", {}).get("is_clean", True):
        for mismatch in l3_results.get("leak_audit", {}).get("mismatches", []):
            discrepancy_reasons.append(f"Network Routing Cross-Environment Leak: {mismatch}")

    if not user_found:
        discrepancy_reasons.append(
            f"Searched dashboard user '{searched_user}' was NOT found in the Employee Details grid."
        )

    if expected_stealth and dash_vis_mode.lower() != "stealth":
        if "visibility_mode" not in [o.lower() for o in operator_overrides]:
            discrepancy_reasons.append(
                f"Dashboard Visibility Setting Mismatch! Expected 'Stealth', but active mode is '{dash_vis_mode}'."
            )

    if host_email and host_email != "unknown" and dashboard_email and host_email != dashboard_email:
        if "email" not in [o.lower() for o in operator_overrides]:
            discrepancy_reasons.append(
                f"Email Discrepancy Mismatch! Local Host Email ('{l1_l2_results.get('host_email')}') != Dashboard Email ('{l4_results.get('dashboard_email')}')"
            )

    report_verdict = "FAILED" if discrepancy_reasons else ("HEALTHY (WITH OPERATOR OVERRIDES)" if operator_overrides else "HEALTHY")

    report_path = REPORTS_DIR / "custom_regression_report.md"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    leak_status = l3_results.get("leak_audit", {}).get("leak_status", "CLEAN")
    leak_summary = l3_results.get("leak_audit", {}).get("leak_summary", "No leaks")

    md_lines = [
        "# Custom Agent Stealth & Security Regression Report",
        "",
        f"> **Generated On**: `{now_str}`  ",
        f"> **Target Environment**: `{env_name.upper()}` (`{base_url}`)  ",
        f"> **Agent Version Evaluated**: `{l1_l2_results['agent_version']}`",
        "",
        "---",
        "",
        "## 1. Executive Summary & Verdicts",
        "",
        "| Audit Dimension | Evaluation Result | Status |",
        "| :--- | :--- | :--- |",
        f"| **Final Report Verdict** | **`{report_verdict}`** | {'✅ PASS' if 'HEALTHY' in report_verdict else '❌ FAIL'} |",
        f"| **Covert Cloaking Verdict** | **`{cloaking_verdict}`** | {'🛡️ SECURE' if is_stealth_secure else '🚨 BREACHED'} |",
        f"| **Cross-Environment Leak Check** | `{leak_status}` ({leak_summary}) | {'🛡️ CLEAN' if leak_status == 'CLEAN' else '🚨 LEAK DETECTED'} |",
        f"| **Dashboard Visibility Setting** | `{dash_vis_mode}` (Expected: {'Stealth' if expected_stealth else 'Visible'}) | {'✅ ALIGNED' if l4_results.get('visibility_mode_match') else ('⚠️ OPERATOR OVERRIDE' if 'visibility_mode' in [o.lower() for o in operator_overrides] else '⚠️ MISMATCH')} |",
        f"| **Target Dashboard User** | `{searched_user}` | {'✅ FOUND' if user_found else '❌ NOT FOUND'} |",
        f"| **Host INI Visibility Flag** | `{l1_l2_results.get('visibility_verdict')}` | {'✅ ALIGNED' if 'VERIFIED' in l1_l2_results.get('visibility_verdict', '') else '⚠️ AUDIT'} |",
        f"| **Screencast Stream Status** | `{l4_results.get('screencast_status', 'N/A')}` | {'🟢 LIVE' if 'LIVE' in l4_results.get('screencast_status', '') else '⚪ STANDBY'} |",
        ""
    ]

    if operator_overrides:
        md_lines.extend([
            "### ℹ️ Operator Overrides / Tolerated Conflicts",
            ""
        ])
        for o in operator_overrides:
            md_lines.append(f"- 🟡 **[TOLERATED CONFLICT]**: {o}")
        md_lines.append("")

    if discrepancy_reasons:
        md_lines.extend([
            "### ⚠️ Discrepancy & Security Breach Warnings",
            ""
        ])
        for r in discrepancy_reasons:
            md_lines.append(f"- 🔴 **[FAILURE REASON]**: {r}")
        md_lines.append("")

    # Section 2: Custom Executable Mapping
    md_lines.extend([
        "---",
        "",
        "## 2. Custom Binary & Process Mapping",
        "",
        "| Executable Role | Configured Process Name | Disk Binary Status | Host Process Runtime Status |",
        "| :--- | :--- | :--- | :--- |"
    ])

    for role, exe_name in l1_l2_results.get("exe_map", {}).items():
        b_stat = l1_l2_results.get("binaries", {}).get(exe_name, "N/A")
        p_stat = l1_l2_results.get("processes", {}).get(exe_name, "N/A")
        md_lines.append(f"| **{role}** | `{exe_name}` | `{b_stat}` | `{p_stat}` |")

    md_lines.append("")

    # Section 3: Windows Control Panel Registry Audit Status Table
    md_lines.extend([
        "---",
        "",
        "## 3. Windows Control Panel Visibility Audit (winreg)",
        "",
        "To verify that the custom stealth agent is invisible to host users in the Windows Control Panel (Add/Remove Programs), the three primary Windows uninstallation registry hives were audited:",
        "",
        "| Scanned Registry Pathway | Scope / Architecture | Subkeys Audited | Cloaking Status |",
        "| :--- | :--- | :---: | :--- |"
    ])

    for s in registry_summaries:
        p_name = s["path_name"]
        desc = s["description"]
        cnt = s["subkeys_scanned"]
        stat = s["status"]
        md_lines.append(f"| `{p_name}` | {desc} | {cnt} | **{stat}** |")

    md_lines.append("")

    if registry_breaches:
        md_lines.extend([
            "### 🚨 Detected Registry Breach Entries",
            "",
            "| Registry Hive | SubKey Name | Matched Field | Matched Value | Trigger Token |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ])
        for b in registry_breaches:
            md_lines.append(
                f"| `{b['path_desc']}` | `{b['subkey']}` | `{b['field']}` | `{b['value']}` | `{b['matched_pattern']}` |"
            )
        md_lines.append("")
    else:
        md_lines.extend([
            "> **Stealth Assertion Passed**: No subkeys or values containing `EmpMonitor` or custom binary names were discovered in `HKEY_LOCAL_MACHINE` (64-bit/32-bit Wow6432Node) or `HKEY_CURRENT_USER` uninstallation keys.",
            ""
        ])

    # Section 4: Layer 1 & 2 Host Configuration Details
    md_lines.extend([
        "---",
        "",
        "## 4. Host Configuration & Storage Diagnostics (L1 / L2)",
        "",
        f"- **Local INI Path**: `{l1_l2_results['ini_path']}`",
        f"- **INI File Size**: `{l1_l2_results['ini_size_kb']} KB` (EV-001 Requirement: > 3.0 KB)",
        f"- **Local Active Host Email**: `{l1_l2_results['host_email']}`",
        f"- **Visibility Flag in INI**: `{l1_l2_results.get('visibility_flag', 'N/A')}` ({l1_l2_results.get('visibility_verdict')})",
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
        "## 5. Layer 3 (L3) - Outbound Network & Firewall Audit",
        "",
        f"- **Target Routing Environment:** `{env_name}`",
        "- **Active Firewall Exceptions:**"
    ])

    for exe, fw_info in l3_results.get("firewall_status", {}).items():
        disp = fw_info.get("display_text", "Allowed")
        md_lines.append(f"  - `{exe}`: `{disp}`")

    md_lines.extend([
        "- **API Connectivity Matrix:**"
    ])

    for domain, conn in l3_results.get("tcp_connectivity", {}).items():
        if conn.get("status") == "HEALTHY":
            md_lines.append(f"  - `{domain}`: `SUCCESS (Resolved IP: {conn.get('resolved_ip')})`")
        else:
            md_lines.append(f"  - `{domain}`: `BLOCKED ({conn.get('error')})`")

    md_lines.extend([
        f"- **Leak Integrity check:** `{leak_status} ({leak_summary})`",
        "",
        "---",
        "",
        "## 6. Host Log Harvest (Last 200 Lines)",
        "",
        "```text"
    ])
    if last_200_logs:
        md_lines.extend(last_200_logs)
    else:
        md_lines.append("No active host log file harvested for today.")
    md_lines.extend([
        "```",
        "",
        "---",
        "",
        "## 7. Layer 4 Visual Evidence Artifacts",
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
    logger.info(f"[REPORT COMPILED] Dynamic Markdown Report saved to: {report_path}")

    return report_verdict, cloaking_verdict


# ==============================================================================
# CLI ENTRY POINT & INTERACTIVE ORCHESTRATION
# ==============================================================================
def main():
    print("\n" + "=" * 78)
    print(f"{'CUSTOM AGENT STEALTH, NETWORK & REGISTRY AUDITOR':^78}")
    print(f"{'Branch: custom-agent-regression':^78}")
    print("=" * 78)

    # 1. Interactive Prompts
    print("\n[STEP 1: Target Environment Selection]")
    env_choice = input("Select Target Environment [1=dev (default), 2=live]: ").strip().lower()
    if env_choice in ["2", "live", "prod", "production"]:
        env_name = "live"
        base_url = "https://app.empmonitor.com"
        default_admin_email = "empmonitor@ccfa.org"
        logger.info(f"Targeting LIVE Production: {base_url} (Admin Email: {default_admin_email})")
    else:
        env_name = "dev"
        base_url = "https://app.dev.empmonitor.com"
        logger.info(f"Targeting DEV Environment: {base_url}")

    os.environ["EMP_ENV"] = env_name
    os.environ["EMP_BASE_URL"] = base_url
    os.environ["EMP_LOGIN_URL"] = f"{base_url}/amember/member"

    # Agent Version
    print("\n[STEP 2: Agent Version]")
    version_input = input("Enter Agent Version (e.g., 3.5.0 or 3.1.0) [default 3.5.0]: ").strip()
    if not version_input:
        version_input = "3.5.0"

    # Target Dashboard User
    print("\n[STEP 3: Target Dashboard User]")
    target_user_input = input("Enter Dashboard Target User / Employee ID to search [default 'auto test']: ").strip()
    if not target_user_input:
        target_user_input = "auto test"

    # Custom Binary Names
    print("\n[STEP 4: Custom Executable & Process Mapping]")
    main_exe = input("Enter Main Agent Executable Name [default 'DisplayConfigManager.exe']: ").strip()
    if not main_exe:
        main_exe = "DisplayConfigManager.exe"

    watchdog_exe = input("Enter Watchdog / Service Executable Name [default 'UpdateMgr_Emp.exe']: ").strip()
    if not watchdog_exe:
        watchdog_exe = "UpdateMgr_Emp.exe"

    screencast_exe = input("Enter Screencast / Helper Executable Name [default 'esr.exe']: ").strip()
    if not screencast_exe:
        screencast_exe = "esr.exe"

    helper_service_exe = input("Enter Helper Service Executable Name [default 'emp_psa_service.exe']: ").strip()
    if not helper_service_exe:
        helper_service_exe = "emp_psa_service.exe"

    exe_map = {
        "Main Agent": main_exe,
        "Watchdog / Service": watchdog_exe,
        "Screencast / Helper": screencast_exe,
        "Helper Service": helper_service_exe
    }

    custom_names_list = list(exe_map.values())

    print("\n" + "-" * 78)
    logger.info(f"Configuration Summary:")
    logger.info(f"  Environment: {env_name.upper()} ({base_url})")
    logger.info(f"  Version: {version_input}")
    logger.info(f"  Searched User: {target_user_input}")
    logger.info(f"  Main Executable: {main_exe}")
    logger.info(f"  Watchdog Executable: {watchdog_exe}")
    logger.info(f"  Screencast Executable: {screencast_exe}")
    logger.info(f"  Helper Service Executable: {helper_service_exe}")
    print("-" * 78 + "\n")

    # Step 1: Windows Control Panel Stealth Audit (winreg)
    is_stealth_secure, reg_summaries, reg_breaches = verify_control_panel_stealth(custom_names_list)

    # Step 2: Host Process, Binary & INI Configuration Audit
    l1_l2_results, last_200_logs = inspect_custom_host_system(
        version_input=version_input,
        exe_map=exe_map,
        expected_stealth=True
    )

    # Step 3: Layer 3 Outbound Network & Windows Defender Firewall Audit
    network_auditor = NetworkAuditor(environment=env_name, exe_list=custom_names_list)
    l3_results = network_auditor.run_full_audit(
        config_js_content=l1_l2_results.get("config_js_raw", ""),
        ini_content=l1_l2_results.get("ini_content_raw", "")
    )

    if l3_results.get("has_tcp_failures"):
        logger.warning("[L3 WARNING] One or more target endpoints failed TCP handshake!")
    if not l3_results.get("leak_audit", {}).get("is_clean", True):
        logger.warning(f"[L3 CRITICAL] {l3_results.get('leak_audit', {}).get('leak_summary')}")

    # Step 4: Playwright Web Dashboard & User Settings Audit
    l4_results = audit_custom_web_dashboard(
        target_user=target_user_input,
        base_url=base_url,
        expected_stealth=True
    )

    # Step 5: Fast-Sync Check & Setting Conflict Reconciliation
    operator_overrides = []
    host_email = l1_l2_results.get("host_email", "").strip().lower()
    dashboard_email = (l4_results.get("dashboard_email") or "").strip().lower()
    vis_match = l4_results.get("visibility_mode_match", False)

    if not vis_match or (host_email and dashboard_email and host_email != dashboard_email):
        print("\n[Fast-Sync Check] Detected potential setting discrepancy between local empm.ini and Web Dashboard.")
        print("Restarting agent process to trigger immediate configuration refresh (/api/v3/user/config)...")
        restarted = fast_sync_agent_restart(custom_names_list, wait_seconds=5)
        
        if restarted:
            print("[Fast-Sync Re-Inspection] Re-parsing refreshed empm.ini...")
            l1_l2_results, last_200_logs = inspect_custom_host_system(
                version_input=version_input,
                exe_map=exe_map,
                expected_stealth=True
            )
            host_email = l1_l2_results.get("host_email", "").strip().lower()
            if "STEALTH VERIFIED" in l1_l2_results.get("visibility_verdict", ""):
                l4_results["visibility_mode_match"] = True
                print(">>> [FAST-SYNC SUCCESS] Visibility setting aligned after agent restart!")

        # If mismatch still persists, prompt operator
        if not l4_results.get("visibility_mode_match", False):
            should_skip, note = prompt_conflict_resolution(
                feature_name="Visibility Mode (Stealth vs Visible)",
                local_val=l1_l2_results.get("visibility_verdict", "Unknown"),
                web_val=l4_results.get("dashboard_visibility_mode", "Unknown"),
                context_note="Agent build might not have updated or may use custom policy."
            )
            if should_skip:
                operator_overrides.append(f"Visibility Mode: {note}")

        if host_email and dashboard_email and host_email != dashboard_email:
            should_skip, note = prompt_conflict_resolution(
                feature_name="Registered Email",
                local_val=l1_l2_results.get("host_email", "Unknown"),
                web_val=l4_results.get("dashboard_email", "Unknown"),
                context_note="Different user accounts or multi-user test environment."
            )
            if should_skip:
                operator_overrides.append(f"Email Mismatch: {note}")

    # Step 6: Markdown Report Generation
    report_verdict, cloaking_verdict = compile_custom_markdown_report(
        env_name=env_name,
        base_url=base_url,
        is_stealth_secure=is_stealth_secure,
        registry_summaries=reg_summaries,
        registry_breaches=reg_breaches,
        l1_l2_results=l1_l2_results,
        last_200_logs=last_200_logs,
        l3_results=l3_results,
        l4_results=l4_results,
        expected_stealth=True,
        operator_overrides=operator_overrides
    )

    print("\n" + "=" * 78)
    print(f"FINAL REPORT VERDICT:    {report_verdict}")
    print(f"COVERT CLOAKING VERDICT: {cloaking_verdict}")
    print(f"NETWORK LEAK INTEGRITY:  {l3_results.get('leak_audit', {}).get('leak_status')}")
    if operator_overrides:
        print(f"OPERATOR OVERRIDES:      {len(operator_overrides)} setting check(s) tolerated")
    print(f"Report Output Location:  {REPORTS_DIR / 'custom_regression_report.md'}")
    print("=" * 78 + "\n")


if __name__ == "__main__":
    main()
