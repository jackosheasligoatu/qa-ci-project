import os

BASE_URL = os.getenv("BASE_URL", "https://portal5.omegasys.eu/login")
APP_USERNAME = os.getenv("APP_USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

GAME_ID = os.getenv("GAME_ID", "aztec_fire")
SPINS = int(os.getenv("SPINS", "5"))
SPIN_DELAY = float(os.getenv("SPIN_DELAY", "1"))

DEPOSIT_AMOUNT = os.getenv("DEPOSIT_AMOUNT", "1000")
WITHDRAWAL_AMOUNT = os.getenv("WITHDRAWAL_AMOUNT", "100")
