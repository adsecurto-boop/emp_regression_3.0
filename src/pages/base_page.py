"""
Base Page module providing common Playwright page interactions and utilities.
All Page Object Models (POM) should inherit from BasePage.
"""
from typing import Optional
from playwright.sync_api import Page, Response
from config.settings import BASE_URL, DEFAULT_TIMEOUT


class BasePage:
    """Base Page Object class encapsulating common Playwright browser interactions."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = BASE_URL
        self.default_timeout = DEFAULT_TIMEOUT

    def navigate(self, path_or_url: str = "") -> Optional[Response]:
        """Navigate to a given path relative to BASE_URL or full URL."""
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            target_url = path_or_url
        else:
            target_url = f"{self.base_url.rstrip('/')}/{path_or_url.lstrip('/')}"
        return self.page.goto(target_url, wait_until="domcontentloaded", timeout=self.default_timeout)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Click on an element specified by CSS selector or XPath."""
        timeout_ms = timeout or self.default_timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
        self.page.click(selector, timeout=timeout_ms)

    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Fill an input field specified by CSS selector or XPath."""
        timeout_ms = timeout or self.default_timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
        self.page.fill(selector, value, timeout=timeout_ms)

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: Optional[int] = None):
        """Wait for an element to reach a specific state ('attached', 'detached', 'visible', 'hidden')."""
        timeout_ms = timeout or self.default_timeout
        return self.page.wait_for_selector(selector, state=state, timeout=timeout_ms)

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if an element is visible on the page."""
        try:
            timeout_ms = timeout or 3000
            return self.page.is_visible(selector, timeout=timeout_ms)
        except Exception:
            return False

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get inner text of an element."""
        timeout_ms = timeout or self.default_timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
        return self.page.inner_text(selector, timeout=timeout_ms).strip()

    def take_screenshot(self, path: str) -> None:
        """Save a screenshot of the current page state."""
        self.page.screenshot(path=path, full_page=True)
