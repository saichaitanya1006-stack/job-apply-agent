from playwright.sync_api import sync_playwright

def open_page(url: str, headless: bool = False):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()

    page.goto(url, wait_until="domcontentloaded", timeout=60000)

    return pw, browser, context, page


def close_browser(pw, browser):
    browser.close()
    pw.stop()
