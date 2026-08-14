"""Captura capas reais dos Reels via embed público do Instagram (Playwright)."""

from __future__ import annotations

import re
from pathlib import Path

import requests

MIN_COVER_BYTES = 8_000
EMBED_SUFFIX = "/embed/captioned"


def _embed_url(permalink: str) -> str | None:
    if not permalink:
        return None
    return permalink.rstrip("/") + EMBED_SUFFIX


def _download_poster(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        if len(r.content) < MIN_COVER_BYTES:
            return False
        dest.write_bytes(r.content)
        dest.with_suffix(".src").write_text(f"embed-poster:{url}", encoding="utf-8")
        return True
    except requests.RequestException:
        return False


def _largest_media_img(page) -> str | None:
    return page.evaluate(
        """() => {
        const imgs = [...document.querySelectorAll('img')]
          .filter(i => i.src && (i.src.includes('fbcdn.net') || i.src.includes('cdninstagram')) && i.naturalWidth >= 200)
          .sort((a, b) => (b.naturalWidth * b.naturalHeight) - (a.naturalWidth * a.naturalHeight));
        return imgs[0]?.src || null;
    }"""
    )


def capture_reel_cover(page, permalink: str, dest: Path) -> bool:
    """Uma capa: poster do embed ou screenshot do vídeo (sem depender da API)."""
    embed = _embed_url(permalink)
    if not embed:
        return False

    dest.parent.mkdir(parents=True, exist_ok=True)
    page.goto(embed, wait_until="domcontentloaded", timeout=60_000)
    page.wait_for_timeout(3500)

    poster = page.evaluate(
        """() => {
        const v = document.querySelector('video');
        return v && v.poster ? v.poster : null;
    }"""
    )
    if poster and _download_poster(poster, dest):
        return True

    img_url = _largest_media_img(page)
    if img_url and _download_poster(img_url, dest):
        return True

    page.add_style_tag(
        content="[class*='PlayButton'], [class*='play-button'] { visibility: hidden !important; }"
    )
    video = page.locator("video").first
    if video.count():
        try:
            video.screenshot(path=str(dest), type="jpeg", quality=92)
            if dest.exists() and dest.stat().st_size >= MIN_COVER_BYTES:
                dest.with_suffix(".src").write_text(f"embed-screenshot:{embed}", encoding="utf-8")
                return True
        except Exception:
            pass

    return dest.exists() and dest.stat().st_size >= MIN_COVER_BYTES


def capture_portfolio_covers(
    posts: list[dict], assets_dir: Path, skip_media_ids: set[str] | None = None
) -> None:
    """Captura capas de todos os Reels do portfólio (uma sessão Playwright)."""
    skip = skip_media_ids or set()
    videos = [
        p
        for p in posts
        if p.get("media_type") in ("VIDEO", "REEL")
        and p.get("permalink")
        and str(p.get("id", "")) not in skip
    ]
    if not videos:
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  Aviso: Playwright não instalado — capas via API apenas.")
        return

    print(f"  Capturando {len(videos)} capas do Instagram (embed)...")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 540, "height": 960})
        ok = 0
        for i, post in enumerate(videos, 1):
            media_id = str(post.get("id", ""))
            dest = assets_dir / f"reel-{media_id}.jpg"
            perm = post.get("permalink", "")
            short = re.search(r"/reel/([^/]+)", perm or "")
            label = short.group(1) if short else perm[-12:]
            try:
                if capture_reel_cover(page, perm, dest):
                    ok += 1
                    print(f"    [{i}/{len(videos)}] {label} OK")
                else:
                    print(f"    [{i}/{len(videos)}] {label} falhou")
            except Exception as exc:
                print(f"    [{i}/{len(videos)}] {label} erro: {exc}")
        browser.close()
    print(f"  Capas capturadas: {ok}/{len(videos)}")
