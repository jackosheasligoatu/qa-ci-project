from playwright.sync_api import sync_playwright
import time

import os

print("ENV:", os.getenv("APP_ENV"))

USERNAME = os.getenv("APP_USERNAME")
PASSWORD = os.getenv("APP_PASSWORD")
SPINS = 20
SPIN_DELAY = 2

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        session_key = None

        # Capture login API response
        def capture_login_response(response):
            nonlocal session_key
            if "login" in response.url and response.status == 200:
                try:
                    data = response.json()
                    if "sessionKey" in data:
                        session_key = data["sessionKey"]
                    elif "associateAccounts" in data:
                        eur_acc = next((a for a in data["associateAccounts"] if a["currency"] == "EUR"), None)
                        if eur_acc:
                            session_key = eur_acc.get("sessionKey")
                    print(f"🎯 Captured sessionKey: {session_key}")
                except Exception as e:
                    print(f"⚠️ Failed to parse login response: {e}")

        page.on("response", capture_login_response)

        # Login steps
        page.goto("https://portal5.omegasys.eu/login")
        page.fill('input[placeholder="Username or Email"]', USERNAME)
        page.fill('input[placeholder="Password"]', PASSWORD)
        page.click('button:has-text("Submit")')
        page.wait_for_selector("text=This is a demo environment")

        if not session_key:
            raise RuntimeError("❌ No session key captured!")

        print("✅ Login successful")

        # Build and launch game
        game_url = (
            f"https://ps.omegasys.eu/ps/game/GameContainer.action"
            f"?gameId=magic_apple&playForReal=true&isMobile=true"
            f"&gameCurrency=EUR&platform=THREEOAKS&sessionKey={session_key}"
        )
        page.goto(game_url)

        # Wait for the game to load
        time.sleep(5)

        # Click dead center of the viewport to focus game
        viewport_size = page.viewport_size
        center_x = viewport_size["width"] / 2
        center_y = viewport_size["height"] / 2
        page.mouse.move(center_x, center_y)
        page.mouse.click(center_x, center_y)
        print("🖱 Clicked center of screen to focus game")

        # Give it a moment to transition into game mode
        time.sleep(3)

        # Perform spins
        for i in range(SPINS):
            page.keyboard.press("Enter")
            print(f"🎰 Spin {i+1}/{SPINS}")
            time.sleep(SPIN_DELAY)

        print("✅ Completed all spins")
        browser.close()

if __name__ == "__main__":
    run()
