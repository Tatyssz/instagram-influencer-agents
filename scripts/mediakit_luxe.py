"""Media Kit LUXE — portfólio web (galeria de trabalhos) + PDF."""

from __future__ import annotations

import html as H
import re

from mediakit_assets import format_piece_views, portfolio_categories


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
        (fmt_num(mk.get("views_30d_official", 0)), "Views", "30d"),
        (fmt_num(mk.get("interactions_30d_official", 0)), "Interações", "30d"),
        (f"{mk.get('interaction_rate_on_views_pct', 16.5)}%", "Engajamento", ""),
        (fmt_num(mk.get("median_views_per_reel", mk.get("avg_views_per_reel", 0))), "Views/Reel", ""),
        (fmt_num(mk.get("best_reach_per_reel", 0)), "Pico alcance", ""),
    ]

    aud = [
        ("Brasil", float(mk.get("brazil_audience_pct", 84))),
        ("Mulheres", float(mk.get("female_audience_pct", 71.8))),
        ("25–44", float(mk.get("core_age_25_44_pct", 57.1))),
        ("Baixada", float(mk.get("baixada_santista_pct", 24.2))),
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
        "hero_float_uris": assets.get("hero_float_uris", []),
        "reels": reels,
        "case_thumbs": case_thumbs,
        "about": config.get("about", ""),
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


def _theme_css(config: dict) -> str:
    t = config.get("theme") or {}
    d = {
        "bg": "#F3EBE6",
        "white": "#FFFAF7",
        "warm": "#E8DED6",
        "ink": "#3A2E28",
        "body": "#5A4842",
        "muted": "#9A8580",
        "blush": "#E8A89A",
        "peach": "#E8956F",
        "mauve": "#C9A0A8",
        "copper": "#D4846A",
        "copper_deep": "#B86B58",
        "blush_light": "#F0C4B8",
        "line": "#DDD0C8",
        "mocha": "#52463E",
    }
    c = {k: t.get(k, v) for k, v in d.items()}
    return f"""
:root{{
  --bg:{c['bg']};--white:{c['white']};--warm:{c['warm']};
  --ink:{c['ink']};--body:{c['body']};--muted:{c['muted']};
  --blush:{c['blush']};--peach:{c['peach']};--mauve:{c['mauve']};
  --copper:{c['copper']};--copper-deep:{c['copper_deep']};--blush-light:{c['blush_light']};
  --accent:var(--copper);--accent-deep:var(--copper-deep);--accent-light:var(--blush-light);
  --mocha:{c['mocha']};--line:{c['line']};
  --shadow:0 16px 48px rgba(58,46,40,.09);
  --max:1140px;--ease:cubic-bezier(.22,1,.36,1);
}}"""


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

    portrait = (
        f'<img src="{H.escape(d["profile_img"])}" alt="{H.escape(dn)}" class="hero-portrait"/>'
        if d["profile_img"]
        else '<div class="hero-portrait hero-ph"></div>'
    )

    photo = f"""
    <div class="intro-visual">
      <figure class="prisma">
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

    category_options = (
        f'<button type="button" class="brand-opt active" data-category="all" '
        f'data-label="Todas as categorias"><span>Todas as categorias</span><em>{work_count}</em></button>'
    )
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
      <button type="button" class="brand-picker-toggle" aria-expanded="false" aria-haspopup="listbox">
        <span class="brand-picker-kicker">Categoria</span>
        <span class="brand-picker-value">Todas as categorias</span>
        <span class="brand-picker-chevron" aria-hidden="true"></span>
      </button>
      <div class="brand-picker-panel" role="listbox" hidden>{category_options}
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
        gallery_html += f"""
        <article class="piece" data-brand="{H.escape(slug)}" data-category="{H.escape(category)}" data-categories="{categories_attr}" data-media-id="{H.escape(reel.get('media_id', ''))}">
          <button type="button" class="piece-btn" data-permalink="{H.escape(permalink)}"
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

    stats_html = "".join(
        f"""<div class="stat">
          <b>{H.escape(n)}</b>
          <span>{H.escape(l)}{f' · {H.escape(s)}' if s else ''}</span>
        </div>"""
        for n, l, s in d["stats"][:4]
    )

    aud_html = "".join(
        f"""<div class="aud"><b>{H.escape(str(int(v) if v == int(v) else v))}%</b><span>{H.escape(k)}</span></div>"""
        for k, v in d["aud"]
    )

    brand_items = "".join(f"<li>{H.escape(b['name'])}</li>" for b in d["brands"])
    marquee = brand_items + brand_items
    cta = d["contact"].get("cta", "Parcerias via DM")
    theme_css = _theme_css(config)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="description" content="{H.escape(d['about'][:160])}"/>
<title>{H.escape(dn)} · Portfólio UGC Beauty</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<style>
{theme_css}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:"Plus Jakarta Sans",system-ui,sans-serif;font-size:15px;line-height:1.65;color:var(--body);background:var(--bg);-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.topbar{{position:sticky;top:0;z-index:100;background:rgba(243,235,230,.92);backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}}
.topbar-inner{{max-width:var(--max);margin:0 auto;padding:1rem clamp(1.5rem,5vw,2.5rem);display:flex;align-items:center;justify-content:space-between;gap:1rem}}
.topbar-name{{font-family:"Cormorant Garamond",serif;font-size:1.08rem;font-weight:600;color:var(--ink);letter-spacing:.04em}}
.topbar-links{{display:flex;gap:1.75rem;align-items:center}}
.topbar-links a{{font-size:.65rem;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);transition:color .25s}}
.topbar-links a:hover{{color:var(--copper)}}
.topbar-cta{{padding:.55rem 1.15rem;border-radius:999px;background:var(--mocha);color:#FBF7F2;font-size:.65rem;font-weight:600;letter-spacing:.08em;transition:background .25s}}
.topbar-cta:hover{{background:var(--copper-deep)}}
.intro{{padding:clamp(3rem,7vw,5rem) clamp(1.5rem,5vw,2.5rem);background:linear-gradient(180deg,var(--white) 0%,var(--bg) 55%,rgba(232,168,154,.08) 100%);border-bottom:1px solid var(--line)}}
.intro-inner{{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,5vw,4rem);align-items:center}}
.intro-visual{{display:flex;justify-content:center;align-items:center}}
.prisma{{margin:0;width:min(460px,100%);display:grid;grid-template-columns:1fr repeat(3,minmax(54px,.19fr));background:var(--white);border-radius:26px 8px 18px 26px;overflow:hidden;box-shadow:0 28px 72px rgba(58,46,40,.1),0 0 0 1px var(--line)}}
.prisma-main{{grid-column:1;grid-row:1;min-height:min(440px,72vw);position:relative;background:var(--warm)}}
.hero-portrait{{width:100%;height:100%;min-height:inherit;object-fit:cover;object-position:center 8%;display:block}}
.hero-ph{{width:100%;min-height:inherit;background:linear-gradient(165deg,var(--blush-light),var(--warm))}}
.prisma-strips{{grid-column:2/-1;grid-row:1;display:grid;grid-template-rows:repeat(3,1fr);border-left:1px solid var(--line)}}
.prisma-strip{{position:relative;overflow:hidden;border-bottom:1px solid var(--line)}}
.prisma-strip:last-child{{border-bottom:none}}
.prisma-strip img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s var(--ease),filter .6s var(--ease)}}
.prisma-strip:hover img{{transform:scale(1.08);filter:saturate(1.06)}}
.prisma-strip .fi-1{{object-position:center 42%}}
.prisma-strip .fi-2{{object-position:center 40%}}
.prisma-strip .fi-3{{object-position:center 12%}}
.prisma-tag{{position:absolute;left:0;right:0;bottom:0;padding:.45rem .2rem;font-size:.46rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;text-align:center;color:#FBF7F2;background:linear-gradient(0deg,rgba(82,70,62,.78),transparent);opacity:0;transition:opacity .35s var(--ease)}}
.prisma-strip:hover .prisma-tag{{opacity:1}}
.intro-copy{{display:flex;flex-direction:column;justify-content:center;min-width:0}}
.intro-badge{{font-size:.58rem;font-weight:600;letter-spacing:.28em;text-transform:uppercase;color:var(--copper);margin-bottom:1rem}}
.intro h1{{font-family:"Cormorant Garamond",serif;font-size:clamp(2.8rem,6vw,4.2rem);font-weight:400;line-height:1.02;color:var(--ink);letter-spacing:-.01em}}
.intro h1 em{{font-style:italic;font-weight:400;color:var(--peach)}}
.intro-lead{{margin-top:1.15rem;max-width:34rem;font-size:1rem;line-height:1.75;color:var(--body);font-weight:300}}
.intro-meta{{margin-top:2rem;padding-top:1.35rem;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:2rem 2.75rem}}
.meta-item{{display:flex;flex-direction:column;gap:.25rem}}
.meta-item strong{{font-family:"Cormorant Garamond",serif;font-size:1.35rem;font-weight:600;color:var(--ink);line-height:1}}
.meta-item span{{font-size:.58rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--copper)}}
.meta-loc strong{{font-family:"Plus Jakarta Sans",sans-serif;font-size:1rem;font-weight:600;letter-spacing:.06em}}
.gallery{{background:var(--white);border-top:1px solid var(--line);padding:clamp(3.5rem,6vw,5rem) 0 clamp(4rem,7vw,5.5rem)}}
.gallery-top{{max-width:var(--max);margin:0 auto;padding:0 clamp(1.25rem,4vw,2rem);display:flex;justify-content:space-between;align-items:flex-end;gap:2rem}}
.gallery-head{{min-width:0;flex:1}}
.gallery-eyebrow{{font-size:.58rem;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--copper);margin-bottom:.5rem}}
.gallery-head h2{{font-family:"Cormorant Garamond",serif;font-size:clamp(2rem,3.8vw,2.75rem);font-weight:400;line-height:1.05;color:var(--ink)}}
.gallery-actions{{flex-shrink:0;display:flex;align-items:flex-end;justify-content:flex-end}}
.brand-picker{{position:relative}}
.brand-picker-toggle{{display:flex;flex-direction:column;align-items:flex-start;gap:.2rem;min-width:min(240px,42vw);padding:.75rem 2.25rem .75rem 1rem;border:1px solid var(--line);border-radius:14px;background:var(--white);cursor:pointer;text-align:left;transition:border-color .25s var(--ease),box-shadow .25s var(--ease)}}
.brand-picker-toggle:hover,.brand-picker-toggle[aria-expanded="true"]{{border-color:var(--blush);box-shadow:0 8px 28px rgba(58,46,40,.08)}}
.brand-picker-kicker{{font-size:.52rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}}
.brand-picker-value{{font-family:"Cormorant Garamond",serif;font-size:1.05rem;color:var(--ink);line-height:1.2}}
.brand-picker-chevron{{position:absolute;right:1rem;top:50%;width:.45rem;height:.45rem;border-right:1.5px solid var(--copper);border-bottom:1.5px solid var(--copper);transform:translateY(-65%) rotate(45deg);transition:transform .25s var(--ease)}}
.brand-picker-toggle[aria-expanded="true"] .brand-picker-chevron{{transform:translateY(-35%) rotate(-135deg)}}
.brand-picker-panel{{position:absolute;z-index:40;right:0;top:calc(100% + .5rem);width:min(360px,calc(100vw - 2.5rem));max-height:min(380px,58vh);overflow-y:auto;padding:.45rem;border:1px solid var(--line);border-radius:16px;background:var(--white);box-shadow:0 20px 56px rgba(58,46,40,.14);scrollbar-width:thin}}
.brand-opt{{display:flex;align-items:center;justify-content:space-between;gap:1rem;width:100%;padding:.7rem .85rem;border:none;border-radius:10px;background:transparent;cursor:pointer;text-align:left;transition:background .2s var(--ease)}}
.brand-opt span{{font-family:"Cormorant Garamond",serif;font-size:1rem;color:var(--ink)}}
.brand-opt em{{font-family:"Plus Jakarta Sans",sans-serif;font-size:.62rem;font-style:normal;font-weight:500;letter-spacing:.06em;color:var(--muted)}}
.brand-opt:hover{{background:var(--warm)}}
.brand-opt.active{{background:rgba(232,168,154,.14)}}
.brand-opt.active span{{color:var(--copper-deep)}}
.grid{{max-width:var(--max);margin:0 auto;padding:clamp(2rem,4vw,2.75rem) clamp(1.25rem,4vw,2rem) 0;display:grid;grid-template-columns:repeat(4,1fr);gap:1.35rem;border-top:1px solid var(--line);margin-top:clamp(1.75rem,3vw,2.25rem)}}
.gallery-empty{{grid-column:1/-1;display:none;padding:3rem 1rem;text-align:center;font-family:"Cormorant Garamond",serif;font-size:1.25rem;color:var(--muted)}}
.gallery-empty.show{{display:block}}
.piece{{transition:transform .35s var(--ease)}}
.piece:hover{{transform:translateY(-3px)}}
.piece.hidden{{display:none}}
.piece-btn{{display:block;width:100%;padding:0;border:none;background:none;cursor:pointer;text-align:left;font:inherit;color:inherit}}
.piece-btn:focus-visible{{outline:2px solid var(--copper);outline-offset:3px;border-radius:16px}}
.piece-img{{position:relative;aspect-ratio:4/5;border-radius:16px 16px 0 0;overflow:hidden;background:var(--warm);box-shadow:var(--shadow)}}
.piece-img img{{width:100%;height:100%;object-fit:cover;object-position:top center;display:block;transform-origin:top center;transition:transform .55s var(--ease)}}
.piece[data-media-id="18071655761192823"] .piece-img img{{object-position:50% 26%;transform-origin:50% 26%}}
.piece[data-media-id="18015297932414597"] .piece-img img{{object-position:50% 50%;transform-origin:50% 50%}}
.piece[data-media-id="18146252194343099"] .piece-img img{{object-position:50% 100%;transform-origin:50% 100%}}
.piece:hover .piece-img img{{transform:scale(1.03)}}
.piece-cap{{padding:.75rem .85rem .85rem;background:var(--white);border:1px solid var(--line);border-top:none;border-radius:0 0 16px 16px}}
.piece-brand{{display:block;font-family:"Cormorant Garamond",serif;font-size:1rem;font-weight:500;color:var(--ink);line-height:1.2}}
.piece-stat{{display:block;margin-top:.25rem;font-size:.62rem;font-weight:500;letter-spacing:.06em;color:var(--muted)}}
.lightbox{{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:clamp(1rem,4vw,2rem);background:rgba(58,46,40,.82);backdrop-filter:blur(8px)}}
.lightbox[hidden]{{display:none}}
.lightbox-inner{{position:relative;width:min(420px,100%);max-height:92vh;display:flex;flex-direction:column;gap:1rem}}
.lightbox-close{{position:absolute;z-index:2;top:-.25rem;right:0;width:2.25rem;height:2.25rem;border:none;border-radius:50%;background:rgba(251,247,242,.15);color:#FBF7F2;font-size:1.35rem;line-height:1;cursor:pointer}}
.lightbox-close:hover{{background:rgba(251,247,242,.28)}}
.lightbox-img{{width:100%;max-height:min(72vh,720px);object-fit:contain;border-radius:16px;background:var(--ink);box-shadow:0 24px 64px rgba(0,0,0,.35)}}
.lightbox-meta{{padding:.25rem .15rem 0;color:#FBF7F2}}
.lightbox-brand{{font-family:"Cormorant Garamond",serif;font-size:1.35rem;line-height:1.2}}
.lightbox-stat{{margin-top:.35rem;font-size:.72rem;opacity:.78}}
.lightbox-ig{{display:inline-block;margin-top:1rem;padding:.65rem 1.15rem;border-radius:999px;background:#FBF7F2;color:var(--mocha);font-size:.68rem;font-weight:600;letter-spacing:.06em;text-decoration:none;transition:background .25s}}
.lightbox-ig:hover{{background:var(--blush-light)}}
.lightbox-ig.hidden{{display:none}}
.stats-band{{border-block:1px solid var(--line);background:linear-gradient(180deg,var(--warm) 0%,rgba(232,168,154,.1) 100%);padding:2rem clamp(1.25rem,4vw,2rem)}}
.stats-row{{max-width:var(--max);margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}
.stat{{text-align:center}}
.stat b{{display:block;font-family:"Cormorant Garamond",serif;font-size:clamp(1.4rem,2.5vw,1.9rem);font-weight:600;color:var(--ink);line-height:1}}
.stat span{{display:block;margin-top:.25rem;font-size:.6rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
.marquee{{overflow:hidden;padding:1.5rem 0;border-bottom:1px solid var(--line);background:var(--white)}}
.marquee-track{{display:flex;width:max-content;animation:marquee 38s linear infinite}}
.marquee-track ul{{display:flex;gap:2.5rem;list-style:none;padding:0 1.25rem}}
.marquee-track li{{font-family:"Cormorant Garamond",serif;font-size:1.15rem;color:var(--muted);white-space:nowrap}}
.marquee-track li::after{{content:"·";margin-left:2.5rem;opacity:.35}}
@keyframes marquee{{to{{transform:translateX(-50%)}}}}
.bottom{{max-width:var(--max);margin:0 auto;padding:3.5rem clamp(1.25rem,4vw,2rem);display:grid;grid-template-columns:1.2fr 1fr;gap:2.5rem;align-items:start}}
.bottom h3{{font-family:"Cormorant Garamond",serif;font-size:1.5rem;font-weight:500;color:var(--ink);margin-bottom:.65rem}}
.bottom p{{color:var(--body);line-height:1.75}}
.aud-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem}}
.aud{{text-align:center;padding:1rem;background:var(--white);border:1px solid var(--line);border-radius:14px}}
.aud b{{display:block;font-family:"Cormorant Garamond",serif;font-size:1.5rem;font-weight:600;color:var(--ink)}}
.aud span{{font-size:.58rem;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.contact{{margin:0 clamp(1.25rem,4vw,2rem) 2rem;padding:3rem 2rem;border-radius:24px;background:linear-gradient(145deg,var(--mocha) 0%,#4A4038 100%);color:#FBF7F2;text-align:center}}
.contact h2{{font-family:"Cormorant Garamond",serif;font-size:clamp(2rem,4vw,2.8rem);font-weight:400;font-style:italic}}
.contact p{{margin-top:.5rem;font-size:.9rem;opacity:.8}}
.contact a{{display:inline-block;margin-top:1.5rem;padding:.85rem 1.75rem;border-radius:999px;background:#FBF7F2;color:var(--mocha);font-size:.78rem;font-weight:600;transition:transform .25s,background .25s}}
.contact a:hover{{transform:translateY(-2px);background:var(--blush-light)}}
.contact small{{display:block;margin-top:1rem;font-size:.68rem;opacity:.5}}
.footer{{text-align:center;padding:1.5rem;font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
@media(max-width:900px){{
  .intro-inner{{grid-template-columns:1fr}}
  .gallery-top{{flex-direction:column;align-items:stretch;gap:1.25rem}}
  .gallery-actions{{width:100%;justify-content:flex-end}}
  .brand-picker{{flex:1;max-width:100%}}
  .brand-picker-toggle{{width:100%;min-width:0}}
  .brand-picker-panel{{left:0;right:0;width:100%}}
  .intro-visual{{order:-1}}
  .prisma{{grid-template-columns:1fr;grid-template-rows:auto auto auto;border-radius:22px}}
  .prisma-main{{min-height:min(380px,68vw)}}
  .prisma-strips{{grid-column:1;grid-row:2;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr;border-left:none;border-top:1px solid var(--line);min-height:108px}}
  .prisma-strip{{border-bottom:none;border-right:1px solid var(--line)}}
  .prisma-strip:last-child{{border-right:none}}
  .prisma-tag{{opacity:1;font-size:.42rem;padding:.35rem .15rem}}
  .grid{{grid-template-columns:repeat(3,1fr)}}
  .stats-row{{grid-template-columns:repeat(2,1fr)}}
  .bottom{{grid-template-columns:1fr}}
}}
@media(max-width:600px){{
  .intro-inner{{text-align:center}}
  .intro-lead{{margin-left:auto;margin-right:auto}}
  .intro-meta{{justify-content:center;gap:1.5rem 2rem}}
  .prisma-main{{min-height:min(340px,78vw)}}
  .prisma-strips{{min-height:92px}}
  .grid{{grid-template-columns:repeat(2,1fr);gap:.85rem}}
  .topbar-links a:not(.topbar-cta){{display:none}}
}}
</style>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a class="topbar-name" href="#">{H.escape(dn)}</a>
    <div class="topbar-links">
      <a href="#trabalhos">Trabalhos e Parcerias</a>
      <a href="#contato">Contato</a>
      <a class="topbar-cta" href="https://instagram.com/{H.escape(ig)}">@{H.escape(ig)}</a>
    </div>
  </div>
</header>

<section class="intro">
  <div class="intro-inner">
    <div class="intro-copy">
      <p class="intro-badge">{H.escape(d['hero_subtitle'])}</p>
      <h1>{H.escape(first)} <em>{H.escape(rest)}</em></h1>
      <p class="intro-lead">{H.escape(d['tagline'])}</p>
      <div class="intro-meta">{meta_html}</div>
    </div>
    {photo}
  </div>
</section>

<section id="trabalhos" class="gallery">
  <div class="gallery-top">
    <div class="gallery-head">
      <p class="gallery-eyebrow">Parcerias beauty &amp; hair · 2024–2026</p>
      <h2>Trabalhos e Parcerias</h2>
    </div>
    <div class="gallery-actions">
      {brand_picker}
    </div>
  </div>
  <div class="grid">{gallery_html}
    <p class="gallery-empty" id="gallery-empty">Nenhum trabalho nesta categoria.</p>
  </div>
</section>

<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Visualizar trabalho">
  <div class="lightbox-inner">
    <button type="button" class="lightbox-close" aria-label="Fechar">&times;</button>
    <img class="lightbox-img" alt=""/>
    <div class="lightbox-meta">
      <p class="lightbox-brand"></p>
      <p class="lightbox-stat"></p>
      <a class="lightbox-ig" href="#" target="_blank" rel="noopener noreferrer">Ver no Instagram</a>
    </div>
  </div>
</div>

<div class="stats-band">
  <div class="stats-row">{stats_html}</div>
</div>

<div class="marquee">
  <div class="marquee-track"><ul>{marquee}</ul></div>
</div>

<div class="bottom">
  <div>
    <h3>Sobre</h3>
    <p>{H.escape(d['about'])}</p>
  </div>
  <div>
    <h3>Audiência</h3>
    <div class="aud-grid">{aud_html}</div>
  </div>
</div>

<section id="contato" class="contact">
  <h2>{H.escape(cta)}</h2>
  <p>{H.escape(d['pricing_note'])}</p>
  <a href="https://instagram.com/{H.escape(ig)}">@{H.escape(ig)}</a>
  <small>{H.escape(d['period'])}</small>
</section>

<footer class="footer">{H.escape(dn)} · UGC Beauty · {work_count} peças</footer>

<script>
(function() {{
  const picker = document.getElementById('brand-picker');
  const galleryEmpty = document.getElementById('gallery-empty');
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = lightbox?.querySelector('.lightbox-img');
  const lightboxBrand = lightbox?.querySelector('.lightbox-brand');
  const lightboxStat = lightbox?.querySelector('.lightbox-stat');
  const lightboxIg = lightbox?.querySelector('.lightbox-ig');
  const lightboxClose = lightbox?.querySelector('.lightbox-close');

  function updateEmptyState() {{
    if (!galleryEmpty) return;
    const visible = document.querySelectorAll('.piece:not(.hidden)').length;
    galleryEmpty.classList.toggle('show', visible === 0);
  }}

  function openLightbox(btn) {{
    if (!lightbox || !lightboxImg) return;
    const img = btn.querySelector('.piece-img img');
    if (!img) return;
    lightboxImg.src = img.currentSrc || img.src;
    lightboxImg.alt = btn.dataset.brandName || '';
    if (lightboxBrand) lightboxBrand.textContent = btn.dataset.brandName || '';
    if (lightboxStat) lightboxStat.textContent = btn.dataset.stat || '';
    const link = btn.dataset.permalink || '';
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
    if (lightboxImg) lightboxImg.src = '';
  }}

  document.querySelectorAll('.piece-btn').forEach(btn => {{
    btn.addEventListener('click', () => openLightbox(btn));
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
    document.querySelectorAll('.piece').forEach(el => {{
      const cats = (el.dataset.categories || el.dataset.category || '').split(/\\s+/).filter(Boolean);
      const show = category === 'all' || cats.includes(category);
      el.classList.toggle('hidden', !show);
    }});
    if (valueEl) valueEl.textContent = label;
    options.forEach(opt => opt.classList.toggle('active', opt.dataset.category === category));
    updateEmptyState();
  }}

  toggle?.addEventListener('click', () => {{
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
    if (panel) panel.hidden = open;
  }});

  options.forEach(opt => {{
    opt.addEventListener('click', () => {{
      filterCategory(opt.dataset.category || 'all', opt.dataset.label || 'Todas as categorias');
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
