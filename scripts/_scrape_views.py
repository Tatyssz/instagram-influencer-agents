"""Scrape view counts from public Instagram permalinks (fallback when API has no insights)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_view_count(raw: str) -> int | None:
    s = raw.strip().replace(".", "").replace(",", ".")
    mult = 1
    if s.lower().endswith("k"):
        mult = 1000
        s = s[:-1]
    elif s.lower().endswith("m"):
        mult = 1_000_000
        s = s[:-1]
    try:
        return int(float(s) * mult)
    except ValueError:
        return None


def scrape_views(page, url: str) -> int | None:
    for target in (url.rstrip("/") + "/", url.rstrip("/") + "/embed/captioned/"):
        page.goto(target, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(5000)
        html = page.content()
        for key in ("video_view_count", "play_count", "view_count"):
            m = re.search(rf'"{key}":(\d+)', html)
            if m:
                return int(m.group(1))
        body = page.evaluate("() => document.body?.innerText || ''")
        for pat in (
            r"([0-9][0-9.,kKmM]*)\s*views",
            r"([0-9][0-9.,kKmM]*)\s*visualiza",
        ):
            for raw in re.findall(pat, body, re.I):
                val = parse_view_count(raw)
                if val:
                    return val
            for raw in re.findall(pat, html, re.I):
                val = parse_view_count(raw)
                if val:
                    return val
    return None


def main() -> None:
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from instagram_browser import browser_profile_dir, ensure_browsers_installed, has_browser_session
    from mediakit_assets import resolve_media_views, select_partnership_portfolio

    cfg = json.loads((ROOT / "data/mediakit/config.json").read_text(encoding="utf-8"))
    posts = json.loads((ROOT / "data/sync/profile_snapshot.json").read_text(encoding="utf-8"))["media"]
    selected = select_partnership_portfolio(posts, cfg)
    missing = []
    for p in selected:
        mid = str(p["id"])
        if resolve_media_views(mid, p.get("insights"), cfg):
            continue
        perm = p.get("permalink")
        if perm:
            missing.append((mid, perm))

    if not missing:
        print("nothing to scrape")
        return

    from playwright.sync_api import sync_playwright

    profile_dir = ROOT / "data" / "profile"
    ensure_browsers_installed()
    scraped: dict[str, int] = {}
    with sync_playwright() as pw:
        if has_browser_session(profile_dir):
            context = pw.chromium.launch_persistent_context(
                user_data_dir=str(browser_profile_dir(profile_dir)),
                headless=True,
                viewport={"width": 540, "height": 960},
            )
            page = context.pages[0] if context.pages else context.new_page()
        else:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 540, "height": 960})
        for mid, url in missing:
            try:
                views = scrape_views(page, url)
            except Exception as exc:
                print(mid, "error", exc)
                continue
            print(mid, views, url)
            if views:
                scraped[mid] = views
        if has_browser_session(profile_dir):
            context.close()
        else:
            browser.close()

    if scraped:
        out = ROOT / "data/mediakit/scraped_views.json"
        existing = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
        existing.update({k: int(v) for k, v in scraped.items()})
        out.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("saved", out)


if __name__ == "__main__":
    main()
