"""
Module: activity_simulator.py
Purpose: Automates local Windows 11 host workstation physical user activity simulation 
         over a strict 6-minute (360-second) timeline to generate real-time telemetry logs,
         screenshots, keystrokes (including copy/paste control characters), and screen recordings.
Evidence Mapping: L1/L2 (Host Action Generation) -> L3 Sync -> L4 Web Dashboard Verification
"""

import sys
import time
import logging
import subprocess
import webbrowser
from pathlib import Path

import pyautogui

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ActivitySimulator")

# Configure PyAutoGUI safety thresholds
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5


def run_6min_activity_simulation():
    """
    Executes a structured 6-minute (360-second) user activity simulation:
    - Min 0-1 (60s): Web Navigation (YouTube, Reddit, Gmail - 20s each)
    - Min 1-2 (60s): Host Application Traversal (Chrome 20s, Notepad 20s with full layout, PowerShell 20s)
    - Min 2-3 (60s): Telemetry Baseline Recording Hold in Notepad
    - Min 3-6 (180s): Clipboard Copy/Paste (Ctrl+C / Ctrl+V x3) & 360s Total L3 Cloud Sync Hold
    """
    start_time = time.time()
    logger.info("=== STARTING 6-MINUTE LOCAL ACTIVITY SIMULATION ===")
    logger.info("Target Duration: 360 Seconds (6 Minutes)")

    # -------------------------------------------------------------------------
    # MINUTES 0 - 1: Web Navigation (60s total)
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 0-1] Phase 1: Web Navigation Simulation (60s) ---")
    urls = [
        ("YouTube", "https://www.youtube.com/"),
        ("Reddit", "https://www.reddit.com/"),
        ("Gmail", "https://mail.google.com/"),
    ]

    for name, url in urls:
        logger.info(f"[Web Action] Opening {name}: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            logger.warning(f"Failed to open browser URL {url}: {e}")
        
        # Spend 20s per site performing subtle mouse scrolls to maintain active status
        site_start = time.time()
        while time.time() - site_start < 20:
            pyautogui.scroll(-2)
            time.sleep(5)
            pyautogui.scroll(2)
            time.sleep(5)

    elapsed = time.time() - start_time
    logger.info(f"Phase 1 Complete. Total Elapsed Time: {elapsed:.1f}s")

    # -------------------------------------------------------------------------
    # MINUTES 1 - 2: Host Application Traversal (60s total)
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 1-2] Phase 2: Host Application Traversal (60s) ---")
    
    # 1. Spend 20s focused on Chrome
    logger.info("[App Action] Focusing Chrome Browser (20s)...")
    pyautogui.click(x=500, y=500)
    time.sleep(20)

    # 2. Launch Notepad via Subprocess
    logger.info("[App Action] Launching notepad.exe...")
    notepad_proc = None
    try:
        notepad_proc = subprocess.Popen(["notepad.exe"])
        time.sleep(3)
        
        # Bring focus to Notepad
        pyautogui.click(x=400, y=400)
        time.sleep(1)

        logger.info("[Keyboard Action] Typing complete keyboard layout character payload in Notepad...")
        keyboard_payload = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        pyautogui.typewrite(keyboard_payload, interval=0.08)
        pyautogui.press("enter")
        time.sleep(5)
    except Exception as e:
        logger.error(f"Error executing Notepad simulation: {e}")

    # 3. Launch PowerShell via Subprocess
    logger.info("[App Action] Launching powershell.exe...")
    ps_proc = None
    try:
        ps_proc = subprocess.Popen(["powershell.exe"])
        time.sleep(3)
        
        # Bring focus to PowerShell
        pyautogui.click(x=400, y=400)
        time.sleep(1)

        logger.info("[Keyboard Action] Executing PowerShell diagnostic commands...")
        pyautogui.typewrite("Get-Process | Select-Object -First 5", interval=0.05)
        pyautogui.press("enter")
        time.sleep(3)
        pyautogui.typewrite("whoami", interval=0.05)
        pyautogui.press("enter")
        time.sleep(5)
    except Exception as e:
        logger.error(f"Error executing PowerShell simulation: {e}")

    elapsed = time.time() - start_time
    logger.info(f"Phase 2 Complete. Total Elapsed Time: {elapsed:.1f}s")

    # -------------------------------------------------------------------------
    # MINUTES 2 - 3: Baseline Generation (60s total)
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 2-3] Phase 3: Baseline Generation (60s) ---")
    logger.info("Keeping workstation active on Notepad filler text baseline sampling...")
    
    # Re-focus Notepad window
    if notepad_proc:
        try:
            pyautogui.click(x=400, y=400)
            time.sleep(1)
            pyautogui.typewrite("EmpMonitor 3.0 Baseline Activity Verification", interval=0.05)
            pyautogui.press("enter")
        except Exception:
            pass

    phase3_start = time.time()
    while time.time() - phase3_start < 50:
        pyautogui.moveRel(10, 0, duration=0.2)
        pyautogui.moveRel(-10, 0, duration=0.2)
        time.sleep(15)

    elapsed = time.time() - start_time
    logger.info(f"Phase 3 Complete. Total Elapsed Time: {elapsed:.1f}s")

    # -------------------------------------------------------------------------
    # MINUTES 3 - 6: Clipboard Manipulation & Upload Delay Hold (180s total)
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 3-6] Phase 4: Clipboard Copy/Paste & 360s Sync Hold (180s) ---")
    
    # Refocus Notepad for Clipboard Actions
    try:
        pyautogui.click(x=400, y=400)
        time.sleep(1)

        logger.info("[Clipboard Action] Selecting typed layout (Ctrl+A)...")
        pyautogui.hotkey("ctrl", "a")
        time.sleep(1)

        logger.info("[Clipboard Action] Copying selected text (Ctrl+C)...")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(2)

        logger.info("[Clipboard Action] Performing consecutive Pastes (Ctrl+V x3 with 3s intervals)...")
        for i in range(1, 4):
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            logger.info(f"  - Paste {i} executed.")
            time.sleep(3)
    except Exception as e:
        logger.error(f"Error performing clipboard actions: {e}")

    # Hold remaining time until 360 seconds (6 minutes) total duration
    target_total = 360.0
    current_elapsed = time.time() - start_time
    remaining_hold = max(0.0, target_total - current_elapsed)

    logger.info(f"\n[L3 Cloud Sync Hold] Waiting remaining {remaining_hold:.1f}s to reach 6 minutes total...")
    logger.info("Allowing 5-minute screen recordings, screenshots, and logs to upload to L4 Dashboard...")

    hold_start = time.time()
    while time.time() - hold_start < remaining_hold:
        # Subtle mouse nudge to keep system awake and active
        pyautogui.moveRel(5, 0, duration=0.1)
        pyautogui.moveRel(-5, 0, duration=0.1)
        time.sleep(20)

    # Clean up background process windows
    logger.info("Cleaning up background process windows...")
    if notepad_proc:
        try:
            notepad_proc.terminate()
        except Exception:
            pass
    if ps_proc:
        try:
            ps_proc.terminate()
        except Exception:
            pass

    total_final_elapsed = time.time() - start_time
    logger.info(f"\n=== [COMPLETED] 6-Minute Activity Simulation Finished in {total_final_elapsed:.1f}s ===")


if __name__ == "__main__":
    run_6min_activity_simulation()
