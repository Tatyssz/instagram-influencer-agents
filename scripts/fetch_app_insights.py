#!/usr/bin/env python3
"""
Captura insights do Painel Profissional (app/web) via browser Playwright.

Requer login 1x:
  python scripts/fetch_app_insights.py login

Depois:
  python scripts/fetch_app_insights.py fetch
  python scripts/fetch_app_insights.py fetch --period 30

Atualiza data/sync/insights_app.json e regenera metricas do media kit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from instagram_browser import (  # noqa: E402
    SessionExpiredError,
    _dismiss_overlays,
    _is_login_page,
    browser_profile_dir,
    ensure_browsers_installed,
    has_browser_session,
    run_login,
)

PROFILE_DIR = ROOT / "data" / "profile"
INSIGHTS_PATH = ROOT / "data" / "sync" / "insights_app.json"

INSIGHTS_URLS = (
    "https://www.instagram.com/accounts/insights/?timeframe=90",
    "https://www.instagram.com/accounts/professional_dashboard/?timeframe=90",
    "https://www.instagram.com/accounts/insights/",
    "https://www.instagram.com/accounts/professional_dashboard/",
)

PERIOD_LABELS = {
    90: (
        "Últimos 90 dias",
        "Last 90 days",
        "90 dias",
        "90 days",
    ),
    30: (
        "Últimos 30 dias",
        "Last 30 days",
        "30 dias",
        "30 days",
    ),
}


def _parse_count(raw: str) -> int | None:
    s = raw.strip().lower().replace("\u00a0", " ").replace(" ", "")
    if not s:
        return None
    mult = 1
    if "mil" in s or s.endswith("k"):
        mult = 1_000
        s = re.sub(r"(mil|k)$", "", s)
    elif "mi" in s or s.endswith("m"):
        mult = 1_000_000
        s = re.sub(r"(mi[l]?|m)$", "", s)
    s = s.replace(".", "").replace(",", ".")
    try:
        return int(float(s) * mult)
    except ValueError:
        return None


def _extract_metric(text: str, labels: tuple[str, ...]) -> int | None:
    """Busca numero proximo a rotulos comuns do painel."""
    for label in labels:
        pattern = rf"{re.escape(label)}[^\d]{{0,40}}([\d.,]+(?:\s*(?:mil|mi[l]?|[kKmM]))?)"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            val = _parse_count(match.group(1))
            if val is not None:
                return val
        pattern_rev = rf"([\d.,]+(?:\s*(?:mil|mi[l]?|[kKmM]))?)[^\d]{{0,40}}{re.escape(label)}"
        match = re.search(pattern_rev, text, flags=re.IGNORECASE)
        if match:
            val = _parse_count(match.group(1))
            if val is not None:
                return val
    return None


def _page_text(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=8000)
    except Exception:
        return ""


def _click_period(page, days: int) -> None:
    for label in PERIOD_LABELS.get(days, PERIOD_LABELS[90]):
        for kind in ("button", "div", "span", "a"):
            loc = page.locator(f'{kind}:has-text("{label}")').first
            try:
                if loc.is_visible(timeout=1200):
                    loc.click()
                    page.wait_for_timeout(1500)
                    return
            except Exception:
                continue

    # dropdown comum no topo
    for opener in ("Período", "Period", "Timeframe", "Últimos 30 dias", "Last 30 days"):
        try:
            btn = page.locator(f'button:has-text("{opener}")').first
            if btn.is_visible(timeout=800):
                btn.click()
                page.wait_for_timeout(800)
                break
        except Exception:
            pass
    for label in PERIOD_LABELS.get(days, PERIOD_LABELS[90]):
        try:
            opt = page.locator(f'button:has-text("{label}")').first
            if opt.is_visible(timeout=800):
                opt.click()
                page.wait_for_timeout(1500)
                return
        except Exception:
            pass


def _scrape_painel(page, days: int) -> dict:
    _dismiss_overlays(page)
    _click_period(page, days)
    page.wait_for_timeout(2000)
    text = _page_text(page)

    visualizacoes = _extract_metric(
        text,
        ("Visualizações", "Visualizacoes", "Views", "visualizações totais"),
    )
    interacoes = _extract_metric(
        text,
        ("Interações", "Interacoes", "Interactions", "interações totais"),
    )
    visitas = _extract_metric(
        text,
        ("Visitas ao perfil", "Profile visits", "visitas ao perfil"),
    )

    return {
        "visualizacoes": visualizacoes,
        "interacoes": interacoes,
        "visitas_perfil": visitas,
        "_raw_excerpt": text[:2500],
    }


def fetch_insights(*, period_days: int = 90, headless: bool = False) -> dict:
    ensure_browsers_installed()
    from playwright.sync_api import sync_playwright

    if not has_browser_session(PROFILE_DIR):
        raise SessionExpiredError(
            "Sem sessao no browser. Rode: python scripts/fetch_app_insights.py login"
        )

    user_data = browser_profile_dir(PROFILE_DIR)
    scraped: dict = {}
    last_url = ""

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            headless=headless,
            locale="pt-BR",
            viewport={"width": 390, "height": 844},
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/604.1"
            ),
        )
        page = context.pages[0] if context.pages else context.new_page()

        try:
            for url in INSIGHTS_URLS:
                last_url = url
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(2500)
                _dismiss_overlays(page)

                if _is_login_page(page.url):
                    raise SessionExpiredError(
                        "Sessao expirada. Rode: python scripts/fetch_app_insights.py login"
                    )

                scraped = _scrape_painel(page, period_days)
                if scraped.get("visualizacoes") and scraped.get("interacoes"):
                    scraped["_source_url"] = page.url
                    break
                scraped["_source_url"] = page.url

            if not scraped.get("visualizacoes"):
                debug = ROOT / "output" / "mediakit" / "_insights_debug.txt"
                debug.parent.mkdir(parents=True, exist_ok=True)
                debug.write_text(
                    f"url={last_url}\n\n{scraped.get('_raw_excerpt', '')}",
                    encoding="utf-8",
                )
                raise RuntimeError(
                    "Nao encontrei visualizacoes/interacoes na pagina. "
                    f"Trecho salvo em {debug}. Confira login ou envie print."
                )
        finally:
            context.close()

    return scraped


def _merge_insights(period_days: int, scraped: dict) -> dict:
    data: dict = {}
    if INSIGHTS_PATH.exists():
        data = json.loads(INSIGHTS_PATH.read_text(encoding="utf-8"))

    key = f"period_{period_days}d" if period_days != 30 else "period_30d"
    if period_days == 90:
        key = "period_90d"

    period = data.setdefault(key, {})
    painel = period.setdefault("painel_profissional", {})
    if scraped.get("visualizacoes") is not None:
        if period_days == 90:
            period["visualizacoes_total"] = scraped["visualizacoes"]
        painel["visualizacoes"] = scraped["visualizacoes"]
    if scraped.get("interacoes") is not None:
        painel["interacoes"] = scraped["interacoes"]
    if scraped.get("visitas_perfil") is not None:
        period.setdefault("atividade_perfil", {})["visitas_perfil"] = scraped["visitas_perfil"]

    data["source"] = "instagram_app_browser"
    data["captured_at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    data["_last_fetch"] = {
        "period_days": period_days,
        "source_url": scraped.get("_source_url"),
    }
    return data


def save_and_rebuild(data: dict) -> None:
    INSIGHTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    INSIGHTS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Salvo: {INSIGHTS_PATH}")

    import os
    import subprocess

    env = os.environ.copy()
    env["SKIP_COVER_CAPTURE"] = "1"

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_mediakit_metrics.py")],
        cwd=str(ROOT),
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_mediakit_html.py"), "--style", "luxe"],
        cwd=str(ROOT),
        check=False,
        env=env,
    )


def cmd_login(*, interactive: bool = False) -> None:
    run_login(PROFILE_DIR, interactive=interactive)


def cmd_fetch(period_days: int, headless: bool) -> None:
    scraped = fetch_insights(period_days=period_days, headless=headless)
    print(
        f"Capturado ({period_days}d): "
        f"views={scraped.get('visualizacoes')} "
        f"interacoes={scraped.get('interacoes')} "
        f"visitas={scraped.get('visitas_perfil')}"
    )
    data = _merge_insights(period_days, scraped)
    save_and_rebuild(data)
    print("Media kit atualizado.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Captura insights do Instagram via browser")
    parser.add_argument("command", choices=["login", "fetch"])
    parser.add_argument("--period", type=int, default=90, choices=(30, 90))
    parser.add_argument("--headless", action="store_true")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="login: aguardar ENTER manual (padrao: detecta login sozinho)",
    )
    args = parser.parse_args()

    if args.command == "login":
        cmd_login(interactive=args.interactive)
    else:
        cmd_fetch(args.period, args.headless)


if __name__ == "__main__":
    main()
