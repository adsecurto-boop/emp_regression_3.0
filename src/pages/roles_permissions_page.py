"""
Module: roles_permissions_page.py
Layer: Layer 4 (L4) - Web Dashboard Automation
Ticket: Ticket 2028 - Auto Checkout & Permissions
"""

import re
from typing import Dict, List, Optional
from playwright.sync_api import Page, Locator, expect
from config.settings import BASE_URL
from src.pages.base_page import BasePage


class RolesPermissionsPage(BasePage):
    """
    Page Object Model for the Roles & Permissions management panel.
    Encapsulates role grid interactions, permission modal configurations, and snapshot audits.
    """

    def __init__(self, page: Page, base_url: str = BASE_URL):
        super().__init__(page)
        self.base_url = base_url

        # Navigation Controls
        self.nav_settings = page.locator("a:has-text('Settings')")
        self.nav_link = page.locator("a[href*='roles-permission'], a:has-text('Roles and Permission')")
        self.nav_roles_permissions = self.nav_link

        # Grid Controls & Dynamic Row Locators
        self.role_row = lambda role_name: page.locator(f"tr:has-text('{role_name}')")
        self.role_permission_btn = lambda role_id: page.locator(f"#role{role_id}").get_by_title("Permission Settings")
        self.role_view_btn = lambda role_id: page.locator(f"#role{role_id}").get_by_title("View")

        # Modal Containers
        self.modal_container = page.locator("#roleSet")
        self.permission_modal = self.modal_container
        self.view_display_modal = page.locator("#roledisplay")
        self.modal_close_button = page.locator("#roleSet button[aria-label='Close'], #roleSet .close")
        self.modal_close_btn = self.modal_close_button
        self.view_close_btn = page.locator("#roledisplay button:has-text('Close'), #roledisplay .close")

        # Save & Confirmation Action Controls
        self.save_button = page.locator("button:has-text('Save'), input[value='Save']")
        self.confirm_ok_button = page.locator("button:has-text('OK'), .swal2-confirm, button.confirm")

    def navigate(self, path_or_url: str = "") -> None:
        """Navigates to the Roles & Permissions management section."""
        if path_or_url:
            super().navigate(path_or_url)
        else:
            if self.nav_settings.is_visible(timeout=3000):
                self.nav_settings.click()
            self.nav_roles_permissions.click()
        self.page.wait_for_load_state("networkidle")

    def open_permission_modal(self, role_name: str) -> None:
        """Locates the row matching the role name and opens its permission settings modal."""
        row = self.role_row(role_name).first
        row.wait_for(state="visible", timeout=8000)
        row.locator("a[title='Permission Settings'], i.fa-cog").click()
        expect(self.modal_container).to_be_visible(timeout=8000)

    def open_permission_settings(self, role_id: str) -> None:
        """Opens permission settings modal for a specific numerical role ID (e.g., '566')."""
        btn = self.role_permission_btn(role_id)
        btn.wait_for(state="visible", timeout=8000)
        btn.click()
        expect(self.permission_modal).to_be_visible(timeout=8000)

    def toggle_section_permission(self, section_name: str, permission_type: str, enable: bool = True) -> None:
        """
        Expands a section accordion (e.g., 'Employee', 'Monitoring', 'Auto Checkout') inside the modal,
        and checks or unchecks the target permission action checkbox.
        :param permission_type: 'write', 'delete', 'view', or exact checkbox ID suffix.
        """
        section_trigger = self.modal_container.locator(f"a:has-text('{section_name}')").first
        if section_trigger.is_visible(timeout=3000):
            section_trigger.click()

        clean_type = permission_type.lstrip("#")
        if not clean_type.endswith("C"):
            clean_type = f"{clean_type}C"
            
        checkbox_id = f"#{clean_type}"
        checkbox = self.modal_container.locator(checkbox_id).first

        if not checkbox.is_visible(timeout=3000):
            checkbox = self.modal_container.locator(f"input[name*='{permission_type}'], label:has-text('{permission_type}')").first

        if enable and not checkbox.is_checked():
            checkbox.check()
        elif not enable and checkbox.is_checked():
            checkbox.uncheck()

    def configure_module_permissions(self, module_section_id: str, permissions: List[str]) -> None:
        """
        Expands a permission module (e.g., 'EmployeeSettings', 'DashboardSettings')
        and checks specified permissions (e.g., ['View', 'Modify', 'Create', 'Auto Checkout']).
        """
        module_tab = self.permission_modal.locator(f"#{module_section_id}").first
        if module_tab.is_visible(timeout=3000):
            module_tab.click()

        body_id = module_section_id.replace("Settings", "")
        module_body = self.permission_modal.locator(f"#{body_id}").first
        for perm in permissions:
            perm_locator = module_body.locator(f"label:has-text('{perm}'), input[value*='{perm}'], input[name*='{perm}']").first
            if perm_locator.is_visible(timeout=3000):
                perm_locator.click()

    def set_grid_role_checkboxes(self, role_name: str, read: bool = True, write: bool = False, delete: bool = False) -> None:
        """Directly toggles Read/Write/Delete checkboxes from the outer roles table grid."""
        row = self.role_row(role_name).first
        row.wait_for(state="visible", timeout=8000)

        if read:
            row.locator("#readC, input[name*='read']").first.check()
        if write:
            row.locator("#writeC, input[name*='write']").first.check()
        if delete:
            row.locator("#deleteC, input[name*='delete']").first.check()

    def commit_changes(self) -> None:
        """Saves active permission settings and confirms the alert modal."""
        self.save_button.first.click()
        expect(self.confirm_ok_button).to_be_visible(timeout=8000)
        self.confirm_ok_button.click()
        self.page.wait_for_load_state("networkidle")

    def save_permissions(self) -> None:
        """Alias method to commit active permission modal changes."""
        self.commit_changes()

    def verify_role_view_snapshot(self, role_id: str) -> str:
        """Opens the View modal for a role and retrieves formatted permissions text for snapshot auditing."""
        view_btn = self.role_view_btn(role_id)
        view_btn.click()
        expect(self.view_display_modal).to_be_visible(timeout=8000)
        summary_text = self.view_display_modal.inner_text()
        self.view_close_btn.first.click()
        return summary_text

    def toggle_client_auto_email_permission(self, role_id_or_name: str, enable: bool = True) -> None:
        """
        Opens the role's Permission Settings and toggles the 'Manage Client Auto-Email Reports' checkbox.
        """
        # 1. Open Permission Settings for the role
        if str(role_id_or_name).isdigit():
            self.open_permission_settings(str(role_id_or_name))
        else:
            self.open_permission_modal(str(role_id_or_name))

        # Expand the Auto Email Reports or Reseller settings accordion if present
        auto_email_section = self.permission_modal.locator(
            "#AutoEmailReportsSettings, a:has-text('Auto Email Reports'), #ResellerAccessSettings, a:has-text('Reports')"
        ).first
        if auto_email_section.is_visible(timeout=2000):
            auto_email_section.click()

        # 2. Toggle the Manage Client Auto-Email Reports permission checkbox
        permission_cb = self.permission_modal.locator(
            "label:has-text('Manage Client Auto-Email Reports'), "
            "label:has-text('Auto Email Reports') input[type='checkbox'], "
            "#autoEmailReportC, #autoEmailReportsC, input[name*='auto_email_report']"
        ).first

        if permission_cb.is_visible(timeout=3000):
            if enable and not permission_cb.is_checked():
                permission_cb.check()
            elif not enable and permission_cb.is_checked():
                permission_cb.uncheck()

        # 3. Commit changes
        self.commit_changes()

