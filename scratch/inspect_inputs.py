from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="playwright-profile/auth.json", ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://app.dev.empmonitor.com/admin/employee-details", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)
    
    inputs = page.eval_on_selector_all("input", """
        elements => elements.map(e => ({
            tag: e.tagName,
            type: e.type,
            id: e.id,
            class: e.className,
            placeholder: e.placeholder,
            name: e.name,
            outerHTML: e.outerHTML
        }))
    """)
    print(json.dumps(inputs, indent=2))
    context.close()
    browser.close()
