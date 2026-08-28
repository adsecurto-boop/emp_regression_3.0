"""
Module: auto_email_reports_page.py
Layer: Layer 4 (L4) - Web Dashboard Automation
Ticket: Ticket 2025 - Auto Email Reports & Permissions
"""

import re
from typing import List, Optional
from playwright.sync_api import Page, Locator, expect
from config.settings import BASE_URL
from src.pages.base_page import BasePage


class AutoEmailReportsPage(BasePage):
    """
    Page Object Model for the Auto Email Reports Beta panel.
    Encapsulates schedule creation, target role selection, Silah PDF report format options,
    and report template naming convention configurations.
    """

    def __init__(self, page: Page, base_url: str = BASE_URL):
        super().__init__(page)
        self.base_url = base_url

        # Navigation Locators
        self.reports_menu = page.locator("a:has-text('Reports')")
        self.nav_reports = self.reports_menu
        self.auto_email_reports_beta_link = page.locator("a[href*='auto-email-report'], a:has-text('Auto Email Reports')")
        self.nav_auto_email_reports = self.auto_email_reports_beta_link

        # Action Triggers & Modal Containers
        self.create_new_reports_button = page.locator("button:has-text('Create New Reports'), #createNewReportBtn, #createReportBtn")
        self.btn_create_new_report = self.create_new_reports_button
        self.modal_container = page.locator("#reportModal, .modal-dialog, div.modal.show")
        self.btn_modal_close = page.locator("button[aria-label='Close'], button.close, button:has-text('x')")

        # Form Controls
        self.role_select = page.locator("select[name*='role'], #roleSelect, select#role_id")
        self.dropdown_role_select = self.role_select
        self.timeline_pdf_cb = page.locator("tr, div, label").filter(has_text="Timeline (Silah PDF)").locator("input[type='checkbox']")
        self.checkbox_timeline_silah = self.timeline_pdf_cb
        self.task_pdf_cb = page.locator("tr, div, label").filter(has_text="Task (Silah PDF)").locator("input[type='checkbox']")
        self.checkbox_task_silah = self.task_pdf_cb
        self.naming_convention_input = page.locator("input[name*='template_name'], input[placeholder*='Template Name'], input[name*='report_name'], input[placeholder*='Report Name'], #naming_convention, input#template_name")
        self.input_template_name = self.naming_convention_input

        # Submit & Action Controls
        self.save_button = page.locator("button:has-text('Save'), input[type='submit'][value='Save']")
        self.btn_save_report = self.save_button
        self.confirm_ok_button = page.locator("button:has-text('OK'), .swal2-confirm")
        self.btn_confirm_ok = self.confirm_ok_button
        self.reports_table_rows = page.locator("table#reportsTable tbody tr, tbody tr, div[role='row']")

    def navigate_to_auto_reports(self) -> None:
        """Navigates from root to the Auto Email Reports Beta panel."""
        if self.reports_menu.is_visible(timeout=3000):
            self.reports_menu.click()
        self.auto_email_reports_beta_link.click()
        self.page.wait_for_load_state("networkidle")

    def navigate(self, path_or_url: str = "") -> None:
        """Alias navigation method."""
        if path_or_url:
            super().navigate(path_or_url)
        else:
            self.navigate_to_auto_reports()

    def open_create_report_dialog(self) -> None:
        """Clicks the button to open the Create New Reports configuration dialog."""
        self.btn_create_new_report.wait_for(state="visible", timeout=10000)
        self.btn_create_new_report.click()
        self.modal_container.wait_for(state="visible", timeout=8000)

    def create_monthly_auto_email_schedule(self, role_name: str, naming_template: str) -> None:
        """
        Clicks Create New Report, selects target role, enables both Timeline & Task Silah PDFs,
        applies the naming convention syntax, and saves configuration.
        """
        if not self.modal_container.is_visible(timeout=2000):
            self.open_create_report_dialog()

        # Select role (e.g., 'Company Manager')
        if self.role_select.is_visible(timeout=3000):
            self.role_select.select_option(label=role_name)

        # Select target Silah PDF formats
        if not self.timeline_pdf_cb.is_checked():
            self.timeline_pdf_cb.check()
        if not self.task_pdf_cb.is_checked():
            self.task_pdf_cb.check()

        # Fill custom naming syntax: [Company Name] – Monthly Report – [Month] [Year]
        self.naming_convention_input.fill(naming_template)

        # Save and verify
        self.save_button.click()
        expect(self.confirm_ok_button).to_be_visible(timeout=8000)
        self.confirm_ok_button.click()
        self.page.wait_for_load_state("networkidle")

    def configure_silah_pdf_report(
        self,
        template_name: str,
        target_role: str = "Company Manager",
        include_timeline: bool = True,
        include_task: bool = True,
    ) -> None:
        """
        Selects the specified role, configures Timeline & Task Silah PDF options, and sets template naming.
        """
        if not self.modal_container.is_visible(timeout=2000):
            self.open_create_report_dialog()

        if self.dropdown_role_select.is_visible(timeout=3000):
            self.dropdown_role_select.select_option(label=target_role)

        if self.input_template_name.is_visible(timeout=3000):
            self.input_template_name.fill(template_name)

        if include_timeline:
            if not self.checkbox_timeline_silah.is_checked():
                self.checkbox_timeline_silah.check()
        else:
            if self.checkbox_timeline_silah.is_checked():
                self.checkbox_timeline_silah.uncheck()

        if include_task:
            if not self.checkbox_task_silah.is_checked():
                self.checkbox_task_silah.check()
        else:
            if self.checkbox_task_silah.is_checked():
                self.checkbox_task_silah.uncheck()

    def save_report_configuration(self) -> None:
        """Submits the form and confirms the alert dialog."""
        self.btn_save_report.click()
        if self.btn_confirm_ok.is_visible(timeout=5000):
            self.btn_confirm_ok.click()
        self.page.wait_for_load_state("networkidle")

    def verify_report_exists(self, template_name: str) -> bool:
        """Verifies if the specified template is present in the reports grid."""
        target_row = self.reports_table_rows.filter(has_text=template_name)
        return target_row.count() > 0
