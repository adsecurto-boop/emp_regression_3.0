"""
Test Suite: EMP-REGRESSION-3.0
Feature: Web Dashboard Live Screencast & Remote Management Verification
Evidence Mapping: EV-013 (Dashboard Navigation), EV-014 (Live Screencast Stream & Remote Command Tools)
"""

import os
import logging
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

from src.pages.screencast_page import ScreencastPage

logger = logging.getLogger("TestScreencastLive")
EVIDENCE_DIR = Path("tests/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def test_live_screencast_and_remote_tools_verification(authenticated_page: Page):
    """
    Automated regression test validating:
    1. Navigation to active employee monitoring grid and Screen Cast viewport.
    2. Live canvas telemetry rendering (#canvas-img-0).
    3. Remote administrative command palette verification via aria-snapshot.
    4. Disconnect / Connect stream toggles.
    5. Visual evidence capture (EV-014_screencast_active.png).
    """
    screencast_page = ScreencastPage(authenticated_page)

    # 1. Navigate to target user live screencast ("auto test")
    logger.info("=== STEP 1: Navigate to Live User Screencast ===")
    screencast_page.navigate_to_live_user_screencast(username="auto test")

    # 2. Verify screencast pipeline & remote command palette
    logger.info("=== STEP 2: Verify Screencast Telemetry & Remote Tools ===")
    screencast_page.verify_screencast_pipeline()

    # 3. Evidence Gathering: Capture live streaming state (EV-014)
    logger.info("=== STEP 3: Capturing Screencast Evidence (EV-014) ===")
    evidence_path = EVIDENCE_DIR / "EV-014_screencast_active.png"
    authenticated_page.wait_for_timeout(3000)
    authenticated_page.screenshot(path=str(evidence_path), full_page=True, timeout=30000)

    # Assert evidence file creation & integrity
    assert evidence_path.exists(), f"Evidence screenshot not found at: {evidence_path}"
    assert evidence_path.stat().st_size > 0, f"Evidence screenshot file is empty: {evidence_path}"
    logger.info(f"[SUCCESS] Screencast verified and visual evidence saved to: {evidence_path}")
