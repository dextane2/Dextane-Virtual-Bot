import subprocess

print("Installing Playwright Chromium browser...")
subprocess.run(["playwright", "install", "chromium"], check=True)
print("Playwright Chromium installed successfully ✅")
