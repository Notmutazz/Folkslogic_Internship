import os
import shutil
from pathlib import Path
from datetime import datetime
from dateutil.parser import parse
from tqdm import tqdm
root = Path("sample_files")
organized = Path("organized_files")
organized.mkdir(exist_ok=True)
def normalize(name):
    name = name.strip()
    name = name.replace(" ", "_")
    return name
for p in tqdm(list(root.iterdir())):
    if p.is_file():
        ext = p.suffix.lower().lstrip(".") or "noext"
        folder = organized / ext
        folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        target = folder / normalize(p.name)
        if target.exists():
            base = target.stem
            newname = f"{base}_{timestamp}{p.suffix}"
            target = folder / newname
        shutil.move(str(p), str(target))
log = organized / "clean_summary.txt"
with open(log, "w") as f:
    f.write(f"Cleaned at {datetime.now().isoformat()}\n")
    for d in organized.iterdir():
        if d.is_dir():
            f.write(f"{d.name}: {len(list(d.iterdir()))}\n")
print("done")
