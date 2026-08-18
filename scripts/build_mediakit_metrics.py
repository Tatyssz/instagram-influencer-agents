#!/usr/bin/env python3
"""Gera estimativa de metricas para Media Kit a partir do profile_snapshot.json."""

from __future__ import annotations

import json
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "data" / "sync" / "profile_snapshot.json"
APP_INSIGHTS = ROOT / "data" / "sync" / "insights_app.json"
CONFIG = ROOT / "data" / "mediakit" / "config.json"
OUT_DIR = ROOT / "output" / "mediakit"


def load_config() -> dict:
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    return {}


def load_app_insights() -> dict | None:
    if APP_INSIGHTS.exists():
        return json.loads(APP_INSIGHTS.read_text(encoding="utf-8"))
    return None


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("+0000", "+00:00"))


def pct(part: int, whole: int) -> float:
    return round(part / whole * 100, 1) if whole else 0.0


def top_demographics(demo: dict, key: str, limit: int = 5) -> list[dict]:
    rows = demo.get(key, [])
    if not isinstance(rows, list):
        return []
    total = sum(r["count"] for r in rows)
    return [
        {
            "label": r["dimension"],
            "count": r["count"],
            "percent": pct(r["count"], total),
        }
        for r in rows[:limit]
    ]


def summarize_reels(posts: list[dict], followers: int) -> dict:
    """Metricas so de Reels/VIDEO com insights da API (nao e 'ultimos 30 dias')."""
    reels = [
        p for p in posts
        if p.get("media_type") in ("VIDEO", "REEL")
        and p.get("insights")
        and (p["insights"].get("reach") or p["insights"].get("views"))
    ]
    if not reels:
        return {}

    reaches = [p["insights"].get("reach", 0) for p in reels]
    views = [p["insights"].get("views", 0) for p in reels]
    shares = [p["insights"].get("shares", 0) for p in reels]
    saves = [p["insights"].get("saved", 0) for p in reels]
    likes = [p.get("like_count", 0) for p in reels]
    comments = [p.get("comments_count", 0) for p in reels]
    interactions = [p["insights"].get("total_interactions", 0) for p in reels]

    avg_reach = round(statistics.mean(reaches)) if reaches else 0
    median_reach = round(statistics.median(reaches)) if reaches else 0
    avg_views = round(statistics.mean(views)) if views else 0
    median_views = round(statistics.median(views)) if views else 0

    eng_by_followers = (
        round(statistics.mean((l + c) / followers * 100 for l, c in zip(likes, comments)), 2)
        if followers
        else 0
    )
    eng_by_reach = (
        round(statistics.mean(i / r * 100 for i, r in zip(interactions, reaches) if r > 0), 2)
        if reaches
        else 0
    )

    ranked_reach = sorted(reels, key=lambda p: p.get("insights", {}).get("reach", 0), reverse=True)
    ranked_views = sorted(reels, key=lambda p: p.get("insights", {}).get("views", 0), reverse=True)

    def _top_entry(p: dict) -> dict:
        return {
            "date": p.get("timestamp", "")[:10],
            "reach": p.get("insights", {}).get("reach", 0),
            "views": p.get("insights", {}).get("views", 0),
            "shares": p.get("insights", {}).get("shares", 0),
            "likes": p.get("like_count", 0),
            "permalink": p.get("permalink", ""),
            "caption": (p.get("caption") or "")[:80],
        }

    return {
        "count": len(reels),
        "reach_sum": sum(reaches),
        "reach_avg": avg_reach,
        "reach_median": median_reach,
        "reach_min": min(reaches) if reaches else 0,
        "reach_max": max(reaches) if reaches else 0,
        "views_sum": sum(views),
        "views_avg": avg_views,
        "views_median": median_views,
        "views_max": max(views) if views else 0,
        "shares_sum": sum(shares),
        "shares_avg": round(statistics.mean(shares)) if shares else 0,
        "saves_sum": sum(saves),
        "likes_sum": sum(likes),
        "comments_sum": sum(comments),
        "engagement_rate_followers_pct": eng_by_followers,
        "engagement_rate_reach_pct": eng_by_reach,
        "top_by_reach": [_top_entry(p) for p in ranked_reach[:5]],
        "top_by_views": [_top_entry(p) for p in ranked_views[:5]],
    }


def summarize_posts(posts: list[dict], followers: int) -> dict:
    if not posts:
        return {}

    reaches = [p["insights"].get("reach", 0) for p in posts if p.get("insights")]
    views = [p["insights"].get("views", 0) for p in posts if p.get("insights")]
    shares = [p["insights"].get("shares", 0) for p in posts if p.get("insights")]
    saves = [p["insights"].get("saved", 0) for p in posts if p.get("insights")]
    likes = [p.get("like_count", 0) for p in posts]
    comments = [p.get("comments_count", 0) for p in posts]
    interactions = [p["insights"].get("total_interactions", 0) for p in posts if p.get("insights")]

    avg_reach = round(statistics.mean(reaches)) if reaches else 0
    median_reach = round(statistics.median(reaches)) if reaches else 0

    eng_by_followers = (
        round(statistics.mean((l + c) / followers * 100 for l, c in zip(likes, comments)), 2)
        if followers
        else 0
    )
    eng_by_reach = (
        round(statistics.mean(i / r * 100 for i, r in zip(interactions, reaches) if r > 0), 2)
        if reaches
        else 0
    )

    ranked = sorted(
        posts,
        key=lambda p: p.get("insights", {}).get("reach", 0),
        reverse=True,
    )

    return {
        "count": len(posts),
        "reach_sum": sum(reaches),
        "reach_avg": avg_reach,
        "reach_median": median_reach,
        "reach_min": min(reaches) if reaches else 0,
        "reach_max": max(reaches) if reaches else 0,
        "views_sum": sum(views),
        "views_avg": round(statistics.mean(views)) if views else 0,
        "shares_sum": sum(shares),
        "shares_avg": round(statistics.mean(shares)) if shares else 0,
        "saves_sum": sum(saves),
        "likes_sum": sum(likes),
        "comments_sum": sum(comments),
        "engagement_rate_followers_pct": eng_by_followers,
        "engagement_rate_reach_pct": eng_by_reach,
        "top_by_reach": [
            {
                "date": p.get("timestamp", "")[:10],
                "reach": p.get("insights", {}).get("reach", 0),
                "views": p.get("insights", {}).get("views", 0),
                "shares": p.get("insights", {}).get("shares", 0),
                "likes": p.get("like_count", 0),
                "permalink": p.get("permalink", ""),
                "caption": (p.get("caption") or "")[:80],
            }
            for p in ranked[:5]
        ],
    }


def _interactions_from_period(period: dict) -> int | None:
    painel = period.get("painel_profissional") or {}
    if painel.get("interacoes") is not None:
        return int(painel["interacoes"])
    reel = period.get("interacoes_reels") or {}
    parts = [v for v in reel.values() if isinstance(v, (int, float))]
    return int(sum(parts)) if parts else None


def _reel_interactions_from_period(period: dict) -> int | None:
    reel = period.get("interacoes_reels") or {}
    parts = [v for v in reel.values() if isinstance(v, (int, float))]
    return int(sum(parts)) if parts else None


def _reel_views_from_period(period: dict) -> int | None:
    painel = period.get("painel_profissional") or {}
    if painel.get("visualizacoes_reels") is not None:
        return int(painel["visualizacoes_reels"])
    total = period.get("visualizacoes_total") or painel.get("visualizacoes")
    reels_pct = (period.get("por_tipo") or {}).get("reels_pct")
    if total and reels_pct is not None:
        return round(int(total) * float(reels_pct) / 100)
    return None


def merge_app_insights(data: dict, app: dict | None) -> dict:
    if not app:
        return data

    p30 = app.get("period_30d", {})
    p90 = app.get("period_90d", {})
    painel = p30.get("painel_profissional", {})
    aud = p30.get("audiencia", {})
    ativ = p30.get("atividade_perfil", {})

    views_30d = painel.get("visualizacoes")
    interactions_30d = painel.get("interacoes")
    interaction_rate_views = (
        round(interactions_30d / views_30d * 100, 1)
        if views_30d and interactions_30d
        else None
    )

    views_90d = p90.get("visualizacoes_total")
    interactions_90d = _interactions_from_period(p90)
    interaction_rate_90d = (
        round(interactions_90d / views_90d * 100, 1)
        if views_90d and interactions_90d
        else None
    )

    interactions_reels_90d = _reel_interactions_from_period(p90)
    views_reels_90d = _reel_views_from_period(p90)
    interaction_rate_reels_90d = (
        round(interactions_reels_90d / views_reels_90d * 100, 1)
        if views_reels_90d and interactions_reels_90d
        else None
    )

    data["app_insights_official"] = {
        "captured_at": app.get("captured_at"),
        "period_30d": p30,
        "period_90d": p90,
    }
    data["app_insights_placeholder"] = {
        "views_30d_official": views_30d,
        "interactions_30d_official": interactions_30d,
        "profile_visits_30d": ativ.get("visitas_perfil"),
        "content_shared_30d": painel.get("conteudo_compartilhado"),
        "interaction_rate_on_views_pct": interaction_rate_views,
        "visualizadores_90d": p90.get("visualizadores_unicos"),
        "views_90d": views_90d,
        "interactions_90d_official": interactions_90d,
        "interaction_rate_90d_on_views_pct": interaction_rate_90d,
        "interactions_reels_90d": interactions_reels_90d,
        "views_reels_90d": views_reels_90d,
        "interaction_rate_reels_90d_on_views_pct": interaction_rate_reels_90d,
    }

    h = data["media_kit_highlights"]
    h["views_30d_official"] = views_30d
    h["interactions_30d_official"] = interactions_30d
    h["views_90d_official"] = views_90d
    h["interactions_90d_official"] = interactions_90d
    h["interaction_rate_90d_on_views_pct"] = interaction_rate_90d
    h["interactions_reels_90d"] = interactions_reels_90d
    h["views_reels_90d"] = views_reels_90d
    h["interaction_rate_reels_90d_on_views_pct"] = interaction_rate_reels_90d
    h["profile_visits_30d"] = ativ.get("visitas_perfil")
    h["brazil_audience_pct"] = next(
        (c["percent"] for c in aud.get("paises", []) if c.get("pais") == "Brasil"),
        h.get("brazil_audience_pct"),
    )
    h["female_audience_pct"] = aud.get("genero", {}).get("mulheres_pct", h.get("female_audience_pct"))
    h["core_age_25_44_pct"] = round(
        sum(a["percent"] for a in aud.get("idade", []) if a.get("faixa") in ("25-34", "35-44")),
        1,
    )
    h["baixada_santista_pct"] = round(
        sum(c["percent"] for c in aud.get("cidades", []) if c.get("cidade") in (
            "São Vicente", "Santos", "Praia Grande"
        )),
        1,
    )
    h["views_non_followers_pct_90d"] = p90.get("views_nao_seguidores_pct")

    data["demographics"]["app_audience_30d"] = aud
    return data


def summarize_beauty_reels(posts: list[dict], config: dict) -> dict:
    """Metricas dos Reels beauty com insights — para exibir pico real de parcerias."""
    from mediakit_assets import select_beauty_reels

    beauty = select_beauty_reels(posts, config, limit=80)
    measured = [p for p in beauty if p.get("insights", {}).get("reach")]
    if not measured:
        return {}

    reaches = [p["insights"]["reach"] for p in measured]
    views = [p["insights"].get("views", 0) for p in measured]
    best = max(measured, key=lambda p: p["insights"]["reach"])
    return {
        "count": len(measured),
        "reach_median": round(statistics.median(reaches)),
        "views_median": round(statistics.median(views)),
        "best_reach": max(reaches),
        "best_views": max(views),
        "best_reel": {
            "date": best.get("timestamp", "")[:10],
            "reach": best["insights"]["reach"],
            "views": best["insights"].get("views", 0),
            "likes": best.get("like_count", 0),
            "permalink": best.get("permalink", ""),
            "caption": (best.get("caption") or "")[:80],
        },
    }


def build_estimate(snapshot: dict, config: dict | None = None) -> dict:
    synced_at = parse_ts(snapshot["synced_at"])
    profile = snapshot["profile"]
    followers = profile.get("followers_count", 0)
    all_posts = snapshot.get("media", [])

    windows = {
        "last_30_days": synced_at - timedelta(days=30),
        "last_60_days": synced_at - timedelta(days=60),
        "last_90_days": synced_at - timedelta(days=90),
    }

    by_window: dict[str, dict] = {}
    for name, since in windows.items():
        filtered = [p for p in all_posts if parse_ts(p["timestamp"]) >= since]
        by_window[name] = summarize_posts(filtered, followers)

    sample_reels = summarize_reels(all_posts, followers)
    beauty_reels = summarize_beauty_reels(all_posts, config or {})
    sample_30 = summarize_posts(all_posts, followers)

    demo = snapshot.get("account_insights", {}).get("demographics", {})
    days_28 = snapshot.get("account_insights", {}).get("by_period", {}).get("days_28", {})

    # Estimativa mensual (heuristica): media alcance x frequencia de posts
    if all_posts:
        oldest = min(parse_ts(p["timestamp"]) for p in all_posts)
        span_days = max((synced_at - oldest).days, 1)
        posts_per_month = len(all_posts) / span_days * 30
    else:
        posts_per_month = 0

    estimated_monthly_reach_heuristic = round(sample_reels.get("reach_median", 0) * posts_per_month)
    estimated_monthly_views_heuristic = round(sample_reels.get("views_median", 0) * posts_per_month)

    return {
        "generated_at": snapshot["synced_at"],
        "profile": {
            "username": profile.get("username"),
            "name": profile.get("name"),
            "followers": followers,
            "posts_total": profile.get("media_count"),
            "bio": profile.get("biography"),
        },
        "official_api_partial": {
            "reach_28d_unique": days_28.get("reach"),
            "views_28d": days_28.get("views"),
            "accounts_engaged_28d": days_28.get("accounts_engaged"),
            "note": "API acumula desde conexao OAuth (~11/08/2026). Substituir por print do app quando disponivel.",
        },
        "app_insights_placeholder": {
            "reach_30d_official": None,
            "views_30d_official": None,
            "profile_visits_30d": None,
            "engagement_rate_30d_official": None,
            "instructions": "Preencher com print: Instagram > Painel Profissional > Insights > Ultimos 30 dias",
        },
        "demographics": {
            "age_top": top_demographics(demo, "age"),
            "gender": top_demographics(demo, "gender"),
            "cities_brazil_focus": [
                c for c in top_demographics(demo, "city", 15)
                if "Brazil" in c["label"] or "São Paulo" in c["label"] or "Santos" in c["label"]
                   or "Rio de Janeiro" in c["label"] or "Bahia" in c["label"] or "Minas" in c["label"]
            ][:5],
            "countries_top": top_demographics(demo, "country"),
        },
        "reels_beauty_with_insights": beauty_reels,
        "reels_sample_last_30_posts": sample_30,
        "reels_by_period": by_window,
        "monthly_estimate": {
            "method": "media_alcance_por_reel x posts_publicados_por_mes (amostra ultimos 30 Reels)",
            "posts_per_month_estimated": round(posts_per_month, 1),
            "reach_unique_estimated_low": by_window["last_30_days"].get("reach_sum"),
            "reach_unique_estimated_heuristic": estimated_monthly_reach_heuristic,
            "views_estimated_heuristic": estimated_monthly_views_heuristic,
            "disclaimer": (
                "Soma de alcance por post SUPerestima contas unicas (mesma pessoa em varios Reels). "
                "Heuristica (media x frequencia) e aproximacao. Numero oficial vem do print Insights 30d."
            ),
        },
        "media_kit_highlights": {
            "followers": followers,
            "avg_reach_per_reel": beauty_reels.get("reach_median") or sample_reels.get("reach_median"),
            "median_reach_per_reel": beauty_reels.get("reach_median") or sample_reels.get("reach_median"),
            "mean_reach_per_reel": sample_reels.get("reach_avg"),
            "best_reach_per_reel": beauty_reels.get("best_reach") or sample_reels.get("reach_max"),
            "avg_views_per_reel": beauty_reels.get("views_median") or sample_reels.get("views_median"),
            "median_views_per_reel": beauty_reels.get("views_median") or sample_reels.get("views_median"),
            "mean_views_per_reel": sample_reels.get("views_avg"),
            "best_views_per_reel": beauty_reels.get("best_views") or sample_reels.get("views_max"),
            "reels_measured_count": beauty_reels.get("count") or sample_reels.get("count"),
            "avg_shares_per_reel": sample_reels.get("shares_avg"),
            "engagement_by_followers_pct": sample_reels.get("engagement_rate_followers_pct"),
            "engagement_by_reach_pct": sample_reels.get("engagement_rate_reach_pct"),
            "top_reach_reel": beauty_reels.get("best_reel") or sample_reels.get("top_by_reach", [{}])[0],
            "top_views_reel": beauty_reels.get("best_reel") or sample_reels.get("top_by_views", [{}])[0],
            "brazil_audience_pct": next(
                (c["percent"] for c in top_demographics(demo, "country") if c["label"] == "BR"),
                None,
            ),
            "female_audience_pct": next(
                (g["percent"] for g in top_demographics(demo, "gender") if g["label"] == "F"),
                None,
            ),
            "core_age_25_44_pct": round(
                sum(
                    a["percent"]
                    for a in top_demographics(demo, "age", 10)
                    if a["label"] in ("25-34", "35-44")
                ),
                1,
            ),
        },
    }


def _fmt(n: int | float | None) -> str:
    if n is None:
        return "—"
    if isinstance(n, float):
        return f"{n:.1f}".replace(".", ",")
    return f"{n:,}".replace(",", ".")


def render_markdown(data: dict) -> str:
    h = data["media_kit_highlights"]
    m = data["monthly_estimate"]
    s = data["reels_sample_last_30_posts"]
    demo = data["demographics"]
    api = data["official_api_partial"]
    ph = data.get("app_insights_placeholder", {})
    app = data.get("app_insights_official", {})
    p30 = app.get("period_30d", {})
    p90 = app.get("period_90d", {})
    aud = demo.get("app_audience_30d", p30.get("audiencia", {}))

    lines = [
        "# Metricas — Media Kit @tatyzacharias",
        "",
        f"Gerado em {data['generated_at'][:10]} · Dados oficiais do app (prints 12/08/2026)",
        "",
        "---",
        "",
        "## Numeros oficiais (Instagram — 30 dias)",
        "",
        f"**Periodo:** {p30.get('label', '13 jul – 11 ago 2026')}",
        "",
        "| Metrica | Valor |",
        "|---------|-------|",
        f"| Seguidores | **{_fmt(h['followers'])}** |",
        f"| Visualizacoes (Painel Profissional) | **{_fmt(ph.get('views_30d_official'))}** |",
        f"| Interacoes | **{_fmt(ph.get('interactions_30d_official'))}** |",
        f"| Conteudo publicado | **{ph.get('content_shared_30d', '-')}** posts/stories/reels |",
        f"| Visitas ao perfil | **{_fmt(ph.get('profile_visits_30d'))}** |",
        f"| Taxa interacao/views | **{_fmt(ph.get('interaction_rate_on_views_pct'))}%** |",
        "",
        "### Audiencia que viu seu conteudo (30 dias)",
        "",
        f"| Metrica | Valor |",
        f"|---------|-------|",
        f"| Brasil | **{_fmt(h.get('brazil_audience_pct'))}%** |",
        f"| Mulheres | **{_fmt(h.get('female_audience_pct'))}%** |",
        f"| Faixa 25-44 anos | **{_fmt(h.get('core_age_25_44_pct'))}%** |",
        f"| Baixada Santista (SV+Santos+PG) | **{_fmt(h.get('baixada_santista_pct'))}%** |",
        "",
        "**Cidades top:**",
    ]
    for city in aud.get("cidades", []):
        lines.append(f"- {city['cidade']}: {city['percent']}%")

    lines.extend([
        "",
        "---",
        "",
        "## Numeros por Reel (API — ultimos 30 Reels)",
        "",
        "| Metrica | Valor |",
        "|---------|-------|",
        f"| Alcance medio por Reel | **{_fmt(h['avg_reach_per_reel'])}** contas |",
        f"| Alcance mediano por Reel | **{_fmt(h['median_reach_per_reel'])}** contas |",
        f"| Views medias por Reel | **{_fmt(h['avg_views_per_reel'])}** |",
        f"| Shares medios por Reel | **{_fmt(h['avg_shares_per_reel'])}** |",
        "",
        "---",
        "",
        "## Referencia 90 dias (14 mai – 11 ago)",
        "",
        f"| Metrica | Valor |",
        f"|---------|-------|",
        f"| Visualizacoes totais | **{_fmt(p90.get('visualizacoes_total'))}** |",
        f"| Visualizadores unicos | **{_fmt(p90.get('visualizadores_unicos'))}** (+{p90.get('visualizadores_variacao_pct', 0)}%) |",
        f"| Views de nao-seguidores | **{_fmt(p90.get('views_nao_seguidores_pct'))}%** |",
        f"| Stories / Reels | **{p90.get('por_tipo', {}).get('stories_pct')}%** / **{p90.get('por_tipo', {}).get('reels_pct')}%** |",
        f"| Curtidas em Reels (90d) | **{_fmt(p90.get('interacoes_reels', {}).get('curtidas'))}** |",
        f"| Visitas ao perfil (90d) | **{_fmt(p90.get('atividade_perfil', {}).get('visitas_perfil'))}** |",
        "",
        "---",
        "",
        "## API Meta (parcial — desde OAuth)",
        "",
        f"- Alcance 28d (API): **{api['reach_28d_unique']:,}**".replace(",", "."),
        f"- Views 28d (API): **{api['views_28d']:,}**".replace(",", "."),
        f"- *{api['note']}*",
        "",
        "---",
        "",
        "## Top 5 Reels por alcance",
        "",
    ])

    for i, post in enumerate(s.get("top_by_reach", []), 1):
        lines.append(
            f"{i}. **{post['reach']:,}** alcance · {post['views']:,} views · "
            f"{post['shares']:,} shares · {post['likes']} likes — {post['date']}".replace(",", ".")
        )
        lines.append(f"   - {post['caption']}...")
        lines.append(f"   - {post['permalink']}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Demografia (seguidores)",
        "",
        "**Idade:**",
    ])
    for row in demo["age_top"]:
        lines.append(f"- {row['label']}: {row['percent']}%")

    lines.extend(["", "**Genero:**"])
    gender_labels = {"F": "Feminino", "M": "Masculino", "U": "Nao informado"}
    for row in demo["gender"]:
        lines.append(f"- {gender_labels.get(row['label'], row['label'])}: {row['percent']}%")

    lines.extend(["", "**Brasil — cidades relevantes:**"])
    for row in demo["cities_brazil_focus"][:5]:
        lines.append(f"- {row['label']}: {row['percent']}%")

    views_30 = ph.get("views_30d_official") or h.get("avg_views_per_reel")
    lines.extend([
        "",
        "---",
        "",
        "## Frase pronta para proposta comercial",
        "",
        f"> *{data['profile']['name']} · {_fmt(h['followers'])} seguidores · "
        f"{_fmt(views_30)} visualizacoes/30d · "
        f"{_fmt(h.get('brazil_audience_pct'))}% BR · "
        f"{_fmt(h.get('female_audience_pct'))}% mulheres · "
        f"L'Oréal Star · UGC beauty & hair cacheado · Baixada Santista*",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    config = load_config()
    data = merge_app_insights(build_estimate(snapshot, config), load_app_insights())

    followers = snapshot.get("profile", {}).get("followers_count")
    if followers:
        data["profile"]["followers"] = followers
        data["media_kit_highlights"]["followers"] = followers

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "estimativa-metricas.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "estimativa-metricas.md").write_text(render_markdown(data), encoding="utf-8")

    h = data["media_kit_highlights"]
    print(f"Salvo em {OUT_DIR}")
    print(f"  Seguidores: {h['followers']}")
    print(f"  Alcance medio/Reel: {h['avg_reach_per_reel']}")
    print(f"  Estimativa mensal (heuristica): {data['monthly_estimate']['reach_unique_estimated_heuristic']}")


if __name__ == "__main__":
    main()
