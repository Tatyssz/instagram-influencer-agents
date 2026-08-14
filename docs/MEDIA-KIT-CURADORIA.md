# Media Kit @tatyzacharias — curadoria e rebuild

**Sessão:** 14/08/2026 · estilo **luxe**  
**Objetivo:** portfólio web + PDF com parcerias reais, categorias filtráveis e curadoria manual via prints.

---

## Resultado atual

| Categoria | Peças |
|-----------|------:|
| **Todas** | 84 |
| Beleza | 29 |
| Cabelo | 16 |
| Eventos | 32 |
| Perfume | 6 |
| Moda | 4 |

**Arquivos gerados:**

- `output/mediakit/portfolio.html` — galeria interativa (filtro por categoria)
- `output/mediakit/media-kit.html` — versão impressa/PDF
- `output/mediakit/estimativa-metricas.json` — métricas para o hero

---

## Comandos

```powershell
cd "c:\Users\taty_\OneDrive\Desktop\Projetos Cursor\instagram-influencer-agents"

# 1. Sync amplo (catálogo completo de posts)
.venv\Scripts\python scripts/sync_instagram.py sync --media-limit 900

# 2. Métricas do media kit
.venv\Scripts\python scripts/build_mediakit_metrics.py

# 3. Gerar HTML + PDF (estilo luxe)
.venv\Scripts\python scripts/build_mediakit_html.py --style luxe --all
```

Após rebuild: **Ctrl+F5** no browser ao abrir `portfolio.html`.

---

## Onde configurar

| Arquivo | Função |
|---------|--------|
| `data/mediakit/config.json` | Marcas, categorias, exclusões, overrides |
| `data/mediakit/manual-covers/` | Capas curadas à mão (ex.: Festa Junina) |
| `scripts/mediakit_assets.py` | Seleção de posts, categorias, capas |
| `scripts/mediakit_luxe.py` | Layout luxe da galeria |
| `scripts/build_mediakit_html.py` | Orquestra build + PDF |

---

## Regras de categorização (implementadas)

1. **Cabelo** = reels de **marcas capilares** (`brand_partnerships` com `category: "cabelo"`).
2. **Tranças pessoais / humor / TikTok** = excluídos via `exclude_media_ids` (curadoria por print).
3. **Overrides manuais** em `media_categories` vencem a detecção automática.

### Marcas capilares detectadas

Salon Line, Haskell, Widi Care, Bello Cachos, Beyou Hair, Felps, Embelleze, Inoar, Yamá, Cless, Kohll Beauty, Raavi, All Nature, Amávia, L'Oréal Elseve (via caption).

### Overrides de curadoria (exemplos)

| media_id | Categoria | Motivo |
|----------|-----------|--------|
| `18560255209047274`, `18410198098192200` | perfume | Xêrosa body splash |
| `17875801038244955` | eventos | Kohll Beauty @ Beauty Show |
| `18221763445295425` | beleza | Raavi Pós Carnaval |
| `18034072727511775` | eventos | Yamá @ evento (Yamasterol gigante) |
| `17944669855099124` | beleza | Salon Line Na Pele (skincare) |

### Exclusões manuais (prints)

Reels removidos por pedido: Widi Care novidade, Bello Cachos pessoais/sorteio, Embelleze TikTok, tranças/humor, Ikesaki miscategorizado, eventos Espaço 19 / Embaixadores / Dolfinha, etc. — lista completa em `config.json` → `portfolio.exclude_media_ids`.

---

## Fluxo de curadoria no curso

1. Gerar portfólio inicial (`build_mediakit_html.py --style luxe`).
2. Abrir `portfolio.html` e revisar categoria por categoria.
3. Enviar **prints** no Cursor pedindo: mover de categoria ou remover.
4. Agente adiciona `media_categories` ou `exclude_media_ids` em `config.json`.
5. Rebuild + Ctrl+F5.

**Prompt útil:**

```
Revise output/mediakit/portfolio.html. Mova [marca/reel] de [categoria] para [categoria].
Ou: tire esse reel do portfólio (não quero).
```

---

## Lições técnicas

- **Capas erradas:** o ID no HTML pode diferir da capa visual — confirmar pelo arquivo em `output/mediakit/assets/reel-{id}.jpg` antes de excluir.
- **PowerShell:** usar `;` em vez de `&&` entre comandos.
- **Match de marcas:** tokens curtos (ex. `todecacho`) usam word boundary para não pegar `garotodecachos`.
- **Feiras:** posts com `@beautyshow` vão para Eventos, exceto quando override ou marca capilar com prioridade manual.

---

*Documento de apoio ao módulo 5 do curso · projeto instagram-influencer-agents.*
