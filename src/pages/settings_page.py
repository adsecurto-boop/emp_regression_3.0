"""
Module: src/pages/settings_page.py
Purpose: Page Object Model for EmpMonitor User Tracking Settings Page.
Evidence Mapping: EV-015 (User Tracking Settings Automation & Alignment)
"""

import logging
from typing import Dict, Any, Optional
from playwright.sync_api import Page, expect

from src.pages.base_page import BasePage

logger = logging.getLogger("SettingsPage")


class SettingsPage(BasePage):
    """
    Page Object Model encapsulating the User Settings Panel on EmpMonitor Web Dashboard.
    """

    # --- Selectors ---
    SEARCH_INPUT = "#search, input.search-field, input[placeholder*='Search']"
    SEARCH_BUTTON = "button.search-btn, .search-btn"
    USER_LINK_TEMPLATE = "a:has-text('{name}'), td:has-text('{name}')"
    SETTINGS_LINK = "a:has-text('Settings'), [href*='track-user-setting']"
    
    # Feature Toggle Locators
    KEYSTROKES_ENABLE = "#KeyStrokeRadio1"
    KEYSTROKES_DISABLE = "#KeyStrokeRadio0"
    
    EMAIL_MONITORING_ENABLE = "#EmailMonitoringRadio1"
    EMAIL_MONITORING_DISABLE = "#EmailMonitoringRadio0"
    
    USB_BLOCKING_ENABLE = "#usb_enable"
    USB_BLOCKING_DISABLE = "#usb_disable"
    
    SCREEN_CAST_ENABLE = "#ScreenCast1"
    SCREEN_CAST_DISABLE = "#ScreenCast0"
    
    REMOTE_TERMINAL_ENABLE = "#remoteTerminalOption1"
    REMOTE_TERMINAL_DISABLE = "#remoteTerminalOption0"
    
    BLUETOOTH_DETECTION_ENABLE = "#bluetooth_detection_enable"
    BLUETOOTH_DETECTION_DISABLE = "#bluetooth_detection_disable"
    
    BLUETOOTH_BLOCKING_ENABLE = "#bluetooth_block_enable"
    BLUETOOTH_BLOCKING_DISABLE = "#bluetooth_block_disable"
    
    CLIPBOARD_DETECTION_ENABLE = "#clipboard_detection_enable"
    CLIPBOARD_DETECTION_DISABLE = "#clipboard_detection_disable"
    
    CLIPBOARD_BLOCKING_ENABLE = "#clipboard_block_enable"
    CLIPBOARD_BLOCKING_DISABLE = "#clipboard_block_disable"
    
    FILE_UPLOAD_BLOCKING_ENABLE = "#fileUploadBlocking1"
    FILE_UPLOAD_BLOCKING_DISABLE = "#fileUploadBlocking0"
    
    PRINT_BLOCKING_ENABLE = "#printBlocking1"
    PRINT_BLOCKING_DISABLE = "#printBlocking0"
    
    PRINT_DETECTION_ENABLE = "#printDetection1"
    PRINT_DETECTION_DISABLE = "#printDetection0"
    
    MANUAL_CLOCK_IN_ENABLE = "#manual_clock_in"
    MANUAL_CLOCK_OUT_ENABLE = "#manual_clock_out"
    
    ATTENDANCE_OVERRIDE_IN = "#attendance_in"
    ATTENDANCE_OVERRIDE_OUT = "#attendance_out"
    
    SYSTEM_LOCK_ENABLE = "#system_lock_enable"
    SYSTEM_LOCK_DISABLE = "#system_lock_disable"
    
    GEO_LOCATION_LOGS_ENABLE = "#mobile_data_enable"
    GEO_LOCATION_LOGS_DISABLE = "#mobile_data_disable"
    
    AUTO_CHECKOUT_ENABLE = "#autoCheckOut1"
    AUTO_CHECKOUT_DISABLE = "#autoCheckOut0"

    # Dropdowns & Radios
    SS_FREQUENCY_SELECT = "#SSFrequencySelected"
    VIDEO_QUALITY_SELECT = "#videoQuality"
    STEALTH_RADIO_VISIBLE = "input[name='systemVisibility'][value='1'], input[type='radio'][value='1']"
    STEALTH_RADIO_STEALTH = "input[name='systemVisibility'][value='0'], input[type='radio'][value='0']"

    # Action Buttons
    SAVE_BUTTON = "button:has-text('Save'), input[value='Save'], .btn-primary:has-text('Save')"
    OK_CONFIRM_BUTTON = "button:has-text('OK'), button:has-text('Yes'), .swal-button--confirm"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate_to_user_settings(self, user_name: str = "auto test", user_id: str = "45009") -> None:
        """
        Navigates directly to the user's tracking settings page (or via Employee Details search).
        """
        from config.settings import BASE_URL
        target_url = f"{BASE_URL}/admin/track-user-setting?id={user_id}"
        logger.info(f"Navigating to User Settings page: {target_url}")
        self.page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        
        # Auto-heal session redirect if thrown back to login page
        try:
            if self.page.get_by_role("textbox", name="Username/Email").count() > 0 and self.page.get_by_role("textbox", name="Username/Email").is_visible():
                logger.info("Session expired. Auto-healing login state...")
                from src.utils.auth_helper import get_dashboard_credentials
                dash_user, dash_pass = get_dashboard_credentials(prompt_if_missing=True)
                if dash_user and dash_pass:
                    self.page.get_by_role("textbox", name="Username/Email").fill(dash_user)
                    self.page.get_by_role("textbox", name="Password").fill(dash_pass)
                    self.page.get_by_role("button", name="Login").click()
                    self.page.wait_for_load_state("networkidle")
                    self.page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            pass

        self.page.wait_for_timeout(2000)

    def set_keystrokes(self, state: str) -> None:
        """Set Keystroke Monitoring toggle (enable/disable)."""
        selector = self.KEYSTROKES_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.KEYSTROKES_DISABLE
        self.click_if_present(selector)

    def set_email_monitoring(self, state: str) -> None:
        """Set Email Monitoring toggle (enable/disable)."""
        selector = self.EMAIL_MONITORING_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.EMAIL_MONITORING_DISABLE
        self.click_if_present(selector)

    def set_usb_blocking(self, state: str) -> None:
        """Set USB Blocking toggle (enable/disable)."""
        selector = self.USB_BLOCKING_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.USB_BLOCKING_DISABLE
        self.click_if_present(selector)

    def set_screen_cast(self, state: str) -> None:
        """Set Screen Cast toggle (enable/disable)."""
        selector = self.SCREEN_CAST_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.SCREEN_CAST_DISABLE
        self.click_if_present(selector)

    def set_remote_terminal(self, state: str) -> None:
        """Set Remote Terminal Access toggle (enable/disable)."""
        selector = self.REMOTE_TERMINAL_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.REMOTE_TERMINAL_DISABLE
        self.click_if_present(selector)

    def set_bluetooth_detection(self, state: str) -> None:
        """Set Bluetooth Detection toggle (enable/disable)."""
        selector = self.BLUETOOTH_DETECTION_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.BLUETOOTH_DETECTION_DISABLE
        self.click_if_present(selector)

    def set_bluetooth_blocking(self, state: str) -> None:
        """Set Bluetooth Blocking toggle (enable/disable)."""
        selector = self.BLUETOOTH_BLOCKING_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.BLUETOOTH_BLOCKING_DISABLE
        self.click_if_present(selector)

    def set_clipboard_detection(self, state: str) -> None:
        """Set Clipboard Detection toggle (enable/disable)."""
        selector = self.CLIPBOARD_DETECTION_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.CLIPBOARD_DETECTION_DISABLE
        self.click_if_present(selector)

    def set_clipboard_blocking(self, state: str) -> None:
        """Set Clipboard Blocking toggle (enable/disable)."""
        selector = self.CLIPBOARD_BLOCKING_ENABLE if state.lower() in ["enable", "enabled", "1"] else self.CLIPBOARD_BLOCKING_DISABLE
        self.click_if_present(selector)

    def set_screenshot_frequency(self, frequency: str) -> None:
        """Set Screenshot Frequency dropdown (e.g., '60 Per Hour', '12 Per Hour', '30 Per Hour')."""
        try:
            select = self.page.locator(self.SS_FREQUENCY_SELECT).first
            if select.count() > 0 and select.is_visible():
                select.select_option(label=frequency) if any(c.isalpha() for c in frequency) else select.select_option(value=frequency)
        except Exception as e:
            logger.warning(f"Could not set screenshot frequency '{frequency}': {e}")

    def set_video_quality(self, quality_value: str) -> None:
        """Set Video Quality dropdown (e.g., '1', '2', '3')."""
        try:
            select = self.page.locator(self.VIDEO_QUALITY_SELECT).first
            if select.count() > 0 and select.is_visible():
                select.select_option(value=quality_value)
        except Exception as e:
            logger.warning(f"Could not set video quality '{quality_value}': {e}")

    def set_stealth_mode(self, mode: str) -> None:
        """Set agent mode ('stealth' vs 'visible')."""
        if mode.lower() in ["stealth", "hidden", "0"]:
            self.click_if_present(self.STEALTH_RADIO_STEALTH)
        else:
            self.click_if_present(self.STEALTH_RADIO_VISIBLE)

    def get_active_visibility_mode(self) -> str:
        """
        Detects the active Visibility Mode on the Web Dashboard settings page.
        Returns "Visible" if the Visible radio button is checked, or "Stealth" if the Stealth radio button is checked.
        """
        try:
            visible_radio = self.page.get_by_role("radio", name="Visible")
            if visible_radio.count() > 0 and visible_radio.is_checked():
                return "Visible"

            stealth_radio = self.page.get_by_role("radio", name="Stealth")
            if stealth_radio.count() > 0 and stealth_radio.is_checked():
                return "Stealth"

            # Fallback check using element attributes
            fallback_visible = self.page.locator(self.STEALTH_RADIO_VISIBLE).first
            if fallback_visible.count() > 0 and fallback_visible.is_checked():
                return "Visible"

            fallback_stealth = self.page.locator(self.STEALTH_RADIO_STEALTH).first
            if fallback_stealth.count() > 0 and fallback_stealth.is_checked():
                return "Stealth"
        except Exception as e:
            logger.warning(f"Could not extract visibility mode: {e}")

        return "Stealth"

    def click_if_present(self, selector: str) -> None:
        """Safely clicks an element if present and visible."""
        try:
            elem = self.page.locator(selector).first
            if elem.count() > 0 and elem.is_visible():
                elem.check() if elem.get_attribute("type") in ["checkbox", "radio"] else elem.click()
        except Exception as e:
            logger.debug(f"Locator click skipped for '{selector}': {e}")

    def apply_scenario_settings(self, settings_dict: Dict[str, Any]) -> None:
        """
        Accepts a dictionary mapping feature names to target states and automates clicking controls.
        Example:
            {
                "keystrokes": "enable",
                "screenshot_frequency": "12 Per Hour",
                "usb_blocking": "disable",
                "stealth_mode": "stealth",
                "screen_cast": "enable",
                "remote_terminal": "enable"
            }
        """
        logger.info(f"Applying scenario settings: {settings_dict}")

        if "keystrokes" in settings_dict:
            self.set_keystrokes(settings_dict["keystrokes"])

        if "email_monitoring" in settings_dict:
            self.set_email_monitoring(settings_dict["email_monitoring"])

        if "usb_blocking" in settings_dict:
            self.set_usb_blocking(settings_dict["usb_blocking"])

        if "screen_cast" in settings_dict:
            self.set_screen_cast(settings_dict["screen_cast"])

        if "remote_terminal" in settings_dict:
            self.set_remote_terminal(settings_dict["remote_terminal"])

        if "bluetooth_detection" in settings_dict:
            self.set_bluetooth_detection(settings_dict["bluetooth_detection"])

        if "bluetooth_blocking" in settings_dict:
            self.set_bluetooth_blocking(settings_dict["bluetooth_blocking"])

        if "clipboard_detection" in settings_dict:
            self.set_clipboard_detection(settings_dict["clipboard_detection"])

        if "clipboard_blocking" in settings_dict:
            self.set_clipboard_blocking(settings_dict["clipboard_blocking"])

        if "screenshot_frequency" in settings_dict:
            self.set_screenshot_frequency(settings_dict["screenshot_frequency"])

        if "video_quality" in settings_dict:
            self.set_video_quality(settings_dict["video_quality"])

        if "stealth_mode" in settings_dict:
            self.set_stealth_mode(settings_dict["stealth_mode"])

    def save_settings(self) -> None:
        """Clicks the Save button and handles confirmation popups/alerts cleanly."""
        logger.info("Saving settings changes...")
        try:
            save_btn = self.page.locator(self.SAVE_BUTTON).first
            if save_btn.count() > 0 and save_btn.is_visible():
                save_btn.click()
                self.page.wait_for_timeout(2000)
                
                # Dismiss modal alerts or confirmation dialogs if shown
                try:
                    ok_btn = self.page.locator(self.OK_CONFIRM_BUTTON).first
                    if ok_btn.count() > 0 and ok_btn.is_visible():
                        ok_btn.click()
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
