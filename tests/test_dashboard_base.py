"""
Test Suite: EMP-REGRESSION-2.0
Feature: Web Dashboard Sanity Check
Evidence IDs: EV-013 (L4 Dashboard Automation)
"""

import pytest
from playwright.sync_api import expect


def test_login_bypass_and_dashboard_render(authenticated_context):
    """
    Verifies that the cached storage state successfully bypasses the 
    login screen and loads the administrative dashboard immediately.
    """
    # Open a clean page inside our authenticated context
    page = authenticated_context.new_page()
    
    # Go directly to the member dashboard URL
    page.goto("https://app.dev.empmonitor.com/amember/member", wait_until="domcontentloaded", timeout=60000)
    
    # ASSERTION: The dashboard heading should be visible immediately.
    # If the session was invalid or expired, the application would have
    # redirected us back to the login page, and this assertion would fail.
    dashboard_header = page.get_by_role("heading", name="Dashboard")
    
    expect(dashboard_header).to_be_visible(timeout=15000)
    
    page.close()
