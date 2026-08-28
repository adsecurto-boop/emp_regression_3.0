"""
Module: reseller_client_page.py
Layer: Layer 4 (L4) - Web Dashboard Automation
Ticket: Ticket 2025 (Auto Email Switch) & Ticket 2029 (Reseller Bulk ZIP & Pagination)
"""

import re
from typing import Optional
from playwright.sync_api import Page, Locator, Download, expect
from config.settings import BASE_URL
from src.pages.base_page import BasePage


class ResellerClientPage(BasePage):
    """
    Page Object Model for the Reseller Client Management & Monthly Reports Dashboard.
    Encapsulates:
    - Client grid interactions & Monthly Auto-Email switch toggles (Ticket 2025)
    - Impersonation login as client
    - Reseller bulk ZIP package download & "Paginate by Employee" configuration (Ticket 2029)
    """

    def __init__(self, page: Page, base_url: str = BASE_URL):
        super().__init__(page)
        self.base_url = base_url

        # Navigation Locators
        self.reseller_link = page.locator("a:has-text('Reseller')")
        self.nav_reseller = self.reseller_link
        self.reseller_dashboard_link = page.locator("a[href*='reseller-dashboard'], a:has-text('Dashboard')")
        self.nav_reseller_dashboard = self.reseller_dashboard_link

        # Grid & Search Controls (Ticket 2025)
        self.search_input = page.locator("input[type='search'], input[placeholder*='Search']").first
        self.client_table_rows = page.locator("table#resellerClientTable tbody tr, tbody tr")
        self.client_row = lambda identifier: page.locator(
            f"tr:has-text('{identifier}'), tr[id='{identifier}']"
        )
        self.impersonate_proceed_btn = page.locator("button:has-text('Proceed')")

        # Reseller Bulk Download Locators (Ticket 2029 - Extracted from Codegen Audit)
        self.download_all_reports_btn = page.locator(
            "button:has-text('Download All Reports'), #downloadAllReportsBtn, button:has-text('Download All')"
        )
        self.bulk_download_modal = page.locator(
            "div[role='dialog'], #downloadAllModal, .modal:has-text('Download All Companies')"
        )
        self.paginate_by_employee_chk = page.locator(
            "text=Start each employee's report, label:has-text('Start each employee\'s report'), label:has-text('Paginate by Employee'), input[name='paginate_by_employee']"
        )
        self.reporting_month_input = page.locator(
            "input[name='reporting_month'], input[placeholder*='Reporting month'], input[type='month']"
        )
        self.company_scope_all_radio = page.locator(
            "text='All companies', label:has-text('All companies'), input[value='all']"
        )
        self.company_scope_selected_radio = page.locator(
            "text='Selected companies only', label:has-text('Selected companies only'), input[value='selected']"
        )
        self.generate_reports_btn = page.locator(
            "button:has-text('Generate Reports'), #generateReportsBtn"
        )
        self.progress_container = page.locator("#darProgressWrap, .progress-wrapper")
        self.zip_ready_banner = page.locator("text='Completed. Your ZIP is ready.'")
        self.download_zip_link = page.locator(
            "a:has-text('Download ZIP'), button:has-text('Download ZIP')"
        )
        self.modal_close_btn = page.locator(
            "#downloadAllModal button:has-text('Close'), button:has-text('Close')"
        )

    def navigate_to_reseller_dashboard(self) -> None:
        """Navigates to the Reseller Dashboard page."""
        target_url = f"{self.base_url.rstrip('/')}/admin/reseller-dashboard"
        if not self.page.url.startswith("http"):
            self.page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            return

        if self.reseller_link.is_visible(timeout=3000):
            self.reseller_link.click()
            if self.reseller_dashboard_link.first.is_visible(timeout=3000):
                self.reseller_dashboard_link.first.click()
                return

        self.page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
        self.page.wait_for_load_state("networkidle")

    def navigate(self, path_or_url: str = "") -> None:
        """Alias navigation method."""
        if path_or_url:
            super().navigate(path_or_url)
        else:
            self.navigate_to_reseller_dashboard()

    # --------------------------------------------------------------------------
    # Ticket 2025: Client Grid & Monthly Auto-Email Controls
    # --------------------------------------------------------------------------
    def get_client_row(self, client_email_or_id: str) -> Locator:
        """Returns the locator representing the client row based on email, username, or client ID."""
        return self.client_row(client_email_or_id).first

    def toggle_client_monthly_auto_email(self, client_identifier: str, enable: bool = True) -> None:
        """Locates the specific client's row and toggles their Monthly Auto-Email Reports switch."""
        row = self.get_client_row(client_identifier)
        row.wait_for(state="visible", timeout=10000)

        toggle_switch = row.locator(
            "input[id*='monthly_manager_report_'], input[type='checkbox'].monthly-report-switch, input[type='checkbox'].auto-email-switch"
        ).first
        toggle_switch.wait_for(state="attached", timeout=5000)

        is_checked = toggle_switch.is_checked()
        if enable and not is_checked:
            toggle_switch.check()
        elif not enable and is_checked:
            toggle_switch.uncheck()

        self.page.wait_for_load_state("networkidle")

    def toggle_monthly_manager_report(self, client_identifier: str, enable: bool = True) -> None:
        """Alias method to toggle the Monthly Manager Auto-Email Report switch."""
        self.toggle_client_monthly_auto_email(client_identifier, enable)

    def impersonate_client(self, client_identifier: str) -> None:
        """Clicks the Login As Client (impersonation link) within the target client's row."""
        row = self.get_client_row(client_identifier)
        row.wait_for(state="visible", timeout=10000)
        impersonation_link = row.locator("a[title*='Login'], a:has(.fa-sign-in), a.loginAsUser, td:nth-child(10) > a").first
        impersonation_link.click()

    def login_as_client(self, client_identifier: str) -> Page:
        """Clicks impersonation icon for target client and returns the newly spawned client session Page popup."""
        row = self.get_client_row(client_identifier)
        row.wait_for(state="visible", timeout=10000)
        login_icon = row.locator("a[title*='Login'], a:has(.fa-sign-in), a.loginAsUser, td:nth-child(10) > a").first

        with self.page.expect_popup() as popup_info:
            login_icon.click()
            if self.impersonate_proceed_btn.is_visible(timeout=3000):
                self.impersonate_proceed_btn.click()

        client_page = popup_info.value
        client_page.wait_for_load_state("networkidle")
        return client_page

    # --------------------------------------------------------------------------
    # Ticket 2029: Bulk Reseller PDF Downloads & Pagination Methods
    # --------------------------------------------------------------------------
    def open_bulk_download_modal(self) -> None:
        """Opens the 'Download All Reports' bulk ZIP generation dialog."""
        self.download_all_reports_btn.first.wait_for(state="visible", timeout=10000)
        self.download_all_reports_btn.first.click()
        expect(self.bulk_download_modal.first).to_be_visible(timeout=8000)

    def configure_bulk_download_options(
        self,
        month: str,
        year: str,
        paginate_by_employee: bool = True,
        all_companies: bool = True
    ) -> None:
        """
        Configures reporting month/year, pagination option, and company scope inside bulk download modal.
        :param month: E.g., '08' or '8' or 'August'
        :param year: E.g., '2026'
        """
        if not self.bulk_download_modal.first.is_visible(timeout=2000):
            self.open_bulk_download_modal()

        # 1. Toggle 'Paginate by Employee' option ("Start each employee's report on a separate page")
        if paginate_by_employee:
            chk = self.paginate_by_employee_chk.first
            if chk.is_visible(timeout=3000):
                chk.click()
                logger_msg = "Enabled 'Paginate by Employee' option."

        # 2. Scope companies selection
        if all_companies and self.company_scope_all_radio.first.is_visible(timeout=2000):
            self.company_scope_all_radio.first.click()
        elif not all_companies and self.company_scope_selected_radio.first.is_visible(timeout=2000):
            self.company_scope_selected_radio.first.click()

        # 3. Format & fill reporting month input (YYYY-MM)
        clean_month = month.zfill(2) if month.isdigit() else "08"
        month_val = f"{year}-{clean_month}"
        if self.reporting_month_input.first.is_visible(timeout=3000):
            self.reporting_month_input.first.fill(month_val)

    def download_bulk_monthly_archive(
        self,
        month: str = "08",
        year: str = "2026",
        paginate_by_employee: bool = True,
        reporting_period: Optional[str] = None,
        timeout_ms: int = 60000
    ) -> Download:
        """
        Executes complete bulk ZIP download flow:
        1. Opens bulk download modal.
        2. Configures target month, year, and 'Paginate by Employee' setting.
        3. Clicks 'Generate Reports'.
        4. Waits for background generation completion.
        5. Intercepts and returns Playwright Download payload via expect_download().
        """
        if reporting_period:
            parts = reporting_period.split("-")
            if len(parts) == 2:
                year, month = parts[0], parts[1]

        self.configure_bulk_download_options(
            month=month,
            year=year,
            paginate_by_employee=paginate_by_employee,
            all_companies=True
        )

        # Trigger background report generation
        self.generate_reports_btn.first.click()

        # Wait for ZIP ready link/banner to appear
        self.download_zip_link.first.wait_for(state="visible", timeout=timeout_ms)

        # Intercept download stream
        with self.page.expect_download(timeout=timeout_ms) as download_info:
            self.download_zip_link.first.click()

        download_payload = download_info.value

        # Clean up modal container if close button is present
        if self.modal_close_btn.first.is_visible(timeout=2000):
            self.modal_close_btn.first.click()

        return download_payload
