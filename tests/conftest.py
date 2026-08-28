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

from config.environments import get_environment_config


def pytest_addoption(parser):
    """Add --env CLI option to pytest (e.g., pytest --env=silah_live or pytest --env=dev)."""
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Target environment: 'dev' (https://app.dev.empmonitor.com) or 'silah_live' (https://tts.silah.com.sa)"
    )


def pytest_configure(config):
    """Configure environment variables based on --env CLI flag."""
    env_opt = config.getoption("--env", default=None)
    if env_opt:
        env_choice = env_opt.strip().lower()
        if env_choice in ["silah", "silah_live", "silah-live", "prod", "production"]:
            os.environ["EMP_ENV"] = "silah_live"
            os.environ["EMP_BASE_URL"] = "https://tts.silah.com.sa"
            os.environ["EMP_LOGIN_URL"] = "https://tts.silah.com.sa/admin-login"
        else:
            os.environ["EMP_ENV"] = "dev"
            os.environ["EMP_BASE_URL"] = "https://app.dev.empmonitor.com"
            os.environ["EMP_LOGIN_URL"] = "https://app.dev.empmonitor.com/amember/member"


def get_active_auth_path() -> Path:
    from config.settings import AUTH_STATE_PATH, EMP_ENV
    env_cfg = get_environment_config(EMP_ENV)
    auth_path = env_cfg["auth_profile"]
    if auth_path.exists():
        return auth_path
    return AUTH_STATE_PATH


@pytest.fixture(scope="session")
def auth_state_file() -> Path:
    """Fixture returning path to cached auth state JSON file."""
    return get_active_auth_path()


@pytest.fixture(scope="session")
def authenticated_context(playwright: Playwright):
    """
    Spawns a clean, pre-authenticated browser context using the cached session state.
    Bypasses the login process entirely for rapid test execution.
    """
    target_auth_path = get_active_auth_path()
    if not target_auth_path.exists():
        pytest.fail(
            f"Cached authentication state not found at: {target_auth_path}. "
            f"Please run 'python scripts/generate_auth_state.py --env={os.getenv('EMP_ENV', 'dev')}' first!"
        )
        
    # Launch browser (set headless=True when running in CI/Jenkins)
    is_headless = os.getenv("HEADLESS", "false").lower() == "true"
    browser = playwright.chromium.launch(headless=is_headless)
    
    # Load the cached state directly into the new context
    context = browser.new_context(storage_state=str(target_auth_path), ignore_https_errors=True)

    # Validate & auto-heal session if expired
    page = context.new_page()
    try:
        from config.settings import LOGIN_URL
        page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30000)
        user_field = page.locator("input[name='username'], input[name='email'], input[type='email'], input[placeholder*='Username']").first
        if user_field.count() > 0 and user_field.is_visible():
            from src.utils.auth_helper import get_dashboard_credentials
            dash_user, dash_pass = get_dashboard_credentials(prompt_if_missing=False)
            if dash_user and dash_pass:
                user_field.fill(dash_user)
                page.locator("input[name='password'], input[type='password']").first.fill(dash_pass)
                page.locator("button[type='submit'], input[type='submit'], button:has-text('Login')").first.click()
                page.wait_for_load_state("networkidle")
                context.storage_state(path=str(target_auth_path))
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

