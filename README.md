# Instagram Influencer Agents

Toolkit **open source** (MIT) para creators e UGC: conecta Instagram à **Meta Graph API**, sincroniza dados reais do perfil e otimiza a presença comercial para **parcerias pagas** — com automação opcional via **Playwright** + **Cursor IDE**.

> **Projeto pessoal** de [Tatiana Zacharias](https://github.com/Tatyssz) · portfólio profissional · sem vínculo empresarial · licenciável para curso/template.

![Status](https://img.shields.io/badge/status-beta-orange)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Problema

Creators precisam de **dados reais** (posts, insights, engajamento) e um **perfil comercial** claro para receber propostas — mas:

- A Meta API **lê** perfil/posts, mas **não edita** bio/nome
- Planilhas e prints manuais não escalam
- Otimizar perfil “no feeling” perde conversões de marcas

## Solução

| Camada | O que faz |
|--------|-----------|
| **Meta API** | OAuth + sync de perfil, posts, insights + demografia |
| **Análise** | Diagnóstico comercial (pilares, horários, top posts) |
| **Profile workflow** | Edição item a item com aprovação + validação |
| **Playwright** | Aplica mudanças no instagram.com quando a API não permite |
| **Media Kit** | Portfólio web luxe + PDF com parcerias curadas |

**Case study:** conta Creator beauty/UGC (~32k seguidores, L'Oréal Star, Baixada Santista).

---

## Stack

- **Python 3.12** — scripts de sync e automação
- **Meta Instagram API** (Instagram Login 2025+)
- **Playwright** — automação de browser
- **Cursor IDE** — agentes + documentação + curso

---

## Início rápido

### 1. Clonar e instalar

```powershell
git clone https://github.com/Tatyssz/instagram-influencer-agents.git
cd instagram-influencer-agents
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

### 2. Configurar Meta Developers

1. Criar app Business em [developers.facebook.com](https://developers.facebook.com)
2. Adicionar **Instagram** → API with Instagram Login
3. Anotar `META_APP_ID`, `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET`
4. Redirect URI: `https://localhost:8765/callback`
5. Adicionar-se como **Testador do Instagram** (modo dev)

Detalhes completos: [`docs/CURSO-PASSO-A-PASSO.md`](docs/CURSO-PASSO-A-PASSO.md)

### 3. Configurar `.env`

```powershell
copy .env.example .env
```

### 4. Autorizar e sincronizar

```powershell
python scripts/sync_instagram.py auth
# Se SSL falhar no callback, copie a URL e rode:
python scripts/sync_instagram.py exchange "URL_COM_CODE"
python scripts/sync_instagram.py sync --media-limit 900
```

Dados em `data/sync/profile_snapshot.json`.

### 5. Otimizar perfil (opcional)

```powershell
copy data\profile\target.example.json data\profile\target.json
# Edite target.json com sua bio (max 150 chars)

python scripts/update_profile.py login    # 1x
python scripts/update_profile.py apply
python scripts/update_profile.py verify
```

### 6. Media Kit (portfólio para marcas)

```powershell
python scripts/build_mediakit_metrics.py
python scripts/build_mediakit_html.py --style luxe --all
```

Abrir `output/mediakit/portfolio.html`. Curadoria: [`docs/MEDIA-KIT-CURADORIA.md`](docs/MEDIA-KIT-CURADORIA.md)

---

## Comandos

| Comando | Descrição |
|---------|-----------|
| `sync_instagram.py auth` | OAuth Instagram |
| `sync_instagram.py exchange "URL"` | Trocar code por token |
| `sync_instagram.py sync --media-limit 900` | Catálogo amplo + demografia |
| `build_mediakit_html.py --style luxe --all` | Portfólio web + PDF |
| `build_mediakit_metrics.py` | Métricas para o media kit |
| `update_profile.py login` | Login 1x no Chrome (Playwright) |
| `update_profile.py status` | Comparar alvo vs perfil atual |
| `update_profile.py apply` | Aplicar mudanças via browser |
| `update_profile.py verify` | Confirmar via API |

---

## Estrutura

```
instagram-influencer-agents/
├── scripts/
│   ├── sync_instagram.py      # API Meta
│   ├── update_profile.py      # CLI perfil
│   └── instagram_browser.py   # Playwright
├── data/
│   ├── sync/                  # dump API (gitignored)
│   └── profile/               # target + sessão (gitignored)
├── docs/
│   └── CURSO-PASSO-A-PASSO.md # material de curso
├── PROJECT_STATUS.md          # status de projeto real
├── ROADMAP.md
└── CHANGELOG.md
```

---

## Documentação do projeto

| Arquivo | Conteúdo |
|---------|----------|
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Fases, progresso, métricas, riscos |
| [ROADMAP.md](ROADMAP.md) | Versões futuras + produto vendável |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de releases |
| [docs/CURSO-PASSO-A-PASSO.md](docs/CURSO-PASSO-A-PASSO.md) | Tutorial completo (curso) |

---

## Limitações conhecidas

- API **não edita** nome/bio/link → use Playwright ou manual
- Sync traz ~**30 posts** por vez (paginação planejada)
- Demografia completa exige Insights no app ou scopes extras
- Bio Instagram: **máximo 150 caracteres**

---

## Licença

[MIT](LICENSE) — use, modifique e venda (curso, template, consultoria). Atribuição apreciada.

---

## Autora

**Tatiana Zacharias** · [@Tatyssz](https://github.com/Tatyssz) · [@tatyzacharias](https://instagram.com/tatyzacharias)

Projeto desenvolvido como case study real de creator economy + automação com IA no Cursor.
