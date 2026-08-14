"""Templates visuais para media kit (inspirados em layouts Canva beauty/UGC)."""

from __future__ import annotations

import html as html_mod


def build_editorial(
    metrics: dict,
    config: dict,
    profile_pic: str | None,
    reel_thumbs: list[dict],
    period: str,
    fmt_num,
) -> str:
    h = metrics.get("media_kit_highlights", {})
    profile = metrics.get("profile", {})
    username = profile.get("username", config["contact"]["instagram"])
    name = profile.get("name", "Taty Zacharias").split("|")[0].strip()
    contact = config.get("contact", {})

    about = (
        "Creator de beleza e cabelo cacheado na Baixada Santista. "
        "Reels autênticos, tutoriais e UGC para marcas de hair & beauty — "
        "com representatividade e conversa real com a audiência."
    )

    hero_stats = [
        (fmt_num(h.get("followers", 0)), "seguidores"),
        (fmt_num(h.get("views_30d_official", 0)), "views · 30d"),
        (f"{h.get('interaction_rate_on_views_pct', 16.5)}%", "interação"),
    ]

    grid_stats = [
        (fmt_num(h.get("interactions_30d_official", 0)), "Interações", "30 dias"),
        (fmt_num(h.get("avg_reach_per_reel", 0)), "Alcance/Reel", "últimos 30 posts"),
        (fmt_num(h.get("avg_shares_per_reel", 0)), "Shares/Reel", "média"),
        (str(h.get("profile_visits_30d", 117)), "Visitas perfil", "30 dias"),
        (f"{h.get('views_non_followers_pct_90d', 0)}%", "Novos públicos", "90 dias"),
        (fmt_num(h.get("avg_views_per_reel", 0)), "Views/Reel", "média"),
    ]

    audience = [
        ("Brasil", f"{h.get('brazil_audience_pct', 0)}%"),
        ("Mulheres", f"{h.get('female_audience_pct', 0)}%"),
        ("25–44", f"{h.get('core_age_25_44_pct', 0)}%"),
        ("Baixada", f"{h.get('baixada_santista_pct', 0)}%"),
    ]

    pic = profile_pic or ""
    hero_img = (
        f'<img src="{html_mod.escape(pic)}" alt="" class="hero-photo" />'
        if pic
        else '<div class="hero-photo hero-photo-fallback"></div>'
    )

    hero_stats_html = "".join(
        f'<div class="hero-stat"><span>{html_mod.escape(v)}</span><small>{html_mod.escape(l)}</small></div>'
        for v, l in hero_stats
    )

    grid_html = "".join(
        f"""<div class="gstat">
          <div class="gstat-val">{html_mod.escape(v)}</div>
          <div class="gstat-lbl">{html_mod.escape(l)}</div>
          <div class="gstat-sub">{html_mod.escape(s)}</div>
        </div>"""
        for v, l, s in grid_stats
    )

    aud_html = "".join(
        f"""<div class="aud">
          <div class="aud-bar"><span style="width:{html_mod.escape(v.replace('%',''))}%"></span></div>
          <div class="aud-meta"><strong>{html_mod.escape(v)}</strong> {html_mod.escape(k)}</div>
        </div>"""
        for k, v in audience
    )

    brands = config.get("brands", [])
    brands_html = "".join(
        f'<span>{html_mod.escape(b["name"])}</span>' for b in brands[:8]
    )
    if len(brands) > 8:
        brands_html += f'<span class="more">+{len(brands) - 8}</span>'

    cases = config.get("cases", [])[:3]
    cases_html = ""
    for i, case in enumerate(cases):
        thumb = reel_thumbs[i]["url"] if i < len(reel_thumbs) else ""
        thumb_block = (
            f'<img src="{html_mod.escape(thumb)}" alt="" />' if thumb else '<div class="thumb-ph"></div>'
        )
        cases_html += f"""
        <div class="work">
          <div class="work-thumb">{thumb_block}</div>
          <div class="work-body">
            <p class="work-brand">{html_mod.escape(case.get("brand", ""))}</p>
            <h3>{html_mod.escape(case.get("title", ""))}</h3>
            <p>{html_mod.escape(case.get("metrics", ""))}</p>
          </div>
        </div>"""

    services_html = "".join(
        f'<li><strong>{html_mod.escape(s["name"])}</strong> — {html_mod.escape(s.get("detail", ""))}</li>'
        for s in config.get("services", [])
    )

    badges = "".join(
        f'<span class="pill">{html_mod.escape(b)}</span>' for b in config.get("badges", [])
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <title>Media Kit — {html_mod.escape(name)}</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #faf6f1;
      --paper: #fffdf9;
      --ink: #2c211e;
      --muted: #7a6b63;
      --peach: #e8a98a;
      --rose: #c9788a;
      --sand: #e8ddd0;
      --line: rgba(44,33,30,.1);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    @page {{ size: A4 portrait; margin: 0; }}
    html, body {{
      font-family: Outfit, system-ui, sans-serif;
      font-size: 8.5pt;
      color: var(--ink);
      background: #ddd5cb;
    }}
    .sheet {{
      width: 210mm;
      height: 297mm;
      margin: 0 auto;
      background: var(--bg);
      display: grid;
      grid-template-columns: 78mm 1fr;
      grid-template-rows: 1fr auto;
      overflow: hidden;
    }}
    @media screen {{
      .sheet {{ margin: 16px auto; box-shadow: 0 12px 48px rgba(0,0,0,.15); }}
    }}
    @media print {{
      html, body {{ background: white; }}
      .hint {{ display: none !important; }}
    }}

    .hero {{
      grid-row: 1 / 3;
      position: relative;
      background: #1a1412;
      color: white;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
    }}
    .hero-photo {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center top;
    }}
    .hero-photo-fallback {{
      background: linear-gradient(160deg, #3d2c29 0%, #c9788a 100%);
    }}
    .hero-overlay {{
      position: relative;
      z-index: 1;
      padding: 8mm 7mm;
      background: linear-gradient(transparent 0%, rgba(26,20,18,.55) 35%, rgba(26,20,18,.92) 100%);
      min-height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      gap: 4mm;
    }}
    .hero .eyebrow {{
      font-size: 6.5pt;
      letter-spacing: .18em;
      text-transform: uppercase;
      color: var(--peach);
      font-weight: 500;
    }}
    .hero h1 {{
      font-family: "Playfair Display", serif;
      font-size: 26pt;
      font-weight: 600;
      line-height: .95;
      letter-spacing: -.02em;
    }}
    .hero .handle {{
      font-size: 9pt;
      font-weight: 500;
      opacity: .9;
    }}
    .pills {{ display: flex; flex-wrap: wrap; gap: 2mm; }}
    .pill {{
      font-size: 6pt;
      font-weight: 600;
      letter-spacing: .06em;
      text-transform: uppercase;
      padding: 1.2mm 2.5mm;
      border: 1px solid rgba(255,255,255,.35);
      border-radius: 999px;
    }}
    .hero-stats {{
      display: flex;
      gap: 4mm;
      margin-top: 2mm;
      padding-top: 4mm;
      border-top: 1px solid rgba(255,255,255,.2);
    }}
    .hero-stat span {{
      display: block;
      font-family: "Playfair Display", serif;
      font-size: 14pt;
      font-weight: 600;
    }}
    .hero-stat small {{
      font-size: 6pt;
      text-transform: uppercase;
      letter-spacing: .08em;
      opacity: .75;
    }}

    .main {{
      padding: 7mm 8mm 5mm;
      display: flex;
      flex-direction: column;
      gap: 4mm;
      min-height: 0;
    }}
    .label {{
      font-size: 6pt;
      font-weight: 600;
      letter-spacing: .14em;
      text-transform: uppercase;
      color: var(--rose);
      margin-bottom: 2mm;
    }}
    .about {{
      font-size: 8pt;
      line-height: 1.45;
      color: var(--muted);
      max-width: 100%;
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 2.5mm;
    }}
    .gstat {{
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 3mm;
      padding: 3mm;
      text-align: center;
    }}
    .gstat-val {{
      font-family: "Playfair Display", serif;
      font-size: 13pt;
      font-weight: 600;
      color: var(--ink);
      line-height: 1;
    }}
    .gstat-lbl {{
      font-size: 6.5pt;
      font-weight: 600;
      margin-top: 1mm;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    .gstat-sub {{
      font-size: 5.5pt;
      color: var(--muted);
      margin-top: .5mm;
    }}
    .audience {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; }}
    .aud {{ background: var(--paper); border-radius: 2.5mm; padding: 2.5mm; border: 1px solid var(--line); }}
    .aud-bar {{
      height: 3px;
      background: var(--sand);
      border-radius: 999px;
      overflow: hidden;
      margin-bottom: 1.5mm;
    }}
    .aud-bar span {{
      display: block;
      height: 100%;
      background: linear-gradient(90deg, var(--peach), var(--rose));
      border-radius: 999px;
    }}
    .aud-meta {{ font-size: 7pt; color: var(--muted); }}
    .aud-meta strong {{ color: var(--ink); font-size: 9pt; }}

    .brands {{
      display: flex;
      flex-wrap: wrap;
      gap: 1.5mm;
    }}
    .brands span {{
      font-size: 6.5pt;
      padding: 1.2mm 2.5mm;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 999px;
    }}
    .brands .more {{ background: var(--sand); border: none; }}

    .bottom {{
      grid-column: 2;
      background: var(--paper);
      border-top: 1px solid var(--line);
      padding: 5mm 8mm 6mm;
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 5mm;
      align-items: start;
    }}
    .works {{ display: grid; gap: 2.5mm; }}
    .work {{
      display: grid;
      grid-template-columns: 14mm 1fr;
      gap: 2.5mm;
      align-items: center;
    }}
    .work-thumb {{
      width: 14mm;
      height: 18mm;
      border-radius: 2mm;
      overflow: hidden;
      background: var(--sand);
      box-shadow: 0 2px 8px rgba(0,0,0,.08);
    }}
    .work-thumb img {{ width: 100%; height: 100%; object-fit: cover; }}
    .thumb-ph {{ width: 100%; height: 100%; background: linear-gradient(135deg, var(--sand), var(--peach)); }}
    .work-brand {{
      font-size: 5.5pt;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--rose);
      font-weight: 600;
    }}
    .work h3 {{
      font-family: "Playfair Display", serif;
      font-size: 9pt;
      font-weight: 600;
      line-height: 1.15;
      margin: .5mm 0;
    }}
    .work-body p:last-child {{ font-size: 6.5pt; color: var(--muted); }}

    .side {{ display: flex; flex-direction: column; gap: 3mm; }}
    .services ul {{
      list-style: none;
      font-size: 7pt;
      color: var(--muted);
      display: grid;
      gap: 1.5mm;
    }}
    .services strong {{ color: var(--ink); font-weight: 600; }}
    .cta-box {{
      background: var(--ink);
      color: white;
      border-radius: 3mm;
      padding: 4mm;
    }}
    .cta-box .label {{ color: var(--peach); }}
    .cta-box h2 {{
      font-family: "Playfair Display", serif;
      font-size: 13pt;
      font-weight: 600;
      margin: 1mm 0;
    }}
    .cta-box p {{ font-size: 7.5pt; opacity: .85; }}
    .cta-box .pricing {{
      font-size: 6.5pt;
      opacity: .65;
      margin-top: 2mm;
    }}
    .foot {{
      grid-column: 1 / -1;
      font-size: 5.5pt;
      color: var(--muted);
      text-align: center;
      padding-top: 2mm;
      border-top: 1px solid var(--line);
      margin-top: 1mm;
    }}

    .hint {{
      position: fixed; bottom: 12px; right: 12px;
      background: var(--ink); color: white;
      padding: 8px 14px; border-radius: 8px; font-size: 11px;
    }}
  </style>
</head>
<body>
  <p class="hint">Canva-style v2 · Ctrl+P → PDF · Margens: Nenhuma</p>
  <div class="sheet">
    <aside class="hero">
      {hero_img}
      <div class="hero-overlay">
        <p class="eyebrow">Media Kit · {html_mod.escape(period)}</p>
        <h1>{html_mod.escape(name)}</h1>
        <p class="handle">@{html_mod.escape(username)}</p>
        <div class="pills">{badges}</div>
        <div class="hero-stats">{hero_stats_html}</div>
      </div>
    </aside>

    <section class="main">
      <div>
        <p class="label">Sobre</p>
        <p class="about">{html_mod.escape(about)}</p>
      </div>
      <div>
        <p class="label">Performance · Instagram</p>
        <div class="stats-grid">{grid_html}</div>
      </div>
      <div>
        <p class="label">Audiência · 30 dias</p>
        <div class="audience">{aud_html}</div>
      </div>
      <div>
        <p class="label">Marcas & parcerias</p>
        <div class="brands">{brands_html}</div>
      </div>
    </section>

    <footer class="bottom">
      <div>
        <p class="label">Conteúdos em destaque</p>
        <div class="works">{cases_html}</div>
      </div>
      <div class="side">
        <div class="services">
          <p class="label">Formatos</p>
          <ul>{services_html}</ul>
        </div>
        <div class="cta-box">
          <p class="label">Contato</p>
          <h2>{html_mod.escape(contact.get("cta", "Parcerias via DM"))}</h2>
          <p>@{html_mod.escape(contact.get("instagram", username))}</p>
          <p class="pricing">{html_mod.escape(config.get("pricing_note", ""))}</p>
        </div>
      </div>
      <p class="foot">Media Kit · @tatyzacharias · métricas oficiais {html_mod.escape(period)} · Reels: amostra API</p>
    </footer>
  </div>
</body>
</html>"""
