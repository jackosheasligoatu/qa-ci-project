from playwright.sync_api import sync_playwright
import time

import os

print("ENV:", os.getenv("APP_ENV"))

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")

def run_deposit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto("https://portal5.omegasys.eu/login")
        page.fill('input[placeholder="Username or Email"]', APP_USERNAME)
        page.fill('input[placeholder="Password"]', APP_PASSWORD)
        page.click('button:has-text("Submit")')

        page.wait_for_selector("text=This is a demo environment", timeout=10000)
        print("✅ Login successful")

        # Click Deposit button
        page.click('span.m_811560b9:has-text("Deposit")')
        print("💰 Clicked Deposit")
        time.sleep(2)

        # Select Omega Bank by image alt attribute
        omega_bank_img = page.locator('img[alt="OMEGA_BANK"]')
        omega_bank_img.wait_for(state='visible', timeout=10000)
        omega_bank_img.click()
        print("🏦 Selected Omega Bank")
        time.sleep(2)

        # Enter deposit amount - Usually an input, but you said image repeated here? 
        # Assuming there's an input field near the bank image to enter amount:
        amount_input = page.locator('input[type="number"], input[placeholder*="amount"]')
        if amount_input.count() == 0:
            raise Exception("Deposit amount input field not found")
        amount_input.fill("1000")
        print("💵 Entered deposit amount: 1000")
        time.sleep(1)

        # Click Next
        page.click('span.m_811560b9:has-text("Next")')
        print("➡️ Clicked Next")
        time.sleep(2)

        # Select Bonus by partial text "Deposit Test - OMEGA"
        bonus_selector = 'div:has-text("Deposit Test - OMEGA")'
        page.wait_for_selector(bonus_selector, timeout=10000)
        page.click(bonus_selector)
        print("🎁 Selected Deposit Test - OMEGA bonus")
        time.sleep(2)

        # Click Submit bonus button
        page.click('span.m_811560b9:has-text("Submit")')
        print("✅ Submitted bonus")
        time.sleep(5)

        # Optional: Verify success message appears
        if page.locator('text=Successful deposit').count() > 0:
            print("🎉 Deposit successful!")
        else:
            print("⚠️ Could not confirm deposit success")

        # Keep browser open a bit so you can see results
        print("⏳ Keeping browser open for 15 seconds...")
        page.wait_for_timeout(15000)

        browser.close()

if __name__ == "__main__":
    run_deposit()
