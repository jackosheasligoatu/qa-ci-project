from playwright.sync_api import sync_playwright
from utils.config import HEADLESS
from pages.login_page import LoginPage


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        LoginPage(page).login()
        browser.close()
