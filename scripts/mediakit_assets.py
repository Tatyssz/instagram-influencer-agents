"""Baixa imagens do media kit para assets locais (PDF confiavel)."""

from __future__ import annotations

import base64
import json
import mimetypes
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests

ASSETS = Path(__file__).resolve().parent.parent / "output" / "mediakit" / "assets"
ROOT = ASSETS.parent.parent.parent
MANUAL_COVERS = ROOT / "data" / "mediakit" / "manual-covers"
MANUAL_VIDEOS = ROOT / "data" / "mediakit" / "manual-videos"
FEEDBACKS_SRC = ROOT / "data" / "mediakit" / "feedbacks"
FEEDBACKS_ASSETS = ASSETS / "feedbacks"
MIN_VIDEO_BYTES = 50_000
GRAPH_IG = "https://graph.instagram.com/v21.0"
LOCAL_HD_CANDIDATES = [
    ROOT / "data" / "mediakit" / "profile-hd.png",
    ROOT / "data" / "mediakit" / "profile-hd.jpg",
    ROOT / "data" / "mediakit" / "profile-hd.webp",
    ASSETS / "profile-hd.jpg",
]

MIN_PROFILE_BYTES = 35_000  # API entrega ~10 KB (206 px) — abaixo disso busca alternativa
MIN_COVER_BYTES = 8_000

DEFAULT_BEAUTY = [
    "maquiagem", "makeup", "batom", "contorno", "cabelo", "cachead", "cachos",
    "skincare", "beauty", "elseve", "haskell", "hidramais", "salon", "dailus",
    "kv", "leave-in", "todecacho", "beautyfair", "hair", "ugc",
]
DEFAULT_EXCLUDE = [
    "gêmeos", "gemeos", "filhos", "família", "familia", "marido", "mãe", "mae",
    "copa", "humor", "textão", "textao", "blogueira", "gratidão define",
    "mães de meninas", "sapo", "#fy", "entendedores",
]

HAIR_STYLE_KEYWORDS = (
    "trança",
    "tranca",
    "tranças",
    "trancas",
    "trancanago",
    "braindstyle",
    "brainds",
    "braid",
)


def _is_hair_style_content(caption: str) -> bool:
    text = _caption_text(caption)
    return any(k in text for k in HAIR_STYLE_KEYWORDS)


def _guess_ext(url: str, content_type: str | None) -> str:
    if content_type and "jpeg" in content_type:
        return ".jpg"
    if content_type and "png" in content_type:
        return ".png"
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        if path.endswith(ext):
            return ext if ext != ".jpeg" else ".jpg"
    return ".jpg"


def _api_token() -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
    except ImportError:
        pass
    return os.getenv("META_ACCESS_TOKEN", "").strip()


def refresh_post_thumbnail(post: dict, token: str | None = None) -> dict:
    """Busca thumbnail_url fresca na API — capa real do Reel, URL sem expirar."""
    token = token or _api_token()
    media_id = post.get("id")
    if not token or not media_id:
        return post
    if post.get("media_type") not in ("VIDEO", "REEL"):
        return post
    try:
        r = requests.get(
            f"{GRAPH_IG}/{media_id}",
            params={"fields": "thumbnail_url", "access_token": token},
            timeout=20,
        )
        r.raise_for_status()
        thumb = r.json().get("thumbnail_url")
        if thumb:
            updated = dict(post)
            updated["thumbnail_url"] = thumb
            return updated
    except requests.RequestException:
        pass
    return post


def _cleanup_stale_reel_assets(valid_ids: set[str]) -> None:
    """Remove cache antigo indexado (reel-0.jpg, reel-1.jpg…)."""
    if not ASSETS.exists():
        return
    for path in ASSETS.glob("reel-*.jpg"):
        stem = path.stem.removeprefix("reel-")
        if stem in valid_ids:
            continue
        if stem.isdigit() and len(stem) < 12:
            path.unlink(missing_ok=True)
            path.with_suffix(".src").unlink(missing_ok=True)


def download(url: str, name: str) -> Path | None:
    if not url:
        return None
    ASSETS.mkdir(parents=True, exist_ok=True)
    base = ASSETS / name
    meta = base.with_suffix(".src")
    dest = base if base.suffix else base.with_suffix(".jpg")
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        if not base.suffix:
            dest = base.with_suffix(_guess_ext(url, r.headers.get("Content-Type")))
        dest.write_bytes(r.content)
        meta.write_text(url, encoding="utf-8")
        return dest
    except requests.RequestException:
        if dest.exists() and meta.exists() and meta.read_text(encoding="utf-8") == url:
            return dest
        return None


def to_data_uri(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _caption_text(caption: str) -> str:
    return (caption or "").lower()


def _extract_brand(caption: str, config: dict | None = None) -> str:
    """Identifica marca de parceria pela legenda (prioridade: brand_partnerships)."""
    matched = _match_partnership_brand(caption, config)
    if matched:
        return matched
    return "Beauty"


def _partnership_rules(config: dict | None) -> list[dict]:
    config = config or {}
    rules = config.get("brand_partnerships")
    if rules:
        return rules
    return [
        {"name": "Salon Line", "match": ["salonline", "todecacho"]},
        {"name": "L'Oréal Paris", "match": ["loreal", "elseve"]},
        {"name": "Haskell", "match": ["haskell"]},
        {"name": "Hidramais", "match": ["hidramais"]},
        {"name": "Dailus", "match": ["dailus"]},
        {"name": "Phálle Beauty", "match": ["phalle"]},
        {"name": "Dalla", "match": ["dalla"]},
        {"name": "KV Makeup", "match": ["kvmakeup", "kv makeup"]},
        {"name": "Nina Makeup", "match": ["ninamakeup", "nina makeup"]},
        {"name": "Catharine Hill", "match": ["catharinehill"]},
        {"name": "Vizzela", "match": ["vizzela"]},
        {"name": "Reiny Cosméticos", "match": ["reiny"]},
        {"name": "Bauny", "match": ["bauny"]},
    ]


def _match_partnership_brand(caption: str, config: dict | None = None) -> str | None:
    text = _caption_text(caption)
    best: tuple[int, str] | None = None
    for rule in _partnership_rules(config):
        for token in rule.get("match", []):
            tok = token.lower()
            if " " in tok:
                if tok not in text:
                    continue
            elif not re.search(rf"(?<![a-z0-9]){re.escape(tok)}(?![a-z0-9])", text):
                continue
            score = len(tok)
            if not best or score > best[0]:
                best = (score, rule["name"])
    return best[1] if best else None


def _normalize_category_id(category: str) -> str:
    """Alias legado — versão anterior usou 'midia' por engano."""
    if category == "midia":
        return "moda"
    return category


def portfolio_categories(config: dict | None = None) -> list[dict]:
    config = config or {}
    cats = config.get("portfolio_categories")
    if cats:
        normalized = []
        for cat in cats:
            entry = dict(cat)
            entry["id"] = _normalize_category_id(entry.get("id", ""))
            if entry["id"] == "moda" and entry.get("name") in ("Mídia", "Midia"):
                entry["name"] = "Moda"
            normalized.append(entry)
        return normalized
    return [
        {"id": "beleza", "name": "Beleza"},
        {"id": "cabelo", "name": "Cabelo"},
        {"id": "moda", "name": "Moda"},
        {"id": "perfume", "name": "Perfume"},
        {"id": "eventos", "name": "Eventos"},
    ]


def _media_categories_map(config: dict | None = None) -> dict[str, list[str]]:
    portfolio = (config or {}).get("portfolio") or {}
    raw = portfolio.get("media_categories") or {}
    mapped: dict[str, list[str]] = {}
    for media_id, categories in raw.items():
        if not categories:
            continue
        mapped[str(media_id)] = [_normalize_category_id(str(c)) for c in categories]
    return mapped


def _media_views_map(config: dict | None = None) -> dict[str, int]:
    portfolio = (config or {}).get("portfolio") or {}
    raw = portfolio.get("media_views") or {}
    mapped: dict[str, int] = {}
    for media_id, views in raw.items():
        try:
            mapped[str(media_id)] = int(views)
        except (TypeError, ValueError):
            continue
    return mapped


def _scraped_views_map() -> dict[str, int]:
    path = ROOT / "data" / "mediakit" / "scraped_views.json"
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    mapped: dict[str, int] = {}
    for media_id, views in raw.items():
        try:
            mapped[str(media_id)] = int(views)
        except (TypeError, ValueError):
            continue
    return mapped


def resolve_media_views(
    media_id: str,
    insights: dict | None,
    config: dict | None = None,
    like_count: int = 0,
) -> int:
    """Views do Reel — override manual, API, cache scrape, reach ou estimativa por curtidas."""
    ins = insights or {}
    portfolio = (config or {}).get("portfolio") or {}
    override = _media_views_map(config).get(str(media_id))
    if override is not None:
        return override
    api_views = int(ins.get("views") or 0)
    if api_views:
        return api_views
    scraped = _scraped_views_map().get(str(media_id))
    if scraped:
        return scraped
    reach = int(ins.get("reach") or 0)
    if reach:
        return reach
    likes = int(like_count or 0)
    if likes > 0 and portfolio.get("views_fallback_from_likes", True):
        ratio = float(portfolio.get("views_likes_ratio") or 14)
        minimum = int(portfolio.get("views_likes_min") or 300)
        return max(int(likes * ratio), minimum)
    return 0


def _brand_category_map(config: dict | None = None) -> dict[str, str]:
    return {
        rule["name"]: rule["category"]
        for rule in _partnership_rules(config)
        if rule.get("category")
    }


def resolve_piece_category(brand: str, caption: str, config: dict | None = None) -> str:
    """Categoria UGC da peça — Beleza, Cabelo, Moda, Perfume ou Eventos."""
    return resolve_piece_categories(brand, caption, config)[0]


def resolve_piece_categories(
    brand: str,
    caption: str,
    config: dict | None = None,
    media_id: str | None = None,
) -> list[str]:
    """Categorias da peça — suporta exceções (ex.: Lua e Neve em Moda + Perfume)."""
    config = config or {}
    if media_id:
        override = _media_categories_map(config).get(str(media_id))
        if override:
            return override

    text = _caption_text(caption)
    brand_map = _brand_category_map(config)

    if brand in brand_map and _normalize_category_id(brand_map[brand]) == "cabelo":
        if brand == "L'Oréal Paris":
            if any(k in text for k in ("parfum", "perfume", "eau de", "fragr")):
                return ["perfume"]
            if any(
                k in text
                for k in (
                    "elseve",
                    "leave-in",
                    "cabelo",
                    "cachos",
                    "collagen lifter",
                    "mascara capilar",
                    "cabeloelseve",
                    "cabeloselseve",
                )
            ):
                return ["cabelo"]
            if any(k in text for k in ("look", "outfit", "moda", "fashion", "styling")):
                return ["moda"]
        else:
            return ["cabelo"]

    if any(k in text for k in ("beautyshow", "beauty show", "@beautyshowoficial")):
        return ["eventos"]

    categories: list[str] = []
    is_event = _is_event_content(caption, config)

    if brand in brand_map:
        if brand == "L'Oréal Paris":
            if any(k in text for k in ("parfum", "perfume", "eau de", "fragr")):
                categories.append("perfume")
            elif any(
                k in text
                for k in (
                    "elseve",
                    "leave-in",
                    "cabelo",
                    "cachos",
                    "collagen lifter",
                    "mascara capilar",
                    "cabeloelseve",
                    "cabeloselseve",
                )
            ):
                categories.append("cabelo")
            elif any(k in text for k in ("look", "outfit", "moda", "fashion", "styling")):
                categories.append("moda")
            else:
                categories.append("beleza")
        elif brand == "Lua e Neve" and any(
            k in text for k in ("blush", "make", "batom", "gloss", "pigment", "coracao", "coração")
        ):
            categories.append("beleza")
        else:
            categories.append(_normalize_category_id(brand_map[brand]))
            if brand == "Lua e Neve" and brand_map[brand] == "perfume" and any(
                k in text for k in ("bolsa", "look", "outfit", "moda", "fashion", "styling")
            ):
                categories.append("moda")
    elif is_event:
        categories.append("eventos")
    elif brand == "L'Oréal Paris":
        if any(k in text for k in ("parfum", "perfume", "eau de", "fragr")):
            categories.append("perfume")
        elif any(
            k in text
            for k in ("elseve", "leave-in", "cabelo", "cachos", "collagen lifter", "mascara capilar")
        ):
            categories.append("cabelo")
        elif any(k in text for k in ("look", "outfit", "moda", "fashion", "styling")):
            categories.append("moda")
        else:
            categories.append("beleza")
    elif re.search(r"\blook\b", text) or any(
        k in text for k in ("outfit", "moda", "look do dia", "lookmulher", "styling", "fashionblackgirls")
    ):
        categories.append("moda")
    if not categories:
        if any(
            k in text
            for k in (
                "parfum",
                "perfume",
                "fragr",
                "eau de",
                "colônia",
                "colonia",
                "body splash",
                "essenciart",
            )
        ):
            categories.append("perfume")
        elif any(k in text for k in ("cabelo", "cachos", "cachead", "hair", "leave-in", "mascara capilar")):
            categories.append("cabelo")
        else:
            categories.append("beleza")

    deduped: list[str] = []
    for cat in categories:
        cat = _normalize_category_id(cat)
        if cat not in deduped:
            deduped.append(cat)
    return deduped or ["beleza"]


DEFAULT_EVENT_KEYWORDS = [
    "beauty fair",
    "beautyfair",
    "beauty show",
    "beautyshow",
    "beautyfairprofissional",
    "beautyshowoficial",
    "beauty city",
    "blogueirasnabeautyfair",
    "bbfassessoria",
    "feira profissional",
    "passei no stand",
    "passei pelo stand",
    "visitei o stand",
    "stand da ",
    "stand do ",
    "stand impecável",
    "stand super",
    "confirmadíssima em mais uma edição",
    "rolou no evento",
    "acompanhar o evento",
    "conferir tudo que rolou",
    "seguimos na @beautyfair",
    "pronta pro beauty fair",
    "vem pra beauty fair",
    "yamá transforma",
    "yama transforma",
    "ikesaki beauty city",
    "conhecendo a beauty city",
    "reinventbartenders",
    "reinve bartenders",
    "playlighteventos",
    "flashbackjunino",
    "festajunin",
    "redercircus",
    "abracadabra",
    "dedesantana",
    "churrasco",
]


def _event_keywords(config: dict | None = None) -> list[str]:
    config = config or {}
    custom = (config.get("portfolio") or {}).get("event_keywords")
    if custom:
        return [k.lower() for k in custom]
    return DEFAULT_EVENT_KEYWORDS


def _is_event_content(caption: str, config: dict | None = None) -> bool:
    text = _caption_text(caption)
    if any(k in text for k in _event_keywords(config)):
        return True
    if "evento" in text and any(
        k in text for k in ("beleza", "beauty", "stand", "feira", "makeup", "marca", "profissional")
    ):
        return True
    return False


def beauty_score(caption: str, beauty_kw: list[str], exclude_kw: list[str]) -> int:
    text = _caption_text(caption)
    for word in exclude_kw:
        if word.lower() in text:
            return -1
    score = 0
    for word in beauty_kw:
        if word.lower() in text:
            score += 2
    if re.search(r"@\w*(makeup|beauty|hair|oficial|line)\w*", text):
        score += 3
    return score


def _post_by_id(posts: list[dict], media_id: str) -> dict | None:
    for post in posts:
        if str(post.get("id")) == str(media_id):
            return post
    return None


def _success_tuple(post: dict) -> tuple[int, int, int, int]:
    ins = post.get("insights") or {}
    return (
        int(post.get("like_count") or 0),
        int(ins.get("views") or 0),
        int(ins.get("reach") or 0),
        int(post.get("comments_count") or 0),
    )


def _reel_cover_url(post: dict) -> str | None:
    """Capa oficial do Reel (thumbnail_url da API) ou imagem do post."""
    media_type = post.get("media_type") or ""
    if media_type in ("VIDEO", "REEL"):
        return post.get("thumbnail_url") or None
    return post.get("media_url") or post.get("thumbnail_url")


def _media_image_url(post: dict) -> str | None:
    return _reel_cover_url(post)


def _is_portfolio_media(post: dict) -> bool:
    if post.get("media_type") in ("VIDEO", "REEL", "IMAGE", "CAROUSEL_ALBUM"):
        return bool(_media_image_url(post))
    return False


def _instagram_timestamp(post: dict) -> str:
    return post.get("timestamp") or ""


def _sort_portfolio_posts(posts: list[dict], config: dict) -> list[dict]:
    sort_by = (config.get("portfolio") or {}).get("sort_by", "instagram")
    if sort_by in ("instagram", "chronological", "feed"):
        return sorted(posts, key=_instagram_timestamp, reverse=True)
    if sort_by == "brand_then_success":
        rules = _partnership_rules(config)
        buckets: dict[str, list[dict]] = {r["name"]: [] for r in rules}
        for post in posts:
            brand = _match_partnership_brand(post.get("caption", ""), config)
            if brand:
                buckets[brand].append(post)
        ordered: list[dict] = []
        for rule in rules:
            name = rule["name"]
            items = sorted(buckets.get(name, []), key=_success_tuple, reverse=True)
            cap = rule.get("max_show")
            if cap:
                items = items[: int(cap)]
            ordered.extend(items)
        return ordered
    return sorted(posts, key=_instagram_timestamp, reverse=True)


def format_piece_views(views: int, fmt_num) -> str:
    """Legenda da galeria — visualizações do Reel (insights API)."""
    v = int(views or 0)
    if v <= 0:
        return ""
    return f"{fmt_num(v)} visualizações"


def partnership_media_ids(posts: list[dict], config: dict) -> set[str]:
    """IDs de mídia do portfólio de parcerias — prioridade para buscar insights."""
    selected = select_partnership_portfolio(posts, config)
    return {str(p.get("id", "")) for p in selected if p.get("id")}


def _portfolio_excluded(post: dict, config: dict) -> bool:
    """Exclui posts marcados explicitamente no config (prints / curadoria manual)."""
    portfolio = config.get("portfolio", {})
    media_id = str(post.get("id", ""))
    permalink = (post.get("permalink") or "").rstrip("/")

    if media_id and media_id in {str(x) for x in portfolio.get("exclude_media_ids", [])}:
        return True

    excluded_perms = {(p or "").rstrip("/") for p in portfolio.get("exclude_permalinks", [])}
    if permalink and permalink in excluded_perms:
        return True

    caption = post.get("caption") or ""
    text = _caption_text(caption)

    min_date = portfolio.get("min_date")
    if min_date:
        ts = (post.get("timestamp") or "")[:10]
        if ts and ts < min_date:
            return True

    if portfolio.get("reels_only"):
        if post.get("media_type") not in ("VIDEO", "REEL"):
            return True

    for kw in portfolio.get("exclude_keywords", []):
        if kw.lower() in text:
            return True

    return False


def _caption_signature(caption: str) -> str:
    line = (caption or "").split("\n")[0][:60]
    return re.sub(r"\s+", " ", line).strip().lower()


def _dedupe_portfolio_posts(posts: list[dict], config: dict) -> list[dict]:
    """Remove duplicatas (mesma marca no mesmo dia ou legenda quase igual)."""
    portfolio = config.get("portfolio", {})
    if not portfolio.get("dedupe", False):
        return posts

    best_by_day: dict[tuple[str, str], dict] = {}
    for post in posts:
        brand = _match_partnership_brand(post.get("caption", ""), config) or ""
        day = (post.get("timestamp") or "")[:10]
        key = (brand, day)
        prev = best_by_day.get(key)
        if not prev or _success_tuple(post) > _success_tuple(prev):
            best_by_day[key] = post

    by_sig: dict[str, dict] = {}
    order: list[str] = []
    for post in posts:
        brand = _match_partnership_brand(post.get("caption", ""), config) or ""
        day = (post.get("timestamp") or "")[:10]
        if best_by_day.get((brand, day)) is not post:
            continue
        sig = f"{brand}|{_caption_signature(post.get('caption', ''))}"
        if sig not in by_sig:
            order.append(sig)
            by_sig[sig] = post
        elif _success_tuple(post) > _success_tuple(by_sig[sig]):
            by_sig[sig] = post

    return [by_sig[s] for s in order if s in by_sig]


def _display_brand(brand: str, category: str) -> str:
    if brand != "Beauty":
        return brand
    category = _normalize_category_id(category)
    if category == "moda":
        return "Moda"
    if category == "perfume":
        return "Perfume"
    if category == "eventos":
        return "Eventos"
    if category == "cabelo":
        return "Cabelo"
    return brand


def _piece_matches_include_categories(categories: list[str], include_cats: set[str]) -> bool:
    normalized = {_normalize_category_id(c) for c in categories}
    return bool(normalized.intersection(include_cats))


def select_partnership_portfolio(posts: list[dict], config: dict, limit: int | None = None) -> list[dict]:
    """Parcerias + reels extras de categorias configuradas (moda, perfume, etc.)."""
    portfolio = config.get("portfolio", {})
    include_cats = {_normalize_category_id(c) for c in portfolio.get("include_categories", [])}
    extra_reels_only = portfolio.get("reels_only_extra_categories", True)
    forced_ids = {str(x) for x in portfolio.get("include_media_ids", [])}

    brand_map = _brand_category_map(config)
    selected: list[dict] = []
    seen_ids: set[str] = set()

    for post in posts:
        if not _is_portfolio_media(post):
            continue
        media_id = str(post.get("id", ""))
        if media_id in seen_ids:
            continue
        if _portfolio_excluded(post, config):
            continue

        caption = post.get("caption") or ""
        brand = _match_partnership_brand(caption, config)
        if brand:
            categories = resolve_piece_categories(brand, caption, config, media_id=media_id)
            brand_default = _normalize_category_id(brand_map.get(brand, ""))
            if brand_default in include_cats or _piece_matches_include_categories(categories, include_cats):
                if post.get("media_type") not in ("VIDEO", "REEL"):
                    continue
                if brand == "Lua e Neve" and not _piece_matches_include_categories(categories, {"perfume", "moda"}):
                    continue
            seen_ids.add(media_id)
            selected.append(post)
            continue

        if media_id in forced_ids:
            if extra_reels_only and post.get("media_type") not in ("VIDEO", "REEL"):
                continue
            seen_ids.add(media_id)
            selected.append(post)
            continue

        extra_include = include_cats - {"cabelo"}
        if not extra_include:
            continue
        if extra_reels_only and post.get("media_type") not in ("VIDEO", "REEL"):
            continue
        categories = resolve_piece_categories("Beauty", caption, config, media_id=media_id)
        if not _piece_matches_include_categories(categories, extra_include):
            continue
        seen_ids.add(media_id)
        selected.append(post)

    if forced_ids:
        posts_by_id = {str(p.get("id", "")): p for p in posts}
        for media_id in forced_ids:
            if media_id in seen_ids:
                continue
            post = posts_by_id.get(media_id)
            if not post or not _is_portfolio_media(post) or _portfolio_excluded(post, config):
                continue
            if extra_reels_only and post.get("media_type") not in ("VIDEO", "REEL"):
                continue
            seen_ids.add(media_id)
            selected.append(post)

    selected = _dedupe_portfolio_posts(selected, config)
    selected = _sort_portfolio_posts(selected, config)

    if limit and len(selected) > limit:
        return selected[:limit]
    return selected


def select_beauty_reels(posts: list[dict], config: dict, limit: int = 4) -> list[dict]:
    """Beauty reels/fotos — parcerias reais ou fallback por score genérico."""
    portfolio_cfg = config.get("portfolio", {})
    if portfolio_cfg.get("mode") == "partnerships":
        partnership = select_partnership_portfolio(posts, config, limit=limit if limit < 999 else None)
        if partnership:
            return partnership

    filt = config.get("content_filter", {})
    beauty_kw = filt.get("beauty_keywords", DEFAULT_BEAUTY)
    exclude_kw = filt.get("exclude_keywords", DEFAULT_EXCLUDE)

    candidates: list[dict] = []
    for post in posts:
        if not _is_portfolio_media(post):
            continue
        score = beauty_score(post.get("caption", ""), beauty_kw, exclude_kw)
        if score < 2:
            continue
        candidates.append(post)

    candidates.sort(key=_success_tuple, reverse=True)
    return candidates[:limit]


def _reel_cover_path(media_id: str) -> Path:
    return ASSETS / f"reel-{media_id}.jpg"


def _reel_video_path(media_id: str) -> Path:
    return ASSETS / f"reel-{media_id}.mp4"


def _manual_cover_path(media_id: str) -> Path | None:
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = MANUAL_COVERS / f"reel-{media_id}{ext}"
        if path.exists() and path.stat().st_size >= MIN_COVER_BYTES:
            return path
    return None


def _manual_video_path(media_id: str) -> Path | None:
    for ext in (".mp4", ".webm", ".mov"):
        path = MANUAL_VIDEOS / f"reel-{media_id}{ext}"
        if path.exists() and path.stat().st_size >= MIN_VIDEO_BYTES:
            return path
    return None


def _apply_manual_videos(posts: list[dict]) -> set[str]:
    """Copia vídeos curados para assets/ (reel-{id}.mp4|.webm|.mov)."""
    applied: set[str] = set()
    if not MANUAL_VIDEOS.is_dir():
        return applied
    ASSETS.mkdir(parents=True, exist_ok=True)
    ids = {str(p.get("id", "")) for p in posts if p.get("id")}
    for path in MANUAL_VIDEOS.iterdir():
        if not path.is_file() or path.suffix.lower() not in {".mp4", ".webm", ".mov"}:
            continue
        media_id = path.stem.removeprefix("reel-")
        if media_id not in ids:
            continue
        dest = ASSETS / f"reel-{media_id}{path.suffix.lower()}"
        dest.write_bytes(path.read_bytes())
        (ASSETS / f"reel-{media_id}.video.src").write_text(f"manual:{path.name}", encoding="utf-8")
        applied.add(media_id)
    return applied


def _apply_manual_covers(posts: list[dict]) -> set[str]:
    """Copia capas curadas para assets/ e devolve IDs que não devem ser recapturados."""
    applied: set[str] = set()
    if not MANUAL_COVERS.is_dir():
        return applied
    ASSETS.mkdir(parents=True, exist_ok=True)
    ids = {str(p.get("id", "")) for p in posts if p.get("id")}
    for path in MANUAL_COVERS.iterdir():
        if not path.is_file() or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        media_id = path.stem.removeprefix("reel-")
        if media_id not in ids:
            continue
        dest = _reel_cover_path(media_id)
        dest.write_bytes(path.read_bytes())
        dest.with_suffix(".src").write_text(f"manual:{path.name}", encoding="utf-8")
        applied.add(media_id)
    return applied


def _valid_video_file(path: Path | None) -> bool:
    return bool(path and path.exists() and path.stat().st_size >= MIN_VIDEO_BYTES)


def _reel_video_asset(media_id: str) -> tuple[Path | None, str]:
    for ext in (".mp4", ".webm", ".mov"):
        path = ASSETS / f"reel-{media_id}{ext}"
        if _valid_video_file(path):
            return path, f"assets/reel-{media_id}{ext}"
    return None, ""


def _valid_cover_file(path: Path | None) -> bool:
    return bool(path and path.exists() and path.stat().st_size >= MIN_COVER_BYTES)


def _post_to_reel(post: dict, index: int, config: dict | None = None) -> dict:
    media_id = str(post.get("id", ""))
    path = _reel_cover_path(media_id)

    if not _valid_cover_file(path):
        cover_url = _reel_cover_url(post)
        if cover_url:
            downloaded = download(cover_url, f"reel-{media_id}")
            if downloaded:
                path = downloaded

    if not _valid_cover_file(path):
        stale = _reel_cover_path(media_id)
        if stale.exists() and stale.stat().st_size > 500:
            path = stale
        else:
            path = None

    asset_path = f"assets/reel-{media_id}.jpg" if path else ""
    cover_url = _reel_cover_url(post) or ""
    _, asset_video = _reel_video_asset(media_id)
    caption = post.get("caption") or ""
    title = caption.split("\n")[0][:72]
    ins = post.get("insights") or {}
    brand = _extract_brand(caption, config)
    categories = resolve_piece_categories(brand, caption, config, media_id=media_id)
    category = categories[0]
    brand = _display_brand(brand, category)
    return {
        "path": path,
        "cover_url": cover_url or "",
        "asset_path": asset_path,
        "asset_video": asset_video,
        "data_uri": to_data_uri(path),
        "media_id": str(post.get("id", "")),
        "permalink": post.get("permalink") or "",
        "reach": ins.get("reach", 0),
        "likes": post.get("like_count", 0),
        "views": resolve_media_views(media_id, ins, config, like_count=int(post.get("like_count") or 0)),
        "caption": caption[:120],
        "title": title,
        "brand": brand,
        "category": category,
        "categories": categories,
        "media_type": post.get("media_type", ""),
    }


def _file_size(path: Path | None) -> int:
    return path.stat().st_size if path and path.exists() else 0


def _config_image_path(relative_or_absolute: str) -> Path | None:
    p = Path(relative_or_absolute)
    if not p.is_absolute():
        p = ROOT / p
    return p if p.exists() else None


def resolve_hero_floats(config: dict | None) -> list[str]:
    """URIs das mini-fotos flutuantes do hero (molduras caramelo)."""
    config = config or {}
    uris: list[str] = []
    for entry in config.get("hero_floats", []):
        path = _config_image_path(entry)
        uri = to_data_uri(path)
        if uri:
            uris.append(uri)
    return uris


def resolve_hero_video(config: dict | None) -> tuple[str, str]:
    """Copia vídeo do hero para assets/ — retorna (video_path, poster_path) relativos."""
    config = config or {}
    ASSETS.mkdir(parents=True, exist_ok=True)

    candidates: list[Path] = []
    custom = config.get("hero_video")
    if custom:
        p = _config_image_path(custom)
        if p:
            candidates.append(p)
    mediakit = ROOT / "data" / "mediakit"
    for name in (
        "Apresentação Taty.mp4",
        "Apresentacao Taty.mp4",
        "hero-video.mp4",
    ):
        candidates.append(mediakit / name)
    candidates.append(mediakit / "manual-videos" / "hero-video.mp4")

    src = next((p for p in candidates if p.exists() and p.stat().st_size >= MIN_VIDEO_BYTES), None)
    if not src:
        return "", ""

    dest = ASSETS / "hero-video.mp4"
    if src.resolve() != dest.resolve():
        dest.write_bytes(src.read_bytes())
    dest.with_suffix(".video.src").write_text(f"hero:{src.name}", encoding="utf-8")

    poster_dest = ASSETS / "hero-poster.jpg"
    poster_src = _local_hd_path(config)
    if poster_src and poster_src.exists():
        poster_dest.write_bytes(poster_src.read_bytes())

    return "assets/hero-video.mp4", "assets/hero-poster.jpg" if poster_dest.exists() else ""


def _local_hd_path(config: dict | None) -> Path | None:
    config = config or {}
    custom = config.get("profile_photo")
    if custom:
        p = _config_image_path(custom)
        if p:
            return p
    for p in LOCAL_HD_CANDIDATES:
        if p.exists():
            return p
    return None


def _best_hero_post(posts: list[dict], config: dict) -> dict | None:
    """Melhor foto/reel beauty por desempenho — não por recência."""
    selected = select_beauty_reels(posts, config, limit=8)
    if not selected:
        return None
    videos = [p for p in selected if p.get("media_type") in ("VIDEO", "REEL")]
    return videos[0] if videos else selected[0]


def _best_reel_thumb(posts: list[dict], config: dict) -> str | None:
    post = _best_hero_post(posts, config)
    return _media_image_url(post) if post else None


def resolve_hero_image(snapshot: dict, config: dict | None = None) -> tuple[Path | None, str]:
    """Foto HD local, senão thumb do conteúdo beauty com maior sucesso."""
    config = config or {}

    local = _local_hd_path(config)
    if local:
        return local, "local"

    posts = snapshot.get("media", [])
    profile_url = snapshot.get("profile", {}).get("profile_picture_url", "")
    profile_path = download(profile_url, "profile") if profile_url else None

    if _file_size(profile_path) >= MIN_PROFILE_BYTES:
        return profile_path, "api"

    hero_post = _best_hero_post(posts, config)
    hero_url = _media_image_url(hero_post) if hero_post else None
    if hero_url:
        reel_path = download(hero_url, "hero-top")
        if _file_size(reel_path) > _file_size(profile_path):
            return reel_path, "top-success"

    return profile_path, "api"


def _case_thumbnails(reels: list[dict], cases: list[dict]) -> dict[str, str]:
    by_id = {r["media_id"]: r["data_uri"] for r in reels if r.get("media_id")}
    mapped: dict[str, str] = {}
    for case in cases:
        media_id = str(case.get("media_id", ""))
        if media_id and media_id in by_id:
            mapped[media_id] = by_id[media_id]
    return mapped


def build_success_cases(reels: list[dict], fmt_num, limit: int = 6) -> list[dict]:
    cases: list[dict] = []
    for reel in reels[:limit]:
        views = reel.get("views", 0)
        metrics = format_piece_views(views, fmt_num) or "Reel patrocinado"
        cases.append(
            {
                "title": reel.get("title") or reel.get("brand", "Beauty"),
                "brand": reel.get("brand", "Beauty"),
                "metrics": metrics,
                "note": "Reel" if reel.get("media_type") in ("VIDEO", "REEL") else "Foto",
                "media_id": reel.get("media_id", ""),
            }
        )
    return cases


def build_highlight_cases(
    posts: list[dict], config: dict, fmt_num, media_ids: list[str] | None = None
) -> list[dict]:
    portfolio_cfg = config.get("portfolio", {})
    ids = media_ids or portfolio_cfg.get("highlight_case_ids") or []
    if not ids:
        return []
    by_id = {str(p.get("id", "")): p for p in posts}
    rows: list[dict] = []
    for media_id in ids:
        post = by_id.get(str(media_id))
        if not post:
            continue
        caption = post.get("caption") or ""
        ins = post.get("insights") or {}
        brand = _extract_brand(caption, config)
        categories = resolve_piece_categories(brand, caption, config, media_id=str(media_id))
        brand = _display_brand(brand, categories[0])
        rows.append(
            {
                "media_id": str(media_id),
                "title": caption.split("\n")[0][:72],
                "brand": brand,
                "views": resolve_media_views(
                    str(media_id), ins, config, like_count=int(post.get("like_count") or 0)
                ),
                "media_type": post.get("media_type", ""),
            }
        )
    return build_success_cases(rows, fmt_num, limit=len(rows))


def resolve_pdf_cases(posts: list[dict], config: dict, fmt_num) -> list[dict]:
    portfolio_cfg = config.get("portfolio", {})
    highlight_ids = portfolio_cfg.get("highlight_case_ids")
    if highlight_ids:
        cases = build_highlight_cases(posts, config, fmt_num, highlight_ids)
        if cases:
            return cases
    if portfolio_cfg.get("auto_cases", True):
        limit = int(portfolio_cfg.get("pdf_cases_limit", 3))
        return build_top_cases(posts, config, fmt_num, limit=limit)
    return config.get("cases", [])


def build_top_cases(posts: list[dict], config: dict, fmt_num, limit: int = 3) -> list[dict]:
    """Top parcerias do portfólio inteiro por views (sem baixar capas)."""
    rows: list[dict] = []
    for post in select_beauty_reels(posts, config, limit=999):
        media_id = str(post.get("id", ""))
        caption = post.get("caption") or ""
        ins = post.get("insights") or {}
        brand = _extract_brand(caption, config)
        categories = resolve_piece_categories(brand, caption, config, media_id=media_id)
        brand = _display_brand(brand, categories[0])
        rows.append(
            {
                "media_id": media_id,
                "title": caption.split("\n")[0][:72],
                "brand": brand,
                "views": resolve_media_views(
                    media_id, ins, config, like_count=int(post.get("like_count") or 0)
                ),
                "media_type": post.get("media_type", ""),
            }
        )
    rows.sort(key=lambda r: int(r.get("views") or 0), reverse=True)
    return build_success_cases(rows[:limit], fmt_num, limit=limit)


def prepare_assets(snapshot: dict, config: dict | None = None, limit_reels: int = 4, fmt_num=None) -> dict:
    config = config or {}
    hero_path, hero_source = resolve_hero_image(snapshot, config)
    profile_url = snapshot.get("profile", {}).get("profile_picture_url", "")
    profile_path = ASSETS / "profile.jpg"
    if not profile_path.exists() and profile_url:
        download(profile_url, "profile")

    posts = snapshot.get("media", [])
    selected = select_beauty_reels(posts, config, limit_reels)
    refreshed = list(selected)

    valid_ids = {str(p.get("id", "")) for p in refreshed if p.get("id")}
    _cleanup_stale_reel_assets(valid_ids)

    manual_cover_ids = _apply_manual_covers(refreshed)
    _apply_manual_videos(refreshed)

    try:
        from capture_reel_covers import capture_portfolio_covers

        if os.getenv("SKIP_COVER_CAPTURE") != "1":
            capture_portfolio_covers(refreshed, ASSETS, skip_media_ids=manual_cover_ids)
    except Exception as exc:
        print(f"  Aviso: captura de capas embed falhou ({exc})")

    reels = [_post_to_reel(post, i, config) for i, post in enumerate(refreshed)]
    hero_uri = to_data_uri(hero_path)
    hero_video, hero_poster = resolve_hero_video(config)
    if config.get("hero_video") and not hero_video:
        wanted = config.get("hero_video")
        print(f"  Aviso: hero video nao encontrado ({wanted}) — coloque em data/mediakit/")

    portfolio_cfg = config.get("portfolio", {})
    if portfolio_cfg.get("auto_cases", True) and fmt_num:
        cases = build_top_cases(posts, config, fmt_num, limit=6)
    else:
        cases = config.get("cases", [])

    return {
        "profile_data_uri": hero_uri,
        "hero_data_uri": hero_uri,
        "hero_source": hero_source,
        "hero_float_uris": resolve_hero_floats(config),
        "hero_video": hero_video,
        "hero_poster": hero_poster,
        "reels": reels,
        "cases": cases,
        "case_thumbnails": _case_thumbnails(reels, cases),
        "feedbacks": resolve_feedbacks(config),
    }


def resolve_feedbacks(config: dict) -> list[dict]:
    items = config.get("feedbacks") or []
    if not items:
        return []

    FEEDBACKS_ASSETS.mkdir(parents=True, exist_ok=True)
    resolved: list[dict] = []

    for item in items:
        img = (item.get("image") or "").strip()
        if not img:
            continue

        src = Path(img)
        if not src.is_absolute():
            src = FEEDBACKS_SRC / Path(img).name

        if not src.exists():
            print(f"  Aviso: imagem de feedback nao encontrada ({img})")
            continue

        dest = FEEDBACKS_ASSETS / src.name
        if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
            shutil.copy2(src, dest)

        resolved.append({**item, "asset_path": f"assets/feedbacks/{dest.name}"})

    return resolved
