from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="playwright-profile/auth.json", ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://app.dev.empmonitor.com/amember/member", wait_until="domcontentloaded", timeout=60000)
    
    if page.get_by_role("textbox", name="Username/Email").count() > 0 and page.get_by_role("textbox", name="Username/Email").is_visible():
        from src.utils.auth_helper import get_dashboard_credentials
        u, p = get_dashboard_credentials()
        page.get_by_role("textbox", name="Username/Email").fill(u)
        page.get_by_role("textbox", name="Password").fill(p)
        page.get_by_role("button", name="Login").click()
        page.wait_for_load_state("networkidle")
        context.storage_state(path="playwright-profile/auth.json")

    page.goto("https://app.dev.empmonitor.com/admin/track-user-setting?id=45009", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)
    
    print("PAGE TITLE:", page.title())
    print("PAGE URL:", page.url)
    
    inputs = page.locator("input, select, button").all()
    for inp in inputs:
        try:
            val = inp.input_value() if inp.get_attribute("type") not in ["checkbox", "radio"] else inp.is_checked()
            name = inp.get_attribute("name") or inp.get_attribute("id") or inp.get_attribute("class")
            print(f"Tag: {inp.evaluate('e => e.tagName')} | ID/Name: {name} | Value/Checked: {val}")
        except Exception:
            pass
            
    context.close()
    browser.close()
