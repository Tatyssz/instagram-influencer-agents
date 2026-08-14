#!/usr/bin/env python3
"""Gera Media Kit Modelo A (HTML 1 página, pronto para PDF) a partir das métricas."""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from pathlib import Path

from mediakit_assets import prepare_assets
from mediakit_glow import build_glow
from mediakit_luxe import build_portfolio, build_print
from mediakit_templates import build_editorial

ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / "output" / "mediakit" / "estimativa-metricas.json"
SNAPSHOT = ROOT / "data" / "sync" / "profile_snapshot.json"
CONFIG = ROOT / "data" / "mediakit" / "config.json"
OUT_DIR = ROOT / "output" / "mediakit"
OUT_HTML = OUT_DIR / "media-kit.html"
OUT_PORTFOLIO = OUT_DIR / "portfolio.html"
OUT_PDF = OUT_DIR / "media-kit.pdf"


def fmt_num(n: int | float) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 10_000:
        return f"{n / 1_000:.1f}k".replace(".0k", "k")
    if n >= 1_000:
        s = f"{n / 1_000:.1f}k"
        return s.replace(".0k", "k")
    if isinstance(n, float):
        return f"{n:.1f}".rstrip("0").rstrip(".")
    return str(n)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def period_label(metrics: dict) -> str:
    official = metrics.get("app_insights_official", {})
    period = official.get("period_30d", {})
    if period.get("label"):
        return period["label"]
    return "últimos 30 dias"


def build_html(metrics: dict, config: dict, profile_pic: str | None) -> str:
    h = metrics.get("media_kit_highlights", {})
    profile = metrics.get("profile", {})
    username = profile.get("username", config["contact"]["instagram"])
    name = profile.get("name", "Taty Zacharias").split("|")[0].strip()
    period = period_label(metrics)

    stats = [
        ("Seguidores", fmt_num(h.get("followers", 0))),
        ("Visualizações", fmt_num(h.get("views_30d_official", 0)), f"30d · {period}"),
        ("Interações", fmt_num(h.get("interactions_30d_official", 0)), "30d"),
        ("Visualizações med./Reel", fmt_num(h.get("median_views_per_reel", h.get("avg_views_per_reel", 0))), "top Reels API"),
        ("Pico alcance/Reel", fmt_num(h.get("best_reach_per_reel", 0)), "melhor desempenho"),
        ("Taxa interação", f"{h.get('interaction_rate_on_views_pct', h.get('engagement_by_reach_pct', 0))}%", "views · 30d"),
        ("Novos públicos", f"{h.get('views_non_followers_pct_90d', 0)}%", "views · 90d"),
    ]

    audience = [
        ("Brasil", f"{h.get('brazil_audience_pct', 0)}%"),
        ("Mulheres", f"{h.get('female_audience_pct', 0)}%"),
        ("25–44 anos", f"{h.get('core_age_25_44_pct', 0)}%"),
        ("Baixada Santista", f"{h.get('baixada_santista_pct', 0)}%"),
    ]

    badges_html = "".join(
        f'<span class="badge">{html.escape(b)}</span>' for b in config.get("badges", [])
    )
    brands_html = "".join(
        f'<span class="brand">{html.escape(b["name"])}</span>'
        for b in config.get("brands", [])
    )

    cases_html = ""
    for case in config.get("cases", [])[:3]:
        cases_html += f"""
        <article class="case">
          <p class="case-brand">{html.escape(case.get("brand", ""))}</p>
          <h3>{html.escape(case.get("title", ""))}</h3>
          <p class="case-metrics">{html.escape(case.get("metrics", ""))}</p>
          <p class="case-note">{html.escape(case.get("note", ""))}</p>
        </article>"""

    services_html = ""
    for svc in config.get("services", []):
        services_html += f"""
        <li>
          <strong>{html.escape(svc["name"])}</strong>
          <span>{html.escape(svc.get("detail", ""))}</span>
        </li>"""

    contact = config.get("contact", {})
    contact_lines = [f'@{html.escape(contact.get("instagram", username))}']
    if contact.get("email"):
        contact_lines.append(html.escape(contact["email"]))
    if contact.get("whatsapp"):
        contact_lines.append(html.escape(contact["whatsapp"]))
    contact_html = " · ".join(contact_lines)

    pic = profile_pic or ""
    pic_block = (
        f'<img src="{html.escape(pic)}" alt="{html.escape(name)}" class="avatar" />'
        if pic
        else f'<div class="avatar avatar-fallback">{html.escape(name[0])}</div>'
    )

    stats_html = ""
    for i, item in enumerate(stats):
        label, value = item[0], item[1]
        sub = item[2] if len(item) > 2 else ""
        stats_html += f"""
        <div class="stat">
          <span class="stat-value">{html.escape(value)}</span>
          <span class="stat-label">{html.escape(label)}</span>
          {f'<span class="stat-sub">{html.escape(sub)}</span>' if sub else ''}
        </div>"""

    audience_html = "".join(
        f'<div class="aud-item"><span class="aud-val">{html.escape(v)}</span><span class="aud-lbl">{html.escape(k)}</span></div>'
        for k, v in audience
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Media Kit — {html.escape(name)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --ink: #14110f;
      --cream: #f7f2ea;
      --gold: #b8923a;
      --purple: #5c3d8a;
      --muted: #6b635a;
      --line: rgba(20, 17, 15, 0.12);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    @page {{
      size: A4 portrait;
      margin: 8mm;
    }}

    html, body {{
      font-family: "DM Sans", system-ui, sans-serif;
      font-size: 9pt;
      color: var(--ink);
      background: #e8e2d8;
      line-height: 1.35;
    }}

    .page {{
      width: 210mm;
      min-height: 297mm;
      max-height: 297mm;
      margin: 0 auto;
      background: var(--cream);
      padding: 10mm 11mm 8mm;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      gap: 5mm;
      overflow: hidden;
    }}

    @media screen {{
      .page {{
        margin: 16px auto;
        box-shadow: 0 8px 40px rgba(0,0,0,.12);
      }}
    }}

    @media print {{
      html, body {{ background: white; }}
      .page {{ box-shadow: none; margin: 0; }}
      .no-print {{ display: none !important; }}
    }}

    .hero {{
      display: grid;
      grid-template-columns: 22mm 1fr auto;
      gap: 5mm;
      align-items: center;
      padding-bottom: 4mm;
      border-bottom: 1px solid var(--line);
    }}

    .avatar {{
      width: 22mm;
      height: 22mm;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid var(--gold);
    }}

    .avatar-fallback {{
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, var(--purple), var(--gold));
      color: white;
      font-family: "Cormorant Garamond", serif;
      font-size: 18pt;
      font-weight: 600;
    }}

    .hero h1 {{
      font-family: "Cormorant Garamond", serif;
      font-size: 22pt;
      font-weight: 600;
      letter-spacing: -0.02em;
      line-height: 1.05;
    }}

    .hero .tagline {{
      color: var(--muted);
      font-size: 8.5pt;
      margin-top: 1.5mm;
      max-width: 120mm;
    }}

    .hero-meta {{
      text-align: right;
    }}

    .handle {{
      font-weight: 600;
      color: var(--purple);
      font-size: 10pt;
    }}

    .badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 2mm;
      justify-content: flex-end;
      margin-top: 2mm;
    }}

    .badge {{
      font-size: 6.5pt;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 1mm 2.5mm;
      border: 1px solid var(--gold);
      color: var(--gold);
      border-radius: 999px;
    }}

    .section-title {{
      font-size: 6.5pt;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--muted);
      margin-bottom: 2.5mm;
    }}

    .stats {{
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 2.5mm;
    }}

    .stat {{
      background: white;
      border: 1px solid var(--line);
      border-radius: 3mm;
      padding: 3mm 2.5mm;
      text-align: center;
    }}

    .stat-value {{
      display: block;
      font-family: "Cormorant Garamond", serif;
      font-size: 15pt;
      font-weight: 600;
      color: var(--ink);
      line-height: 1;
    }}

    .stat-label {{
      display: block;
      font-size: 6.5pt;
      font-weight: 600;
      margin-top: 1mm;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .stat-sub {{
      display: block;
      font-size: 6pt;
      color: var(--muted);
      margin-top: 0.5mm;
    }}

    .main {{
      display: grid;
      grid-template-columns: 1fr 1.15fr;
      gap: 5mm;
      min-height: 0;
    }}

    .col {{
      display: flex;
      flex-direction: column;
      gap: 4mm;
      min-height: 0;
    }}

    .audience {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 2mm;
    }}

    .aud-item {{
      background: white;
      border: 1px solid var(--line);
      border-radius: 2.5mm;
      padding: 2.5mm;
      text-align: center;
    }}

    .aud-val {{
      display: block;
      font-weight: 600;
      font-size: 11pt;
      color: var(--purple);
    }}

    .aud-lbl {{
      font-size: 6pt;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .brands {{
      display: flex;
      flex-wrap: wrap;
      gap: 1.5mm;
    }}

    .brand {{
      font-size: 7pt;
      padding: 1.2mm 2.5mm;
      background: white;
      border: 1px solid var(--line);
      border-radius: 999px;
    }}

    .cases {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.5mm;
    }}

    .case {{
      background: white;
      border: 1px solid var(--line);
      border-left: 2px solid var(--gold);
      border-radius: 2.5mm;
      padding: 3mm;
    }}

    .case-brand {{
      font-size: 6pt;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--purple);
      font-weight: 600;
    }}

    .case h3 {{
      font-family: "Cormorant Garamond", serif;
      font-size: 11pt;
      font-weight: 600;
      margin: 1mm 0;
      line-height: 1.15;
    }}

    .case-metrics {{
      font-size: 7.5pt;
      font-weight: 600;
    }}

    .case-note {{
      font-size: 6.5pt;
      color: var(--muted);
      margin-top: 1mm;
    }}

    .services ul {{
      list-style: none;
      display: grid;
      gap: 2mm;
    }}

    .services li {{
      background: white;
      border: 1px solid var(--line);
      border-radius: 2.5mm;
      padding: 2.5mm 3mm;
      display: flex;
      flex-direction: column;
      gap: 0.5mm;
    }}

    .services strong {{
      font-size: 8pt;
    }}

    .services span {{
      font-size: 7pt;
      color: var(--muted);
    }}

    .contact-box {{
      margin-top: auto;
      background: var(--ink);
      color: var(--cream);
      border-radius: 3mm;
      padding: 4mm;
    }}

    .contact-box .section-title {{
      color: rgba(247, 242, 234, 0.6);
    }}

    .contact-cta {{
      font-family: "Cormorant Garamond", serif;
      font-size: 14pt;
      font-weight: 600;
      color: var(--gold);
    }}

    .contact-detail {{
      font-size: 8pt;
      margin-top: 1.5mm;
    }}

    .pricing {{
      font-size: 7pt;
      color: rgba(247, 242, 234, 0.75);
      margin-top: 2mm;
    }}

    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 6pt;
      color: var(--muted);
      border-top: 1px solid var(--line);
      padding-top: 2.5mm;
    }}

    .print-hint {{
      position: fixed;
      bottom: 12px;
      right: 12px;
      background: var(--ink);
      color: white;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      z-index: 99;
    }}

    .print-hint kbd {{
      background: rgba(255,255,255,.15);
      padding: 2px 6px;
      border-radius: 4px;
    }}
  </style>
</head>
<body>
  <p class="print-hint no-print">Exportar PDF: <kbd>Ctrl+P</kbd> → Salvar como PDF · Margens: Nenhuma</p>

  <div class="page">
    <header class="hero">
      {pic_block}
      <div>
        <h1>{html.escape(name)}</h1>
        <p class="tagline">{html.escape(config.get("tagline", ""))}</p>
      </div>
      <div class="hero-meta">
        <div class="handle">@{html.escape(username)}</div>
        <div class="badges">{badges_html}</div>
      </div>
    </header>

    <section>
      <h2 class="section-title">Números · Instagram</h2>
      <div class="stats">{stats_html}</div>
    </section>

    <div class="main">
      <div class="col">
        <section>
          <h2 class="section-title">Audiência · 30 dias</h2>
          <div class="audience">{audience_html}</div>
        </section>

        <section>
          <h2 class="section-title">Marcas &amp; parcerias</h2>
          <div class="brands">{brands_html}</div>
        </section>

        <section class="contact-box">
          <h2 class="section-title">Contato comercial</h2>
          <p class="contact-cta">{html.escape(contact.get("cta", "Parcerias via DM"))}</p>
          <p class="contact-detail">{contact_html}</p>
          <p class="pricing">{html.escape(config.get("pricing_note", ""))}</p>
        </section>
      </div>

      <div class="col">
        <section>
          <h2 class="section-title">Cases em destaque</h2>
          <div class="cases">{cases_html}</div>
        </section>

        <section class="services">
          <h2 class="section-title">Formatos disponíveis</h2>
          <ul>{services_html}</ul>
        </section>
      </div>
    </div>

    <footer class="footer">
      <span>Media Kit · Modelo A · gerado em {html.escape(metrics.get("generated_at", "")[:10])}</span>
      <span>Métricas oficiais 30d: {html.escape(period)} · Reels: amostra API (últimos 30 posts)</span>
    </footer>
  </div>
</body>
</html>"""


def export_pdf(html_path: Path, pdf_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    uri = html_path.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 794, "height": 1123})
        page.goto(uri, wait_until="networkidle")
        page.wait_for_timeout(800)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def get_reel_thumbnails(snapshot: dict, limit: int = 3) -> list[dict]:
    posts = snapshot.get("media", [])
    picks: list[dict] = []
    for post in posts:
        if post.get("media_type") in ("VIDEO", "REEL") and post.get("thumbnail_url"):
            picks.append({"url": post["thumbnail_url"], "permalink": post.get("permalink", "")})
        if len(picks) >= limit:
            break
    return picks[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera media kit HTML (Modelo A)")
    parser.add_argument(
        "--style",
        choices=("luxe", "glow", "editorial", "classic"),
        default="luxe",
        help="luxe = portfolio web + PDF ivory (padrao); glow/editorial/classic = versoes anteriores",
    )
    parser.add_argument("--pdf", action="store_true", help="Exporta media-kit.pdf via Playwright")
    parser.add_argument("--all", action="store_true", help="Gera portfolio.html + media-kit.pdf (recomendado)")
    args = parser.parse_args()

    if SNAPSHOT.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_mediakit_metrics.py")],
            check=True,
            cwd=str(ROOT),
        )

    if not METRICS.exists():
        raise SystemExit(f"Arquivo não encontrado: {METRICS}\nRode: python scripts/build_mediakit_metrics.py")

    metrics = load_json(METRICS)
    config = load_json(CONFIG) if CONFIG.exists() else {}

    profile_pic = None
    snapshot = {}
    if SNAPSHOT.exists():
        snapshot = load_json(SNAPSHOT)
        profile_pic = snapshot.get("profile", {}).get("profile_picture_url")

    h = metrics.setdefault("media_kit_highlights", {})
    app = metrics.get("app_insights_official", {}).get("period_30d", {})
    if app.get("interaction_rate_on_views_pct"):
        h["interaction_rate_on_views_pct"] = app["interaction_rate_on_views_pct"]

    period = period_label(metrics)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    want_pdf = args.pdf or args.all or args.style == "luxe"

    if args.style == "luxe":
        assets = prepare_assets(snapshot, config, limit_reels=999, fmt_num=fmt_num) if snapshot else {"profile_data_uri": "", "reels": [], "cases": [], "case_thumbnails": {}}
        assets_pdf = prepare_assets(snapshot, config, limit_reels=6, fmt_num=fmt_num) if snapshot else assets
        portfolio = build_portfolio(metrics, config, assets, period, fmt_num)
        print_html = build_glow(metrics, config, assets_pdf, period, fmt_num)
        OUT_PORTFOLIO.write_text(portfolio, encoding="utf-8")
        OUT_HTML.write_text(print_html, encoding="utf-8")
        print(f"Portfolio web: {OUT_PORTFOLIO}")
        print(f"PDF source:    {OUT_HTML}")
        if want_pdf:
            export_pdf(OUT_HTML, OUT_PDF)
            print(f"PDF:           {OUT_PDF}")
        return

    if args.style == "glow":
        assets = prepare_assets(snapshot, config, fmt_num=fmt_num) if snapshot else {"profile_data_uri": "", "reels": []}
        content = build_glow(metrics, config, assets, period, fmt_num)
    elif args.style == "editorial":
        content = build_editorial(
            metrics, config, profile_pic, get_reel_thumbnails(snapshot), period, fmt_num
        )
    else:
        content = build_html(metrics, config, profile_pic)

    OUT_HTML.write_text(content, encoding="utf-8")
    print(f"HTML ({args.style}): {OUT_HTML}")

    if args.pdf or args.all:
        export_pdf(OUT_HTML, OUT_PDF)
        print(f"PDF:  {OUT_PDF}")


if __name__ == "__main__":
    main()
