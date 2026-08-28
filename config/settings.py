import os
from pathlib import Path
from config.environments import ENVIRONMENTS, get_environment_config

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
PLAYWRIGHT_PROFILE_DIR = BASE_DIR / "playwright-profile"
AUTH_STATE_PATH = PLAYWRIGHT_PROFILE_DIR / "auth.json"
AUTH_SILAH_LIVE_PATH = PLAYWRIGHT_PROFILE_DIR / "auth_silah_live.json"

# Environment & URL Settings
DEV_BASE_URL = ENVIRONMENTS["dev"]["base_url"]
SILAH_LIVE_BASE_URL = ENVIRONMENTS["silah_live"]["base_url"]


def detect_environment() -> str:
    """
    Detects target environment in order of precedence:
    1. Explicit environment variable EMP_ENV ('dev', 'silah_live', or 'live')
    2. Explicit environment variable EMP_BASE_URL ('tts.silah.com.sa', 'app.dev.empmonitor.com')
    3. Cached authentication state in playwright-profile/auth_silah_live.json vs auth.json
    4. Default fallback ('dev')
    """
    env_val = os.getenv("EMP_ENV", "").strip().lower()
    if env_val:
        if env_val in ["silah", "silah_live", "silah-live", "prod", "production", "live"]:
            return "silah_live"
        return "dev"

    base_url_val = os.getenv("EMP_BASE_URL", "").strip().lower()
    if base_url_val:
        if "silah.com.sa" in base_url_val or "tts" in base_url_val:
            return "silah_live"
        return "dev"

    # Inspect cached auth state
    if AUTH_SILAH_LIVE_PATH.exists():
        return "silah_live"

    if AUTH_STATE_PATH.exists():
        try:
            text = AUTH_STATE_PATH.read_text(encoding="utf-8", errors="ignore")
            if "silah.com.sa" in text:
                return "silah_live"
            elif "app.dev.empmonitor.com" in text:
                return "dev"
        except Exception:
            pass

    return "dev"


EMP_ENV = detect_environment()
ENV_CONFIG = get_environment_config(EMP_ENV)

DEFAULT_BASE = ENV_CONFIG["base_url"]
BASE_URL = os.getenv("EMP_BASE_URL", DEFAULT_BASE)
LOGIN_URL = os.getenv("EMP_LOGIN_URL", ENV_CONFIG["login_url"])

# Active Auth Profile Path
if EMP_ENV == "silah_live" or "silah.com.sa" in BASE_URL:
    AUTH_STATE_PATH = AUTH_SILAH_LIVE_PATH
else:
    AUTH_STATE_PATH = PLAYWRIGHT_PROFILE_DIR / "auth.json"

# Browser & Execution Settings
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "15000"))
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
VIEWPORT_SIZE = {"width": 1280, "height": 720}

# Credentials (for generate_auth_state script fallback)
DEFAULT_USERNAME = os.getenv("EMP_USERNAME", os.getenv("EMP_DASHBOARD_USER", ""))
DEFAULT_PASSWORD = os.getenv("EMP_PASSWORD", os.getenv("EMP_DASHBOARD_PASS", ""))

