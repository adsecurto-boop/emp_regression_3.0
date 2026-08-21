"""
Module: generate_auth_state.py
Purpose: Logs in using credentials and caches session state to bypass login forms.
Evidence Mapping: Part of L4 Web Dashboard Setup (EV-013)
"""

import os
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

# Setup logging for clean terminal output
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

AUTH_DIR = Path("playwright-profile")
AUTH_PATH = AUTH_DIR / "auth.json"


def generate_auth_state() -> None:
    # Ensure our target profile directory exists
    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        logging.info("Launching chromium browser (visible mode)...")
        # Launch in non-headless mode so we can verify the transition visually
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        
        logging.info("Navigating to EmpMonitor login interface...")
        page.goto("https://app.dev.empmonitor.com/amember/member", wait_until="domcontentloaded", timeout=60000)
        
        # We fill the credentials using the exact locators recorded in codegen
        logging.info("Entering developer credentials...")
        page.get_by_role("textbox", name="Username/Email").fill("qt_dev")
        page.get_by_role("textbox", name="Password").fill("qt_developers")
        
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
    generate_auth_state()
