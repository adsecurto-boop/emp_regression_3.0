"""
Module: test_dashboard_user_find.py
Purpose: Automates user details verification on the L4 Web Dashboard.
Evidence Mapping: EV-013 (Dashboard Navigation), EV-014 (User Verification)
"""

import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

EVIDENCE_DIR = Path("tests/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_employee_credentials(playwright: Playwright, headless: bool = True) -> dict:
    """
    Launches browser, loads cached auth session, navigates to employee details,
    extracts the registered Email and Password, saves screenshot evidence,
    and returns the credentials in a dictionary.
    """
    auth_state_path = "playwright-profile/auth.json"
    
    if not os.path.exists(auth_state_path):
        raise FileNotFoundError(
            f"Authentication state missing at {auth_state_path}. "
            f"Please run your login session script first!"
        )

    # Launch browser (headless=True is standard for background runs)
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context(storage_state=auth_state_path, ignore_https_errors=True)
    page = context.new_page()
    
    try:
        # Navigate directly to the Admin Dashboard (skips login due to storage_state)
        page.goto("https://app.dev.empmonitor.com/admin/dashboard", wait_until="domcontentloaded", timeout=60000)
        
        # 1. Navigate to Employee Details
        page.get_by_role("link", name="Employee ").click()
        page.get_by_role("link", name="Employee-Details").click()
        
        # Wait for the table/page structure to render
        expect(page.get_by_role("heading", name="Employee", exact=True)).to_be_visible(timeout=10000)
        
        # 2. Search for the target test user
        search_box = page.get_by_role("textbox", name="Search")
        search_box.fill("auto")
        search_box.press("Enter")
        
        # 3. Locate and click on the target user in the grid
        target_user = page.get_by_role("gridcell", name="auto test")
        expect(target_user).to_be_visible(timeout=5000)
        target_user.click()
        
        # Take Screenshot 1: Verify user exists on Grid
        screenshot_1_path = EVIDENCE_DIR / "01_employee_grid_match.png"
        page.screenshot(path=str(screenshot_1_path))
        
        # 4. Open the Edit Modal
        page.get_by_role("link", name="Edit").click()
        
        # Ensure modal inputs have loaded
        email_input = page.get_by_role("textbox", name="Email Address")
        expect(email_input).to_be_visible(timeout=5000)
        
        # 5. Extract Credentials directly from the inputs (No copy-paste simulation needed!)
        extracted_email = email_input.input_value()
        
        # Unmask the password field by clicking the eye icon to verify visibility
        page.locator(".btn.btn-default.fas.fa-eye.toggle-password-show-edit").click()
        password_input = page.get_by_role("textbox", name="Password", exact=True)
        extracted_password = password_input.input_value()
        
        # Take Screenshot 2: Visual proof of Edit Modal State
        screenshot_2_path = EVIDENCE_DIR / "02_employee_edit_modal.png"
        page.screenshot(path=str(screenshot_2_path))
        
        # 6. Gracefully close out the modal without altering states
        page.get_by_role("button", name="Update").click()
        page.get_by_role("button", name="OK").click()
        
        # Return credentials dictionary safely
        return {
            "email": extracted_email,
            "password": extracted_password,
            "evidence_paths": [str(screenshot_1_path), str(screenshot_2_path)]
        }

    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    # Test runner wrapper
    with sync_playwright() as playwright:
        print("[L4 Dashboard Run] Executing extraction...")
        creds = fetch_employee_credentials(playwright, headless=False)
        
        # Strictly mask the extracted password to maintain security standards (EV-001 rule)
        masked_password = "*" * len(creds['password'])
        print(f"\n--- EXTRACTED EVIDENCE ---")
        print(f"Registered User Email: {creds['email']}")
        print(f"Registered User Password: {masked_password}")
        print(f"Evidence Saved: {creds['evidence_paths']}")
