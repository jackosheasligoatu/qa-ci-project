import time
from utils.config import GAME_ID, SPINS, SPIN_DELAY


class GamePage:
    def __init__(self, page):
        self.page = page
        self.session_key = None

    def attach_login_response_listener(self):
        def capture_login_response(response):
            if "login" in response.url and response.status == 200:
                try:
                    data = response.json()
                    if "sessionKey" in data:
                        self.session_key = data["sessionKey"]
                    elif "associateAccounts" in data:
                        eur_acc = next((a for a in data["associateAccounts"] if a["currency"] == "EUR"), None)
                        if eur_acc:
                            self.session_key = eur_acc.get("sessionKey")
                except Exception:
                    pass

        self.page.on("response", capture_login_response)

    def build_game_url(self):
        if not self.session_key:
            raise RuntimeError("No session key captured")

        return (
            f"https://ps.omegasys.eu/ps/game/GameContainer.action"
            f"?gameId={GAME_ID}&playForReal=true&isMobile=true"
            f"&gameCurrency=EUR&platform=THREEOAKS&sessionKey={self.session_key}"
        )

    def launch_game(self, game_url: str):
        self.page.goto(game_url)
        self.page.wait_for_load_state("networkidle")
        time.sleep(3)

    def focus_game(self):
        viewport_size = self.page.viewport_size
        center_x = viewport_size["width"] / 2
        center_y = viewport_size["height"] / 2
        self.page.mouse.move(center_x, center_y)
        self.page.mouse.click(center_x, center_y)
        time.sleep(2)

    def perform_spins(self):
        for _ in range(SPINS):
            self.page.keyboard.press("Enter")
            time.sleep(SPIN_DELAY)
