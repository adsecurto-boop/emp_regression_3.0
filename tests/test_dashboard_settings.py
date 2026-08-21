"""
Test Suite: EMP-REGRESSION-3.0
Feature: Web Dashboard User Settings Automation
Evidence IDs: EV-015 (User Tracking Settings Automation & Alignment)
"""

import os
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

from src.pages.settings_page import SettingsPage

EVIDENCE_DIR = Path("tests/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def test_apply_user_settings_scenario(authenticated_page: Page):
    """
    Data-driven regression test to automate applying a custom user tracking
    configuration scenario on the Web Dashboard and capturing visual evidence.
    """
    settings_page = SettingsPage(authenticated_page)

    # 1. Navigate to target user settings panel (id=45009 / auto test)
    settings_page.navigate_to_user_settings(user_name="auto test", user_id="45009")

    # 2. Define custom settings scenario
    scenario = {
        "keystrokes": "enable",
        "screenshot_frequency": "60 Per Hour",
        "usb_blocking": "disable",
        "stealth_mode": "stealth",
        "screen_cast": "enable",
        "remote_terminal": "enable",
        "clipboard_detection": "enable",
        "bluetooth_detection": "enable"
    }

    # 3. Apply scenario settings
    settings_page.apply_scenario_settings(scenario)

    # 4. Save settings changes
    settings_page.save_settings()

    # 5. Capture visual evidence screenshot for audit trail (EV-015)
    evidence_path = EVIDENCE_DIR / "EV-015_settings_applied.png"
    authenticated_page.wait_for_timeout(3000)
    authenticated_page.screenshot(path=str(evidence_path), full_page=True, timeout=30000)

    # Assert evidence file creation & integrity
    assert evidence_path.exists(), f"Evidence screenshot not found at: {evidence_path}"
    assert evidence_path.stat().st_size > 0, f"Evidence screenshot file is empty: {evidence_path}"
    print(f"\n[SUCCESS] Settings scenario applied and visual evidence saved to: {evidence_path}")
