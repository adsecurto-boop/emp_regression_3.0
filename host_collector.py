"""
Module: host_collector.py
Purpose: Host-Side Telemetry Collector & Environment Validator for EmpMonitor Agent.
Evidence Mapping: L1 (Configuration), L2 (Host Storage & Runtime), L4 (Cross-Layer Alignment)
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
from playwright.sync_api import sync_playwright

# Ensure project root is in python path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_dashboard_user_find import fetch_employee_credentials

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("HostCollector")

# Target installation binary definitions for > v3.1.0
MODERN_BINARIES = [
    r"C:\Program Files\EmpMonitor\EmpMonitor\gui\empmonitor.exe",
    r"C:\Program Files\EmpMonitor\EmpMonitor\gui\UpdateMgr_Emp.exe",
    r"C:\Program Files\EmpMonitor\EmpMonitor\gui\executables\esr.exe",
    r"C:\Program Files\EmpMonitor\EmpMonitor\service\emp_psa_service.exe",
]


def mask_sensitive_value(key: str, value: str) -> str:
    """Mask sensitive config values (tokens, passwords, keys) with asterisks."""
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
# PHASE 1: Versioning, Binary Presence & Running Process Checks
# ==============================================================================
def phase_1_binary_and_version_checks() -> None:
    logger.info("=== PHASE 1: Interactive Versioning & Binary Checks ===")
    
    version_input = input("Enter EmpMonitor Agent Version (e.g., 3.2.0 or 3.1.0): ").strip()
    if not version_input:
        version_input = "3.2.0"
        logger.info(f"No version entered. Defaulting to: {version_input}")

    agent_version = parse_version_string(version_input)
    baseline_version = parse_version_string("3.1.0")

    if agent_version > baseline_version:
        logger.info(f"Modern version detected ({version_input} > 3.1.0). Validating binary paths...")
        missing_binaries = []
        for binary_path in MODERN_BINARIES:
            path_obj = Path(binary_path)
            if path_obj.exists():
                logger.info(f"[FOUND] Binary present: {binary_path}")
            else:
                logger.warning(f"[MISSING] Binary not found: {binary_path}")
                missing_binaries.append(binary_path)
        
        # Check active running processes using psutil
        logger.info("Verifying active running processes using psutil...")
        running_processes = {p.info["name"].lower(): p.info for p in psutil.process_iter(["name", "exe", "status"])}
        
        target_process_names = ["empmonitor.exe", "updatemgr_emp.exe", "esr.exe", "emp_psa_service.exe"]
        for proc_name in target_process_names:
            if proc_name in running_processes:
                status = running_processes[proc_name].get("status", "running")
                logger.info(f"[HEALTHY] Process active: {proc_name} (Status: {status})")
            else:
                logger.warning(f"[INACTIVE] Process not detected running: {proc_name}")
    else:
        logger.warning(f"Legacy version detected ({version_input} <= 3.1.0). Skipping modern process checks.")

    # Locate and print config.js with masked tokens
    config_js_path = Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui\configs\config.js")
    if config_js_path.exists():
        logger.info(f"Reading configuration file: {config_js_path}")
        try:
            content = config_js_path.read_text(encoding="utf-8", errors="ignore")
            masked_lines = []
            for line in content.splitlines():
                if any(k in line.lower() for k in ["key", "token", "password", "secret"]):
                    line = re.sub(r'([\'"][^\'"]*[\'"])\s*:\s*([\'"][^\'"]*[\'"])', r'\1: "***MASKED***"', line)
                masked_lines.append(line)
            logger.info("--- config.js Contents (Masked) ---")
            print("\n".join(masked_lines[:30]))
        except Exception as e:
            logger.error(f"Failed to read config.js: {e}")
    else:
        logger.info(f"config.js file not present at: {config_js_path}")


# ==============================================================================
# PHASE 2: Interactive Dashboard Verification (L4 Handoff)
# ==============================================================================
def get_email_from_dashboard() -> str:
    """Invokes L4 Playwright automation to fetch employee email from Dashboard."""
    logger.info("[L4 Automation] Spawning headless Playwright browser to extract dashboard details...")
    with sync_playwright() as p:
        try:
            creds = fetch_employee_credentials(p, headless=True)
            extracted_email = creds.get("email", "")
            logger.info(f"[L4 Dashboard Extracted Email]: {extracted_email}")
            return extracted_email
        except Exception as e:
            logger.error(f"[L4 ERROR] Failed to extract details from dashboard: {e}")
            return ""


def phase_2_dashboard_handoff() -> Optional[str]:
    logger.info("\n=== PHASE 2: Interactive Dashboard Verification (L4 Handoff) ===")
    choice = input("Is the user registered in the dashboard? Enter 'y' for Dashboard Match, or 'n' for local checks only: ").strip().lower()
    
    if choice in ["y", "yes"]:
        return get_email_from_dashboard()
    else:
        logger.info("Skipping dashboard email extraction. Proceeding with local checks only.")
        return None


# ==============================================================================
# PHASE 3: Dynamic AppData Discovery, Log Harvest & Config Extraction
# ==============================================================================
def phase_3_appdata_and_log_harvest() -> Tuple[Path, Optional[Path], Optional[str]]:
    logger.info("\n=== PHASE 3: Dynamic AppData Discovery & Log Harvest ===")
    
    appdata_dir = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
    screen_dir = Path(appdata_dir) / "screen"
    logger.info(f"Resolved AppData Screen Path: {screen_dir}")

    if not screen_dir.exists():
        logger.warning(f"Screen directory does not exist: {screen_dir}")

    empm_dir = screen_dir / "empm"
    if empm_dir.exists():
        logger.info(f"[FOUND] empm directory present at: {empm_dir}")
    else:
        logger.warning(f"[MISSING] empm directory missing at: {empm_dir}")

    # Discover active config directory starting with prefix 'OjU'
    oju_matches = list(screen_dir.glob("OjU*"))
    oju_dir: Optional[Path] = oju_matches[0] if oju_matches else None
    
    if oju_dir:
        logger.info(f"[FOUND] Active configuration directory: {oju_dir.name} ({oju_dir})")
    else:
        logger.warning("No configuration directory starting with 'OjU*' found under AppData screen!")

    # Log Harvest: Retrieve last 50 lines of today's log file
    today_str = datetime.now().strftime("%Y-%m-%d")
    logs_dir = empm_dir / "logs"
    today_log_path = logs_dir / f"{today_str}.txt"
    
    if not today_log_path.exists():
        # Fallback to most recent log file if today's file doesn't exist
        log_files = sorted(logs_dir.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True) if logs_dir.exists() else []
        today_log_path = log_files[0] if log_files else None

    if today_log_path and today_log_path.exists():
        logger.info(f"Harvesting last 50 log lines from: {today_log_path}")
        try:
            lines = today_log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            last_50 = lines[-50:]
            print("\n--- [LOG HARVEST - LAST 50 LINES] ---")
            print("\n".join(last_50))
            print("--- [END LOG HARVEST] ---\n")
        except Exception as e:
            logger.error(f"Error reading log file {today_log_path}: {e}")
    else:
        logger.warning(f"No active log file found under: {logs_dir}")

    # Configuration Extraction (EV-001): Parse empm.ini
    host_email: Optional[str] = None
    if oju_dir:
        ini_path = oju_dir / "empm.ini"
        if ini_path.exists():
            file_size_kb = ini_path.stat().st_size / 1024.0
            logger.info(f"Found empm.ini ({file_size_kb:.2f} KB) at: {ini_path}")
            
            if file_size_kb > 3.0:
                logger.info("empm.ini size is > 3 KB (EV-001 condition met). Extracting config...")
            else:
                logger.warning(f"empm.ini size ({file_size_kb:.2f} KB) is <= 3 KB.")

            try:
                content = ini_path.read_text(encoding="utf-8", errors="ignore")
                
                # Parse key-values with masking
                config = configparser.ConfigParser(interpolation=None, strict=False, allow_no_value=True)
                try:
                    config.read_string(content)
                except Exception:
                    # Fallback for INI without section headers
                    config.read_string("[DEFAULT]\n" + content)

                logger.info("--- Parsed empm.ini Configurations (Masked) ---")
                for section in config.sections():
                    for key, val in config.items(section):
                        if key.lower() == "email":
                            host_email = val
                        masked_val = mask_sensitive_value(key, val or "")
                        print(f"  {key} = {masked_val}")

                # Backup regex search for email if section parsing missed it
                if not host_email:
                    email_match = re.search(r"email\s*=\s*([^\s\r\n]+)", content, re.IGNORECASE)
                    if email_match:
                        host_email = email_match.group(1)
                
                if host_email:
                    logger.info(f"[EXTRACTED] Host Email: {host_email}")
            except Exception as e:
                logger.error(f"Failed to parse empm.ini: {e}")
        else:
            logger.warning(f"empm.ini file not found at: {ini_path}")

    return screen_dir, oju_dir, host_email


# ==============================================================================
# PHASE 4: Cross-Layer Email Alignment
# ==============================================================================
def phase_4_cross_layer_alignment(dashboard_email: Optional[str], host_email: Optional[str]) -> bool:
    logger.info("\n=== PHASE 4: Cross-Layer Email Alignment ===")
    
    if dashboard_email is None:
        logger.info("Dashboard match was not enabled. Skipping alignment check.")
        return True

    if not host_email:
        logger.error("[CRITICAL ERROR] Host email could not be extracted from local empm.ini!")
        return False

    logger.info(f"Comparing Host Email: '{host_email}' <---> Dashboard Email: '{dashboard_email}'")
    
    if host_email.strip().lower() == dashboard_email.strip().lower():
        logger.info("[SUCCESS] Cross-Layer Email Match Validated!")
        return True
    else:
        logger.critical(
            f"[CRITICAL ERROR] Cross-Layer Email Mismatch! "
            f"Host Email: '{host_email}' != Dashboard Email: '{dashboard_email}'"
        )
        return False


# ==============================================================================
# PHASE 5: Telemetry Directory & SQLite Integrity Audit
# ==============================================================================
def phase_5_telemetry_and_sqlite_audit(screen_dir: Path, oju_dir: Optional[Path]) -> None:
    logger.info("\n=== PHASE 5: Telemetry Directory & SQLite Integrity Audit ===")
    
    # Resolve target telemetry directory (prefer OjU folder empm, fallback to screen/empm)
    telemetry_dir = (oju_dir / "empm") if (oju_dir and (oju_dir / "empm").exists()) else (screen_dir / "empm")
    logger.info(f"Auditing telemetry folder: {telemetry_dir}")

    required_items = [
        ("failed_screenrecords", "dir"),
        ("failed_screenshots", "dir"),
        ("logs", "dir"),
        ("screen_records", "dir"),
        ("local_db20.db", "file"),
    ]

    for item_name, item_type in required_items:
        target_path = telemetry_dir / item_name
        exists = target_path.is_dir() if item_type == "dir" else target_path.is_file()
        
        if exists:
            logger.info(f"[FOUND] Telemetry item present: {item_name}")
        else:
            # Print warning in red/highlighted text
            print(f"\033[91mCRITICAL DIRECTORY MISSING: {item_name}\033[0m")
            choice = input(f"Missing {item_name}. Do you want to continue the regression test or stop? [Continue/Stop]: ").strip().lower()
            if choice in ["stop", "s"]:
                logger.error(f"Execution halted by user due to missing telemetry item: {item_name}")
                sys.exit(1)
            else:
                logger.info(f"Continuing audit despite missing item: {item_name}")

    # Database Integrity Audit (EV-003)
    db_path = telemetry_dir / "local_db20.db"
    if db_path.exists():
        logger.info(f"Opening SQLite database connection to: {db_path}")
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchall()
            conn.close()
            
            if result and result[0][0] == "ok":
                logger.info("[HEALTHY] SQLite database structure integrity validated (PRAGMA integrity_check = ok).")
            else:
                logger.error(f"[FAILED] SQLite database integrity check failed. Result: {result}")
        except Exception as e:
            logger.error(f"[FAILED] Error connecting to SQLite database {db_path}: {e}")
    else:
        logger.warning(f"SQLite database file not found for integrity audit: {db_path}")


# ==============================================================================
# MAIN EXECUTION FLOW
# ==============================================================================
def main() -> None:
    logger.info("Starting Host Collector Telemetry & Environment Audit...")
    
    # Phase 1: Interactive Versioning & Binary Checks
    phase_1_binary_and_version_checks()

    # Phase 2: Interactive Dashboard Verification (L4 Handoff)
    dashboard_email = phase_2_dashboard_handoff()

    # Phase 3: Dynamic AppData Discovery & Log Harvest
    screen_dir, oju_dir, host_email = phase_3_appdata_and_log_harvest()

    # Phase 4: Cross-Layer Email Alignment
    alignment_success = phase_4_cross_layer_alignment(dashboard_email, host_email)
    if not alignment_success and dashboard_email is not None:
        logger.error("Halting execution due to cross-layer email mismatch.")
        sys.exit(1)

    # Phase 5: Telemetry Directory & SQLite Integrity Audit
    phase_5_telemetry_and_sqlite_audit(screen_dir, oju_dir)

    logger.info("\n[COMPLETED] Host Collector Audit Execution Finished Successfully!")


if __name__ == "__main__":
    main()
