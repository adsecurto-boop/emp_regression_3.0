"""
Module: conftest.py
Purpose: Global Pytest fixtures to load pre-authenticated browser contexts.
"""

import os
import sys
from pathlib import Path
from typing import Generator
import pytest
from playwright.sync_api import Playwright, BrowserContext, Page

# Ensure project root is in sys.path for test imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.pages.base_page import BasePage
except ImportError:
    BasePage = None

AUTH_PATH = "playwright-profile/auth.json"


@pytest.fixture(scope="session")
def auth_state_file() -> Path:
    """Fixture returning path to cached auth state JSON file."""
    return Path(AUTH_PATH)


@pytest.fixture(scope="session")
def authenticated_context(playwright: Playwright):
    """
    Spawns a clean, pre-authenticated browser context using the cached session state.
    Bypasses the login process entirely for rapid test execution.
    """
    if not os.path.exists(AUTH_PATH):
        pytest.fail(
            f"Cached authentication state not found at: {AUTH_PATH}. "
            f"Please run 'python scripts/generate_auth_state.py' first!"
        )
        
    # Launch browser (set headless=True when running in CI/Jenkins)
    browser = playwright.chromium.launch(headless=False)
    
    # Load the cached state directly into the new context
    context = browser.new_context(storage_state=AUTH_PATH, ignore_https_errors=True)

    # Validate & auto-heal session if expired
    page = context.new_page()
    try:
        from config.settings import LOGIN_URL
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        user_field = page.get_by_role("textbox", name="Username/Email")
        if user_field.count() > 0 and user_field.is_visible():
            from src.utils.auth_helper import get_dashboard_credentials
            dash_user, dash_pass = get_dashboard_credentials(prompt_if_missing=False)
            if dash_user and dash_pass:
                user_field.fill(dash_user)
                page.get_by_role("textbox", name="Password").fill(dash_pass)
                page.get_by_role("button", name="Login").click()
                page.wait_for_load_state("networkidle")
                context.storage_state(path=AUTH_PATH)
    except Exception:
        pass
    finally:
        page.close()
    
    yield context
    
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def authenticated_page(authenticated_context: BrowserContext) -> Generator[Page, None, None]:
    """Fixture providing a fresh page initialized within the authenticated context."""
    page = authenticated_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def base_page(authenticated_page: Page):
    """Fixture providing an instance of BasePage using the authenticated page."""
    if BasePage:
        return BasePage(authenticated_page)
    return None
