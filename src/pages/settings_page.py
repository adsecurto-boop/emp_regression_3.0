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

    # Website & Application Blocking Locators
    WEBSITES_ENABLE = "input[name='WebsiteOption']"
    WEBSITES_ADV_MODAL = "#Websites_adv"
    ADVANCE_SAVE_BUTTON = "#AdvanceSaveButton"

    # Dropdowns & Radios
    SS_FREQUENCY_SELECT = "#SSFrequencySelected"
    VIDEO_QUALITY_SELECT = "#videoQuality"
    STEALTH_RADIO_VISIBLE = "#visable, input[name='EmpIcon'][value='true']"
    STEALTH_RADIO_STEALTH = "#stealth, input[name='EmpIcon'][value='false']"

    # Action Buttons
    SAVE_BUTTON = "button:has-text('Save'), input[value='Save'], .btn-primary:has-text('Save')"
    OK_CONFIRM_BUTTON = "button:has-text('OK'), button:has-text('Yes'), .swal-button--confirm"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate_to_user_settings(self, user_name: str = "auto test", user_id: str = "237232") -> None:
        """
        Navigates directly to the user's tracking settings page (or via Employee Details search).
        """
        from config.settings import BASE_URL, LOGIN_URL
        logger.info(f"Navigating to User Settings for '{user_name}' (id={user_id})...")

        # 1. Try direct track-user-setting URL first
        target_url = f"{BASE_URL}/admin/track-user-setting?id={user_id}"
        self.page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(2000)

        # Check if already on the user settings page (has #visable / #stealth or #KeyStrokeRadio1)
        if self.page.locator("#visable, #stealth, #KeyStrokeRadio1, input[name='EmpIcon']").count() > 0:
            logger.info("Direct Settings URL loaded successfully.")
            return

        # 2. Ensure authenticated session if redirected to login
        user_field = self.page.get_by_role("textbox", name="Username/Email")
        if user_field.count() > 0 and user_field.is_visible():
            logger.info("Session unauthenticated. Logging in...")
            from src.utils.auth_helper import get_dashboard_credentials
            u, p = get_dashboard_credentials(prompt_if_missing=False)
            if u and p:
                user_field.fill(u)
                self.page.get_by_role("textbox", name="Password").fill(p)
                self.page.get_by_role("button", name="Login").click()
                self.page.wait_for_timeout(5000)
                try:
                    self.page.context.storage_state(path="playwright-profile/auth.json")
                except Exception:
                    pass

        # Try direct URL again after authenticating
        self.page.goto(target_url, wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(2000)
        if self.page.locator("#visable, #stealth, #KeyStrokeRadio1, input[name='EmpIcon']").count() > 0:
            logger.info("Direct Settings URL loaded successfully after auth.")
            return

        # 3. Fallback: Search user via Employee Details UI
        logger.info("Direct URL not available. Navigating via Employee Details...")
        self.page.goto(f"{BASE_URL}/employee/employee-details", wait_until="domcontentloaded", timeout=60000)
        self.page.wait_for_timeout(3000)

        close_btn = self.page.get_by_role("button", name="×")
        if close_btn.count() > 0 and close_btn.first.is_visible():
            try:
                close_btn.first.click()
                self.page.wait_for_timeout(1000)
            except Exception:
                pass

        search_box = self.page.locator("#search, #Search, input.search-field, input[placeholder*='Search']").first
        if search_box.count() > 0:
            search_box.fill(user_name)
            search_btn = self.page.locator("#SearchButton, button.search-btn, .search-btn, button:has-text('Search')").first
            if search_btn.count() > 0 and search_btn.is_visible():
                search_btn.click()
            else:
                search_box.press("Enter")
            self.page.wait_for_timeout(3000)

        user_link = self.page.locator(f"a:has-text('{user_name}'), td:has-text('{user_name}') a, #td{user_id} a").first
        if user_link.count() > 0:
            user_link.click()
            self.page.wait_for_timeout(3000)

        settings_btn = self.page.locator("a[href*='track-user-setting'], a.btn:has-text('Settings'), a.btn-link:has-text('Settings')").first
        if settings_btn.count() > 0:
            settings_btn.click()
            self.page.wait_for_timeout(3000)

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
        Returns "Visible" if the Visible radio button (#visable / EmpIcon=true) is checked,
        or "Stealth" if the Stealth radio button (#stealth / EmpIcon=false) is checked.
        """
        try:
            # Wait for settings elements to be attached/visible
            try:
                self.page.wait_for_selector("#visable, #stealth, input[name='EmpIcon']", state="attached", timeout=10000)
            except Exception:
                pass

            # 1. Primary check: EmpIcon radio inputs (#visable and #stealth)
            vis_input = self.page.locator("#visable, input[name='EmpIcon'][value='true']").first
            if vis_input.count() > 0 and vis_input.is_checked():
                return "Visible"

            stealth_input = self.page.locator("#stealth, input[name='EmpIcon'][value='false']").first
            if stealth_input.count() > 0 and stealth_input.is_checked():
                return "Stealth"

            # 2. Check by role or label text
            visible_radio = self.page.get_by_role("radio", name="Visible")
            if visible_radio.count() > 0 and visible_radio.is_checked():
                return "Visible"

            stealth_radio = self.page.get_by_role("radio", name="Stealth")
            if stealth_radio.count() > 0 and stealth_radio.is_checked():
                return "Stealth"

            # 3. Fallback check using element attributes
            fallback_visible = self.page.locator(self.STEALTH_RADIO_VISIBLE).first
            if fallback_visible.count() > 0 and fallback_visible.is_checked():
                return "Visible"

            fallback_stealth = self.page.locator(self.STEALTH_RADIO_STEALTH).first
            if fallback_stealth.count() > 0 and fallback_stealth.is_checked():
                return "Stealth"
        except Exception as e:
            logger.warning(f"Could not extract visibility mode: {e}")

        return "Unknown"

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

    def enable_web_used(self) -> None:
        """Enables the Web Used monitoring option."""
        logger.info("Enabling Web Used monitoring option...")
        try:
            web_checkbox = self.page.locator(self.WEBSITES_ENABLE).first
            if web_checkbox.count() > 0 and not web_checkbox.is_checked():
                web_checkbox.check()
        except Exception as e:
            logger.warning(f"Could not enable Web Used option directly: {e}")

    def open_websites_advanced_settings(self) -> None:
        """Opens the Advanced Settings modal for Web Used / Website Blocking (#Websites_adv)."""
        logger.info("Opening Websites Advanced Settings modal (#Websites_adv)...")
        adv_btn = self.page.locator(
            "tr:has-text('Web Used') button:has-text('Advanced Settings'), "
            "button[data-target='#Websites_adv'], "
            "button[data-bs-target='#Websites_adv'], "
            "button[onclick*='Websites_adv']"
        ).first
        if adv_btn.count() > 0 and adv_btn.is_visible():
            adv_btn.click()
        else:
            all_adv_buttons = self.page.get_by_role("button", name="Advanced Settings")
            if all_adv_buttons.count() >= 3:
                all_adv_buttons.nth(2).click()
            elif all_adv_buttons.count() > 0:
                all_adv_buttons.first.click()

        self.page.locator(self.WEBSITES_ADV_MODAL).wait_for(state="visible", timeout=10000)

    def configure_website_blocking(
        self,
        domains: list,
        clear_existing: bool = True
    ) -> None:
        """
        Configures blocked website domains in the #Websites_adv modal.
        """
        logger.info(f"Configuring blocked website domains: {domains}")
        modal = self.page.locator(self.WEBSITES_ADV_MODAL).first
        modal.wait_for(state="visible", timeout=10000)

        web_group = modal.locator(".form-group:has(#userTrackBlockingWebsite), .form-group:has-text('Blocking Websites')").first

        # Clear existing items in website blocking section if requested
        if clear_existing and web_group.count() > 0:
            remove_icons = web_group.locator(".select2-search-choice-close, .select2-selection__choice__remove, span:has-text('×')")
            for _ in range(remove_icons.count()):
                try:
                    if remove_icons.first.is_visible():
                        remove_icons.first.click()
                        self.page.wait_for_timeout(300)
                except Exception:
                    break

        # Add target domains
        for domain in domains:
            logger.info(f"Adding domain to blocklist: {domain}")
            searchbox = web_group.locator(
                "input.select2-search__field, input[type='search'], input[role='searchbox'], input.select2-input"
            ).first
            if searchbox.count() == 0 or not searchbox.is_visible():
                searchbox = modal.locator("input.select2-search__field").first

            searchbox.click()
            searchbox.fill(domain)
            self.page.wait_for_timeout(500)

            option = self.page.get_by_role("option", name=domain).first
            if option.count() > 0 and option.is_visible():
                option.click()
            else:
                searchbox.press("Enter")
            self.page.wait_for_timeout(500)

    def configure_application_blocking(
        self,
        applications: list,
        clear_existing: bool = True
    ) -> None:
        """
        Configures blocked applications (e.g. ['notepad.exe', 'chrome.exe']) in the #Websites_adv modal.
        Uses the exact selectors for the Blocking Applications select2 field (#userTrackBlockingApplciation).
        """
        logger.info(f"Configuring blocked applications: {applications}")
        modal = self.page.locator(self.WEBSITES_ADV_MODAL).first
        modal.wait_for(state="visible", timeout=10000)

        app_group = modal.locator(".form-group:has(#userTrackBlockingApplciation), .form-group:has-text('Blocking Applications')").first

        # Clear existing items in application blocking section if requested
        if clear_existing and app_group.count() > 0:
            remove_icons = app_group.locator(".select2-search-choice-close, .select2-selection__choice__remove, span:has-text('×')")
            for _ in range(remove_icons.count()):
                try:
                    if remove_icons.first.is_visible():
                        remove_icons.first.click()
                        self.page.wait_for_timeout(300)
                except Exception:
                    break

        # Add target application filenames (e.g. chrome.exe, notepad.exe)
        for app in applications:
            logger.info(f"Adding application to blocklist: {app}")
            searchbox = app_group.locator(
                "input.select2-search__field, input[type='search'], input[role='searchbox'], input.select2-input"
            ).first
            if searchbox.count() == 0 or not searchbox.is_visible():
                searchbox = modal.locator("input.select2-search__field").nth(1)

            searchbox.click()
            searchbox.fill(app)
            self.page.wait_for_timeout(500)

            option = self.page.get_by_role("option", name=app).first
            if option.count() > 0 and option.is_visible():
                option.click()
            else:
                searchbox.press("Enter")
            self.page.wait_for_timeout(500)

    def save_advanced_settings(self) -> None:
        """Saves and closes the Advanced Settings modal."""
        logger.info("Saving Advanced Settings modal (#AdvanceSaveButton)...")
        adv_save = self.page.locator(self.ADVANCE_SAVE_BUTTON).first
        if adv_save.count() > 0 and adv_save.is_visible():
            adv_save.click()
            self.page.wait_for_timeout(1000)

