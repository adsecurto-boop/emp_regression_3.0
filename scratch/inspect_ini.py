import os
import glob
from pathlib import Path
import configparser

appdata_dir = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
screen_dir = Path(appdata_dir) / "screen"
print("Screen Dir:", screen_dir, "Exists:", screen_dir.exists())

if screen_dir.exists():
    oju_matches = list(screen_dir.glob("OjU*"))
    print("OjU Matches:", oju_matches)
    if oju_matches:
        oju_dir = oju_matches[0]
        ini_path = oju_dir / "empm.ini"
        print("INI Path:", ini_path, "Exists:", ini_path.exists())
        if ini_path.exists():
            print("Size:", ini_path.stat().st_size, "bytes")
            content = ini_path.read_text(encoding="utf-8", errors="ignore")
            print("--- empm.ini RAW CONTENT ---")
            print(content[:1000])

config_js = Path(r"C:\Program Files\EmpMonitor\EmpMonitor\gui\configs\config.js")
print("\nConfig JS Path:", config_js, "Exists:", config_js.exists())
if config_js.exists():
    print(config_js.read_text(encoding="utf-8", errors="ignore")[:500])
