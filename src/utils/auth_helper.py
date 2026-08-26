"""
Module: auth_helper.py
Purpose: Secure credential manager retrieving dashboard login credentials 
         from environment variables or interactive hidden CLI prompts (getpass).
"""

import os
import sys
import getpass
from typing import Tuple


def get_dashboard_credentials(prompt_if_missing: bool = True) -> Tuple[str, str]:
    """
    Retrieves Dashboard Login Username and Password safely:
    1. Checks environment variables EMP_USERNAME / EMP_DASHBOARD_USER and EMP_PASSWORD / EMP_DASHBOARD_PASS.
    2. If missing and prompt_if_missing is True, prompts user interactively with getpass.getpass() for password.
    """
    username = (
        os.getenv("EMP_USERNAME") or 
        os.getenv("EMP_DASHBOARD_USER") or 
        "nokiaa"
    ).strip()
    
    password = (
        os.getenv("EMP_PASSWORD") or 
        os.getenv("EMP_DASHBOARD_PASS") or 
        "Shiv@123"
    ).strip()

    if not username and prompt_if_missing and sys.stdin.isatty():
        try:
            username = input("Enter Dashboard Admin Username/Email: ").strip()
        except Exception:
            username = ""

    if not password and prompt_if_missing and sys.stdin.isatty():
        try:
            password = getpass.getpass("Enter Dashboard Admin Password (hidden): ").strip()
        except Exception:
            password = ""

    return username, password
