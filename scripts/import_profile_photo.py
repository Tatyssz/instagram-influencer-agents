"""Copia foto de perfil HD para data/mediakit/profile-hd.png"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "data" / "mediakit" / "profile-hd.png"


def _find_in_cursor_attachments() -> Path | None:
    """Busca a foto mais recente enviada no chat (WhatsApp / anexo Cursor)."""
    storage = Path.home() / "AppData" / "Roaming" / "Cursor" / "User" / "workspaceStorage"
    if not storage.exists():
        return None
    candidates: list[Path] = []
    for path in storage.rglob("*"):
        try:
            if not path.is_file():
                continue
            name = path.name.lower()
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                continue
            if "whatsapp" in name or "profile" in name:
                candidates.append(path)
        except OSError:
            continue
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main() -> None:
    src: Path | None = None
    if len(sys.argv) >= 2:
        src = Path(sys.argv[1]).expanduser().resolve()
        if not src.exists():
            print(f"Arquivo não encontrado: {src}")
            sys.exit(1)
    else:
        src = _find_in_cursor_attachments()
        if not src:
            print("Nenhuma foto encontrada. Envie a imagem no chat ou passe o caminho:")
            print("  python scripts/import_profile_photo.py CAMINHO_DA_FOTO")
            sys.exit(1)
        print(f"Usando: {src}")

    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        DEST.unlink()
    shutil.copy2(src, DEST)
    print(f"OK: {DEST} ({DEST.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
