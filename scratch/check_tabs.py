from pathlib import Path
from playwright.sync_api import sync_playwright

EVIDENCE_DIR = Path("reports/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="playwright-profile/auth.json")
    page = context.new_page()
    page.goto("https://app.dev.empmonitor.com/admin/get-employee-details?id=45009", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    tabs = [
        ("03_keystrokes_module.png", "#keyLogger", "Key Strokes"),
        ("04_app_history_module.png", "#AppHistory", "App History"),
        ("05_web_history_module.png", "#BrowserHistory", "Web History"),
        ("06_screenshots_module.png", "#Screenshots", "Screenshots"),
        ("07_productivity_module.png", "#Productivity", "Productivity"),
        ("08_screen_recording_module.png", "#ScreenRecording", "Screen Recording")
    ]

    for fname, href, text in tabs:
        try:
            btn = page.locator(f"a[href*='{href}']").first
            btn.click()
            page.wait_for_timeout(3000)
            page.screenshot(path=str(EVIDENCE_DIR / fname), full_page=True)
            print(f"[SUCCESS] Captured {fname}")
        except Exception as e:
            print(f"[ERROR] Failed {fname}: {e}")

    context.close()
    browser.close()
