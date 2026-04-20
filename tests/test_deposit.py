from playwright.sync_api import sync_playwright
from utils.config import HEADLESS, DEPOSIT_AMOUNT
from pages.login_page import LoginPage
from pages.cashier_page import CashierPage


def test_deposit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        LoginPage(page).login()

        cashier = CashierPage(page)
        cashier.open_deposit()
        cashier.select_omega_bank_image()
        cashier.enter_amount(DEPOSIT_AMOUNT)
        cashier.click_next()
        cashier.select_bonus("Deposit Test - OMEGA")
        cashier.submit()
        cashier.assert_deposit_success()

        browser.close()
