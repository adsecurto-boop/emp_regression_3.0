"""
Module: generate_auth_state.py
Purpose: Logs in using credentials and caches session state to bypass login forms.
Evidence Mapping: Part of L4 Web Dashboard Setup (EV-013)
"""

import sys
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Setup logging for clean terminal output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

AUTH_DIR = Path("playwright-profile")
AUTH_PATH = AUTH_DIR / "auth.json"


def generate_auth_state() -> None:
    from config.settings import LOGIN_URL
    # Ensure our target profile directory exists
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        logging.info("Launching chromium browser (visible mode)...")
        # Launch in non-headless mode so we can verify the transition visually
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        logging.info(f"Navigating to EmpMonitor login interface: {LOGIN_URL}")
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
        
        # We fill the credentials dynamically using auth_helper
        logging.info("Retrieving dashboard login credentials...")
        from src.utils.auth_helper import get_dashboard_credentials
        username, password = get_dashboard_credentials(prompt_if_missing=True)
        if not username or not password:
            logging.error("Dashboard credentials not provided! Cannot generate auth state.")
            return

        logging.info("Entering credentials into login form...")
        page.get_by_role("textbox", name="Username/Email").fill(username)
        page.get_by_role("textbox", name="Password").fill(password)
        
        logging.info("Submitting login form...")
        page.get_by_role("button", name="Login").click()
        
        # Crucial: Wait for the landing page's main 'Dashboard' header to render.
        # This guarantees our session is fully authenticated before we save.
        logging.info("Waiting for dashboard redirect...")
        dashboard_header = page.get_by_role("heading", name="Dashboard")
        dashboard_header.wait_for(timeout=15000)
        
        # Take screenshot evidence of the authenticated dashboard session
        evidence_dir = Path("tests/evidence")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = evidence_dir / "00_authenticated_dashboard.png"
        page.wait_for_timeout(3000)
        page.screenshot(path=str(screenshot_path), timeout=15000)
        logging.info(f"Dashboard screenshot evidence saved at: {screenshot_path}")
        
        # Save cookies and local storage state into our profile directory
        context.storage_state(path=str(AUTH_PATH))
        logging.info(f"Success! Session state successfully cached at: {AUTH_PATH}")
        
        context.close()
        browser.close()


if __name__ == "__main__":
    if sys.stdin.isatty():
        env_choice = input("Select Environment [1=dev (default), 2=live]: ").strip().lower()
        if env_choice in ["2", "live", "prod", "production"]:
            import os
            os.environ["EMP_ENV"] = "live"
            os.environ["EMP_BASE_URL"] = "https://app.empmonitor.com"
            os.environ["EMP_LOGIN_URL"] = "https://app.empmonitor.com/amember/member"
    generate_auth_state()
