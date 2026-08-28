"""
Module: config/environments.py
Purpose: Multi-tenant environment configuration router defining Dev and Silah Live environments.
"""
from typing import Dict, Any
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENTS: Dict[str, Dict[str, Any]] = {
    "dev": {
        "name": "dev",
        "base_url": "https://app.dev.empmonitor.com",
        "login_url": "https://app.dev.empmonitor.com/amember/member",
        "auth_profile": BASE_DIR / "playwright-profile" / "auth.json",
        "description": "Standard Development Environment"
    },
    "silah_live": {
        "name": "silah_live",
        "base_url": "https://tts.silah.com.sa",
        "login_url": "https://tts.silah.com.sa/admin-login",
        "auth_profile": BASE_DIR / "playwright-profile" / "auth_silah_live.json",
        "description": "Production Silah TTS Dashboard"
    }
}


def get_environment_config(env_name: str) -> Dict[str, Any]:
    """Retrieve configuration dictionary for given environment key ('dev' or 'silah_live')."""
    clean_key = env_name.strip().lower() if env_name else "dev"
    if clean_key in ["silah", "silah_live", "silah-live", "tts.silah.com.sa"]:
        return ENVIRONMENTS["silah_live"]
    return ENVIRONMENTS.get(clean_key, ENVIRONMENTS["dev"])
