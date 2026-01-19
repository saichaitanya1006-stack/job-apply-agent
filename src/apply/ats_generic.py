import time
from src.utils.browser import open_page, close_browser

def open_and_prefill_ats(job, assets, cfg):
    # Semi-auto mode: open the ATS page and let user click submit
    pw, browser, context, page = open_page(job.url, headless=False)

    try:
        print(f"🟡 Opened application page for: {job.title} @ {job.company}")
        print("Semi-auto mode: Review & click submit manually.")
        time.sleep(120)  # give user time to complete manually
    finally:
        close_browser(pw, browser)
