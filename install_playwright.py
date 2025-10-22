from playwright.sync_api import sync_playwright

print("Installing Chromium for Playwright...")

with sync_playwright() as p:
    for browser_type in [p.chromium]:
        browser_type.install()

print("✅ Chromium installation complete.")
