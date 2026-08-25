"""
Module: path_resolver.py
Purpose: Dynamic path resolution and discovery for EmpMonitor Agent across 
         both Local and Roaming AppData (supporting both Legacy < 3.1.0 and Modern >= 3.1.0).
"""

import os
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional, Dict, Any

logger = logging.getLogger("PathResolver")


def parse_version_string(version_str: str) -> Tuple[int, ...]:
    """Parse version string into a comparable tuple of integers."""
    parts = re.findall(r"\d+", version_str)
    return tuple(int(p) for p in parts) if parts else (0, 0, 0)


def get_appdata_roots() -> Dict[str, Path]:
    """
    Dynamically resolves Local and Roaming AppData paths using environment 
    variables with fallbacks to Path.home() so the username is never hardcoded.
    """
    user_home = Path.home()
    local_appdata = Path(os.environ.get("LOCALAPPDATA", str(user_home / "AppData" / "Local")))
    roaming_appdata = Path(os.environ.get("APPDATA", str(user_home / "AppData" / "Roaming")))
    return {
        "local": local_appdata,
        "roaming": roaming_appdata
    }


def find_screen_dirs() -> Dict[str, Optional[Path]]:
    """Returns existing screen directories under Local and Roaming AppData."""
    roots = get_appdata_roots()
    local_screen = roots["local"] / "screen"
    roaming_screen = roots["roaming"] / "screen"
    return {
        "local": local_screen if local_screen.exists() else None,
        "roaming": roaming_screen if roaming_screen.exists() else None
    }


def discover_oju_directories() -> List[Path]:
    """
    Discovers all OjU* directories (e.g. OjUxFCN, OjUabc123) across both 
    Local and Roaming screen folders.
    """
    screen_dirs = find_screen_dirs()
    discovered_oju = []
    
    for screen_dir in [screen_dirs["local"], screen_dirs["roaming"]]:
        if screen_dir and screen_dir.exists():
            for item in screen_dir.iterdir():
                if item.is_dir() and item.name.lower().startswith("oju"):
                    if item not in discovered_oju:
                        discovered_oju.append(item)
                        
    return discovered_oju


def resolve_empm_ini() -> Tuple[Optional[Path], float]:
    """
    Finds the active empm.ini configuration file across Roaming and Local AppData.
    Prioritizes files > 3.0 KB (full configuration vs stub).
    
    Returns:
        (ini_path, size_in_kb)
    """
    screen_dirs = find_screen_dirs()
    candidate_paths: List[Path] = []
    
    # 1. Check OjU* directories in Roaming and Local
    for oju_dir in discover_oju_directories():
        candidate_ini = oju_dir / "empm.ini"
        if candidate_ini.exists() and candidate_ini not in candidate_paths:
            candidate_paths.append(candidate_ini)
            
    # 2. Check root of Roaming and Local screen directories
    for screen_dir in [screen_dirs["roaming"], screen_dirs["local"]]:
        if screen_dir and screen_dir.exists():
            root_ini = screen_dir / "empm.ini"
            if root_ini.exists() and root_ini not in candidate_paths:
                candidate_paths.append(root_ini)
                
    # 3. Fallback recursive search if not found
    if not candidate_paths:
        for screen_dir in [screen_dirs["roaming"], screen_dirs["local"]]:
            if screen_dir and screen_dir.exists():
                for found in screen_dir.rglob("empm.ini"):
                    if found not in candidate_paths:
                        candidate_paths.append(found)

    if not candidate_paths:
        return None, 0.0

    # Sort candidates: prefer files > 3 KB (3072 bytes), then largest file size, then mtime
    def ini_sort_key(p: Path):
        try:
            stat = p.stat()
            size = stat.st_size
            is_valid_size = 1 if size > 3072 else 0
            return (is_valid_size, size, stat.st_mtime)
        except Exception:
            return (0, 0, 0)

    candidate_paths.sort(key=ini_sort_key, reverse=True)
    best_ini = candidate_paths[0]
    size_kb = round(best_ini.stat().st_size / 1024.0, 2)
    return best_ini, size_kb


def resolve_local_db() -> Optional[Path]:
    """
    Finds local_db20.db across Local and Roaming screen/empm directories.
    Prioritizes Local AppData as standard for < 3.1.0 and modern agents.
    """
    screen_dirs = find_screen_dirs()
    candidate_paths: List[Path] = []
    
    # Check Local AppData first, then Roaming
    for prefix_key in ["local", "roaming"]:
        screen_dir = screen_dirs[prefix_key]
        if not screen_dir or not screen_dir.exists():
            continue
            
        # Check inside OjU*/empm
        for item in screen_dir.iterdir():
            if item.is_dir() and item.name.lower().startswith("oju"):
                db_file = item / "empm" / "local_db20.db"
                if db_file.exists() and db_file not in candidate_paths:
                    candidate_paths.append(db_file)
                    
        # Check inside screen/empm
        direct_db = screen_dir / "empm" / "local_db20.db"
        if direct_db.exists() and direct_db not in candidate_paths:
            candidate_paths.append(direct_db)

    # Recursive fallback
    if not candidate_paths:
        for screen_dir in [screen_dirs["local"], screen_dirs["roaming"]]:
            if screen_dir and screen_dir.exists():
                for found in screen_dir.rglob("local_db*.db"):
                    if found not in candidate_paths:
                        candidate_paths.append(found)

    if candidate_paths:
        # Sort by mtime descending
        candidate_paths.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
        return candidate_paths[0]
    return None


def resolve_log_directories() -> List[Path]:
    """
    Finds all active logs directories across Local and Roaming screen folders.
    """
    screen_dirs = find_screen_dirs()
    log_dirs: List[Path] = []
    
    for screen_dir in [screen_dirs["local"], screen_dirs["roaming"]]:
        if not screen_dir or not screen_dir.exists():
            continue
            
        # 1. Direct empm/logs
        direct_logs = screen_dir / "empm" / "logs"
        if direct_logs.exists() and direct_logs not in log_dirs:
            log_dirs.append(direct_logs)
            
        # 2. OjU*/empm/logs
        for item in screen_dir.iterdir():
            if item.is_dir() and item.name.lower().startswith("oju"):
                oju_logs = item / "empm" / "logs"
                if oju_logs.exists() and oju_logs not in log_dirs:
                    log_dirs.append(oju_logs)
                    
    return log_dirs


def harvest_latest_logs(line_count: int = 200) -> Tuple[Optional[Path], List[str]]:
    """
    Finds the active log file (today's YYYY-MM-DD.txt or latest modified .txt)
    and extracts the last N lines.
    """
    log_dirs = resolve_log_directories()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    candidate_logs: List[Path] = []
    
    # 1. Search for today's log file
    for ld in log_dirs:
        today_file = ld / f"{today_str}.txt"
        if today_file.exists():
            candidate_logs.append(today_file)
            
    # 2. If no today log found, search for any *.txt log file
    if not candidate_logs:
        for ld in log_dirs:
            for txt_file in ld.glob("*.txt"):
                candidate_logs.append(txt_file)

    if not candidate_logs:
        return None, []

    # Sort candidate logs: prefer largest file size & newest modification
    candidate_logs.sort(key=lambda p: (p.stat().st_size, p.stat().st_mtime), reverse=True)
    active_log = candidate_logs[0]

    try:
        lines = active_log.read_text(encoding="utf-8", errors="ignore").splitlines()
        return active_log, lines[-line_count:]
    except Exception as e:
        logger.error(f"Failed to read log file {active_log}: {e}")
        return active_log, []


def resolve_telemetry_directory() -> Optional[Path]:
    """
    Resolves the primary telemetry directory containing local_db20.db, logs, etc.
    """
    db_file = resolve_local_db()
    if db_file:
        return db_file.parent
        
    screen_dirs = find_screen_dirs()
    for screen_dir in [screen_dirs["local"], screen_dirs["roaming"]]:
        if not screen_dir or not screen_dir.exists():
            continue
        for item in screen_dir.iterdir():
            if item.is_dir() and item.name.lower().startswith("oju"):
                empm_sub = item / "empm"
                if empm_sub.exists():
                    return empm_sub
        if (screen_dir / "empm").exists():
            return screen_dir / "empm"
            
    return None
