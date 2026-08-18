"""Media Kit LUXE — portfólio web (galeria de trabalhos) + PDF."""

from __future__ import annotations

import html as H
import re
from datetime import datetime

from mediakit_assets import format_piece_views, portfolio_categories


def _pdf_download_filename(display_name: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", display_name, flags=re.UNICODE).strip().replace(" ", "-")
    day = datetime.now().strftime("%Y%m%d")
    return f"{slug or 'Media-Kit'}-Media-Kit-{day}.pdf"


def _case_highlight(metrics: str) -> str:
    nums = re.findall(r"[\d]+(?:[.,]\d+)?k?", metrics or "")
    return nums[-1] if nums else "—"


def _shared_data(metrics: dict, config: dict, assets: dict, period: str, fmt_num) -> dict:
    mk = metrics.get("media_kit_highlights", {})
    profile = metrics.get("profile", {})
    username = profile.get("username", "tatyzacharias")
    name = profile.get("name", "Taty Zacharias").split("|")[0].strip()

    stats = [
        (fmt_num(mk.get("followers", 0)), "Seguidores", ""),
        (fmt_num(mk.get("views_90d_official", mk.get("views_90d", 0))), "Views", "90d"),
        (fmt_num(mk.get("interactions_90d_official", 0)), "Interações", "90d"),
        (
            f"{mk.get('interaction_rate_reels_90d_on_views_pct', 0)}%",
            "Engajamento em Reels",
            "90d",
        ),
        (
            f"{mk.get('views_non_followers_pct_90d', 65.2)}%",
            "Novos públicos",
            "90d",
        ),
        (fmt_num(mk.get("median_views_per_reel", mk.get("avg_views_per_reel", 0))), "Views/Reel", ""),
        (fmt_num(mk.get("best_reach_per_reel", 0)), "Pico alcance", ""),
    ]

    aud = [
        ("Brasil", float(mk.get("brazil_audience_pct", 84))),
        ("Mulheres", float(mk.get("female_audience_pct", 71.8))),
        ("25–44", float(mk.get("core_age_25_44_pct", 57.1))),
        ("Baixada Santista", float(mk.get("baixada_santista_pct", 24.2))),
    ]

    reels = assets.get("reels", [])
    case_thumbs = assets.get("case_thumbnails", {})

    return {
        "mk": mk,
        "username": username,
        "name": name,
        "first": name.split()[0] if name else "Taty",
        "last": " ".join(name.split()[1:]) if len(name.split()) > 1 else "Zacharias",
        "period": period,
        "stats": stats,
        "aud": aud,
        "profile_img": assets.get("hero_data_uri") or assets.get("profile_data_uri", ""),
        "hero_video": assets.get("hero_video", ""),
        "hero_poster": assets.get("hero_poster", ""),
        "hero_float_uris": assets.get("hero_float_uris", []),
        "reels": reels,
        "case_thumbs": case_thumbs,
        "about": config.get("about", ""),
        "about_extra": config.get("about_extra") or config.get("quem_sou_extra", ""),
        "tagline": config.get("tagline", ""),
        "brands": config.get("brands", []),
        "cases": assets.get("cases") or config.get("cases", []),
        "services": config.get("services", []),
        "contact": config.get("contact", {}),
        "pricing_note": config.get("pricing_note", ""),
        "display_name": config.get("display_name") or name,
        "hero_subtitle": config.get("hero_subtitle", "UGC Creator · Beauty"),
        "fmt_num": fmt_num,
    }


def _brand_slug(brand: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", brand.lower()).strip("-")


_PLATFORM_LABEL = {
    "tiktok": "TikTok",
    "instagram": "Instagram",
    "whatsapp": "WhatsApp",
}

_FB_ROTATE = (-2.2, 1.6, -1.1, 2.0, -1.4, 1.2)


def _build_feedbacks_html(feedbacks: list[dict]) -> tuple[str, str, str]:
    if not feedbacks:
        return "", "", ""

    cards = ""
    for i, fb in enumerate(feedbacks):
        src = fb.get("asset_path") or ""
        if not src:
            continue
        platform = fb.get("platform", "instagram")
        platform_label = _PLATFORM_LABEL.get(platform, platform.title())
        brand = fb.get("brand", "")
        quote = fb.get("quote", "")
        rotate = _FB_ROTATE[i % len(_FB_ROTATE)]
        cards += f"""
        <article class="fb-card fb-card--{H.escape(platform)}" style="--fb-rotate:{rotate}deg">
          <div class="fb-device">
            <div class="fb-device-bar">
              <span class="fb-platform">{H.escape(platform_label)}</span>
              <span class="fb-brand">{H.escape(brand)}</span>
            </div>
            <button type="button" class="fb-shot-btn"
              data-full="{H.escape(src)}"
              data-brand="{H.escape(brand)}"
              data-platform="{H.escape(platform_label)}"
              aria-label="Ampliar feedback de {H.escape(brand)}">
              <img src="{H.escape(src)}" alt="Feedback {H.escape(brand)}" loading="lazy"/>
            </button>
          </div>
          {f'<p class="fb-quote">"{H.escape(quote)}"</p>' if quote else ''}
        </article>"""

    if not cards:
        return "", "", ""

    nav = """
    <div class="fb-nav" id="fb-nav">
      <button type="button" class="carousel-btn fb-prev" aria-label="Feedback anterior">&larr;</button>
      <span class="carousel-hint">Depoimentos reais · deslize</span>
      <button type="button" class="carousel-btn fb-next" aria-label="Próximo feedback">&rarr;</button>
    </div>"""

    section = f"""
<section class="feedbacks" id="feedbacks">
  <div class="feedbacks-bg" aria-hidden="true"></div>
  <div class="feedbacks-inner">
    <div class="feedbacks-head">
      <p class="feedbacks-sticker" aria-hidden="true">Feedback</p>
      <p class="feedbacks-kicker">Social proof</p>
      <h2>O que as marcas <em>dizem</em></h2>
      <p class="feedbacks-lead">DMs, comentários e parcerias — feedback de verdade, não roteirizado.</p>
    </div>
    <div class="feedbacks-track" id="feedbacks-track">{cards}
    </div>
    {nav}
  </div>
</section>"""

    css = """
.feedbacks{position:relative;overflow:hidden;padding:clamp(3.5rem,7vw,5.5rem) 0 clamp(3rem,6vw,4.5rem);background:radial-gradient(ellipse 52% 42% at 50% 40%,rgba(235,220,200,.42) 0%,transparent 58%),var(--grad-edge);color:#FAF6F0;border-block:1px solid rgba(232,217,196,.12)}
.feedbacks-bg{position:absolute;inset:0;pointer-events:none;overflow:hidden;background:radial-gradient(ellipse 62% 48% at 50% 44%,rgba(250,240,225,.3) 0%,transparent 58%)}
.feedbacks-inner{position:relative;z-index:1;max-width:var(--max);margin:0 auto;padding:0 clamp(1.25rem,4vw,2rem)}
.feedbacks-head{text-align:center;margin-bottom:clamp(2rem,4vw,2.75rem)}
.feedbacks-sticker{display:inline-block;margin-bottom:.35rem;font-family:"Great Vibes",cursive;font-size:clamp(2.6rem,6.5vw,3.8rem);font-weight:400;color:#FAF6F0;text-shadow:0 2px 16px rgba(77,51,40,.35);transform:rotate(-3deg);line-height:1}
.feedbacks-kicker{font-size:.58rem;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:rgba(250,246,240,.72);margin-bottom:.65rem}
.feedbacks-head h2{font-family:"Cormorant Garamond",serif;font-size:clamp(2rem,4vw,2.85rem);font-weight:400;line-height:1.05;color:#FAF6F0;text-shadow:0 1px 12px rgba(77,51,40,.2)}
.feedbacks-head h2 em{font-style:italic;color:var(--blush-light)}
.feedbacks-lead{margin-top:.85rem;max-width:32rem;margin-inline:auto;font-size:.92rem;line-height:1.65;color:rgba(250,246,240,.78);font-weight:300}
.feedbacks-track{display:flex;flex-wrap:nowrap;gap:1.35rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;padding:1rem .25rem 1.75rem;scrollbar-width:thin}
.fb-card{flex:0 0 min(280px,82vw);max-width:min(300px,82vw);scroll-snap-align:center;transform:rotate(var(--fb-rotate,0deg));transition:transform .45s var(--ease)}
.fb-card:hover{transform:rotate(0deg) translateY(-6px)}
.fb-device{border-radius:22px;overflow:hidden;background:#1A1512;box-shadow:0 24px 56px rgba(0,0,0,.35),0 0 0 1px rgba(255,250,247,.08)}
.fb-device-bar{display:flex;align-items:center;justify-content:space-between;gap:.75rem;padding:.55rem .85rem;font-size:.58rem;font-weight:600;letter-spacing:.06em}
.fb-card--tiktok .fb-device-bar{background:linear-gradient(90deg,#010101,#121212);color:#FBF7F2}
.fb-card--tiktok .fb-platform{color:#25F4EE}
.fb-card--instagram .fb-device-bar{background:linear-gradient(90deg,#833AB4,#FD1D1D,#FCAF45);color:#FBF7F2}
.fb-card--whatsapp .fb-device-bar{background:linear-gradient(90deg,#075E54,#128C7E);color:#FBF7F2}
.fb-card--whatsapp .fb-platform{color:#DCF8C6}
.fb-brand{opacity:.92;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:58%}
.fb-shot-btn{display:block;width:100%;padding:0;border:none;background:#0D0D0D;cursor:pointer;line-height:0}
.fb-shot-btn:focus-visible{outline:2px solid var(--copper);outline-offset:3px}
.fb-shot-btn img{width:100%;height:auto;display:block;max-height:min(420px,58vh);object-fit:contain;object-position:center top;background:#0D0D0D}
.fb-quote{margin-top:.85rem;padding:0 .35rem;font-family:"Cormorant Garamond",serif;font-size:1.05rem;font-style:italic;line-height:1.45;color:rgba(251,247,242,.88);text-align:center}
.fb-nav{margin-top:.5rem;display:flex;align-items:center;justify-content:center;gap:1rem}
.fb-nav .carousel-btn{border-color:rgba(255,255,255,.22);background:rgba(255,255,255,.08);color:#FAF6F0}
.fb-nav .carousel-btn:hover{border-color:rgba(255,255,255,.4);background:rgba(255,255,255,.14)}
.fb-nav .carousel-hint{color:rgba(250,246,240,.55)}
@media(max-width:600px){{
  .fb-card{{flex-basis:min(260px,86vw)}}
  .feedbacks-sticker{{font-size:2.2rem}}
}}"""

    return section, css, nav


def _build_contact_html(contact: dict, ig: str, dn: str) -> tuple[str, str]:
    email = (contact.get("email") or "").strip()
    script_head = contact.get("headline_script") or "Vamos criar juntos?"
    serif_head = contact.get("headline_serif") or "Entre em contato"
    subline = (contact.get("subline") or "").strip()

    ig_url = f"https://instagram.com/{H.escape(ig)}"
    ig_handle = f"@{H.escape(ig)}"

    email_row = ""
    if email:
        email_row = f"""
      <a class="contact-link" href="mailto:{H.escape(email)}">
        <span class="contact-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2" y="5" width="20" height="14" rx="2.5"/><path d="M2 8l10 6.5L22 8"/></svg>
        </span>
        <span class="contact-text">
          <span class="contact-label">E-mail</span>
          <span class="contact-value">{H.escape(email)}</span>
        </span>
      </a>"""

    subline_html = f'<p class="contact-lead">{H.escape(subline)}</p>' if subline else ""

    section = f"""
<section id="contato" class="contact">
  <div class="contact-glow" aria-hidden="true"></div>
  <div class="contact-inner">
    <p class="contact-script">{H.escape(script_head)}</p>
    <h2 class="contact-serif">{H.escape(serif_head)}</h2>
    {subline_html}
    <div class="contact-card">
      <div class="contact-links">
      <a class="contact-link" href="{ig_url}" target="_blank" rel="noopener noreferrer">
        <span class="contact-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>
        </span>
        <span class="contact-text">
          <span class="contact-label">Instagram</span>
          <span class="contact-value">{ig_handle}</span>
        </span>
      </a>{email_row}
      <a class="contact-link" href="{H.escape(_pdf_download_filename(dn))}" download="{H.escape(_pdf_download_filename(dn))}" target="_blank" rel="noopener noreferrer">
        <span class="contact-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 3v10m0 0l3.5-3.5M12 13l-3.5-3.5"/><path d="M5 17v2a2 2 0 002 2h10a2 2 0 002-2v-2"/></svg>
        </span>
        <span class="contact-text">
          <span class="contact-label">Media kit</span>
          <span class="contact-value">Baixar PDF</span>
        </span>
      </a>
      </div>
    </div>
  </div>
</section>"""

    css = """
.contact{position:relative;margin:0 clamp(1rem,3vw,1.75rem) clamp(2rem,4vw,2.75rem);padding:clamp(3.5rem,8vw,5.5rem) clamp(1.5rem,5vw,2.5rem);border-radius:clamp(20px,3vw,32px);overflow:hidden;color:#FAF6F0;text-align:center;box-shadow:var(--shadow);background:radial-gradient(ellipse 52% 42% at 50% 40%,rgba(235,220,200,.42) 0%,transparent 58%),var(--grad-edge)}
.contact-glow{position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 62% 48% at 50% 44%,rgba(250,240,225,.3) 0%,transparent 58%)}
.contact-inner{position:relative;z-index:1;max-width:40rem;margin:0 auto}
.contact-script{font-family:"Great Vibes",cursive;font-size:clamp(2.6rem,7vw,4.2rem);font-weight:400;line-height:1.05;color:#FAF6F0;text-shadow:0 2px 16px rgba(77,51,40,.35);margin-bottom:.15rem}
.contact-serif{font-family:"Cormorant Garamond",serif;font-size:clamp(1.35rem,3vw,1.85rem);font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:rgba(250,246,240,.92);line-height:1.2;text-shadow:0 1px 12px rgba(77,51,40,.25)}
.contact-lead{margin-top:1rem;font-size:.88rem;line-height:1.65;color:rgba(250,246,240,.78);font-weight:300;max-width:26rem;margin-inline:auto}
.contact-card{margin-top:clamp(2rem,4vw,2.75rem);padding:clamp(1.35rem,3vw,1.75rem);border-radius:24px;border:1px solid rgba(255,255,255,.55);background:linear-gradient(158deg,rgba(42,31,24,.88) 0%,rgba(61,46,36,.82) 100%);box-shadow:0 20px 50px rgba(45,33,28,.32),inset 0 1px 0 rgba(255,255,255,.1)}
.contact-links{display:flex;flex-direction:row;align-items:stretch;justify-content:center;gap:.85rem;max-width:100%;margin-inline:auto}
.contact-link{flex:1 1 0;min-width:0;display:flex;align-items:center;gap:.85rem;padding:.95rem 1rem;border-radius:999px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06);color:#FAF6F0;text-decoration:none;transition:border-color .3s var(--ease),background .3s var(--ease),transform .3s var(--ease),box-shadow .3s var(--ease)}
.contact-link:hover{border-color:rgba(255,255,255,.35);background:rgba(255,255,255,.1);transform:translateY(-2px);box-shadow:0 10px 28px rgba(45,33,28,.25)}
.contact-icon{flex-shrink:0;display:flex;align-items:center;justify-content:center;width:2.5rem;height:2.5rem;border-radius:50%;background:#d3bba1;color:#4d3328;box-shadow:0 2px 8px rgba(45,33,28,.2)}
.contact-icon svg{width:1.1rem;height:1.1rem}
.contact-text{display:flex;flex-direction:column;align-items:flex-start;gap:.15rem;text-align:left;min-width:0;flex:1}
.contact-label{font-size:.52rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:rgba(250,246,240,.55)}
.contact-value{font-family:"Plus Jakarta Sans",sans-serif;font-size:clamp(.78rem,2vw,.92rem);font-weight:500;letter-spacing:.02em;color:#FAF6F0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
@media(max-width:600px){
  .contact-links{flex-direction:column;max-width:22rem;margin-inline:auto}
  .contact-link{padding:.85rem 1rem}
}"""

    return section, css


def _theme_css(config: dict) -> str:
    t = config.get("theme") or {}
    d = {
        "bg": "#EDE4D8",
        "white": "#FAF6F0",
        "warm": "#E2D5C6",
        "surface": "#F5EFE6",
        "glow": "#E8D9C4",
        "ink": "#2C2118",
        "body": "#5C4A3E",
        "muted": "#8E7968",
        "blush": "#C9A882",
        "peach": "#B8886A",
        "mauve": "#A8907E",
        "copper": "#A67C52",
        "copper_deep": "#7D5A3C",
        "blush_light": "#E8D4BE",
        "line": "#D4C4B0",
        "mocha": "#3D2E24",
    }
    c = {k: t.get(k, v) for k, v in d.items()}
    return f"""
:root{{
  --bg:{c['bg']};--white:{c['white']};--warm:{c['warm']};--surface:{c['surface']};--glow:{c['glow']};
  --ink:{c['ink']};--body:{c['body']};--muted:{c['muted']};
  --blush:{c['blush']};--peach:{c['peach']};--mauve:{c['mauve']};
  --copper:{c['copper']};--copper-deep:{c['copper_deep']};--blush-light:{c['blush_light']};
  --accent:var(--copper);--accent-deep:var(--copper-deep);--accent-light:var(--blush-light);
  --mocha:{c['mocha']};--line:{c['line']};
  --shadow:0 18px 52px rgba(44,33,24,.09),0 2px 10px rgba(44,33,24,.04);
  --shadow-soft:0 10px 36px rgba(44,33,24,.07);
  --max:1140px;--ease:cubic-bezier(.22,1,.36,1);
  --chocolate:#4d3328;--beige:#d3bba1;
  --grad-edge:linear-gradient(90deg,#4d3328 0%,#6B5344 12%,#9A7B62 28%,#C4A882 42%,#d3bba1 50%,#C4A882 58%,#9A7B62 72%,#6B5344 88%,#4d3328 100%);
  --grad-edge-soft:linear-gradient(90deg,{c['blush']} 0%,{c['line']} 14%,{c['glow']} 30%,{c['white']} 50%,{c['glow']} 70%,{c['line']} 86%,{c['blush']} 100%);
  --grad-luxe:linear-gradient(135deg,#4d3328 0%,#8B6F56 38%,#C4A882 62%,#d3bba1 78%,#8B6F56 100%);
  --grad-soft:linear-gradient(180deg,var(--white) 0%,var(--bg) 50%,var(--warm) 100%);
  --grad-mesh:linear-gradient(90deg,rgba(77,51,40,.12) 0%,transparent 16%,transparent 84%,rgba(77,51,40,.12) 100%),radial-gradient(ellipse 70% 50% at 50% 0%,rgba(240,226,206,.42) 0%,transparent 55%),var(--bg);
}}"""


def _layout_css() -> str:
    return """
body{font-family:"Plus Jakarta Sans",system-ui,sans-serif;font-size:15px;line-height:1.65;color:var(--body);background:var(--grad-mesh);background-attachment:fixed;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.section-eyebrow{font-size:.58rem;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:var(--copper-deep);margin-bottom:.55rem}
.section-lead{margin-top:.65rem;max-width:28rem;font-size:.9rem;line-height:1.65;color:var(--muted);font-weight:300}
.topbar{position:sticky;top:0;z-index:100;background:rgba(250,246,240,.88);backdrop-filter:blur(18px) saturate(1.08);border-bottom:1px solid rgba(212,196,176,.65);box-shadow:0 1px 0 rgba(255,255,255,.5)}
.topbar-inner{max-width:var(--max);margin:0 auto;padding:.9rem clamp(1.5rem,5vw,2.5rem);display:flex;align-items:center;justify-content:space-between;gap:1rem}
.topbar-name{font-family:"Cormorant Garamond",serif;font-size:1.12rem;font-weight:600;color:var(--ink);letter-spacing:.04em}
.topbar-links{display:flex;gap:1.5rem;align-items:center}
.topbar-links a{font-size:.62rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);transition:color .25s var(--ease)}
.topbar-links a:hover{color:var(--copper-deep)}
.topbar-cta{padding:.55rem 1.2rem;border-radius:999px;background:var(--grad-luxe);color:#FAF6F0;font-size:.62rem;font-weight:600;letter-spacing:.08em;box-shadow:0 4px 18px rgba(77,51,40,.22);transition:transform .25s var(--ease),box-shadow .25s var(--ease)}
.topbar-cta:hover{transform:translateY(-1px);box-shadow:0 6px 22px rgba(77,51,40,.28)}
.topbar-pdf{padding:.5rem .95rem;border-radius:999px;border:1px solid var(--line);background:rgba(255,255,255,.55);color:var(--copper-deep)!important}
.topbar-pdf:hover{border-color:var(--copper);background:var(--white);color:var(--ink)!important}
.intro{padding:clamp(3.25rem,7vw,5.25rem) clamp(1.5rem,5vw,2.5rem) clamp(3.5rem,7vw,5.5rem);background:radial-gradient(ellipse 52% 42% at 50% 40%,rgba(235,220,200,.42) 0%,transparent 58%),var(--grad-edge);border-bottom:1px solid rgba(232,217,196,.12);position:relative;overflow:hidden;color:#FAF6F0}
.intro::before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 62% 48% at 50% 44%,rgba(250,240,225,.22) 0%,transparent 58%)}
.intro::after{content:"";position:absolute;left:50%;bottom:0;width:1px;height:clamp(2.5rem,5vw,3.5rem);background:linear-gradient(180deg,rgba(211,187,161,.65),transparent);opacity:.5;transform:translateX(-50%)}
.intro-inner{position:relative;z-index:1;max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,5vw,4rem);align-items:center}
.intro-visual{display:flex;justify-content:center;align-items:center;max-width:min(400px,100%);margin-inline:auto;width:100%}
.intro-visual--video{max-width:min(420px,100%)}
.prisma{margin:0;width:100%;max-width:380px;display:grid;grid-template-columns:1fr minmax(64px,22%);grid-template-rows:1fr;background:var(--surface);border-radius:26px 8px 18px 26px;overflow:hidden;box-shadow:var(--shadow),0 0 0 1px rgba(255,255,255,.45);aspect-ratio:5/4;max-height:min(420px,52vh)}
.prisma--video{max-width:min(390px,100%);aspect-ratio:auto;max-height:none;grid-template-columns:minmax(0,1fr) 112px;align-items:stretch}
.prisma-main{grid-column:1;grid-row:1;min-height:0;position:relative;overflow:hidden;background:var(--warm)}
.prisma--video .prisma-main{aspect-ratio:9/16;min-height:min(380px,48vh);width:100%}
.hero-portrait{position:absolute;inset:0;width:100%;height:100%;min-height:0;object-fit:cover;object-position:center 12%;display:block}
.hero-video{object-fit:contain;object-position:center center;background:#1a1512}
.hero-ph{position:absolute;inset:0;min-height:0;background:linear-gradient(165deg,var(--blush-light),var(--warm),var(--glow))}
.prisma-strips{grid-column:2;grid-row:1;display:grid;grid-template-rows:repeat(3,1fr);border-left:1px solid var(--line);min-height:0;width:112px}
.prisma--video .prisma-strips{width:112px}
.prisma-strip{position:relative;overflow:hidden;border-bottom:1px solid var(--line);min-height:0}
.prisma-strip:last-child{border-bottom:none}
.prisma-strip img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s var(--ease),filter .6s var(--ease)}
.prisma-strip:hover img{transform:scale(1.08);filter:saturate(1.06)}
.prisma-strip .fi-1{object-position:center 18%}
.prisma-strip .fi-2{object-position:center 40%}
.prisma-strip .fi-3{object-position:center 12%}
.prisma-tag{position:absolute;left:0;right:0;bottom:0;padding:.45rem .2rem;font-size:.46rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;text-align:center;color:#FAF6F0;background:linear-gradient(0deg,rgba(61,42,34,.78),transparent);opacity:0;transition:opacity .35s var(--ease)}
.prisma-strip:hover .prisma-tag{opacity:1}
.intro-copy{display:flex;flex-direction:column;justify-content:center;min-width:0}
.intro-badge{display:inline-flex;align-self:flex-start;padding:.45rem .85rem;border-radius:999px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.12);font-size:.56rem;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:rgba(250,246,240,.88);margin-bottom:1.15rem;backdrop-filter:blur(6px)}
.intro-greeting{font-family:"Great Vibes",cursive;font-size:clamp(2.2rem,5.5vw,3.4rem);font-weight:400;color:rgba(250,246,240,.95);margin-bottom:.1rem;line-height:1.05;text-shadow:0 2px 14px rgba(45,33,28,.15)}
.intro h1{font-family:"Cormorant Garamond",serif;font-size:clamp(2.85rem,6.2vw,4.35rem);font-weight:400;line-height:1.02;color:#FAF6F0;letter-spacing:-.015em;text-shadow:0 2px 18px rgba(45,33,28,.18);margin-top:0}
.intro h1 em{font-style:italic;font-weight:400;color:var(--blush-light)}
.intro-lead{margin-top:1.15rem;max-width:34rem;font-size:1.02rem;line-height:1.75;color:rgba(250,246,240,.82);font-weight:300}
.intro-meta{margin-top:2rem;display:flex;flex-wrap:wrap;gap:.85rem}
.meta-item{display:flex;flex-direction:column;gap:.2rem;padding:.85rem 1.15rem;border-radius:16px;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.88);box-shadow:0 10px 28px rgba(45,33,28,.16);min-width:7rem}
.meta-item strong{font-family:"Cormorant Garamond",serif;font-size:1.45rem;font-weight:600;color:var(--ink);line-height:1}
.meta-item span{font-size:.56rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--copper-deep)}
.meta-loc strong{font-family:"Plus Jakarta Sans",sans-serif;font-size:1rem;font-weight:600;letter-spacing:.06em}
.gallery{background:var(--grad-edge-soft);border-top:1px solid var(--line);padding:clamp(3.75rem,6.5vw,5.25rem) 0 clamp(4rem,7vw,5.5rem);position:relative}
.gallery::before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 55% 45% at 50% 38%,rgba(250,246,240,.55) 0%,transparent 62%)}
.gallery-top{position:relative;z-index:10;max-width:var(--max);margin:0 auto;padding:0 clamp(1.25rem,4vw,2rem);display:flex;justify-content:space-between;align-items:flex-end;gap:2rem}
.gallery-head{min-width:0;flex:1}
.gallery-head h2{font-family:"Cormorant Garamond",serif;font-size:clamp(2.1rem,4vw,2.85rem);font-weight:400;line-height:1.05;color:var(--ink)}
.gallery-head h2 em{font-style:italic;color:var(--copper)}
.gallery-actions{position:relative;z-index:30;flex-shrink:0;display:flex;align-items:flex-end;justify-content:flex-end}
.brand-picker{position:relative;z-index:30;width:min(360px,100%)}
.brand-picker-anchor{position:relative;width:100%}
.brand-picker-toggle{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:.2rem;width:100%;min-width:min(240px,42vw);padding:.8rem 2.25rem .8rem 1rem;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.75);cursor:pointer;text-align:left;transition:border-color .25s var(--ease),box-shadow .25s var(--ease)}
.brand-picker-toggle:hover,.brand-picker-toggle[aria-expanded="true"]{border-color:var(--copper);box-shadow:var(--shadow-soft)}
.brand-picker-kicker{font-size:.52rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.brand-picker-value{font-family:"Cormorant Garamond",serif;font-size:1.08rem;color:var(--ink);line-height:1.2}
.brand-picker-chevron{position:absolute;right:1rem;top:50%;width:.45rem;height:.45rem;border-right:1.5px solid var(--copper);border-bottom:1.5px solid var(--copper);transform:translateY(-65%) rotate(45deg);transition:transform .25s var(--ease)}
.brand-picker-toggle[aria-expanded="true"] .brand-picker-chevron{transform:translateY(-35%) rotate(-135deg)}
.brand-picker-panel{position:absolute;z-index:50;left:0;right:0;top:calc(100% + .5rem);width:100%;max-height:min(380px,58vh);overflow-y:auto;padding:.45rem;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.97);box-shadow:var(--shadow);scrollbar-width:thin}
.brand-picker-panel[hidden]{display:none!important}
.brand-opt{display:flex;align-items:center;justify-content:space-between;gap:1rem;width:100%;padding:.7rem .85rem;border:none;border-radius:12px;background:transparent;cursor:pointer;text-align:left;transition:background .2s var(--ease)}
.brand-opt span{font-family:"Cormorant Garamond",serif;font-size:1rem;color:var(--ink)}
.brand-opt em{font-family:"Plus Jakarta Sans",sans-serif;font-size:.62rem;font-style:normal;font-weight:500;letter-spacing:.06em;color:var(--muted)}
.brand-opt:hover{background:var(--warm)}
.brand-opt.active{background:rgba(166,124,82,.14)}
.brand-opt.active span{color:var(--copper-deep)}
.grid-wrap{position:relative;z-index:1;max-width:var(--max);margin:0 auto}
.grid-wrap::before,.grid-wrap::after{content:"";position:absolute;top:0;bottom:0;width:clamp(24px,5vw,56px);z-index:2;pointer-events:none}
.grid-wrap::before{left:0;background:linear-gradient(90deg,rgba(201,168,130,.92),transparent)}
.grid-wrap::after{right:0;background:linear-gradient(270deg,rgba(201,168,130,.92),transparent)}
.grid{padding:clamp(2rem,4vw,2.75rem) clamp(1.25rem,4vw,2rem) clamp(1.25rem,3vw,1.75rem);display:flex;flex-wrap:nowrap;gap:1.25rem;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;-webkit-overflow-scrolling:touch;scrollbar-width:thin;margin-top:clamp(1.5rem,3vw,2rem)}
.grid .piece{flex:0 0 min(268px,78vw);max-width:min(288px,78vw);scroll-snap-align:start}
.carousel-nav{position:relative;z-index:1;max-width:var(--max);margin:1rem auto 0;padding:0 clamp(1.25rem,4vw,2rem);display:flex;align-items:center;justify-content:center;gap:1rem}
.carousel-btn{width:2.65rem;height:2.65rem;border:1px solid var(--line);border-radius:50%;background:rgba(255,255,255,.85);color:var(--ink);font-size:1.1rem;line-height:1;cursor:pointer;box-shadow:var(--shadow-soft);transition:border-color .25s var(--ease),background .25s var(--ease),transform .25s var(--ease)}
.carousel-btn:hover{border-color:var(--copper);background:var(--white);transform:translateY(-2px)}
.carousel-hint{font-size:.6rem;font-weight:500;letter-spacing:.1em;color:var(--muted)}
.gallery-empty{flex:1 0 100%;display:none;padding:3rem 1rem;text-align:center;font-family:"Cormorant Garamond",serif;font-size:1.25rem;color:var(--muted)}
.gallery-empty.show{display:block}
.piece{transition:transform .35s var(--ease)}
.piece:hover{transform:translateY(-5px)}
.piece.hidden{display:none}
.piece-btn{display:block;width:100%;padding:0;border:none;background:rgba(255,255,255,.82);cursor:pointer;text-align:left;font:inherit;color:inherit;border-radius:20px;overflow:hidden;box-shadow:var(--shadow-soft);border:1px solid rgba(212,196,176,.55);transition:box-shadow .35s var(--ease),border-color .35s var(--ease)}
.piece-btn:focus-visible{outline:2px solid var(--copper);outline-offset:3px}
.piece:hover .piece-btn{box-shadow:var(--shadow);border-color:rgba(166,124,82,.35)}
.piece-img{position:relative;aspect-ratio:4/5;overflow:hidden;background:var(--warm)}
.piece-img::after{content:"";position:absolute;inset:auto 0 0 0;height:3px;background:var(--grad-luxe);transform:scaleX(0);transform-origin:left;transition:transform .4s var(--ease)}
.piece:hover .piece-img::after{transform:scaleX(1)}
.piece-img img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block;transform-origin:top center;transition:transform .55s var(--ease)}
.piece[data-media-id="18071655761192823"] .piece-img img{object-position:50% 26%;transform-origin:50% 26%}
.piece[data-media-id="18015297932414597"] .piece-img img{object-position:50% 50%;transform-origin:50% 50%}
.piece[data-media-id="18146252194343099"] .piece-img img{object-position:50% 100%;transform-origin:50% 100%}
.piece:hover .piece-img img{transform:scale(1.04)}
.piece-cap{padding:.85rem .95rem 1rem;background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(245,239,230,.88))}
.piece-brand{display:block;font-family:"Cormorant Garamond",serif;font-size:1.05rem;font-weight:500;color:var(--ink);line-height:1.2}
.piece-stat{display:block;margin-top:.3rem;font-size:.6rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--copper-deep)}
.lightbox{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:clamp(1rem,4vw,2rem);background:rgba(44,33,24,.88);backdrop-filter:blur(10px)}
.lightbox[hidden]{display:none}
.lightbox-inner{position:relative;width:min(420px,100%);max-height:92vh;display:flex;flex-direction:column;gap:1rem}
.lightbox-close{position:absolute;z-index:2;top:-.25rem;right:0;width:2.25rem;height:2.25rem;border:none;border-radius:50%;background:rgba(250,246,240,.15);color:#FAF6F0;font-size:1.35rem;line-height:1;cursor:pointer}
.lightbox-close:hover{background:rgba(250,246,240,.28)}
.lightbox-media{position:relative;width:100%;border-radius:18px;overflow:hidden;background:var(--ink);box-shadow:0 28px 72px rgba(0,0,0,.4)}
.lightbox-img{width:100%;max-height:min(72vh,720px);object-fit:contain;display:block}
.lightbox-embed{position:relative;width:100%;aspect-ratio:9/16;max-height:min(72vh,720px);background:#000}
.lightbox-embed iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.lightbox-video{width:100%;max-height:min(72vh,720px);display:block;background:#000}
.lightbox-img.hidden,.lightbox-embed.hidden,.lightbox-video.hidden{display:none}
.lightbox-meta{padding:.25rem .15rem 0;color:#FAF6F0}
.lightbox-brand{font-family:"Cormorant Garamond",serif;font-size:1.35rem;line-height:1.2}
.lightbox-stat{margin-top:.35rem;font-size:.72rem;opacity:.78}
.lightbox-ig{display:inline-block;margin-top:1rem;padding:.65rem 1.15rem;border-radius:999px;background:#FAF6F0;color:var(--mocha);font-size:.68rem;font-weight:600;letter-spacing:.06em;text-decoration:none;transition:background .25s}
.lightbox-ig:hover{background:var(--glow)}
.lightbox-ig.hidden{display:none}
.stats-band{border-block:1px solid var(--line);background:linear-gradient(180deg,var(--warm) 0%,rgba(212,196,176,.22) 100%);padding:clamp(2rem,4vw,2.5rem) clamp(1.25rem,4vw,2rem)}
.stats-row{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:repeat(5,1fr);gap:1rem}
.stat{text-align:center}
.stat b{display:block;font-family:"Cormorant Garamond",serif;font-size:clamp(1.4rem,2.5vw,1.9rem);font-weight:600;color:var(--ink);line-height:1}
.stat span{display:block;margin-top:.25rem;font-size:.6rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.marquee{overflow:hidden;padding:1.65rem 0;border-bottom:1px solid var(--line);background:var(--surface);position:relative}
.marquee-track{display:flex;width:max-content;animation:marquee 42s linear infinite}
.marquee-track ul{display:flex;gap:2.75rem;list-style:none;padding:0 1.25rem}
.marquee-track li{font-family:"Cormorant Garamond",serif;font-size:1.18rem;color:var(--copper-deep);white-space:nowrap;font-weight:500}
.marquee-track li::after{content:"·";margin-left:2.75rem;opacity:.35;color:var(--muted)}
@keyframes marquee{to{transform:translateX(-50%)}}
.marquee-fade{position:absolute;top:0;bottom:0;width:clamp(32px,8vw,96px);z-index:2;pointer-events:none}
.marquee-fade--l{left:0;background:linear-gradient(90deg,var(--surface),transparent)}
.marquee-fade--r{right:0;background:linear-gradient(270deg,var(--surface),transparent)}
.about-card--aud{background:linear-gradient(165deg,rgba(255,255,255,.78),rgba(245,239,230,.92))}
.about-card .section-eyebrow{margin-bottom:.45rem}
.gallery-head .section-lead{margin-top:.75rem;max-width:none;white-space:nowrap}
.bottom{max-width:var(--max);margin:0 auto;padding:clamp(3rem,6vw,4rem) clamp(1.25rem,4vw,2rem);display:grid;grid-template-columns:1.15fr 1fr;gap:1.25rem;align-items:stretch}
.about-card{padding:clamp(1.75rem,3vw,2.25rem);border-radius:22px;border:1px solid var(--line);background:rgba(255,255,255,.62);box-shadow:var(--shadow-soft)}
.about-card h3{font-family:"Cormorant Garamond",serif;font-size:1.65rem;font-weight:500;color:var(--ink);margin-bottom:.75rem;margin-top:.15rem}
.about-card p{color:var(--body);line-height:1.78;font-weight:300}
.about-card p+p{margin-top:1rem}
.aud-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;margin-top:.25rem}
.aud{text-align:center;padding:1.05rem .85rem;background:linear-gradient(165deg,rgba(255,255,255,.92),rgba(245,239,230,.88));border:1px solid var(--line);border-radius:16px;transition:transform .25s var(--ease),box-shadow .25s var(--ease)}
.aud:hover{transform:translateY(-2px);box-shadow:var(--shadow-soft)}
.aud b{display:block;font-family:"Cormorant Garamond",serif;font-size:1.55rem;font-weight:600;color:var(--ink)}
.aud span{font-size:.56rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
@media(max-width:900px){
  .intro-inner{grid-template-columns:1fr}
  .gallery-top{flex-direction:column;align-items:stretch;gap:1.25rem}
  .gallery-head .section-lead{white-space:normal}
  .gallery-actions{width:100%;justify-content:flex-end}
  .brand-picker{width:100%;max-width:100%}
  .brand-picker-anchor{width:100%}
  .brand-picker-toggle{width:100%;min-width:0}
  .intro-visual{order:-1}
  .intro-visual{max-width:min(360px,92vw)}
  .intro-visual--video{max-width:min(400px,92vw)}
  .prisma{max-width:100%;max-height:none;aspect-ratio:auto;border-radius:22px}
  .prisma--video{grid-template-columns:1fr;grid-template-rows:auto auto;max-width:100%}
  .prisma--video .prisma-main{aspect-ratio:9/16;min-height:min(360px,64vw)}
  .prisma--video .prisma-strips{grid-column:1;grid-row:2;width:100%;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr;border-left:none;border-top:1px solid var(--line);min-height:104px;max-height:118px}
  .prisma--video .prisma-strip{border-bottom:none;border-right:1px solid var(--line)}
  .prisma--video .prisma-strip:last-child{border-right:none}
  .prisma-main{aspect-ratio:4/5;min-height:min(320px,62vw)}
  .prisma-strips{grid-column:1;grid-row:2;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr;border-left:none;border-top:1px solid var(--line);min-height:96px;max-height:108px}
  .prisma-strip{border-bottom:none;border-right:1px solid var(--line)}
  .prisma-strip:last-child{border-right:none}
  .prisma-tag{opacity:1;font-size:.42rem;padding:.35rem .15rem}
  .grid .piece{flex-basis:min(240px,80vw)}
  .stats-row{grid-template-columns:repeat(2,1fr)}
  .bottom{grid-template-columns:1fr}
  .intro-badge{align-self:center}
}
@media(max-width:600px){
  .intro-inner{text-align:center}
  .intro-lead{margin-left:auto;margin-right:auto}
  .intro-meta{justify-content:center}
  .meta-item{min-width:0;flex:1 1 calc(50% - .5rem)}
  .intro-visual{max-width:min(320px,94vw)}
  .intro-visual--video{max-width:min(340px,94vw)}
  .prisma--video .prisma-main{min-height:min(340px,72vw)}
  .prisma-main{min-height:min(280px,70vw)}
  .prisma-strips{min-height:84px;max-height:96px}
  .grid{gap:.9rem}
  .grid .piece{flex-basis:min(220px,82vw)}
  .topbar-links a:not(.topbar-cta):not(.topbar-pdf){display:none}
  .grid-wrap::before,.grid-wrap::after{width:20px}
}"""


def build_portfolio(metrics: dict, config: dict, assets: dict, period: str, fmt_num) -> str:
    d = _shared_data(metrics, config, assets, period, fmt_num)
    fn = d["fmt_num"]
    ig = d["contact"].get("instagram", d["username"])
    dn = d["display_name"]
    reels = d["reels"]
    work_count = len([r for r in reels if r.get("data_uri")])

    name_parts = dn.split()
    first = name_parts[0] if name_parts else "Tatiana"
    rest = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Zacharias"

    strip_meta = (("fi-1", "Prêmio"), ("fi-2", "Campanha"), ("fi-3", "Creator"))
    prisma_strips = ""
    float_uris = d.get("hero_float_uris") or []
    if not float_uris:
        float_uris = [r.get("data_uri", "") for r in reels[1:4] if r.get("data_uri")]
    for i, uri in enumerate(float_uris[:3]):
        pos_cls, tag = strip_meta[i] if i < len(strip_meta) else ("", "")
        prisma_strips += f"""
          <div class="prisma-strip">
            <img class="{pos_cls}" src="{H.escape(uri)}" alt="{H.escape(tag)}" loading="lazy"/>
            <span class="prisma-tag">{H.escape(tag)}</span>
          </div>"""

    portrait = ""
    if d.get("hero_video"):
        poster = H.escape(d.get("hero_poster") or "")
        poster_attr = f' poster="{poster}"' if poster else ""
        portrait = (
            f'<video class="hero-portrait hero-video" src="{H.escape(d["hero_video"])}"'
            f'{poster_attr} autoplay muted loop playsinline controls preload="metadata"'
            f' aria-label="{H.escape(dn)}"></video>'
        )
    elif d["profile_img"]:
        portrait = f'<img src="{H.escape(d["profile_img"])}" alt="{H.escape(dn)}" class="hero-portrait"/>'
    else:
        portrait = '<div class="hero-portrait hero-ph"></div>'

    prisma_cls = "prisma prisma--video" if d.get("hero_video") else "prisma"
    visual_cls = "intro-visual intro-visual--video" if d.get("hero_video") else "intro-visual"

    photo = f"""
    <div class="{visual_cls}">
      <figure class="{prisma_cls}">
        <div class="prisma-main">{portrait}</div>
        <div class="prisma-strips">{prisma_strips}
        </div>
      </figure>
    </div>"""

    meta_html = f"""
      <div class="meta-item"><strong>{H.escape(d['stats'][0][0])}</strong><span>seguidores</span></div>
      <div class="meta-item"><strong>{work_count}</strong><span>trabalhos</span></div>
      <div class="meta-item meta-loc"><strong>013</strong><span>Baixada Santista</span></div>"""

    category_counts: dict[str, int] = {}
    for reel in reels:
        cats = reel.get("categories") or [reel.get("category", "beleza")]
        for cat in cats:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    category_options = ""
    for cat in portfolio_categories(config):
        cat_id = cat["id"]
        name = cat["name"]
        count = category_counts.get(cat_id, 0)
        category_options += (
            f'<button type="button" class="brand-opt" data-category="{H.escape(cat_id)}" '
            f'data-label="{H.escape(name)}"><span>{H.escape(name)}</span><em>{count}</em></button>'
        )

    brand_picker = f"""
    <div class="brand-picker" id="brand-picker">
      <div class="brand-picker-anchor">
        <button type="button" class="brand-picker-toggle" aria-expanded="false" aria-haspopup="listbox">
          <span class="brand-picker-kicker">Categoria</span>
          <span class="brand-picker-value">Filtrar por categoria</span>
          <span class="brand-picker-chevron" aria-hidden="true"></span>
        </button>
        <div class="brand-picker-panel" role="listbox" hidden>{category_options}
        </div>
      </div>
    </div>"""

    gallery_html = ""
    for reel in reels:
        img_src = reel.get("asset_path") or reel.get("data_uri") or ""
        if not img_src:
            continue
        brand = reel.get("brand", "Beauty")
        slug = _brand_slug(brand)
        category = reel.get("category", "beleza")
        categories = reel.get("categories") or [category]
        categories_attr = H.escape(" ".join(categories))
        stat = format_piece_views(reel.get("views", 0), fn)
        stat_line = f'<span class="piece-stat">{H.escape(stat)}</span>' if stat else ""
        permalink = reel.get("permalink") or ""
        asset_video = reel.get("asset_video") or ""
        video_attr = f' data-video-url="{H.escape(asset_video)}"' if asset_video else ""
        gallery_html += f"""
        <article class="piece" data-brand="{H.escape(slug)}" data-category="{H.escape(category)}" data-categories="{categories_attr}" data-media-id="{H.escape(reel.get('media_id', ''))}">
          <button type="button" class="piece-btn" data-permalink="{H.escape(permalink)}"{video_attr}
            data-brand-name="{H.escape(brand)}" data-stat="{H.escape(stat)}" aria-label="Ver {H.escape(brand)}">
            <div class="piece-img">
              <img src="{H.escape(img_src)}" alt="{H.escape(brand)}" loading="lazy"/>
            </div>
            <div class="piece-cap">
              <span class="piece-brand">{H.escape(brand)}</span>
              {stat_line}
            </div>
          </button>
        </article>"""

    carousel_nav = """
    <div class="carousel-nav" id="carousel-nav">
      <button type="button" class="carousel-btn carousel-prev" aria-label="Anterior">&larr;</button>
      <span class="carousel-hint">Deslize ou use as setas</span>
      <button type="button" class="carousel-btn carousel-next" aria-label="Próximo">&rarr;</button>
    </div>"""

    stats_html = "".join(
        f"""<div class="stat">
          <b>{H.escape(n)}</b>
          <span>{H.escape(l)}{f' · {H.escape(s)}' if s else ''}</span>
        </div>"""
        for n, l, s in d["stats"][:5]
    )

    aud_html = "".join(
        f"""<div class="aud"><b>{H.escape(str(int(v) if v == int(v) else v))}%</b><span>{H.escape(k)}</span></div>"""
        for k, v in d["aud"]
    )

    brand_items = "".join(f"<li>{H.escape(b['name'])}</li>" for b in d["brands"])
    marquee = brand_items + brand_items
    theme_css = _theme_css(config)
    feedbacks_section, feedbacks_css, _ = _build_feedbacks_html(assets.get("feedbacks", []))
    contact_section, contact_css = _build_contact_html(d["contact"], ig, dn)
    feedbacks_nav_link = (
        '<a href="#feedbacks">Feedbacks</a>' if feedbacks_section else ""
    )
    pdf_name = _pdf_download_filename(dn)
    pdf_nav_link = (
        f'<a class="topbar-pdf" href="{H.escape(pdf_name)}" '
        f'download="{H.escape(pdf_name)}" target="_blank" rel="noopener noreferrer">'
        f"Baixar PDF</a>"
    )
    about_extra_html = (
        f'<p>{H.escape(d["about_extra"])}</p>' if d.get("about_extra") else ""
    )

    from datetime import datetime, timezone
    build_stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M UTC")

    return f"""<!DOCTYPE html>
<!-- mediakit build: {build_stamp} · layout-luxe-v2 -->
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="description" content="{H.escape(d['about'][:160])}"/>
<title>{H.escape(dn)} · Portfólio UGC Beauty</title>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Great+Vibes&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
{theme_css}
{_layout_css()}
{feedbacks_css}
{contact_css}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
</style>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="topbar-name" href="#">{H.escape(dn)}</a>
    <div class="topbar-links">
      <a href="#trabalhos">Trabalhos e Parcerias</a>
      {feedbacks_nav_link}
      <a href="#contato">Contato</a>
      {pdf_nav_link}
      <a class="topbar-cta" href="https://instagram.com/{H.escape(ig)}">@{H.escape(ig)}</a>
    </div>
  </div>
</header>

<section class="intro">
  <div class="intro-inner">
    <div class="intro-copy">
      <p class="intro-badge">{H.escape(d['hero_subtitle'])}</p>
      <p class="intro-greeting">Oi. Eu sou</p>
      <h1>{H.escape(first)} <em>{H.escape(rest)}</em></h1>
      <p class="intro-lead">{H.escape(d['about'])}</p>
      <div class="intro-meta">{meta_html}</div>
    </div>
    {photo}
  </div>
</section>

<div class="stats-band">
  <div class="stats-row">{stats_html}</div>
</div>

<div class="marquee">
  <div class="marquee-fade marquee-fade--l" aria-hidden="true"></div>
  <div class="marquee-fade marquee-fade--r" aria-hidden="true"></div>
  <div class="marquee-track"><ul>{marquee}</ul></div>
</div>

<section id="trabalhos" class="gallery">
  <div class="gallery-top">
    <div class="gallery-head">
      <p class="section-eyebrow">Portfólio</p>
      <h2>Trabalhos e <em>Parcerias</em></h2>
      <p class="section-lead">Campanhas, UGC e conteúdo para marcas de beauty — filtre por categoria.</p>
    </div>
    <div class="gallery-actions">
      {brand_picker}
    </div>
  </div>
  {carousel_nav}
  <div class="grid-wrap">
    <div class="grid" id="gallery-grid">{gallery_html}
      <p class="gallery-empty" id="gallery-empty">Nenhum trabalho nesta categoria.</p>
    </div>
  </div>
</section>

<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Visualizar trabalho">
  <div class="lightbox-inner">
    <button type="button" class="lightbox-close" aria-label="Fechar">&times;</button>
    <div class="lightbox-media">
      <img class="lightbox-img" alt=""/>
      <div class="lightbox-embed hidden" aria-hidden="true">
        <iframe title="Reel no Instagram" loading="lazy" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>
      </div>
      <video class="lightbox-video hidden" controls playsinline preload="metadata"></video>
    </div>
    <div class="lightbox-meta">
      <p class="lightbox-brand"></p>
      <p class="lightbox-stat"></p>
      <a class="lightbox-ig" href="#" target="_blank" rel="noopener noreferrer">Ver no Instagram</a>
    </div>
  </div>
</div>

{feedbacks_section}

<div class="bottom">
  <div class="about-card">
    <p class="section-eyebrow">Quem sou</p>
    <h3>Sobre</h3>
    {about_extra_html}
  </div>
  <div class="about-card about-card--aud">
    <p class="section-eyebrow">Dados</p>
    <h3>Audiência</h3>
    <div class="aud-grid">{aud_html}</div>
  </div>
</div>

{contact_section}

<script>
(function() {{
  const picker = document.getElementById('brand-picker');
  const galleryGrid = document.getElementById('gallery-grid');
  const carouselNav = document.getElementById('carousel-nav');
  const feedbacksTrack = document.getElementById('feedbacks-track');
  const fbNav = document.getElementById('fb-nav');
  const galleryEmpty = document.getElementById('gallery-empty');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = lightbox?.querySelector('.lightbox-img');
  const lightboxEmbed = lightbox?.querySelector('.lightbox-embed');
  const lightboxFrame = lightboxEmbed?.querySelector('iframe');
  const lightboxVideo = lightbox?.querySelector('.lightbox-video');
  const lightboxBrand = lightbox?.querySelector('.lightbox-brand');
  const lightboxStat = lightbox?.querySelector('.lightbox-stat');
  const lightboxIg = lightbox?.querySelector('.lightbox-ig');
  const lightboxClose = lightbox?.querySelector('.lightbox-close');

  function reelEmbedUrl(permalink) {{
    if (!permalink) return '';
    const clean = permalink.split('?')[0].replace(/\\/$/, '');
    if (!/instagram\\.com\\/(reel|reels|p|tv)\\//i.test(clean)) return '';
    return clean + '/embed/captioned/';
  }}

  function updateEmptyState() {{
    if (!galleryEmpty) return;
    const visible = document.querySelectorAll('#gallery-grid .piece:not(.hidden)').length;
    galleryEmpty.classList.toggle('show', visible === 0);
  }}

  function scrollCarousel(dir) {{
    if (!galleryGrid) return;
    const step = Math.max(240, galleryGrid.clientWidth * 0.72);
    galleryGrid.scrollBy({{ left: dir * step, behavior: 'smooth' }});
  }}

  function scrollFeedbacks(dir) {{
    if (!feedbacksTrack) return;
    const step = Math.max(260, feedbacksTrack.clientWidth * 0.68);
    feedbacksTrack.scrollBy({{ left: dir * step, behavior: 'smooth' }});
  }}

  function hideLightboxMedia() {{
    lightboxImg?.classList.add('hidden');
    if (lightboxImg) lightboxImg.removeAttribute('src');
    if (lightboxEmbed) {{
      lightboxEmbed.classList.add('hidden');
      lightboxEmbed.setAttribute('aria-hidden', 'true');
    }}
    if (lightboxFrame) lightboxFrame.src = '';
    if (lightboxVideo) {{
      lightboxVideo.classList.add('hidden');
      lightboxVideo.pause();
      lightboxVideo.removeAttribute('src');
      lightboxVideo.load();
    }}
  }}

  function openLightbox(btn) {{
    if (!lightbox || !lightboxImg) return;
    const img = btn.querySelector('.piece-img img');
    if (!img) return;
    const link = btn.dataset.permalink || '';
    const videoUrl = btn.dataset.videoUrl || '';
    hideLightboxMedia();
    if (videoUrl && lightboxVideo) {{
      lightboxVideo.src = videoUrl;
      lightboxVideo.classList.remove('hidden');
    }} else {{
      const embedUrl = reelEmbedUrl(link);
      if (embedUrl && lightboxEmbed && lightboxFrame) {{
        lightboxFrame.src = embedUrl;
        lightboxEmbed.classList.remove('hidden');
        lightboxEmbed.setAttribute('aria-hidden', 'false');
      }} else {{
        lightboxImg.src = img.currentSrc || img.src;
        lightboxImg.alt = btn.dataset.brandName || '';
        lightboxImg.classList.remove('hidden');
      }}
    }}
    if (lightboxBrand) lightboxBrand.textContent = btn.dataset.brandName || '';
    if (lightboxStat) lightboxStat.textContent = btn.dataset.stat || '';
    if (lightboxIg) {{
      if (link) {{
        lightboxIg.href = link;
        lightboxIg.classList.remove('hidden');
      }} else {{
        lightboxIg.classList.add('hidden');
      }}
    }}
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
  }}

  function closeLightbox() {{
    if (!lightbox) return;
    lightbox.hidden = true;
    document.body.style.overflow = '';
    hideLightboxMedia();
    if (lightboxImg) lightboxImg.classList.remove('hidden');
  }}

  document.querySelectorAll('.piece-btn').forEach(btn => {{
    btn.addEventListener('click', () => openLightbox(btn));
  }});

  carouselNav?.querySelector('.carousel-prev')?.addEventListener('click', () => scrollCarousel(-1));
  carouselNav?.querySelector('.carousel-next')?.addEventListener('click', () => scrollCarousel(1));

  fbNav?.querySelector('.fb-prev')?.addEventListener('click', () => scrollFeedbacks(-1));
  fbNav?.querySelector('.fb-next')?.addEventListener('click', () => scrollFeedbacks(1));

  document.querySelectorAll('.fb-shot-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
      if (!lightbox || !lightboxImg) return;
      hideLightboxMedia();
      lightboxImg.src = btn.dataset.full || btn.querySelector('img')?.currentSrc || btn.querySelector('img')?.src || '';
      lightboxImg.alt = btn.dataset.brand || '';
      lightboxImg.classList.remove('hidden');
      if (lightboxBrand) lightboxBrand.textContent = btn.dataset.brand || '';
      if (lightboxStat) lightboxStat.textContent = btn.dataset.platform || '';
      if (lightboxIg) lightboxIg.classList.add('hidden');
      lightbox.hidden = false;
      document.body.style.overflow = 'hidden';
    }});
  }});

  lightboxClose?.addEventListener('click', closeLightbox);
  lightbox?.addEventListener('click', e => {{
    if (e.target === lightbox) closeLightbox();
  }});

  if (!picker) return;

  const toggle = picker.querySelector('.brand-picker-toggle');
  const panel = picker.querySelector('.brand-picker-panel');
  const valueEl = picker.querySelector('.brand-picker-value');
  const options = picker.querySelectorAll('.brand-opt');

  function closePicker() {{
    if (!panel || !toggle) return;
    panel.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
  }}

  function filterCategory(category, label) {{
    const showAll = category === 'all';
    document.querySelectorAll('#gallery-grid .piece').forEach(el => {{
      const cats = (el.dataset.categories || el.dataset.category || '').split(/\\s+/).filter(Boolean);
      const show = showAll || cats.includes(category);
      el.classList.toggle('hidden', !show);
    }});
    if (valueEl) valueEl.textContent = label;
    options.forEach(opt => opt.classList.toggle('active', !showAll && opt.dataset.category === category));
    if (galleryGrid) galleryGrid.scrollLeft = 0;
    updateEmptyState();
  }}

  toggle?.addEventListener('click', e => {{
    e.stopPropagation();
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
    if (panel) panel.hidden = open;
  }});

  options.forEach(opt => {{
    opt.addEventListener('click', e => {{
      e.stopPropagation();
      if (opt.classList.contains('active')) {{
        filterCategory('all', 'Filtrar por categoria');
      }} else {{
        filterCategory(opt.dataset.category || 'all', opt.dataset.label || 'Filtrar por categoria');
      }}
      closePicker();
    }});
  }});

  document.addEventListener('click', e => {{
    if (!picker.contains(e.target)) closePicker();
  }});

  document.addEventListener('keydown', e => {{
    if (e.key === 'Escape') {{
      closePicker();
      closeLightbox();
    }}
  }});
}})();
</script>
</body>
</html>"""


def build_print(metrics: dict, config: dict, assets: dict, period: str, fmt_num) -> str:
    d = _shared_data(metrics, config, assets, period, fmt_num)

    photo = (
        f'<img src="{H.escape(d["profile_img"])}" class="photo" alt=""/>'
        if d["profile_img"]
        else '<div class="photo ph"></div>'
    )

    stats = "".join(
        f'<div class="st"><b>{H.escape(n)}</b><span>{H.escape(l)}</span></div>'
        for n, l, _ in d["stats"]
    )

    reels = ""
    for reel in d["reels"][:4]:
        uri = reel.get("data_uri", "")
        img = f'<img src="{H.escape(uri)}" alt=""/>' if uri else ""
        reels += f'<div class="reel"><div class="ri">{img}</div><span>{H.escape(reel.get("brand",""))}</span></div>'

    cases = "".join(
        f"""<div class="cs"><b>{H.escape(_case_highlight(c.get('metrics','')))}</b>
        <strong>{H.escape(c.get('brand',''))}</strong>
        <p>{H.escape(c.get('title',''))}</p></div>"""
        for c in d["cases"]
    )

    ig = d["contact"].get("instagram", d["username"])
    brands = " · ".join(H.escape(b["name"]) for b in d["brands"][:9])

    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head>
<meta charset="utf-8"/>
<title>Media Kit — {H.escape(d['name'])}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital@0;1&family=Manrope:wght@400;600&display=swap" rel="stylesheet"/>
<style>
:root{{--bg:#F8F4EE;--ink:#141110;--body:#3D3530;--muted:#8C8178;--rose:#B86B5E;--line:#E0D8CE}}
*{{box-sizing:border-box;margin:0;padding:0}}
@page{{size:A4;margin:0}}
body{{font-family:Manrope,sans-serif;font-size:8pt;color:var(--body);background:var(--bg)}}
.pg{{width:210mm;height:297mm;padding:8mm 9mm;display:grid;grid-template-rows:auto auto 1fr auto;gap:3.5mm}}
.top{{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:3mm;border-bottom:1px solid var(--line)}}
.top h1{{font-family:"Cormorant Garamond",serif;font-size:26pt;font-weight:400;line-height:.92;color:var(--ink)}}
.top h1 em{{font-style:italic;color:var(--rose)}}
.top small{{font-size:5.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}}
.intro{{display:grid;grid-template-columns:40mm 1fr;gap:4mm;align-items:center}}
.photo{{width:100%;height:48mm;object-fit:cover;border-radius:70px 70px 10px 10px;box-shadow:0 6px 20px rgba(0,0,0,.08)}}
.ph{{background:linear-gradient(135deg,#E8C8C0,#EDE6DC);height:48mm;border-radius:70px 70px 10px 10px}}
.lead{{font-size:7.2pt;line-height:1.55;color:var(--body)}}
.ig{{margin-top:2mm;font-weight:700;color:var(--rose);font-size:7.5pt}}
.stats{{display:grid;grid-template-columns:repeat(6,1fr);gap:1.5mm;background:var(--ink);border-radius:2mm;padding:2mm}}
.st{{text-align:center;color:#fff;padding:1.5mm}}
.st b{{display:block;font-family:"Cormorant Garamond",serif;font-size:12pt;font-weight:500}}
.st span{{font-size:4.5pt;text-transform:uppercase;letter-spacing:.1em;opacity:.55}}
.main{{display:grid;grid-template-columns:1fr 30mm;gap:3mm}}
.lbl{{font-size:5pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--rose);margin-bottom:1.5mm}}
.reels{{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5mm}}
.ri{{aspect-ratio:9/14;border-radius:2mm;overflow:hidden;background:var(--line)}}
.ri img{{width:100%;height:100%;object-fit:cover}}
.reel span{{font-size:4.5pt;color:var(--muted);display:block;margin-top:.8mm}}
.cases{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5mm;margin-top:2.5mm}}
.cs{{background:#fff;border:1px solid var(--line);border-radius:2mm;padding:2mm;border-top:2px solid var(--rose)}}
.cs b{{font-family:"Cormorant Garamond",serif;font-size:16pt;color:var(--rose);display:block;line-height:1}}
.cs strong{{font-size:5pt;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}}
.cs p{{font-size:6.5pt;font-weight:600;color:var(--ink);margin-top:.5mm}}
.side{{background:#fff;border:1px solid var(--line);border-radius:2mm;padding:2.5mm;font-size:6pt;line-height:1.55}}
.side p{{margin-bottom:1mm}}
.side b{{color:var(--ink)}}
.bot{{border-top:1px solid var(--line);padding-top:2.5mm;display:flex;justify-content:space-between;align-items:end}}
.brands{{font-size:5.5pt;color:var(--muted);max-width:120mm;line-height:1.45}}
.cta{{text-align:right}}
.cta em{{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:11pt;color:var(--rose);display:block}}
.cta span{{font-size:6.5pt;font-weight:700;color:var(--ink)}}
</style></head><body>
<div class="pg">
  <header class="top">
    <div><small>Media Kit · UGC Beauty · {H.escape(period)}</small>
    <h1>{H.escape(d['first'])} <em>{H.escape(d['last'])}</em></h1></div>
    <small>Baixada Santista</small>
  </header>
  <section class="intro">{photo}
    <div><p class="lead">{H.escape(d['about'])}</p><p class="ig">@{H.escape(ig)}</p></div>
  </section>
  <section class="stats">{stats}</section>
  <section class="main">
    <div>
      <p class="lbl">Portfólio beauty</p>
      <div class="reels">{reels}</div>
      <p class="lbl" style="margin-top:2.5mm">Cases</p>
      <div class="cases">{cases}</div>
    </div>
    <aside class="side"><p class="lbl" style="margin-bottom:2mm">Audiência</p>
    {''.join(f'<p><b>{H.escape(str(int(v) if v==int(v) else v))}%</b> {H.escape(k)}</p>' for k,v in d['aud'])}</aside>
  </section>
  <footer class="bot">
    <p class="brands"><strong style="color:var(--ink)">Marcas:</strong> {brands}<br/>{H.escape(d['pricing_note'])}</p>
    <div class="cta"><em>Vamos criar juntas?</em><span>instagram.com/{H.escape(ig)}</span></div>
  </footer>
</div></body></html>"""
