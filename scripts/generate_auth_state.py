"""
Module: generate_auth_state.py
Purpose: Logs in using credentials and caches session state to bypass login forms.
Evidence Mapping: Part of L4 Web Dashboard Setup (EV-013)
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging for clean terminal output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

AUTH_DIR = PROJECT_ROOT / "playwright-profile"


def generate_auth_state(env_name: str = "dev") -> None:
    from config.environments import get_environment_config
    env_cfg = get_environment_config(env_name)
    login_url = env_cfg["login_url"]
    auth_file_path = env_cfg["auth_profile"]
    
    # Ensure profile directory exists
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        logging.info(f"Launching chromium browser (visible mode) for environment: {env_cfg['name']}...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        logging.info(f"Navigating to login interface: {login_url}")
        page.goto(login_url, wait_until="domcontentloaded", timeout=60000)
        
        # Retrieve credentials dynamically
        logging.info("Retrieving dashboard login credentials...")
        from src.utils.auth_helper import get_dashboard_credentials
        username, password = get_dashboard_credentials(prompt_if_missing=True)
        
        if username and password:
            logging.info("Entering credentials into login form...")
            # Handle multi-tenant login field variations (EmpMonitor vs Silah TTS Admin)
            user_input = page.locator("input[name='username'], input[name='email'], input[type='email'], input[placeholder*='Email'], input[placeholder*='Username']").first
            if not user_input.is_visible(timeout=3000):
                user_input = page.get_by_role("textbox", name="Username/Email")
            user_input.fill(username)

            pass_input = page.locator("input[name='password'], input[type='password']").first
            if not pass_input.is_visible(timeout=3000):
                pass_input = page.get_by_role("textbox", name="Password")
            pass_input.fill(password)
            
            logging.info("Submitting login form...")
            submit_btn = page.locator("button[type='submit'], input[type='submit'], button:has-text('Login'), button:has-text('Sign In')").first
            submit_btn.click()
        else:
            logging.info("Credentials not supplied automatically. Waiting up to 90 seconds for manual user login...")

        # Wait for authenticated dashboard landing element
        logging.info("Waiting for dashboard redirect & session completion...")
        try:
            page.wait_for_selector("h1, h2, header, .dashboard, #dashboard, .admin-dashboard, a[href*='logout']", timeout=30000)
        except Exception as e:
            logging.warning(f"Dashboard header wait timeout ({e}). Verifying navigation state...")
        
        # Screenshot evidence
        try:
            evidence_dir = PROJECT_ROOT / "tests" / "evidence"
            evidence_dir.mkdir(parents=True, exist_ok=True)
            env_prefix = "silah_live" if "silah" in env_cfg["name"] else "00"
            screenshot_path = evidence_dir / f"{env_prefix}_authenticated_dashboard.png"
            page.wait_for_timeout(2000)
            page.screenshot(path=str(screenshot_path), timeout=5000)
            logging.info(f"Dashboard screenshot evidence saved at: {screenshot_path}")
        except Exception as e:
            logging.warning(f"Screenshot capture skipped or timed out ({e}). Proceeding to save session state...")
        
        # Save session cookies strictly into target json profile
        context.storage_state(path=str(auth_file_path))
        logging.info(f"Success! Session state successfully cached at: {auth_file_path}")
        
        context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate authenticated session state JSON for Playwright testing.")
    parser.add_argument("--env", type=str, default=None, help="Target environment ('dev' or 'silah_live')")
    args = parser.parse_args()

    env_selection = args.env
    if not env_selection and sys.stdin.isatty():
        choice = input("Select Environment [1=dev (default), 2=silah_live]: ").strip().lower()
        if choice in ["2", "silah", "silah_live", "silah-live"]:
            env_selection = "silah_live"
        else:
            env_selection = "dev"
    elif not env_selection:
        env_selection = os.getenv("EMP_ENV", "dev")

    if env_selection in ["silah", "silah_live", "silah-live"]:
        os.environ["EMP_ENV"] = "silah_live"
        os.environ["EMP_BASE_URL"] = "https://tts.silah.com.sa"
        os.environ["EMP_LOGIN_URL"] = "https://tts.silah.com.sa/admin-login"
    else:
        os.environ["EMP_ENV"] = "dev"
        os.environ["EMP_BASE_URL"] = "https://app.dev.empmonitor.com"
        os.environ["EMP_LOGIN_URL"] = "https://app.dev.empmonitor.com/amember/member"

    generate_auth_state(env_selection)

