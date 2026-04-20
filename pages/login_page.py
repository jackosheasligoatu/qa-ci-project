from utils.config import BASE_URL, APP_USERNAME, APP_PASSWORD


class LoginPage:
    def __init__(self, page):
        self.page = page

    def login(self):
        if not APP_USERNAME or not APP_PASSWORD:
            raise RuntimeError("Missing APP_USERNAME or APP_PASSWORD")

        self.page.goto(BASE_URL)
        self.page.fill('input[placeholder="Username or Email"]', APP_USERNAME)
        self.page.fill('input[placeholder="Password"]', APP_PASSWORD)
        self.page.click('button:has-text("Submit")')
        self.page.wait_for_selector("text=This is a demo environment", timeout=10000)

        assert self.page.is_visible("text=This is a demo environment")
