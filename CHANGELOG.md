# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [0.3.0] - 2026-08-11

### Adicionado

- Automação de perfil com Playwright (`update_profile.py`, `instagram_browser.py`)
- Fluxo `login` / `apply` / `verify` / `status` para edição semi-automática de bio
- Documentação completa para curso (`docs/CURSO-PASSO-A-PASSO.md`)
- Arquivos de gestão de projeto: `PROJECT_STATUS.md`, `ROADMAP.md`

### Corrigido

- Redirect OAuth: `https://localhost:8765/callback` (Meta rejeita `http://`)
- Scopes Instagram API 2025+ (`instagram_business_basic`, `instagram_business_manage_insights`)
- OAuth via `instagram.com/oauth/authorize` e token exchange via `api.instagram.com`
- Navegação Playwright com retries para redirecionamentos do Instagram
- Seletores da UI web: `#pepBio`, botão `Enviar` com `aria-disabled`

## [0.2.0] - 2026-08-11

### Adicionado

- Otimização de perfil item a item (nome de exibição + bio)
- `data/profile/target.json` como fonte de verdade das mudanças
- Histórico de verificações via API

## [0.1.0] - 2026-08-11

### Adicionado

- Projeto inicial: OAuth Instagram Login API + sync de perfil e posts
- `scripts/sync_instagram.py` (auth, exchange, sync)
- Export para `data/sync/profile_snapshot.json` e `resumo.txt`
- Insights de conta e dos 30 posts mais recentes

[0.3.0]: https://github.com/Tatyssz/instagram-influencer-agents/compare/v0.1.0...v0.3.0
[0.2.0]: https://github.com/Tatyssz/instagram-influencer-agents/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Tatyssz/instagram-influencer-agents/releases/tag/v0.1.0
