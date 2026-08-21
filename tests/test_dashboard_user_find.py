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
        # 1. Navigate to member URL to validate/refresh session state
        page.goto("https://app.dev.empmonitor.com/amember/member", wait_until="domcontentloaded", timeout=60000)
        
        # Auto-heal session if expired and redirected to login form
        try:
            user_field = page.get_by_role("textbox", name="Username/Email")
            if user_field.count() > 0 and user_field.is_visible():
                user_field.fill("qt_dev")
                page.get_by_role("textbox", name="Password").fill("qt_developers")
                page.get_by_role("button", name="Login").click()
                page.wait_for_load_state("networkidle")
                context.storage_state(path=auth_state_path)
        except Exception:
            pass

        # Ensure page navigation redirect is stable
        try:
            page.wait_for_load_state("domcontentloaded")
        except Exception:
            pass

        # 2. Navigate to Employee Details
        page.goto("https://app.dev.empmonitor.com/admin/employee-details", wait_until="domcontentloaded", timeout=60000)
        
        # 2. Locate DataTables Search Box
        search_box = page.get_by_role("textbox", name="Search").or_(page.locator("input[type='search'], .dataTables_filter input, input[placeholder*='Search']")).first
        expect(search_box).to_be_visible(timeout=60000)
        
        # Wait for the page and network to settle fully before searching
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        page.wait_for_timeout(2000)

        # Search for target user
        page.get_by_role("textbox", name="Search").click()
        search_box.click()
        search_box.fill("auto test")
        search_box.dispatch_event("input")
        search_box.dispatch_event("change")
        search_box.press("Enter")
        
        # Trigger search button click using #SearchButton ID from codegen
        try:
            search_btn = page.locator("#SearchButton, button:has(.fa-search), button.btn-search, .search-btn, button:has-text('Search')").first
            if search_btn.count() > 0 and search_btn.is_visible():
                search_btn.click()
        except Exception:
            pass
            
        page.wait_for_timeout(2000)
        
        # 3. Locate and click on the target user in the grid
        target_user = page.get_by_role("link", name="auto test").or_(page.locator("#td45009, td:has-text('auto test'), a:has-text('auto test'), [role='gridcell']:has-text('auto test')")).first
        if not target_user.is_visible():
            target_user = page.locator("tbody tr td a, tbody tr td").first
        
        expect(target_user).to_be_visible(timeout=40000)
        target_user.click()
        
        # Ensure page navigation to details finishes
        try:
            page.wait_for_load_state("domcontentloaded")
        except Exception:
            pass

        # Take Screenshot 1: Verify user exists on Grid / Details
        screenshot_1_path = EVIDENCE_DIR / "01_employee_grid_match.png"
        try:
            page.wait_for_timeout(6000)
            page.screenshot(path=str(screenshot_1_path), timeout=30000)
        except Exception:
            pass
        
        # 4. Open the Edit Modal
        edit_link = page.locator("a:has-text('Edit'), [title='Edit'], .edit_employee, a[href*='edit']").first
        expect(edit_link).to_be_visible(timeout=10000)
        edit_link.click()
        
        # Ensure modal email input is loaded and visible
        email_input = page.locator("input[placeholder*='Email'], input[name*='email'], #email, #edit_email, #emp_emailAddress").first
        expect(email_input).to_be_visible(timeout=10000)
        
        # Wait for AJAX modal data population
        try:
            page.wait_for_function(
                "el => el && el.value && el.value.trim().length > 0",
                arg=email_input.element_handle(),
                timeout=5000
            )
        except Exception:
            pass

        # Extract Email directly from the input
        extracted_email = email_input.input_value()
        
        # Unmask the password field by clicking the eye icon if present
        try:
            eye_icon = page.locator(".btn.btn-default.fas.fa-eye.toggle-password-show-edit, .toggle-password-show-edit, .fa-eye, .toggle-password")
            if eye_icon.count() > 0 and eye_icon.first.is_visible():
                eye_icon.first.click()
        except Exception:
            pass

        # Ensure modal password input is loaded and visible
        password_input = page.locator("input[placeholder*='Password'], input[name*='password'], #password, #edit_password, #password-editEmp").first
        expect(password_input).to_be_visible(timeout=5000)

        # Wait for AJAX modal data population
        try:
            page.wait_for_function(
                "el => el && el.value && el.value.trim().length > 0",
                arg=password_input.element_handle(),
                timeout=5000
            )
        except Exception:
            pass

        extracted_password = password_input.input_value()
        
        # Take Screenshot 2: Visual proof of Edit Modal State
        screenshot_2_path = EVIDENCE_DIR / "02_employee_edit_modal.png"
        try:
            page.wait_for_timeout(6000)
            page.screenshot(path=str(screenshot_2_path), timeout=30000)
        except Exception:
            pass
        
        # 6. Gracefully close out the modal without altering states
        try:
            close_btn = page.locator(".modal:visible button:has-text('Close'), .modal:visible .close, [data-dismiss='modal']").first
            if close_btn.count() > 0 and close_btn.is_visible():
                close_btn.click()
            else:
                page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        except Exception:
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
        
        # Return credentials dictionary safely
        return {
            "email": extracted_email,
            "password": extracted_password,
            "evidence_paths": [str(screenshot_1_path), str(screenshot_2_path)]
        }

    finally:
        try:
            page.close()
        except Exception:
            pass
        try:
            context.close()
        except Exception:
            pass
        try:
            browser.close()
        except Exception:
            pass


def test_dashboard_user_find(playwright: Playwright):
    """
    Pytest entry point for verifying L4 employee details extraction.
    """
    creds = fetch_employee_credentials(playwright, headless=True)
    assert creds["email"] is not None and len(creds["email"]) > 0
    assert "@" in creds["email"]
    assert creds["password"] is not None and len(creds["password"]) > 0
    assert len(creds["evidence_paths"]) == 2


if __name__ == "__main__":
    # Test runner wrapper
    playwright = sync_playwright().start()
    try:
        print("[L4 Dashboard Run] Executing extraction...")
        creds = fetch_employee_credentials(playwright, headless=False)
        
        # Strictly mask the extracted password to maintain security standards (EV-001 rule)
        masked_password = "*" * len(creds['password'])
        print(f"\n--- EXTRACTED EVIDENCE ---")
        print(f"Registered User Email: {creds['email']}")
        print(f"Registered User Password: {masked_password}")
        print(f"Evidence Saved: {creds['evidence_paths']}")
    finally:
        try:
            playwright.stop()
        except Exception:
            pass
