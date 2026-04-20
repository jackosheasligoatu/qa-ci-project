from playwright.sync_api import sync_playwright

def run_withdrawal():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Login
        page.goto("https://portal5.omegasys.eu/login")
        page.fill('input[placeholder="Username or Email"]', 'cloudwarrior')
        page.fill('input[placeholder="Password"]', 'Omega123!')
        page.click('button:has-text("Submit")')
        page.wait_for_selector("text=This is a demo environment", timeout=10000)
        print("✅ Login successful")

        # Click Deposit button
        page.click('span.m_811560b9:has-text("Deposit")')

        # Switch to Withdrawal tab
        withdrawal_tab = page.locator('button[role="tab"]:has-text("Withdrawal")')
        withdrawal_tab.wait_for(state='visible', timeout=10000)
        withdrawal_tab.click()

        # Select Omega Bank
        omega_bank_label = page.locator('p:has-text("OMEGA_BANK")')
        omega_bank_label.wait_for(state='visible', timeout=10000)
        omega_bank_label.click()

        # Enter withdrawal amount
        amount_input = page.locator('input[data-path="amount"]')
        amount_input.wait_for(state='visible', timeout=5000)
        amount_input.fill("100")

        # Click Submit
        submit_button = page.locator('span.m_811560b9:has-text("Submit")')
        submit_button.wait_for(state='visible', timeout=5000)
        submit_button.click()

        # Wait for success message
        try:
            page.locator('text=Withdraw Successful').wait_for(state="visible", timeout=10000)
            print("✅ Withdrawal successful")
        except:
            print("❌ Withdrawal success message not found")

        # Optional wait to observe result before closing
        page.wait_for_timeout(10000)
        browser.close()

if __name__ == "__main__":
    run_withdrawal()
