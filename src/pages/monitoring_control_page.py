"""
Module: monitoring_control_page.py
Layer: Layer 4 (L4) - Web Dashboard Automation
Ticket: Ticket 2028 - Auto Checkout & Permissions
"""

import re
from typing import Optional
from playwright.sync_api import Page, Locator, expect
from config.settings import BASE_URL
from src.pages.base_page import BasePage


class MonitoringControlPage(BasePage):
    """
    Page Object Model for the Monitoring Control settings panel.
    Encapsulates group policy modal triggers, tracking feature toggles (Auto Checkout & Idle Thresholds),
    and role-based accessibility assertions.
    """

    def __init__(self, page: Page, base_url: str = BASE_URL):
        super().__init__(page)
        self.base_url = base_url

        # Navigation Controls
        self.settings_nav_link = page.locator("a:has-text('Settings')")
        self.nav_settings = self.settings_nav_link
        self.monitoring_control_link = page.locator("a[href*='monitoring-control'], a:has-text('Monitoring Control')")
        self.nav_monitoring_control = self.monitoring_control_link

        # Group Settings & Policy Modal Controls
        self.default_settings_row = page.locator("tr:has-text('Default Settings'), tr#0, tr[data-id='0']")
        self.group_settings_button = self.default_settings_row.locator("a[title='Group Settings'], i.fa-cog")
        self.group_settings_btn = lambda group_id="0": page.locator(f"[id='{group_id}'], tr#0, tr[data-id='{group_id}']").get_by_title("Group Settings")

        # Sections & Accordions
        self.tracking_features_section = page.locator("#TrackingFeatures, a:has-text('Tracking Features')")
        self.tab_tracking_features = self.tracking_features_section
        self.tracking_card_body = page.locator("#TrackingFeatures > .card-body, #TrackingFeatures")

        # Feature Control Locators (Auto Check-out & Idle Minutes)
        self.auto_checkout_row = page.locator("tr:has-text('Auto Check-out')")
        self.auto_checkout_radio = self.auto_checkout_row.locator("input[type='radio'], .form-check-label")
        self.idle_threshold_input = page.locator("input#inactive_threshold_minutes, input[name='idle_time'], input[name*='threshold']")
        self.feature_row = lambda feature_name: page.locator(f"tr:has-text('{feature_name}')")

        # Action Buttons
        self.save_button = page.locator("button:has-text('Save'), input[value='Save'], input[type='submit'][value='Save']")
        self.confirm_ok_button = page.locator("button:has-text('OK'), .swal2-confirm, button.confirm")

    def navigate_to_monitoring_control(self) -> None:
        """Navigates from Settings root to Monitoring Control panel."""
        if self.settings_nav_link.is_visible(timeout=3000):
            self.settings_nav_link.click()
        self.monitoring_control_link.click()
        self.page.wait_for_load_state("networkidle")

    def navigate(self, path_or_url: str = "") -> None:
        """Alias navigation method."""
        if path_or_url:
            super().navigate(path_or_url)
        else:
            self.navigate_to_monitoring_control()

    def open_default_group_settings(self) -> None:
        """Opens the main group/global default settings modal."""
        self.group_settings_button.click()
        self.page.wait_for_load_state("networkidle")

    def open_group_settings(self, group_id: str = "0") -> None:
        """Opens the Group Settings configuration modal for a given group ID."""
        settings_button = self.group_settings_btn(group_id).first
        settings_button.wait_for(state="visible", timeout=10000)
        settings_button.click()
        self.page.wait_for_load_state("networkidle")

    def configure_auto_checkout(self, enable: bool, idle_minutes: int = 5) -> None:
        """
        Expands tracking features and configures the idle checkout state and threshold minutes.
        """
        if self.tracking_features_section.is_visible(timeout=3000):
            self.tracking_features_section.click()

        if enable:
            self.auto_checkout_radio.first.click()
            if self.idle_threshold_input.first.is_visible(timeout=3000):
                self.idle_threshold_input.first.fill(str(idle_minutes))
        else:
            self.auto_checkout_radio.last.click()

        self.save_button.first.click()
        expect(self.confirm_ok_button).to_be_visible(timeout=8000)
        self.confirm_ok_button.click()
        self.page.wait_for_load_state("networkidle")

    def toggle_tracking_feature(
        self,
        feature_name: str = "Auto Check-out",
        enable: bool = True,
        threshold_minutes: Optional[int] = None
    ) -> None:
        """
        Expands the Tracking Features section and configures toggle state and optional threshold.
        """
        if self.tab_tracking_features.is_visible(timeout=3000):
            self.tab_tracking_features.click()

        row = self.feature_row(feature_name).first
        row.wait_for(state="visible", timeout=8000)

        option_idx = 0 if enable else 1
        toggle_radio = row.locator(".form-check-label, input[type='radio']").nth(option_idx)
        toggle_radio.click()

        if threshold_minutes is not None:
            threshold_input = row.locator("input[type='number'], input[name*='time'], input[name*='threshold'], input#inactive_threshold_minutes").first
            if threshold_input.is_visible(timeout=3000):
                threshold_input.fill(str(threshold_minutes))

    def save_changes(self) -> None:
        """Saves active modal changes and confirms modal alert."""
        self.save_button.first.click()
        expect(self.confirm_ok_button).to_be_visible(timeout=8000)
        self.confirm_ok_button.click()
        self.page.wait_for_load_state("networkidle")

    def verify_monitoring_control_accessibility(self, should_be_editable: bool) -> None:
        """Asserts whether the settings elements can be altered by the current logged-in role."""
        if should_be_editable:
            expect(self.group_settings_button.first).to_be_enabled()
        else:
            expect(self.group_settings_button.first).to_be_hidden()
