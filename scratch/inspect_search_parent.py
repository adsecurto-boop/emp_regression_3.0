from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="playwright-profile/auth.json", ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://app.dev.empmonitor.com/amember/member", wait_until="domcontentloaded", timeout=60000)
    
    # Auto-heal login if redirected to login form
    if page.get_by_role("textbox", name="Username/Email").count() > 0 and page.get_by_role("textbox", name="Username/Email").is_visible():
        from src.utils.auth_helper import get_dashboard_credentials
        u, p = get_dashboard_credentials()
        page.get_by_role("textbox", name="Username/Email").fill(u)
        page.get_by_role("textbox", name="Password").fill(p)
        page.get_by_role("button", name="Login").click()
        page.wait_for_load_state("networkidle")
        context.storage_state(path="playwright-profile/auth.json")

    page.goto("https://app.dev.empmonitor.com/admin/employee-details", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)
    
    html_summary = page.eval_on_selector("body", """
        b => {
            const inputs = Array.from(document.querySelectorAll("input")).map(i => i.outerHTML);
            const buttons = Array.from(document.querySelectorAll("button, a.btn, .btn")).map(b => b.outerHTML);
            return { url: window.location.href, inputs, buttons };
        }
    """)
    print("URL:", html_summary['url'])
    print("\nINPUTS:")
    for inp in html_summary['inputs']:
        print("  -", inp)
    print("\nBUTTONS:")
    for btn in html_summary['buttons'][:15]:
        print("  -", btn)
    context.close()
    browser.close()
