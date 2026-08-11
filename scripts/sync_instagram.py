#!/usr/bin/env python3
"""
Sincroniza perfil e posts do Instagram via Instagram API with Instagram Login.

Uso:
  python scripts/sync_instagram.py auth   # login OAuth (uma vez)
  python scripts/sync_instagram.py sync   # baixa dados para data/sync/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import load_dotenv

API_VERSION = "v21.0"
GRAPH_IG = f"https://graph.instagram.com/{API_VERSION}"
DEFAULT_REDIRECT = "https://localhost:8765/callback"
DEFAULT_PORT = 8765

# Permissões atuais (jan/2025+) — instagram_basic foi descontinuado
SCOPES = [
    "instagram_business_basic",
    "instagram_business_manage_insights",
]

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
SYNC_DIR = ROOT / "data" / "sync"


def load_config() -> dict[str, str]:
    load_dotenv(ENV_PATH)
    app_id = os.getenv("INSTAGRAM_APP_ID", "").strip() or os.getenv("META_APP_ID", "").strip()
    app_secret = os.getenv("INSTAGRAM_APP_SECRET", "").strip() or os.getenv("META_APP_SECRET", "").strip()
    return {
        "app_id": app_id,
        "app_secret": app_secret,
        "access_token": os.getenv("META_ACCESS_TOKEN", "").strip(),
        "ig_user_id": os.getenv("IG_USER_ID", "").strip(),
        "redirect_uri": os.getenv("OAUTH_REDIRECT_URI", DEFAULT_REDIRECT).strip(),
    }


def save_env(updates: dict[str, str]) -> None:
    lines: list[str] = []
    existing_keys: set[str] = set()

    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key = line.split("=", 1)[0].strip()
                existing_keys.add(key)
                if key in updates:
                    lines.append(f"{key}={updates[key]}")
                    del updates[key]
                else:
                    lines.append(line)
            else:
                lines.append(line)

    for key, value in updates.items():
        if key not in existing_keys:
            lines.append(f"{key}={value}")

    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def ig_get(path: str, token: str, params: dict | None = None) -> dict:
    params = dict(params or {})
    params["access_token"] = token
    url = path if path.startswith("http") else f"{GRAPH_IG}/{path.lstrip('/')}"
    response = requests.get(url, params=params, timeout=60)
    data = response.json()
    if "error" in data:
        err = data["error"]
        raise RuntimeError(f"Instagram API: {err.get('message', err)} (code {err.get('code')})")
    return data


def exchange_code_for_token(app_id: str, app_secret: str, redirect_uri: str, code: str) -> tuple[str, str]:
    response = requests.post(
        "https://api.instagram.com/oauth/access_token",
        data={
            "client_id": app_id,
            "client_secret": app_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        },
        timeout=60,
    )
    data = response.json()
    if "error_message" in data:
        raise RuntimeError(f"Token exchange: {data['error_message']}")
    if "error" in data:
        raise RuntimeError(f"Token exchange: {data['error']}")
    return data["access_token"], str(data["user_id"])


def exchange_long_lived_token(app_secret: str, short_token: str) -> str:
    response = requests.get(
        "https://graph.instagram.com/access_token",
        params={
            "grant_type": "ig_exchange_token",
            "client_secret": app_secret,
            "access_token": short_token,
        },
        timeout=60,
    )
    data = response.json()
    if "error" in data:
        raise RuntimeError(f"Long-lived token: {data['error']}")
    return data["access_token"]


def parse_code_from_input(raw: str) -> str:
    raw = raw.strip().strip('"').strip("'")
    if "code=" in raw:
        query = parse_qs(urlparse(raw).query)
        if "code" in query:
            return query["code"][0].split("#")[0]
    return raw.split("#")[0]


def run_exchange(code_or_url: str) -> None:
    cfg = load_config()
    app_id = cfg["app_id"]
    app_secret = cfg["app_secret"]
    redirect_uri = cfg["redirect_uri"]
    code = parse_code_from_input(code_or_url)

    print("Trocando codigo por token...")
    short_token, user_id = exchange_code_for_token(app_id, app_secret, redirect_uri, code)
    long_token = exchange_long_lived_token(app_secret, short_token)
    save_env({"META_ACCESS_TOKEN": long_token, "IG_USER_ID": user_id})
    profile = fetch_profile(long_token)
    print(f"\nSucesso! Conta @{profile.get('username', user_id)} (ID: {user_id})")
    print(f"Token salvo em {ENV_PATH}")
    print("\nProximo passo: python scripts/sync_instagram.py sync")


def run_oauth() -> None:
    cfg = load_config()
    app_id = cfg["app_id"]
    app_secret = cfg["app_secret"]
    redirect_uri = cfg["redirect_uri"]

    if not app_id or not app_secret:
        print("Erro: preencha INSTAGRAM_APP_ID e INSTAGRAM_APP_SECRET no .env")
        print("Onde achar: Meta App > Instagram > API setup with Instagram login")
        print("  > Business login settings > Instagram App ID / Secret")
        sys.exit(1)

    auth_code: dict[str, str] = {}
    done = threading.Event()

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            query = parse_qs(urlparse(self.path).query)
            if "code" in query:
                auth_code["code"] = query["code"][0].split("#")[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    b"<html><body><h2>Autorizado!</h2>"
                    b"<p>Volte ao terminal do Cursor. Pode fechar esta aba.</p></body></html>"
                )
            else:
                error = query.get("error_description", query.get("error", ["unknown"]))[0]
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<html><body><h2>Erro: {error}</h2></body></html>".encode())
            done.set()

        def log_message(self, format: str, *args) -> None:
            pass

    port = urlparse(redirect_uri).port or DEFAULT_PORT
    server = HTTPServer(("localhost", port), CallbackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    params = urlencode(
        {
            "client_id": app_id,
            "redirect_uri": redirect_uri,
            "scope": ",".join(SCOPES),
            "response_type": "code",
            "enable_fb_login": "false",
        }
    )
    auth_url = f"https://www.instagram.com/oauth/authorize?{params}"

    print("\n=== Autorizacao Instagram (API 2025+) ===\n")
    print("1. Faca login com @tatyzacharias e clique Permitir")
    print(f"2. Redirect URI: {redirect_uri}")
    print("\nIMPORTANTE: Apos autorizar, o browser pode mostrar erro de SSL.")
    print("   Isso e NORMAL. Copie a URL inteira da barra de endereco")
    print("   (contem code=...) e rode:")
    print('   python scripts/sync_instagram.py exchange "URL_COPIADA"\n')
    webbrowser.open(auth_url)

    if not done.wait(timeout=120):
        server.shutdown()
        print("\nNenhum callback HTTP recebido (esperado com HTTPS).")
        print("Cole a URL do browser com o comando exchange acima.")
        sys.exit(0)

    server.shutdown()

    if "code" not in auth_code:
        print("Autorizacao cancelada ou falhou.")
        sys.exit(1)

    print("Trocando codigo por token...")
    short_token, user_id = exchange_code_for_token(app_id, app_secret, redirect_uri, auth_code["code"])
    long_token = exchange_long_lived_token(app_secret, short_token)

    save_env({"META_ACCESS_TOKEN": long_token, "IG_USER_ID": user_id})

    profile = fetch_profile(long_token)
    username = profile.get("username", user_id)

    print(f"\nSucesso! Conta @{username} (ID: {user_id})")
    print(f"Token salvo em {ENV_PATH}")
    print("\nProximo passo: python scripts/sync_instagram.py sync")


def fetch_profile(token: str, ig_user_id: str | None = None) -> dict:
    fields = ",".join(
        [
            "user_id",
            "username",
            "name",
            "biography",
            "followers_count",
            "follows_count",
            "media_count",
            "profile_picture_url",
            "website",
            "account_type",
        ]
    )
    endpoint = ig_user_id if ig_user_id else "me"
    return ig_get(endpoint, token, {"fields": fields})


def fetch_media(token: str, ig_user_id: str, limit: int = 30) -> list[dict]:
    fields = ",".join(
        [
            "id",
            "caption",
            "media_type",
            "media_url",
            "permalink",
            "timestamp",
            "like_count",
            "comments_count",
            "thumbnail_url",
        ]
    )
    items: list[dict] = []
    path = f"{ig_user_id}/media"
    params: dict = {"fields": fields, "limit": min(limit, 50)}

    while path and len(items) < limit:
        data = ig_get(path, token, params if not path.startswith("http") else None)
        items.extend(data.get("data", []))
        next_url = data.get("paging", {}).get("next")
        if next_url and len(items) < limit:
            path = next_url
            params = {}
        else:
            break

    return items[:limit]


def fetch_media_insights(token: str, media_id: str, media_type: str) -> dict:
    if media_type in ("VIDEO", "REEL"):
        metrics = "views,reach,saved,shares,total_interactions"
    else:
        metrics = "reach,saved,shares,total_interactions"

    try:
        data = ig_get(f"{media_id}/insights", token, {"metric": metrics})
        return {item["name"]: item["values"][0]["value"] for item in data.get("data", [])}
    except RuntimeError:
        return {}


def fetch_account_insights(token: str, ig_user_id: str) -> dict:
    result: dict = {}
    try:
        data = ig_get(
            f"{ig_user_id}/insights",
            token,
            {"metric": "reach,views,follower_count", "period": "day", "metric_type": "total_value", "since": "", "until": ""},
        )
        for item in data.get("data", []):
            result[item["name"]] = item.get("total_value") or item.get("values")
    except RuntimeError as exc:
        result["_note"] = f"Insights parciais: {exc}"
    return result


def run_sync() -> None:
    cfg = load_config()
    token = cfg["access_token"]
    ig_user_id = cfg["ig_user_id"]

    if not token or not ig_user_id:
        print("Erro: META_ACCESS_TOKEN ou IG_USER_ID ausentes.")
        print("Rode primeiro: python scripts/sync_instagram.py auth")
        sys.exit(1)

    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    synced_at = datetime.now(timezone.utc).isoformat()

    print(f"Sincronizando conta {ig_user_id}...")

    profile = fetch_profile(token, ig_user_id)
    print(f"  Perfil: @{profile.get('username')} — {profile.get('followers_count')} seguidores")

    media = fetch_media(token, ig_user_id, limit=30)
    print(f"  Posts: {len(media)} recentes")

    for i, item in enumerate(media):
        item["insights"] = fetch_media_insights(token, item["id"], item.get("media_type", "IMAGE"))

    print("  Insights da conta...")
    account_insights = fetch_account_insights(token, ig_user_id)

    snapshot = {
        "synced_at": synced_at,
        "profile": profile,
        "account_insights": account_insights,
        "media": media,
    }

    out_path = SYNC_DIR / "profile_snapshot.json"
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_path = SYNC_DIR / "resumo.txt"
    summary_path.write_text(
        "\n".join(
            [
                f"Sincronizado em: {synced_at}",
                f"@{profile.get('username')} ({profile.get('name', '')})",
                f"Seguidores: {profile.get('followers_count')}",
                f"Posts totais: {profile.get('media_count')}",
                f"Midia recente sincronizada: {len(media)}",
                f"Bio: {profile.get('biography', '')}",
                "",
                f"Arquivo completo: {out_path.name}",
            ]
        ),
        encoding="utf-8",
    )

    print(f"\nSalvo em {out_path}")
    print(f"Resumo em {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Instagram via Instagram Login API")
    parser.add_argument("command", choices=["auth", "sync", "exchange"], help="auth | sync | exchange URL com code")
    parser.add_argument("code_or_url", nargs="?", help="URL ou code (comando exchange)")
    args = parser.parse_args()

    if args.command == "auth":
        run_oauth()
    elif args.command == "exchange":
        if not args.code_or_url:
            print("Uso: python scripts/sync_instagram.py exchange \"URL_COM_CODE\"")
            sys.exit(1)
        run_exchange(args.code_or_url)
    else:
        run_sync()


if __name__ == "__main__":
    main()
