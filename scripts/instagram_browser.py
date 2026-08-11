"""Automacao de perfil Instagram via Playwright (browser real)."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAYWRIGHT_BROWSERS = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "tatyzacharias-playwright"
PLAYWRIGHT_BROWSERS.mkdir(parents=True, exist_ok=True)
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(PLAYWRIGHT_BROWSERS)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EDIT_URL = "https://www.instagram.com/accounts/edit/"
LOGIN_URL = "https://www.instagram.com/accounts/login/"

FIELD_SELECTORS: dict[str, list[str]] = {
    "name": [
        'input[name="displayName"]',
        'input[placeholder="Nome"]',
        'input[aria-label="Nome"]',
        'input[aria-label="Name"]',
    ],
    "biography": [
        "#pepBio",
        'textarea#pepBio',
        'textarea[placeholder="Bio"]',
        'textarea[name="biography"]',
        'textarea[aria-label="Bio"]',
    ],
    "website": [
        'input[placeholder="Site"]',
        'input[name="externalUrl"]',
        'input[aria-label="Link"]',
        'input[aria-label="Site"]',
    ],
}

SUBMIT_SELECTORS = [
    'button:has-text("Enviar")',
    'button[type="submit"]',
    'button:has-text("Submit")',
    'div[role="button"]:has-text("Enviar")',
]


class SessionExpiredError(RuntimeError):
    """Sessao do browser expirou — precisa rodar login de novo."""


class BrowserApplyError(RuntimeError):
    """Falha ao aplicar mudanca via browser."""


def ensure_browsers_installed() -> None:
    if list(PLAYWRIGHT_BROWSERS.glob("chromium-*/chrome-win64/chrome.exe")):
        return
    print("Baixando Chrome do Playwright (1x, ~200 MB)...")
    import subprocess

    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise BrowserApplyError(
            "Falha ao baixar Chrome. Rode manualmente:\n"
            "  .venv\\Scripts\\python -m playwright install chromium"
        )
    print("Chrome instalado.\n")


def browser_profile_dir(profile_dir: Path) -> Path:
    return profile_dir / "browser_profile"


def has_browser_session(profile_dir: Path) -> bool:
    user_data = browser_profile_dir(profile_dir)
    return user_data.exists() and any(user_data.iterdir())


def _find_locator(page, selectors: list[str], timeout_ms: int = 8000):
    deadline = time.time() + (timeout_ms / 1000)
    last_error: Exception | None = None
    while time.time() < deadline:
        for selector in selectors:
            try:
                locator = page.locator(selector).first
                if locator.count() > 0 and locator.is_visible(timeout=500):
                    return locator
            except Exception as exc:
                last_error = exc
        page.wait_for_timeout(300)
    raise BrowserApplyError(
        f"Campo nao encontrado. Seletores: {selectors}. Ultimo erro: {last_error}"
    )


def _dismiss_overlays(page) -> None:
    for label in ("Agora nao", "Not Now", "Cancelar", "Cancel"):
        try:
            btn = page.locator(f'button:has-text("{label}")').first
            if btn.is_visible(timeout=800):
                btn.click()
                page.wait_for_timeout(400)
        except Exception:
            pass


def _is_login_page(url: str) -> bool:
    return "/accounts/login" in url


def _is_edit_page(page) -> bool:
    if "/accounts/edit" in page.url:
        return True
    for field in ("biography", "name", "website"):
        for selector in FIELD_SELECTORS[field]:
            try:
                if page.locator(selector).first.is_visible(timeout=800):
                    return True
            except Exception:
                continue
    return False


def _goto_edit_page(page) -> None:
    """Abre a pagina de edicao; Instagram as vezes redireciona via home."""
    last_error: Exception | None = None
    for attempt in range(4):
        _dismiss_overlays(page)
        try:
            if _is_edit_page(page):
                return
            page.goto(EDIT_URL, wait_until="domcontentloaded", timeout=30000)
        except Exception as exc:
            last_error = exc
            if "interrupted" not in str(exc).lower():
                raise
        page.wait_for_timeout(2000)
        _dismiss_overlays(page)

        if _is_login_page(page.url):
            raise SessionExpiredError(
                "Nao logado no Instagram. Rode: python scripts/update_profile.py login"
            )
        if _is_edit_page(page):
            return

    try:
        _find_locator(page, FIELD_SELECTORS["biography"], timeout_ms=8000)
        return
    except BrowserApplyError as exc:
        raise BrowserApplyError(
            f"Nao consegui abrir Editar perfil. URL atual: {page.url}. "
            f"Tente login de novo. Detalhe: {exc}"
        ) from last_error


def _ensure_logged_in(page) -> None:
    if _is_login_page(page.url):
        raise SessionExpiredError(
            "Nao logado no Instagram. Rode: python scripts/update_profile.py login"
        )
    _goto_edit_page(page)


def _fill_field(page, field: str, value: str) -> None:
    locator = _find_locator(page, FIELD_SELECTORS[field])
    locator.click()
    locator.press("Control+a")
    locator.press("Backspace")
    if field == "biography":
        # Instagram so habilita "Enviar" com eventos reais de input (React).
        locator.press_sequentially(value, delay=5)
    else:
        locator.fill(value)
        locator.press(" ")
        locator.press("Backspace")
    page.wait_for_timeout(600)


def _wait_submit_enabled(page, timeout_ms: int = 15000):
    deadline = time.time() + (timeout_ms / 1000)
    while time.time() < deadline:
        btn = page.locator('div[role="button"]').filter(has_text="Enviar").first
        try:
            if btn.is_visible(timeout=500) and btn.get_attribute("aria-disabled") == "false":
                return btn
        except Exception:
            pass
        page.wait_for_timeout(250)
    raise BrowserApplyError("Botao Enviar continua desabilitado — Instagram nao detectou alteracao.")


def _click_submit(page) -> None:
    btn = _wait_submit_enabled(page)
    btn.scroll_into_view_if_needed()
    btn.click()
    page.wait_for_timeout(2500)


def run_login(profile_dir: Path) -> None:
    ensure_browsers_installed()
    from playwright.sync_api import sync_playwright

    user_data = browser_profile_dir(profile_dir)
    user_data.mkdir(parents=True, exist_ok=True)

    print("\n=== Login Instagram (1x) ===\n")
    print("1. Faca login como @tatyzacharias na janela que abrir")
    print("2. Se aparecer 'Salvar informacoes' ou notificacoes, clique Agora nao")
    print("3. Quando estiver logado (feed ou perfil), volte aqui e pressione ENTER\n")

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            headless=False,
            locale="pt-BR",
            viewport={"width": 1280, "height": 900},
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(LOGIN_URL, wait_until="domcontentloaded")

        input("Pressione ENTER apos login completo... ")

        try:
            _dismiss_overlays(page)
            if _is_login_page(page.url):
                print("\nErro: ainda na tela de login. Faca login e tente de novo.")
                sys.exit(1)
            _goto_edit_page(page)
            print(f"\nLogin OK. Perfil de browser salvo em {user_data}")
        except (SessionExpiredError, BrowserApplyError) as exc:
            print(f"\nErro: {exc}")
            sys.exit(1)
        finally:
            context.close()


def apply_fields(profile_dir: Path, updates: dict[str, str], *, headless: bool = False) -> None:
    ensure_browsers_installed()
    from playwright.sync_api import sync_playwright

    if not has_browser_session(profile_dir):
        raise SessionExpiredError(
            "Nenhuma sessao salva. Rode primeiro: python scripts/update_profile.py login"
        )

    user_data = browser_profile_dir(profile_dir)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            headless=headless,
            locale="pt-BR",
            viewport={"width": 1280, "height": 900},
        )
        page = context.pages[0] if context.pages else context.new_page()

        try:
            _ensure_logged_in(page)

            for field, value in updates.items():
                if field not in FIELD_SELECTORS:
                    raise BrowserApplyError(f"Campo desconhecido: {field}")
                _fill_field(page, field, value)

            _click_submit(page)
            print("Salvo no Instagram via browser.")
        finally:
            context.close()
