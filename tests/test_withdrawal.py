from playwright.sync_api import sync_playwright
import os

print("ENV:", os.getenv("APP_ENV"))

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
WITHDRAWAL_AMOUNT = os.getenv("WITHDRAWAL_AMOUNT", "100")


def run_withdrawal():
    if not USERNAME or not PASSWORD:
        raise RuntimeError("Missing APP_USERNAME or APP_PASSWORD environment variables")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto("https://portal5.omegasys.eu/login")
        page.fill('input[placeholder="Username or Email"]', USERNAME)
        page.fill('input[placeholder="Password"]', PASSWORD)
        page.click('button:has-text("Submit")')

        # Better login success check: wait for logged-in UI
        deposit_button = page.locator('span.m_811560b9:has-text("Deposit")')
        deposit_button.wait_for(state="visible", timeout=20000)
        print("✅ Login successful")

        # Open cashier
        deposit_button.click()

        # Switch to Withdrawal tab
        withdrawal_tab = page.locator('button[role="tab"]:has-text("Withdrawal")')
        withdrawal_tab.wait_for(state='visible', timeout=15000)
        withdrawal_tab.click()

        # Select Omega Bank
        omega_bank_label = page.locator('p:has-text("OMEGA_BANK")')
        omega_bank_label.wait_for(state='visible', timeout=15000)
        omega_bank_label.click()

        # Enter withdrawal amount
        amount_input = page.locator('input[data-path="amount"]')
        amount_input.wait_for(state='visible', timeout=10000)
        amount_input.fill(WITHDRAWAL_AMOUNT)

        # Click Submit
        submit_button = page.locator('span.m_811560b9:has-text("Submit")')
        submit_button.wait_for(state='visible', timeout=10000)
        submit_button.click()

        # Assert success properly
        success_message = page.locator('text=Withdraw Successful')
        success_message.wait_for(state="visible", timeout=15000)
        print("✅ Withdrawal successful")

        browser.close()


if __name__ == "__main__":
    run_withdrawal()
