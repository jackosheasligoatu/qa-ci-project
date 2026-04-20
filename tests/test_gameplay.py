import time
import allure
from playwright.sync_api import sync_playwright

USERNAME = "JaquetteSparkles"
PASSWORD = "Omega123!"
SPINS = 100
SPIN_DELAY = 2


@allure.title("Launch Game and Perform Spins")
@allure.description("Logs into the portal, retrieves a sessionKey, launches a game, and performs spins.")
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
                    allure.attach(session_key, "Session Key", allure.attachment_type.TEXT)
                    print(f"🎯 Captured sessionKey: {session_key}")
                except Exception as e:
                    print(f"⚠️ Failed to parse login response: {e}")

        page.on("response", capture_login_response)

        with allure.step("Login to portal"):
            page.goto("https://portal5.omegasys.eu/login")
            page.fill('input[placeholder="Username or Email"]', USERNAME)
            page.fill('input[placeholder="Password"]', PASSWORD)
            page.click('button:has-text("Submit")')
            page.wait_for_selector("text=This is a demo environment")

        if not session_key:
            allure.attach("No session key captured!", "Error", allure.attachment_type.TEXT)
            raise RuntimeError("❌ No session key captured!")

        with allure.step("Build game launch URL"):
            game_url = (
                f"https://ps.omegasys.eu/ps/game/GameContainer.action"
                f"?gameId=aztec_fire&playForReal=true&isMobile=true"
                f"&gameCurrency=EUR&platform=THREEOAKS&sessionKey={session_key}"
            )
            allure.attach(game_url, "Game Launch URL", allure.attachment_type.TEXT)
            print(f"🎮 Navigating to: {game_url}")

        with allure.step("Launch game"):
            page.goto(game_url)
            time.sleep(5)  # wait for game to load

        with allure.step("Click center of screen to start game"):
            viewport_size = page.viewport_size
            center_x = viewport_size["width"] / 2
            center_y = viewport_size["height"] / 2
            page.mouse.move(center_x, center_y)
            page.mouse.click(center_x, center_y)
            print("🖱 Clicked center of screen to focus game")
            time.sleep(3)

        with allure.step(f"Perform {SPINS} spins"):
            for i in range(SPINS):
                page.keyboard.press("Enter")
                spin_info = f"Spin {i+1}/{SPINS}"
                print(f"🎰 {spin_info}")
                allure.attach(spin_info, f"Spin {i+1}", allure.attachment_type.TEXT)
                time.sleep(SPIN_DELAY)

        browser.close()
        print("✅ Test complete!")


if __name__ == "__main__":
    run()
