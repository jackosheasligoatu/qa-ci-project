from playwright.sync_api import sync_playwright
from utils.config import HEADLESS
from pages.login_page import LoginPage
from pages.game_page import GamePage


def test_gameplay():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        game = GamePage(page)
        game.attach_login_response_listener()

        LoginPage(page).login()
        game_url = game.build_game_url()
        game.launch_game(game_url)
        game.focus_game()
        game.perform_spins()

        browser.close()
