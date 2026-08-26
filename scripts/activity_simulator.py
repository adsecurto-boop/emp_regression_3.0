"""
Module: activity_simulator.py
Purpose: Automates local Windows 11 host workstation physical user activity simulation 
         over a strict 6-minute (360-second) timeline to generate real-time telemetry logs,
         screenshots, keystrokes (including copy/paste control characters in Notepad), and screen recordings.
Evidence Mapping: L1/L2 (Host Action Generation) -> L3 Sync -> L4 Web Dashboard Verification
"""

import sys
import time
import ctypes
import logging
import subprocess
import webbrowser
from ctypes import wintypes
from pathlib import Path

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.5
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "--quiet"])
        import pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.5
    except Exception:
        pyautogui = None

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ActivitySimulator")

user32 = ctypes.windll.user32


def focus_notepad_window() -> bool:
    """
    Locates and forcefully brings the Notepad window to the foreground using Win32 API.
    Restores window if minimized, activates it, and clicks inside the editing canvas.
    """
    hwnd = user32.FindWindowW("Notepad", None)
    if not hwnd:
        found_hwnds = []

        def enum_windows_callback(h, lparam):
            length = user32.GetWindowTextLengthW(h)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(h, buff, length + 1)
                if "notepad" in buff.value.lower():
                    found_hwnds.append(h)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        cb = WNDENUMPROC(enum_windows_callback)
        user32.EnumWindows(cb, 0)
        if found_hwnds:
            hwnd = found_hwnds[0]

    if hwnd:
        # SW_RESTORE = 9, SW_SHOW = 5
        user32.ShowWindow(hwnd, 9)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)

        # Click inside the Notepad editor area to ensure focus
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        click_x = rect.left + max(60, (rect.right - rect.left) // 2)
        click_y = rect.top + max(60, (rect.bottom - rect.top) // 2)
        if pyautogui:
            pyautogui.click(click_x, click_y)
        time.sleep(0.5)
        return True

    return False


def get_remaining_seconds(start_time: float, target_duration: float = 360.0) -> float:
    """Calculates seconds remaining until the target duration is reached."""
    elapsed = time.time() - start_time
    return max(0.0, target_duration - elapsed)


def print_progress_timer(start_time: float, target_duration: float = 360.0, label: str = ""):
    """Displays a live formatted remaining seconds countdown timer."""
    remaining = int(get_remaining_seconds(start_time, target_duration))
    elapsed = int(time.time() - start_time)
    mins_rem, secs_rem = divmod(remaining, 60)
    extra = f" | {label}" if label else ""
    sys.stdout.write(f"\r[TIMER] Remaining: {remaining:3d}s ({mins_rem:02d}m {secs_rem:02d}s) | Elapsed: {elapsed:3d}s / {int(target_duration)}s{extra}")
    sys.stdout.flush()


def run_6min_activity_simulation():
    """
    Executes a structured 6-minute (360-second) user activity simulation:
    - Min 0-1 (60s): Web Navigation (YouTube, Reddit, Gmail - 20s each)
    - Min 1-2 (60s): Host Application Traversal (Chrome 20s, Notepad launched & focused for typing payload)
    - Min 2-3 (60s): Telemetry Baseline Recording Hold in Notepad
    - Min 3-6 (180s): Clipboard Copy/Paste (Ctrl+C / Ctrl+V x3 strictly in Notepad) & 360s Cloud Sync Timer
    """
    target_total_seconds = 360.0
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

        # Spend ~20s per site with countdown timer
        site_start = time.time()
        while time.time() - site_start < 20:
            print_progress_timer(start_time, target_total_seconds, label=f"Browsing {name}")
            if pyautogui:
                pyautogui.scroll(-2)
                time.sleep(2.5)
                pyautogui.scroll(2)
                time.sleep(2.5)
            else:
                time.sleep(5)

    print()
    elapsed = time.time() - start_time
    logger.info(f"Phase 1 Complete. Total Elapsed Time: {elapsed:.1f}s")

    # -------------------------------------------------------------------------
    # MINUTES 1 - 2: Host Application Traversal (60s total)
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 1-2] Phase 2: Host Application Traversal (60s) ---")

    # 1. Spend 20s focused on Chrome
    logger.info("[App Action] Focusing Chrome Browser (20s)...")
    if pyautogui:
        pyautogui.click(x=500, y=500)
    chrome_start = time.time()
    while time.time() - chrome_start < 20:
        print_progress_timer(start_time, target_total_seconds, label="Chrome Active")
        time.sleep(1)
    print()

    # 2. Launch Notepad via Subprocess & Focus strictly on Notepad
    logger.info("[App Action] Launching notepad.exe...")
    notepad_proc = None
    try:
        notepad_proc = subprocess.Popen(["notepad.exe"])
        time.sleep(3)

        # Explicitly ensure Notepad window is in foreground
        focus_notepad_window()

        logger.info("[Keyboard Action] Typing complete keyboard layout character payload strictly in Notepad...")
        keyboard_payload = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        if pyautogui:
            focus_notepad_window()
            pyautogui.typewrite(keyboard_payload, interval=0.08)
            pyautogui.press("enter")
        time.sleep(2)
    except Exception as e:
        logger.error(f"Error executing Notepad simulation: {e}")

    # 3. Optional brief background process check without stealing focus from Notepad
    logger.info("[App Action] Verifying system processes...")
    try:
        subprocess.run(["powershell.exe", "-Command", "Get-Process | Select-Object -First 3"], capture_output=True, timeout=5)
    except Exception as e:
        logger.debug(f"Process check note: {e}")

    # Immediately re-focus Notepad
    focus_notepad_window()

    elapsed = time.time() - start_time
    logger.info(f"Phase 2 Complete. Total Elapsed Time: {elapsed:.1f}s")

    # -------------------------------------------------------------------------
    # MINUTES 2 - 3: Baseline Generation in Notepad (60s total)
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 2-3] Phase 3: Baseline Generation in Notepad (60s) ---")
    logger.info("Keeping workstation active on Notepad filler text baseline sampling...")

    # Ensure Notepad is active
    focus_notepad_window()
    if pyautogui:
        pyautogui.typewrite("EmpMonitor 3.0 Baseline Activity Verification\n", interval=0.05)

    phase3_start = time.time()
    while time.time() - phase3_start < 50:
        print_progress_timer(start_time, target_total_seconds, label="Notepad Baseline Active")
        if pyautogui:
            pyautogui.moveRel(5, 0, duration=0.1)
            pyautogui.moveRel(-5, 0, duration=0.1)
        time.sleep(5)
    print()

    elapsed = time.time() - start_time
    logger.info(f"Phase 3 Complete. Total Elapsed Time: {elapsed:.1f}s")

    # -------------------------------------------------------------------------
    # MINUTES 3 - 6: Clipboard Manipulation & Upload Delay Hold strictly in Notepad
    # -------------------------------------------------------------------------
    logger.info("\n--- [Min 3-6] Phase 4: Clipboard Copy/Paste (in Notepad) & 360s Sync Hold ---")

    # 1. Bring Notepad window to front
    logger.info("Focusing Notepad application for clipboard operations...")
    focus_notepad_window()
    time.sleep(1)

    try:
        # Select all text in Notepad
        logger.info("[Clipboard Action] Selecting text in Notepad (Ctrl+A)...")
        focus_notepad_window()
        if pyautogui:
            pyautogui.hotkey("ctrl", "a")
            time.sleep(1)

            # Copy selected text
            logger.info("[Clipboard Action] Copying selected text in Notepad (Ctrl+C)...")
            pyautogui.hotkey("ctrl", "c")
            time.sleep(2)

            # Perform 3 distinct Pastes inside Notepad
            logger.info("[Clipboard Action] Performing consecutive Pastes strictly in Notepad (Ctrl+V x3)...")
            # Move cursor to end
            pyautogui.press("right")
            pyautogui.press("enter")
            pyautogui.press("enter")

            for i in range(1, 4):
                focus_notepad_window()
                pyautogui.hotkey("ctrl", "v")
                pyautogui.press("enter")
                logger.info(f"  - Paste {i} executed in Notepad.")
                time.sleep(2)
    except Exception as e:
        logger.error(f"Error performing clipboard actions in Notepad: {e}")

    # 2. Live Countdown Timer until exactly 360 seconds (6 minutes) total duration
    logger.info("\n[L3 Cloud Sync Hold] Synchronizing real-time telemetry, logs, and screen recordings...")
    logger.info("Live Countdown Timer active until 360 seconds (6.0 minutes) total:\n")

    while True:
        remaining = get_remaining_seconds(start_time, target_total_seconds)
        if remaining <= 0:
            break

        print_progress_timer(start_time, target_total_seconds, label="Uploading to Cloud")

        # Subtle mouse nudge every 10 seconds to maintain active user status
        if pyautogui and int(remaining) % 10 == 0:
            pyautogui.moveRel(4, 0, duration=0.1)
            pyautogui.moveRel(-4, 0, duration=0.1)

        time.sleep(1)

    print()  # newline after timer finishes

    # Clean up background notepad process
    logger.info("Cleaning up Notepad simulation window...")
    if notepad_proc:
        try:
            notepad_proc.terminate()
        except Exception:
            pass

    total_final_elapsed = time.time() - start_time
    logger.info(f"\n=== [COMPLETED] 6-Minute Activity Simulation Finished in {total_final_elapsed:.1f}s ===")


if __name__ == "__main__":
    run_6min_activity_simulation()
