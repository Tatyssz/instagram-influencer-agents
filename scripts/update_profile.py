#!/usr/bin/env python3
"""
Atualiza perfil Instagram.

A API Meta nao permite editar nome/bio/link. Com Playwright, o script aplica
automaticamente no instagram.com (voce so faz login 1x).

Uso:
  python scripts/update_profile.py login           # login 1x no browser (PC)
  python scripts/update_profile.py status          # compara alvo vs perfil atual
  python scripts/update_profile.py apply           # aplica via browser (automatico)
  python scripts/update_profile.py apply name      # aplica campo especifico
  python scripts/update_profile.py apply --manual  # modo antigo (copiar/colar)
  python scripts/update_profile.py verify          # confere no Instagram (API)
  python scripts/update_profile.py verify name
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import webbrowser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sync_instagram import GRAPH_IG, fetch_profile, load_config  # noqa: E402
from instagram_browser import (  # noqa: E402
    BrowserApplyError,
    SessionExpiredError,
    apply_fields,
    has_browser_session,
    run_login,
)

PROFILE_DIR = ROOT / "data" / "profile"
TARGET_PATH = PROFILE_DIR / "target.json"
HISTORY_PATH = PROFILE_DIR / "history.json"
EDIT_URL = "https://www.instagram.com/accounts/edit/"

FIELDS = ("name", "biography", "website")
FIELD_LABELS = {
    "name": "Nome de exibicao",
    "biography": "Bio",
    "website": "Link",
}


def load_target() -> dict:
    if not TARGET_PATH.exists():
        raise FileNotFoundError(f"Arquivo alvo nao encontrado: {TARGET_PATH}")
    data = json.loads(TARGET_PATH.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))


def save_history(entries: list[dict]) -> None:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_live_profile() -> dict:
    cfg = load_config()
    token = cfg["access_token"]
    ig_user_id = cfg["ig_user_id"]
    if not token or not ig_user_id:
        print("Erro: META_ACCESS_TOKEN ou IG_USER_ID ausentes.")
        print("Rode: python scripts/sync_instagram.py auth")
        sys.exit(1)
    return fetch_profile(token, ig_user_id)


def pending_fields(target: dict, profile: dict) -> list[str]:
    pending: list[str] = []
    for field in FIELDS:
        desired = target.get(field)
        if desired is None:
            continue
        current = (profile.get(field) or "").strip()
        if current != desired.strip():
            pending.append(field)
    return pending


def copy_to_clipboard(text: str) -> bool:
    try:
        proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE, close_fds=True)
        proc.communicate(input=text.encode("utf-16-le"))
        return proc.returncode == 0
    except OSError:
        return False


def try_api_update(field: str, value: str) -> tuple[bool, str]:
    cfg = load_config()
    token = cfg["access_token"]
    ig_user_id = cfg["ig_user_id"]
    if not token or not ig_user_id:
        return False, "Token ou IG_USER_ID ausentes"

    url = f"{GRAPH_IG}/{ig_user_id}"
    response = requests.post(url, data={field: value, "access_token": token}, timeout=30)
    data = response.json()
    if response.ok and "error" not in data:
        return True, "Atualizado via API"
    err = data.get("error", {})
    message = err.get("message", str(data))
    return False, message


def print_field_block(field: str, current: str | None, target: str) -> None:
    label = FIELD_LABELS[field]
    print(f"\n--- {label} ({field}) ---")
    print(f"  Atual:  {current or '(vazio)'}")
    print(f"  Alvo:   {target}")


def cmd_status() -> None:
    target = load_target()
    profile = fetch_live_profile()
    pending = pending_fields(target, profile)

    print(f"Perfil: @{profile.get('username')} — {profile.get('followers_count')} seguidores\n")

    for field in FIELDS:
        desired = target.get(field)
        if desired is None:
            continue
        current = profile.get(field) or ""
        status = "OK" if field not in pending else "PENDENTE"
        print_field_block(field, current, desired)
        print(f"  Status: {status}")

    if not any(target.get(f) is not None for f in FIELDS):
        print("Nenhum campo definido em data/profile/target.json")
        return

    if pending:
        print(f"\nPendentes: {', '.join(pending)}")
        print(f"Proximo passo: python scripts/update_profile.py apply")
    else:
        print("\nPerfil alinhado com target.json")


def cmd_apply(field: str | None, *, manual: bool = False) -> None:
    target = load_target()
    profile = fetch_live_profile()
    pending = pending_fields(target, profile)

    if not pending:
        print("Nada pendente — perfil ja esta igual ao alvo.")
        return

    if field:
        if field not in FIELDS:
            print(f"Campo invalido. Use: {', '.join(FIELDS)}")
            sys.exit(1)
        if field not in pending:
            print(f"Campo '{field}' ja esta atualizado ou nao tem alvo definido.")
            sys.exit(0)
        fields_to_apply = [field]
    else:
        fields_to_apply = [pending[0]]

    field = fields_to_apply[0]
    value = target[field]
    label = FIELD_LABELS[field]

    print(f"Aplicando: {label}")
    print_field_block(field, profile.get(field), value)

    ok, msg = try_api_update(field, value)
    if ok:
        print(f"\nAPI: {msg}")
        print("Rodando verificacao...")
        cmd_verify(field)
        return

    if not manual and has_browser_session(PROFILE_DIR):
        print("\nAplicando via browser (Playwright)...")
        try:
            apply_fields(PROFILE_DIR, {field: value})
            print("Rodando verificacao...")
            cmd_verify(field)
            return
        except SessionExpiredError as exc:
            print(f"\n{exc}")
            sys.exit(1)
        except BrowserApplyError as exc:
            print(f"\nBrowser nao conseguiu aplicar: {exc}")
            print("Tente de novo apos login ou use --manual\n")

    if not manual and not has_browser_session(PROFILE_DIR):
        print("\nSem sessao de browser. Rode primeiro:")
        print("  python scripts/update_profile.py login")
        print("\nOu use --manual para copiar/colar no celular.\n")

    apply_manual(field, value, label)


def apply_manual(field: str, value: str, label: str) -> None:
    print("\nModo manual (copiar/colar):")
    print("\n" + "=" * 50)
    print("COPIE ESTE TEXTO (celular ou PC):")
    print("=" * 50)
    print(value)
    print("=" * 50)
    print("\nIMPORTANTE: o clipboard do PC NAO vai para o celular.\n")

    copied = copy_to_clipboard(value)
    if copied:
        print("Copiado para a area de transferencia DESTE computador.")

    instructions = {
        "name": "Campo NOME (1o campo em Editar perfil — NAO e a Bio).",
        "biography": "Campo BIO (abaixo do nome).",
        "website": "Campo LINK / Site.",
    }
    print("\n--- No CELULAR ---")
    print("1. Instagram > seu perfil > Editar perfil")
    print(f"2. Toque em {instructions[field]}")
    print("3. Apague tudo e cole o texto")
    print("4. Toque em Concluir (canto superior direito)")
    print("\n--- Depois de salvar ---")
    print(f"python scripts/update_profile.py verify {field}")

    webbrowser.open(EDIT_URL)

    guide_path = PROFILE_DIR / "apply_pendente.txt"
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    guide_path.write_text(
        "\n".join(
            [
                f"Campo: {label} ({field})",
                f"Valor para colar:\n{value}",
                "",
                instructions[field],
                EDIT_URL,
            ]
        ),
        encoding="utf-8",
    )
    print(f"\nGuia salvo em {guide_path}")


def cmd_verify(field: str | None) -> None:
    target = load_target()
    profile = fetch_live_profile()
    pending = pending_fields(target, profile)

    fields = [field] if field else list(FIELDS)
    if field and field not in FIELDS:
        print(f"Campo invalido. Use: {', '.join(FIELDS)}")
        sys.exit(1)

    history = load_history()
    verified_at = datetime.now(timezone.utc).isoformat()
    all_ok = True

    for f in fields:
        desired = target.get(f)
        if desired is None:
            continue
        current = (profile.get(f) or "").strip()
        desired = desired.strip()
        ok = current == desired
        all_ok = all_ok and ok

        print_field_block(f, current, desired)
        print(f"  Status: {'OK' if ok else 'AINDA DIFERENTE'}")

        if ok:
            history.append(
                {
                    "field": f,
                    "target": desired,
                    "verified_at": verified_at,
                    "success": True,
                    "value_after": current,
                }
            )

    save_history(history)

    if field:
        if target.get(field) is None:
            print(f"\nCampo '{field}' nao tem alvo em target.json")
            sys.exit(1)
        if (profile.get(field) or "").strip() == (target[field] or "").strip():
            print(f"\nConfirmado: {FIELD_LABELS[field]} atualizado com sucesso.")
        else:
            print(f"\nAinda nao bate. Confira no app e rode verify de novo.")
            sys.exit(1)
        return

    if pending:
        print(f"\nAinda pendentes: {', '.join(pending)}")
        sys.exit(1)
    print("\nTodos os campos definidos estao corretos.")


def cmd_login() -> None:
    run_login(PROFILE_DIR)


def main() -> None:
    parser = argparse.ArgumentParser(description="Atualizar perfil Instagram")
    parser.add_argument("command", choices=["login", "status", "apply", "verify"])
    parser.add_argument("field", nargs="?", choices=FIELDS, help="name | biography | website")
    parser.add_argument("--manual", action="store_true", help="copiar/colar em vez do browser")
    args = parser.parse_args()

    if args.command == "login":
        cmd_login()
    elif args.command == "status":
        cmd_status()
    elif args.command == "apply":
        cmd_apply(args.field, manual=args.manual)
    else:
        cmd_verify(args.field)


if __name__ == "__main__":
    main()
