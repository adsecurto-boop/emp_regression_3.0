import os
from pathlib import Path

appdata_dir = os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
screen_dir = Path(appdata_dir) / "screen"
oju_dir = list(screen_dir.glob("OjU*"))[0]
ini_path = oju_dir / "empm.ini"

print("--- FULL empm.ini CONTENT ---")
print(ini_path.read_text(encoding="utf-8", errors="ignore"))
