import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PLAYWRIGHT_PROFILE_DIR = BASE_DIR / "playwright-profile"
AUTH_STATE_PATH = PLAYWRIGHT_PROFILE_DIR / "auth.json"

# Environment & URL Settings
DEV_BASE_URL = "https://app.dev.empmonitor.com"
LIVE_BASE_URL = "https://app.empmonitor.com"


def detect_environment() -> str:
    """
    Detects target environment in order of precedence:
    1. Explicit environment variable EMP_ENV ('dev' or 'live')
    2. Explicit environment variable EMP_BASE_URL
    3. Cached authentication state in playwright-profile/auth.json
    4. Default fallback ('dev')
    """
    env_val = os.getenv("EMP_ENV", "").strip().lower()
    if env_val:
        return "live" if env_val in ["live", "prod", "production"] else "dev"

    base_url_val = os.getenv("EMP_BASE_URL", "").strip().lower()
    if base_url_val:
        return "live" if ("app.empmonitor.com" in base_url_val and "dev" not in base_url_val) else "dev"

    # Inspect cached auth state
    if AUTH_STATE_PATH.exists():
        try:
            text = AUTH_STATE_PATH.read_text(encoding="utf-8", errors="ignore")
            if "app.dev.empmonitor.com" in text:
                return "dev"
            elif "app.empmonitor.com" in text:
                return "live"
        except Exception:
            pass

    return "dev"


EMP_ENV = detect_environment()
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
