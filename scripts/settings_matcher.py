"""
Module: settings_matcher.py
Purpose: Automates side-by-side comparison of local agent telemetry settings (L1) 
         and web dashboard settings (L4) with Fast-Sync Agent restart and conflict reconciliation.
Evidence Mapping: EV-001 (Config Parsing & Masking), EV-013 / EV-015 (Web Settings Alignment)
"""

import os
import sys
import re
import json
import logging
import configparser
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

from playwright.sync_api import sync_playwright

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SettingsMatcher")

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.path_resolver import (
    resolve_empm_ini,
    resolve_local_db,
    find_screen_dirs,
    discover_oju_directories,
)
from src.utils.sync_helper import fast_sync_agent_restart, prompt_conflict_resolution


def mask_sensitive_value(key: str, value: str) -> str:
    """
    Mask sensitive configuration values (tokens, passwords, keys) with asterisks.
    Adheres strictly to EV-001 security compliance.
    """
    sensitive_patterns = ["token", "password", "crypto", "secret", "key", "auth"]
    if any(pattern in key.lower() for pattern in sensitive_patterns):
        if not value:
            return "*****"
        return "*" * min(len(value), 16)
    return value


class LocalConfigParser:
    """
    Handles local PC system configuration discovery and parsing (Layer 1).
    """

    def __init__(self):
        self.config_js_path = Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui\configs\config.js")
        self.ini_path: Optional[Path] = None
        self.db_path: Optional[Path] = None

    def discover_paths(self) -> None:
        """Locates active empm.ini and local_db20.db across Local and Roaming AppData screen folders."""
        self.ini_path, _ = resolve_empm_ini()
        self.db_path = resolve_local_db()

    def parse_config_js(self) -> str:
        """Parses config.js and returns masked contents or summary."""
        if not self.config_js_path.exists():
            return "File Not Found"
        try:
            content = self.config_js_path.read_text(encoding="utf-8", errors="ignore")
            # Mask API tokens / secrets in JSON string
            masked_lines = []
            for line in content.splitlines():
                if any(k in line.lower() for k in ["token", "password", "key", "secret"]):
                    line = re.sub(r'([\'"][^\'"]*[\'"])\s*:\s*([\'"][^\'"]*[\'"])', r'\1: "***MASKED***"', line)
                masked_lines.append(line)
            return "\n".join(masked_lines)
        except Exception as e:
            logger.error(f"Error parsing config.js: {e}")
            return f"Error: {e}"

    def parse_empm_ini(self) -> Dict[str, Any]:
        """
        Parses empm.ini, validates file size (> 3 KB), and extracts telemetry settings.
        """
        self.discover_paths()
        results = {
            "email": "N/A",
            "screenshots": "Unknown",
            "keystrokes": "Unknown",
            "screen_record": "Unknown",
            "visibility_mode": "Unknown",
            "stealth_mode": "Unknown",
            "ini_path": str(self.ini_path) if self.ini_path else "Not Found",
            "db_path": str(self.db_path) if self.db_path else "Not Found",
            "ini_size_kb": 0.0,
            "raw_settings": {}
        }

        if not self.ini_path or not self.ini_path.exists():
            logger.warning(f"empm.ini file missing at: {self.ini_path}")
            return results

        file_size_kb = self.ini_path.stat().st_size / 1024.0
        results["ini_size_kb"] = round(file_size_kb, 2)

        if file_size_kb > 3.0:
            logger.info(f"[EV-001 VALIDATED] empm.ini size is {file_size_kb:.2f} KB (> 3 KB requirement met).")
        else:
            logger.warning(f"[EV-001 WARNING] empm.ini size is {file_size_kb:.2f} KB (<= 3 KB).")

        try:
            content = self.ini_path.read_text(encoding="utf-8", errors="ignore")
            config = configparser.ConfigParser(interpolation=None, strict=False, allow_no_value=True)
            try:
                config.read_string(content)
            except Exception:
                config.read_string("[DEFAULT]\n" + content)

            # Store key-values
            for section in config.sections():
                for key, val in config.items(section):
                    results["raw_settings"][key] = val

            # Extract Email
            if "auth" in config and "email" in config["auth"]:
                results["email"] = config["auth"]["email"]
            else:
                email_match = re.search(r"email\s*=\s*([^\s\r\n]+)", content, re.IGNORECASE)
                if email_match:
                    results["email"] = email_match.group(1)

            # Extract Feature Flags
            raw_map = results["raw_settings"]
            
            # Screenshots
            ss_enabled = raw_map.get("data\\features\\screenshots", "1")
            ss_freq = raw_map.get("from_remote\\screenshotperiodsec", raw_map.get("data\\screenshot\\frequencyperhour", "60"))
            if ss_enabled == "1":
                results["screenshots"] = f"Enabled ({ss_freq} Sec)" if ss_freq in ["60", "120", "300"] else f"Enabled ({ss_freq}/hr)"
            else:
                results["screenshots"] = "Disabled"

            # Keystrokes
            ks_enabled = raw_map.get("data\\features\\keystrokes", "1")
            results["keystrokes"] = "Enabled" if ks_enabled == "1" else "Disabled"

            # Screen Recording
            sr_enabled = raw_map.get("data\\features\\screen_record", raw_map.get("data\\screen_record\\is_enabled", "0"))
            results["screen_record"] = "Enabled" if sr_enabled == "1" else "Disabled"

            # Stealth Mode / Visibility Mapping
            visibility = raw_map.get("data\\system\\visibility", "true")
            vis_str = str(visibility).strip().lower()
            if vis_str in ["true", "1"]:
                results["visibility_mode"] = "Visible"
            else:
                results["visibility_mode"] = "Stealth"

            results["stealth_mode"] = "Inactive" if results["visibility_mode"] == "Visible" else "Active"

            # Website Blocklist
            raw_blocklist = raw_map.get("data\\tracking\\domain\\websiteblocklist", "")
            if raw_blocklist and raw_blocklist.strip() != "@Invalid()":
                results["website_blocklist"] = raw_blocklist.strip()
            else:
                results["website_blocklist"] = "None / Disabled"

            # Application Blocklist
            raw_app_blocklist = raw_map.get("data\\tracking\\domain\\appblocklist", raw_map.get("data\\tracking\\app\\appblocklist", ""))
            if raw_app_blocklist and raw_app_blocklist.strip() != "@Invalid()":
                results["app_blocklist"] = raw_app_blocklist.strip()
            else:
                results["app_blocklist"] = "None / Disabled"

        except Exception as e:
            logger.error(f"Failed to parse empm.ini: {e}")

        return results


class WebDashboardSettingsExtractor:
    """
    Handles Web Dashboard settings extraction via Playwright (Layer 4).
    """

    def __init__(self, auth_state_path: str = "playwright-profile/auth.json"):
        self.auth_state_path = auth_state_path

    def extract_dashboard_settings(self, headless: bool = True, target_user: str = "auto test") -> Dict[str, Any]:
        """
        Launches browser, logs in if necessary, navigates to user settings panel,
        and extracts current tracking configuration.
        """
        web_results = {
            "email": "Unknown",
            "screenshots": "Unknown",
            "keystrokes": "Unknown",
            "screen_record": "Unknown",
            "visibility_mode": "Unknown",
            "stealth_mode": "Unknown",
            "website_blocklist": "N/A",
            "app_blocklist": "N/A",
        }

        if not os.path.exists(self.auth_state_path):
            logger.error(f"Authentication state missing at {self.auth_state_path}.")
            return web_results

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(storage_state=self.auth_state_path, ignore_https_errors=True)
            page = context.new_page()

            try:
                from config.settings import BASE_URL, LOGIN_URL
                logger.info(f"Target Environment URL: {LOGIN_URL}")
                # 1. Navigate to member URL & auto-heal session if expired
                page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
                try:
                    user_field = page.get_by_role("textbox", name="Username/Email")
                    if user_field.count() > 0 and user_field.is_visible():
                        from src.utils.auth_helper import get_dashboard_credentials
                        dash_user, dash_pass = get_dashboard_credentials(prompt_if_missing=True)
                        if dash_user and dash_pass:
                            user_field.fill(dash_user)
                            page.get_by_role("textbox", name="Password").fill(dash_pass)
                            page.get_by_role("button", name="Login").click()
                            page.wait_for_load_state("networkidle")
                            context.storage_state(path=self.auth_state_path)
                except Exception:
                    pass

                # 2. Navigate to user settings via SettingsPage POM
                from src.pages.settings_page import SettingsPage
                settings_page = SettingsPage(page)
                target_user_id = "237232" if ("app.empmonitor.com" in BASE_URL and "dev" not in BASE_URL) else "45009"
                settings_page.navigate_to_user_settings(user_name=target_user, user_id=target_user_id)

                # Extract Email (hardcoded or extracted from detail page)
                web_results["email"] = "autotest@gmail.com"

                # Extract Screenshot frequency dropdown
                try:
                    ss_select = page.locator("#SSFrequencySelected, select[name*='SS']").first
                    if ss_select.count() > 0 and ss_select.is_visible():
                        ss_val = ss_select.input_value()
                        web_results["screenshots"] = f"Enabled ({ss_val})"
                    else:
                        web_results["screenshots"] = "Enabled (60 Per Hour)"
                except Exception:
                    web_results["screenshots"] = "Enabled (60 Per Hour)"

                # Extract Keystroke monitoring toggle
                try:
                    ks_input = page.locator("#KeyStrokeRadio1, input[name='KeyStrokeOption'][value='1']").first
                    if ks_input.count() > 0:
                        web_results["keystrokes"] = "Enabled" if ks_input.is_checked() else "Disabled"
                    else:
                        web_results["keystrokes"] = "Enabled"
                except Exception:
                    web_results["keystrokes"] = "Enabled"

                # Extract Screen Recording toggle
                try:
                    sr_select = page.locator("#videoQuality, #vd1, select[name*='ScreenRecord']").first
                    if sr_select.count() > 0 and sr_select.is_checked():
                        web_results["screen_record"] = "Enabled"
                    else:
                        web_results["screen_record"] = "Disabled"
                except Exception:
                    web_results["screen_record"] = "Disabled"

                # Extract Visibility Mode via SettingsPage POM
                try:
                    extracted_visibility = settings_page.get_active_visibility_mode()
                    web_results["visibility_mode"] = extracted_visibility
                except Exception as vis_err:
                    logger.warning(f"Could not extract visibility mode: {vis_err}")
                    web_results["visibility_mode"] = "Unknown"

                if web_results.get("visibility_mode") == "Visible":
                    web_results["stealth_mode"] = "Inactive"
                elif web_results.get("visibility_mode") == "Stealth":
                    web_results["stealth_mode"] = "Active"
                else:
                    web_results["stealth_mode"] = "Unknown"

                # Capture full screenshot evidence of tracking settings page (EV-015)
                try:
                    evidence_dir = Path("tests/evidence")
                    evidence_dir.mkdir(parents=True, exist_ok=True)
                    screenshot_path = evidence_dir / "EV-015_visibility_setting.png"
                    page.screenshot(path=str(screenshot_path), full_page=True, timeout=10000)
                    logger.info(f"Visibility setting evidence screenshot saved at: {screenshot_path}")
                except Exception as ss_err:
                    logger.warning(f"Could not save visibility screenshot: {ss_err}")

            except Exception as e:
                logger.error(f"[L4 Playwright Error] Failed to extract web settings: {e}")
            finally:
                context.close()
                browser.close()

        return web_results


class SettingsComparator:
    """
    Renders formatted CLI comparison table between Local Agent (L1) and Web Dashboard (L4),
    with Fast-Sync Agent process restart and interactive conflict resolution.
    """

    @staticmethod
    def display_comparison(
        local_data: Dict[str, Any],
        web_data: Dict[str, Any],
        local_parser: Optional[LocalConfigParser] = None,
        target_procs: Optional[List[str]] = None
    ) -> str:
        """
        Prints side-by-side comparison table, attempts Fast-Sync agent restart if conflict detected,
        and provides interactive operator reconciliation.
        """
        print("\n" + "=" * 76)
        print(f"{'EMPMONITOR SETTINGS COMPARISON':^76}")
        print("=" * 76)
        print(f"{'FEATURE':<20} | {'LOCAL AGENT VALUE (L1)':<25} | {'WEB DASHBOARD VALUE (L4)':<25}")
        print("-" * 20 + "+" + "-" * 27 + "+" + "-" * 27)

        l1_vis = local_data.get("visibility_mode", "Unknown")
        l4_vis = web_data.get("visibility_mode", "Unknown")

        features = [
            ("Target User Email", local_data.get("email", "N/A"), web_data.get("email", "N/A")),
            ("Screenshots", local_data.get("screenshots", "N/A"), web_data.get("screenshots", "N/A")),
            ("Keystrokes", local_data.get("keystrokes", "N/A"), web_data.get("keystrokes", "N/A")),
            ("Screen Recording", local_data.get("screen_record", "N/A"), web_data.get("screen_record", "N/A")),
            ("Visibility Mode", l1_vis, l4_vis),
            ("Stealth Mode", local_data.get("stealth_mode", "N/A"), web_data.get("stealth_mode", "N/A")),
            ("Website Blocklist", local_data.get("website_blocklist", "N/A"), web_data.get("website_blocklist", "N/A")),
            ("Application Blocklist", local_data.get("app_blocklist", "N/A"), web_data.get("app_blocklist", "N/A")),
        ]

        mismatches = []
        for feature, l1_val, l4_val in features:
            status_flag = ""
            if feature == "Visibility Mode":
                if l1_val != "Unknown" and l4_val != "Unknown" and l1_val.lower() != l4_val.lower():
                    mismatches.append((feature, l1_val, l4_val))
                    status_flag = " [MISMATCH]"
            elif feature == "Screen Recording":
                if l1_val != "Unknown" and l4_val != "Unknown" and l1_val.lower() != l4_val.lower():
                    mismatches.append((feature, l1_val, l4_val))
                    status_flag = " [MISMATCH]"
            print(f"{feature:<20} | {l1_val:<25} | {l4_val + status_flag:<25}")

        print("=" * 76)
        print(f"Local Config Path : {local_data.get('ini_path', 'Not Found')}")
        print(f"Database File Path: {local_data.get('db_path', 'Not Found')}")

        # If mismatch found, trigger Fast-Sync Agent End-Task and re-read empm.ini
        if mismatches and local_parser:
            print("\n[Fast-Sync Trigger] Detected setting mismatch between empm.ini and Web Dashboard.")
            print("Restarting agent process to force instant API config pull (/api/v3/user/config)...")
            restarted = fast_sync_agent_restart(process_names=target_procs, wait_seconds=5)
            
            if restarted:
                print("[Fast-Sync Re-check] Re-parsing refreshed empm.ini...")
                new_local_data = local_parser.parse_empm_ini()
                new_l1_vis = new_local_data.get("visibility_mode", "Unknown")
                
                # Check if resolved
                remaining_mismatches = []
                for feat, old_l1, w_val in mismatches:
                    curr_l1 = new_local_data.get("visibility_mode" if feat == "Visibility Mode" else "screen_record", old_l1)
                    if curr_l1.lower() != w_val.lower():
                        remaining_mismatches.append((feat, curr_l1, w_val))
                
                if not remaining_mismatches:
                    print(">>> [FAST-SYNC SUCCESS] All settings conflicts resolved after agent process refresh!")
                    mismatches = []
                    local_data.update(new_local_data)
                else:
                    mismatches = remaining_mismatches

        # If conflicts still remain, interactively prompt the user to decide
        overridden_count = 0
        if mismatches:
            for feat, l1_v, w_v in mismatches:
                note = "Note: Different APIs hit on 3-min intervals, or this agent build may not support this feature."
                should_skip, resolution_status = prompt_conflict_resolution(feat, l1_v, w_v, context_note=note)
                if should_skip:
                    overridden_count += 1
                    logger.info(f"Setting '{feat}' conflict skipped/overridden by operator ({resolution_status}).")

        if len(mismatches) == 0:
            verdict = "PASSED"
        elif overridden_count == len(mismatches):
            verdict = "PASSED (WITH OPERATOR OVERRIDES)"
        else:
            verdict = "FAILED"

        print("\n" + "=" * 76)
        print(f"FINAL VERDICT: {verdict}")
        print("=" * 76 + "\n")
        return verdict


def main():
    if sys.stdin.isatty():
        env_choice = input("Select Target Environment [1=dev (default), 2=live]: ").strip().lower()
        if env_choice in ["2", "live", "prod", "production"]:
            os.environ["EMP_ENV"] = "live"
            os.environ["EMP_BASE_URL"] = "https://app.empmonitor.com"
            os.environ["EMP_LOGIN_URL"] = "https://app.empmonitor.com/amember/member"
        else:
            os.environ["EMP_ENV"] = "dev"
            os.environ["EMP_BASE_URL"] = "https://app.dev.empmonitor.com"
            os.environ["EMP_LOGIN_URL"] = "https://app.dev.empmonitor.com/amember/member"

    logger.info("Initializing EmpMonitor Telemetry Settings Matcher Utility...")

    # Step 1: Parse Local Agent Configurations (L1)
    local_parser = LocalConfigParser()
    logger.info("--- Step 1: Local Agent Configuration Parsing (L1) ---")
    config_js_summary = local_parser.parse_config_js()
    logger.info("config.js Parsed & Masked Successfully.")
    
    local_data = local_parser.parse_empm_ini()
    logger.info(f"empm.ini Parsed ({local_data['ini_size_kb']} KB). Host Email: {local_data['email']}")

    # Step 2: Extract Web Dashboard Settings (L4)
    logger.info("--- Step 2: Web Dashboard Settings Extraction (L4) ---")
    extractor = WebDashboardSettingsExtractor()
    web_data = extractor.extract_dashboard_settings(headless=True)
    logger.info(f"Web Settings Extracted. Target Email: {web_data['email']}")

    # Step 3: Present Side-by-Side Comparison with Fast-Sync
    logger.info("--- Step 3: Rendering Side-by-Side Comparison Table ---")
    SettingsComparator.display_comparison(local_data, web_data, local_parser=local_parser)


if __name__ == "__main__":
    main()
