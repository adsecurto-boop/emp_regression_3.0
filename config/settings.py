import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PLAYWRIGHT_PROFILE_DIR = BASE_DIR / "playwright-profile"
AUTH_STATE_PATH = PLAYWRIGHT_PROFILE_DIR / "auth.json"

# Environment & URL Settings
EMP_ENV = os.getenv("EMP_ENV", "dev").lower()
DEV_BASE_URL = "https://app.dev.empmonitor.com"
LIVE_BASE_URL = "https://app.empmonitor.com"

DEFAULT_BASE = LIVE_BASE_URL if EMP_ENV in ["live", "prod", "production"] else DEV_BASE_URL
BASE_URL = os.getenv("EMP_BASE_URL", DEFAULT_BASE)
LOGIN_URL = os.getenv("EMP_LOGIN_URL", f"{BASE_URL}/amember/member")

# Browser & Execution Settings
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "15000"))
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
VIEWPORT_SIZE = {"width": 1280, "height": 720}

# Credentials (for generate_auth_state script fallback)
DEFAULT_USERNAME = os.getenv("EMP_USERNAME", os.getenv("EMP_DASHBOARD_USER", ""))
DEFAULT_PASSWORD = os.getenv("EMP_PASSWORD", os.getenv("EMP_DASHBOARD_PASS", ""))
