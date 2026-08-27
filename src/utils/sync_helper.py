"""
Module: sync_helper.py
Framework: emp_regression_3.0
Purpose: Fast-tracks synchronization between Web Dashboard settings (L4) and local empm.ini (L1)
         by ending and restarting agent processes, and provides interactive conflict reconciliation.
Evidence Mapping: EV-001 (Config Sync) -> EV-015 (Web Settings Alignment)
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any

import psutil

logger = logging.getLogger("SyncHelper")

DEFAULT_TARGET_PROCS = [
    "empmonitor.exe",
    "displayconfigmanager.exe",
    "updatemgr_emp.exe",
    "esr.exe",
    "emp_psa_service.exe"
]


def _safe_print(msg: str):
    """Safely prints to stdout without raising UnicodeEncodeError on Windows cp1252."""
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))


def fast_sync_agent_restart(
    process_names: Optional[List[str]] = None,
    wait_seconds: int = 5
) -> bool:
    """
    Terminates running agent process (e.g. empmonitor.exe or DisplayConfigManager.exe)
    to trigger an immediate API sync (/api/v3/user/config and /api/v3/user/system-info),
    fast-tracking synchronization with the Web Dashboard without waiting for the 3-minute periodic sync.
    """
    if not process_names:
        process_names = DEFAULT_TARGET_PROCS

    target_names_lower = [Path(p).name.lower() for p in process_names]
    terminated = []

    logger.info("=== FAST-SYNC: Terminating active agent process to trigger immediate configuration refresh ===")
    _safe_print("\n[Fast-Sync] Ending agent process to force instant API config pull...")

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            p_name = proc.info.get("name")
            if p_name and p_name.lower() in target_names_lower:
                pid = proc.info.get("pid")
                logger.info(f"Terminating process '{p_name}' (PID={pid})...")
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except psutil.TimeoutExpired:
                    proc.kill()
                terminated.append(f"{p_name} (PID={pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied, Exception) as e:
            logger.debug(f"Process termination note: {e}")

    if terminated:
        _safe_print(f"  [-] Successfully terminated: {', '.join(terminated)}")
        _safe_print(f"  [-] Waiting {wait_seconds}s for service restart and configuration refresh...")
        time.sleep(wait_seconds)
        return True
    else:
        _safe_print("  [-] No active agent process found running to terminate.")
        return False


def prompt_conflict_resolution(
    feature_name: str,
    local_val: str,
    web_val: str,
    context_note: str = ""
) -> Tuple[bool, str]:
    """
    Interactively prompts the operator when a setting mismatch between empm.ini and the Web Dashboard occurs.
    Allows the operator to skip/ignore the check if a feature (like screen recording) is known to be unsupported
    in the active agent build, or to conclude the check as a failure.

    Returns:
        (should_skip_failure: bool, resolution_note: str)
    """
    _safe_print("\n" + "!" * 76)
    _safe_print(f"[SETTING CONFLICT DETECTED] Feature: {feature_name.upper()}")
    _safe_print(f"    - Local Agent Value (empm.ini) : {local_val}")
    _safe_print(f"    - Web Dashboard Value (L4)    : {web_val}")
    if context_note:
        _safe_print(f"    - Context                     : {context_note}")
    _safe_print("!" * 76)

    # Check non-interactive environment override
    env_override = os.getenv("SKIP_SETTING_CONFLICTS", "").strip().lower()
    if env_override in ["1", "true", "yes", "all"]:
        logger.info(f"Auto-skipping conflict for '{feature_name}' via SKIP_SETTING_CONFLICTS env var.")
        return True, "SKIPPED_VIA_ENV_OVERRIDE"

    if sys.stdin.isatty():
        try:
            _safe_print("\nOptions:")
            _safe_print("  [1] Ignore conflict and proceed (Feature unsupported / tolerated in this test)")
            _safe_print("  [2] Conclude this check as a FAILURE")
            choice = input(f"Choose option for '{feature_name}' [1=Ignore & Proceed (default), 2=Fail]: ").strip()
            if choice == "2":
                return False, "OPERATOR_CONCLUDED_FAILURE"
            else:
                return True, "OPERATOR_SKIPPED_CONFLICT"
        except (KeyboardInterrupt, EOFError):
            return True, "OPERATOR_SKIPPED_CONFLICT"

    # Default in non-interactive mode is to report mismatch
    return False, "NON_INTERACTIVE_MISMATCH"
