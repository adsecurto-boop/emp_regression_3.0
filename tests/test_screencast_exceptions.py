"""
Test Suite: EMP-REGRESSION-3.0
Feature: Screencast Offline & Disconnected Agent Exception Fallback
Evidence Mapping: EV-013 (Dashboard Navigation), EV-014 (Offline Screencast Fallback & Remote Command Tools)
"""

import logging
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

from src.pages.screencast_page import ScreencastPage

logger = logging.getLogger("TestScreencastExceptions")
EVIDENCE_DIR = Path("tests/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def test_offline_screencast_fallback(authenticated_page: Page):
    """
    Negative / Exception Regression Test validating platform handling of offline workstations:
    1. Direct navigation to the authenticated admin dashboard.
    2. Routing to 'Currently Offline' monitoring grid and selecting target user ('Shivam Purohit').
    3. Asserting offline fallback canvas rendering (#canvas-img-default).
    4. Validating remote management tools aria-snapshot layout integrity.
    5. Safe interaction testing for Disconnect / Connect socket toggles without unhandled exceptions.
    6. Capturing visual audit proof saved to 'tests/evidence/EV-014_screencast_offline_fallback.png'.
    """
    screencast_page = ScreencastPage(authenticated_page)

    # 1. Navigate to target offline user workstation ("Shivam Purohit")
    logger.info("=== STEP 1: Navigate to Offline User Workstation ===")
    screencast_page.navigate_to_user_screencast(username="Shivam Purohit", expect_online=False)

    # 2. Verify offline screencast telemetry & remote command palette
    logger.info("=== STEP 2: Verify Offline Telemetry & Fallback Canvas ===")
    telemetry_metrics = screencast_page.verify_screencast_telemetry(expect_online=False)
    logger.info(f"Telemetry Verification Metrics: {telemetry_metrics}")

    # 3. Evidence Gathering: Capture offline workstation layout
    logger.info("=== STEP 3: Capturing Offline Fallback Evidence (EV-014) ===")
    evidence_path = EVIDENCE_DIR / "EV-014_screencast_offline_fallback.png"
    authenticated_page.wait_for_timeout(3000)
    authenticated_page.screenshot(path=str(evidence_path), full_page=True, timeout=30000)

    # Assert evidence file creation & integrity
    assert evidence_path.exists(), f"Evidence screenshot not found at: {evidence_path}"
    assert evidence_path.stat().st_size > 0, f"Evidence screenshot file is empty: {evidence_path}"
    logger.info(f"[SUCCESS] Offline screencast fallback validated! Evidence saved to: {evidence_path}")
