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

    # Click Timesheets tab
    ts_btn = page.locator("a[href*='#Timesheets'], a:has-text('Timesheets')").first
    print("Timesheets tab count:", ts_btn.count(), "visible:", ts_btn.is_visible() if ts_btn.count() > 0 else False)
    
    if ts_btn.count() > 0:
        ts_btn.click()
        page.wait_for_timeout(3000)
        
        # Check container visibility
        container = page.locator("#Timesheets").first
        print("Timesheets container visible:", container.is_visible() if container.count() > 0 else False)
        
        img_path = EVIDENCE_DIR / "03_timesheets_module.png"
        page.screenshot(path=str(img_path), full_page=True)
        print(f"[SUCCESS] Saved Timesheets screenshot at {img_path}")

    context.close()
    browser.close()
