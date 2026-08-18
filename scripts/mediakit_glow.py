"""Media Kit '013 Glow' v2 — editorial beauty, layout refinado."""

from __future__ import annotations

import html as H
from datetime import datetime


def build_glow(metrics: dict, config: dict, assets: dict, period: str, fmt_num) -> str:
    mk = metrics.get("media_kit_highlights", {})
    profile = metrics.get("profile", {})
    username = profile.get("username", "tatyzacharias")
    name = profile.get("name", "Taty Zacharias").split("|")[0].strip()
    display_name = (config.get("display_name") or name).strip()
    name_parts = display_name.split()
    first = name_parts[0] if name_parts else "Tatiana"
    rest = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Zacharias"
    contact = config.get("contact", {})

    profile_img = assets.get("hero_data_uri") or assets.get("profile_data_uri") or ""
    photo = (
        f'<img src="{H.escape(profile_img)}" alt="" class="portrait" />'
        if profile_img
        else '<div class="portrait portrait-empty"></div>'
    )

    metrics_row = [
        (fmt_num(mk.get("followers", 0)), "Seguidores", ""),
        (fmt_num(mk.get("views_30d_official", 0)), "Views", "30d"),
        (fmt_num(mk.get("interactions_30d_official", 0)), "Interações", "30d"),
        (f"{mk.get('interaction_rate_on_views_pct', 16.5)}%", "Engajamento", "views"),
        (fmt_num(mk.get("median_views_per_reel", mk.get("avg_views_per_reel", 0))), "Views", "med./Reel"),
        (f"{mk.get('views_non_followers_pct_90d', 0)}%", "Novos públicos", "90d"),
    ]
    metrics_html = "".join(
        f"""<div class="metric">
          <div class="metric-v">{H.escape(v)}</div>
          <div class="metric-l">{H.escape(l)}</div>
          {f'<div class="metric-s">{H.escape(s)}</div>' if s else ''}
        </div>"""
        for v, l, s in metrics_row
    )

    female = float(mk.get("female_audience_pct", 71.8))
    brazil = float(mk.get("brazil_audience_pct", 84))
    core_age = float(mk.get("core_age_25_44_pct", 57.1))
    baixada = float(mk.get("baixada_santista_pct", 24.2))

    aud_cards = [
        ("Brasil", f"{brazil}%"),
        ("Mulheres", f"{female}%"),
        ("25–44 anos", f"{core_age}%"),
        ("Baixada", f"{baixada}%"),
    ]
    aud_html = "".join(
        f'<div class="aud-card"><b>{H.escape(v)}</b><span>{H.escape(k)}</span></div>'
        for k, v in aud_cards
    )

    reels = assets.get("reels", [])
    reel_cards = ""
    for reel in reels[:4]:
        uri = reel.get("data_uri", "")
        img = f'<img src="{H.escape(uri)}" alt="" />' if uri else ""
        brand = reel.get("brand", "Beauty")
        reel_cards += f"""
        <article class="reel-card">
          <div class="reel-img">{img}<span class="reel-brand">{H.escape(brand)}</span></div>
        </article>"""

    brand_pills = "".join(
        f'<span>{H.escape(b["name"])}</span>' for b in config.get("brands", [])
    )

    cases = assets.get("cases") or config.get("cases", [])
    cases_html = "".join(
        f"""<article class="case-card">
          <span class="case-brand">{H.escape(c.get("brand", ""))}</span>
          <h4>{H.escape(c.get("title", ""))}</h4>
          <p>{H.escape(c.get("metrics", ""))}</p>
          <small>{H.escape(c.get("note", ""))}</small>
        </article>"""
        for c in cases
    )
    if not cases_html:
        cases_html = (
            '<p class="cases-empty">Parcerias com marcas de hair &amp; beauty — '
            "Reels patrocinados e UGC para campanhas.</p>"
        )

    services = config.get("services", [])
    svc_html = "".join(
        f"""<li>
          <span class="svc-n">{H.escape(s["name"])}</span>
          <span class="svc-d">{H.escape(s.get("detail", ""))}</span>
        </li>"""
        for s in services[:4]
    )

    about = config.get("about", config.get("tagline", ""))
    header_badge = config.get("header_badge", "Beauty · Hair · Makeup")
    value_props = config.get("value_props", [])
    props_html = "".join(f"<li>{H.escape(p)}</li>" for p in value_props[:3])

    pdf_rev = datetime.now().strftime("%d/%m/%Y")

    email = (contact.get("email") or "").strip()
    email_html = f'<strong class="cta-email">{H.escape(email)}</strong>'
    contact_tag = H.escape(contact.get("cta", "Parcerias via e-mail"))

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<title>Media Kit — {H.escape(display_name)}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>
:root {{
  --bg:#52463E;
  --surface:#5E5047;
  --elevated:#6B5B51;
  --text:#FBF7F2;
  --soft:rgba(251,247,242,.82);
  --dim:rgba(251,247,242,.58);
  --blush:#E8A89A;
  --peach:#E8956F;
  --mauve:#C9A0A8;
  --copper:#D4846A;
  --line:rgba(251,247,242,.16);
  --glow-warm:rgba(232,149,111,.48);
  --glow-rose:rgba(232,168,154,.38);
  --glow-mauve:rgba(201,160,168,.28);
}}
* {{ box-sizing:border-box; margin:0; padding:0; }}
@page {{ size:A4 portrait; margin:0; }}
html,body {{
  font-family:"Plus Jakarta Sans",system-ui,sans-serif;
  font-size:8pt; color:var(--text); background:#463C35;
}}
.sheet {{
  width:210mm; height:297mm; margin:0 auto;
  background:linear-gradient(165deg,#5C4F47 0%,#52463E 50%,#4A4038 100%);
  overflow:hidden; position:relative;
  display:flex; flex-direction:column;
}}
.sheet::before {{
  content:""; position:absolute; inset:0; pointer-events:none;
  background:
    radial-gradient(ellipse 75% 55% at 92% 6%, var(--glow-warm), transparent 58%),
    radial-gradient(ellipse 60% 50% at 6% 92%, var(--glow-rose), transparent 54%),
    radial-gradient(ellipse 50% 40% at 48% 38%, var(--glow-mauve), transparent 52%);
}}
@media screen {{
  .sheet {{ margin:20px auto; box-shadow:0 20px 60px rgba(0,0,0,.5); }}
}}
@media print {{ .screen-only {{ display:none !important; }} }}

.pad {{ padding:8mm 9mm; position:relative; z-index:1; }}

.hdr {{
  display:flex; justify-content:space-between; align-items:center;
  padding-bottom:4mm; border-bottom:1px solid var(--line);
}}
.hdr-left {{ display:flex; flex-direction:column; gap:1mm; }}
.hdr-kicker {{
  font-size:5.5pt; font-weight:700; letter-spacing:.22em;
  text-transform:uppercase; color:var(--peach);
}}
.hdr-sub {{ font-size:6pt; color:var(--dim); letter-spacing:.06em; }}
.hdr-badge {{
  font-size:6pt; font-weight:600; letter-spacing:.1em; text-transform:uppercase;
  padding:2mm 3.5mm; border-radius:999px;
  border:1px solid var(--line); background:rgba(255,255,255,.03);
}}

.hero {{
  display:grid; grid-template-columns:46mm 1fr; gap:6mm;
  padding:5mm 0 4mm; align-items:center;
}}
.photo-wrap {{ position:relative; }}
.photo-wrap::before {{
  content:""; position:absolute; inset:-2mm;
  border:1px solid rgba(232,160,168,.35); border-radius:2mm;
  transform:rotate(-2deg); z-index:0;
}}
.portrait {{
  position:relative; z-index:1;
  width:100%; height:58mm; object-fit:cover; object-position:center 15%;
  border-radius:2mm; display:block;
  box-shadow:0 12px 32px rgba(0,0,0,.45);
}}
.portrait-empty {{
  height:58mm; border-radius:2mm;
  background:linear-gradient(135deg,var(--mauve),var(--peach));
}}

.intro h1 {{
  font-family:"Cormorant Garamond",serif;
  font-size:30pt; font-weight:400; line-height:.92; letter-spacing:-.01em;
}}
.intro h1 em {{
  font-style:italic; color:var(--peach);
}}
.intro .about {{
  margin-top:2.5mm; font-size:7.5pt; line-height:1.5;
  color:var(--soft); max-width:108mm;
}}
.intro .handle {{
  margin-top:2.5mm; font-size:8.5pt; font-weight:700; color:var(--copper);
}}
.value-list {{
  margin-top:3mm; padding-left:3.5mm;
  border-left:2px solid var(--peach);
  list-style:none; display:grid; gap:1.2mm;
}}
.value-list li {{
  font-size:6.5pt; color:var(--soft); line-height:1.35;
  padding-left:2mm; position:relative;
}}
.value-list li::before {{
  content:""; position:absolute; left:-3.5mm; top:.55em;
  width:4px; height:4px; border-radius:50%; background:var(--blush);
}}

.metrics {{
  display:grid; grid-template-columns:repeat(6,1fr); gap:2mm;
  padding:3mm 0 4mm; border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);
}}
.metric {{
  background:var(--surface); border:1px solid var(--line);
  border-radius:2.5mm; padding:2.5mm; text-align:center;
}}
.metric-v {{
  font-family:"Cormorant Garamond",serif;
  font-size:14pt; line-height:1; color:var(--text);
}}
.metric-l {{
  font-size:5.5pt; font-weight:700; text-transform:uppercase;
  letter-spacing:.08em; margin-top:1mm; color:var(--soft);
}}
.metric-s {{ font-size:5pt; color:var(--dim); margin-top:.3mm; }}

.body {{
  flex:1; display:grid;
  grid-template-columns:1fr 34mm;
  gap:4mm; min-height:0; padding-top:3mm;
}}

.reels-head {{
  display:flex; justify-content:space-between; align-items:baseline;
  margin-bottom:2mm;
}}
.reels-head h2, .panel h2, .foot-grid h2 {{
  font-size:5.5pt; font-weight:700; letter-spacing:.16em;
  text-transform:uppercase; color:var(--blush);
}}
.reels-head span {{ font-size:5.5pt; color:var(--dim); }}

.reels {{
  display:grid; grid-template-columns:repeat(4,1fr); gap:2.5mm;
}}
.reel-card {{ text-align:left; }}
.reel-img {{
  position:relative; aspect-ratio:9/14; border-radius:2mm;
  overflow:hidden; background:var(--elevated);
  border:1px solid var(--line);
  box-shadow:0 6px 16px rgba(0,0,0,.35);
}}
.reel-img img {{ width:100%; height:100%; object-fit:cover; }}
.reel-brand {{
  position:absolute; left:0; right:0; bottom:0;
  padding:2mm 2mm 1.5mm;
  font-size:5pt; font-weight:700; letter-spacing:.06em;
  text-transform:uppercase;
  background:linear-gradient(transparent, rgba(74,64,56,.9));
  color:var(--text);
}}

.panel {{
  background:var(--surface); border:1px solid var(--line);
  border-radius:3mm; padding:3mm;
  display:flex; flex-direction:column; gap:2mm;
}}
.donut-wrap {{ text-align:center; padding:1mm 0 2mm; }}
.donut {{
  width:22mm; height:22mm; border-radius:50%; margin:0 auto 2mm;
  background:conic-gradient(
    var(--peach) 0 {female}%,
    rgba(255,255,255,.12) {female}% 100%
  );
  display:flex; align-items:center; justify-content:center;
  position:relative;
}}
.donut::after {{
  content:""; position:absolute; inset:4.5mm;
  background:var(--surface); border-radius:50%;
}}
.donut b {{
  position:relative; z-index:1;
  font-family:"Cormorant Garamond",serif;
  font-size:11pt; color:var(--text);
}}
.donut-label {{ font-size:5.5pt; color:var(--dim); text-transform:uppercase; letter-spacing:.1em; }}
.aud-grid {{
  display:grid; grid-template-columns:1fr 1fr; gap:1.5mm;
}}
.aud-card {{
  background:var(--elevated); border-radius:2mm;
  padding:2mm; text-align:center; border:1px solid var(--line);
}}
.aud-card b {{
  display:block; font-family:"Cormorant Garamond",serif;
  font-size:11pt; line-height:1;
}}
.aud-card span {{
  font-size:5pt; color:var(--dim); text-transform:uppercase;
  letter-spacing:.06em; margin-top:.5mm; display:block;
}}

.foot-grid {{
  border-top:1px solid var(--line);
  padding-top:3.5mm; margin-top:auto;
  display:grid;
  grid-template-columns:1.15fr 1fr;
  gap:3mm 4mm;
}}
.brands-pills {{
  display:flex; flex-wrap:wrap; gap:1.2mm; margin-top:1.5mm;
}}
.brands-pills span {{
  font-size:5.5pt; padding:1mm 2mm;
  background:var(--surface); border:1px solid var(--line);
  border-radius:999px; color:var(--soft);
}}

.cases {{
  display:flex; justify-content:space-between; align-items:stretch;
  gap:1.6mm; width:100%; margin-top:1.5mm;
}}
.case-card {{
  flex:1 1 0; min-width:0;
  background:var(--surface); border:1px solid var(--line);
  border-radius:2mm; padding:2mm 1.6mm;
  border-top:2px solid var(--peach);
}}
.foot-cases {{ grid-column:1 / -1; }}
.case-brand {{
  font-size:4.8pt; font-weight:700; letter-spacing:.08em;
  text-transform:uppercase; color:var(--mauve);
}}
.case-card h4 {{
  font-family:"Cormorant Garamond",serif;
  font-size:7pt; font-weight:600; line-height:1.18;
  margin:.6mm 0;
  display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical;
  overflow:hidden;
}}
.case-card p {{ font-size:5.5pt; font-weight:600; color:var(--soft); }}
.case-card small {{ font-size:4.8pt; color:var(--dim); display:block; margin-top:.4mm; }}
.cases-empty {{ font-size:6pt; color:var(--dim); line-height:1.45; margin-top:1.5mm; }}

.services ul {{ list-style:none; margin-top:1.5mm; display:grid; gap:1.5mm; }}
.services li {{
  padding-bottom:1.5mm; border-bottom:1px solid var(--line);
}}
.services li:last-child {{ border-bottom:none; padding-bottom:0; }}
.svc-n {{ display:block; font-size:6.5pt; font-weight:600; }}
.svc-d {{ display:block; font-size:5.5pt; color:var(--dim); margin-top:.3mm; }}

.contact-bar {{
  grid-column:1 / -1;
  display:flex; flex-direction:row; align-items:center; justify-content:space-between;
  gap:3mm; padding:2.4mm 3.2mm;
  background:linear-gradient(160deg, rgba(232,160,168,.18), rgba(232,149,111,.12));
  border:1px solid rgba(232,160,168,.28);
  border-radius:3mm;
}}
.contact-tag {{
  font-family:"Cormorant Garamond",serif;
  font-style:italic; font-size:9pt; color:var(--blush);
  white-space:nowrap; flex-shrink:0;
}}
.contact-bar .cta-email {{
  font-size:6pt; font-weight:700; flex:1; text-align:center;
  line-height:1.2; word-break:break-all;
}}
.contact-note {{
  font-size:5pt; color:var(--dim); line-height:1.3;
  white-space:nowrap; flex-shrink:0; text-align:right;
}}

.footer {{
  grid-column:1/-1; text-align:center;
  font-size:5pt; letter-spacing:.14em; text-transform:uppercase;
  color:var(--dim); padding-top:2mm;
}}
</style>
</head>
<body>
<div class="sheet">
  <div class="pad" style="flex:1;display:flex;flex-direction:column;min-height:0">
    <header class="hdr">
      <div class="hdr-left">
        <span class="hdr-kicker">Media Kit · UGC Beauty</span>
        <span class="hdr-sub">{H.escape(period)} · @{H.escape(username)}</span>
      </div>
      <span class="hdr-badge">{H.escape(header_badge)}</span>
    </header>

    <section class="hero">
      <div class="photo-wrap">{photo}</div>
      <div class="intro">
        <h1>{H.escape(first)} <em>{H.escape(rest)}</em></h1>
        <p class="about">{H.escape(about)}</p>
        <p class="handle">instagram.com/{H.escape(username)}</p>
        <ul class="value-list">{props_html}</ul>
      </div>
    </section>

    <section class="metrics">{metrics_html}</section>

    <section class="body">
      <div>
        <div class="reels-head">
          <h2>Portfólio · Reels beauty</h2>
          <span>Hair · Makeup · Skincare</span>
        </div>
        <div class="reels">{reel_cards}</div>

        <div class="foot-grid" style="padding-top:4mm;margin-top:4mm">
          <div>
            <h2>Marcas & parcerias</h2>
            <div class="brands-pills">{brand_pills}</div>
          </div>
          <div class="services">
            <h2>Formatos</h2>
            <ul>{svc_html}</ul>
          </div>
          <div class="foot-cases">
            <h2>Cases em destaque</h2>
            <div class="cases">{cases_html}</div>
          </div>
          <div class="contact-bar">
            <span class="contact-tag">{contact_tag}</span>
            {email_html}
            <span class="contact-note">{H.escape(config.get("pricing_note", ""))}</span>
          </div>
          <p class="footer">013 glow · métricas oficiais {H.escape(period)} · atualizado {H.escape(pdf_rev)}</p>
        </div>
      </div>

      <aside class="panel">
        <h2>Audiência · 30d</h2>
        <div class="donut-wrap">
          <div class="donut"><b>{H.escape(str(int(female)))}%</b></div>
          <div class="donut-label">mulheres</div>
        </div>
        <div class="aud-grid">{aud_html}</div>
      </aside>
    </section>
  </div>
</div>
<p class="screen-only" style="position:fixed;bottom:12px;right:12px;background:#e8a0a8;color:#0c0a09;padding:8px 14px;border-radius:8px;font:600 11px Plus Jakarta Sans,sans-serif">
  013 Glow v2 · Ctrl+P → PDF
</p>
</body>
</html>"""
