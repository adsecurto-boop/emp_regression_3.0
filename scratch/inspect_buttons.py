from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="playwright-profile/auth.json", ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://app.dev.empmonitor.com/admin/employee-details", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)
    
    buttons = page.eval_on_selector_all("button, a, i, span", """
        elements => elements.filter(e => {
            const html = e.outerHTML.toLowerCase();
            return html.includes('search') || html.includes('SearchButton') || e.id.toLowerCase().includes('search');
        }).map(e => ({
            tag: e.tagName,
            id: e.id,
            class: e.className,
            text: e.innerText,
            outerHTML: e.outerHTML
        }))
    """)
    print(json.dumps(buttons, indent=2))
    context.close()
    browser.close()
