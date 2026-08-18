import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
config = json.loads((root / "data/mediakit/config.json").read_text(encoding="utf-8"))
exclude = {str(x) for x in config["portfolio"]["exclude_media_ids"]}
posts = json.loads((root / "data/sync/profile_snapshot.json").read_text(encoding="utf-8"))["media"]

ranges = [
    ("2325", 2280, 2360),
    ("558", 520, 590),
    ("1109", 1070, 1140),
    ("4371", 4320, 4420),
    ("1478", 1440, 1510),
    ("1550", 1510, 1590),
    ("3411", 3360, 3460),
    ("917", 880, 950),
    ("2889", 2850, 2920),
    ("2538", 2480, 2580),
]

videos = [p for p in posts if p.get("media_type") in ("VIDEO", "REEL")]
for label, lo, hi in ranges:
    print(f"\n=== ~{label} views ===")
    found = False
    for p in videos:
        v = int((p.get("insights") or {}).get("views") or 0)
        if lo <= v <= hi:
            found = True
            mid = str(p["id"])
            cap = (p.get("caption") or "")[:75].replace("\n", " ")
            print(f"  {mid} | {v} | excl={mid in exclude} | {cap}")
    if not found:
        print("  (none with insights in range)")
