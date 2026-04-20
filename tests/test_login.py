from playwright.sync_api import sync_playwright
import os

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Step 1: Go to the portal
        page.goto("https://portal5.omegasys.eu/login")

        # Step 2: Fill in credentials
        page.fill('input[placeholder="Username or Email"]', 'APP_USERNAME')
        page.fill('input[placeholder="Password"]', 'APP_PASSWORD')
        page.click('button:has-text("Submit")')  # May need to update this if different

        # Step 3: Wait for a logged-in indicator
        page.wait_for_selector("text=This is a demo environment")  # <-- Replace with real text you find

        print("✅ Login successful!")
        browser.close()

if __name__ == "__main__":
    run()
