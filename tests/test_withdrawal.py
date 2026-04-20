from playwright.sync_api import sync_playwright
from utils.config import HEADLESS, WITHDRAWAL_AMOUNT
from pages.login_page import LoginPage
from pages.cashier_page import CashierPage


def test_withdrawal():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        LoginPage(page).login()

        cashier = CashierPage(page)
        cashier.open_deposit()
        cashier.open_withdrawal_tab()
        cashier.select_omega_bank_label()
        cashier.enter_amount(WITHDRAWAL_AMOUNT)
        cashier.submit()
        cashier.assert_withdrawal_success()

        browser.close()
