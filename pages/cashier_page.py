class CashierPage:
    def __init__(self, page):
        self.page = page

    def open_deposit(self):
        self.page.click('span.m_811560b9:has-text("Deposit")')

    def select_omega_bank_image(self):
        bank = self.page.locator('img[alt="OMEGA_BANK"]')
        bank.wait_for(state="visible", timeout=10000)
        bank.click()

    def select_omega_bank_label(self):
        bank = self.page.locator('p:has-text("OMEGA_BANK")')
        bank.wait_for(state="visible", timeout=10000)
        bank.click()

    def enter_amount(self, amount: str):
        amount_input = self.page.locator('input[type="number"], input[placeholder*="amount"], input[data-path="amount"]')
        if amount_input.count() == 0:
            raise RuntimeError("Amount input field not found")
        amount_input.first.fill(amount)

    def click_next(self):
        self.page.click('span.m_811560b9:has-text("Next")')

    def select_bonus(self, bonus_text: str):
        selector = f'div:has-text("{bonus_text}")'
        self.page.wait_for_selector(selector, timeout=10000)
        self.page.click(selector)

    def submit(self):
        button = self.page.locator('span.m_811560b9:has-text("Submit")')
        button.wait_for(state="visible", timeout=10000)
        button.click()

    def open_withdrawal_tab(self):
        tab = self.page.locator('button[role="tab"]:has-text("Withdrawal")')
        tab.wait_for(state="visible", timeout=10000)
        tab.click()

    def assert_deposit_success(self):
        self.page.locator('text=Successful deposit').wait_for(state="visible", timeout=10000)
        assert self.page.is_visible('text=Successful deposit')

    def assert_withdrawal_success(self):
        self.page.locator('text=Withdraw Successful').wait_for(state="visible", timeout=10000)
        assert self.page.is_visible('text=Withdraw Successful')
