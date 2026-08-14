# Status do Projeto

**Nome:** Instagram Influencer Agents  
**Autora:** Tatiana Zacharias ([@Tatyssz](https://github.com/Tatyssz))  
**Tipo:** Projeto pessoal / portfólio (sem vínculo empresarial)  
**Licença:** MIT — disponível para uso, estudo e comercialização  
**Versão atual:** 0.4.0  
**Última atualização:** 14/08/2026

---

## Resumo executivo

Toolkit Python + Cursor IDE para **creators de Instagram** conectarem a **Meta Graph API**, sincronizarem dados reais do perfil e otimizarem a presença comercial para **parcerias pagas** — com automação opcional via Playwright quando a API não permite editar o perfil.

**Case study:** conta Creator de beauty/UGC (~32k seguidores, nicho cabelo cacheado).

---

## Status geral

| Área | Status | Progresso |
|------|--------|-----------|
| Meta API — OAuth + Sync | ✅ Concluído | 100% |
| Análise de perfil (insights) | ✅ Concluído | 100% |
| Otimização de bio (workflow) | 🔄 Em andamento | 60% |
| Automação Playwright | 🔄 Em teste | 80% |
| Media Kit automático | ✅ Concluído | 100% |
| Sync paginado (>30 posts) | ✅ Concluído | 90% |
| Publicação de Reels via API | 📋 Backlog | 0% |
| Pacotes comerciais / pricing | 📋 Backlog | 0% |

**Status do produto:** `Beta` — funcional para uso real, automação de bio em refinamento.

---

## Fases do projeto (ciclo de vida real)

### Fase 0 — Discovery ✅

- [x] Definir problema: creator precisa de dados + perfil comercial sem fazer tudo manual
- [x] Pesquisar limitações da Meta API (leitura vs escrita)
- [x] Escolher stack: Python, Cursor, requests, Playwright

### Fase 1 — MVP (API) ✅

- [x] App Meta Developers configurado
- [x] OAuth Instagram Login 2025+
- [x] Sync perfil + 30 posts + insights
- [x] Documentação de setup

### Fase 2 — Inteligência ✅

- [x] Análise de pilares de conteúdo
- [x] Métricas para media kit / marcas
- [x] Horários e top posts
- [x] Diagnóstico comercial

### Fase 3 — Otimização de perfil 🔄

- [x] Workflow item a item com aprovação
- [x] Nome de exibição otimizado
- [x] Bio linha 1 otimizada
- [ ] Bio linhas 2–4 + link + CTA
- [ ] Validação automática de 150 caracteres

### Fase 4 — Automação 🔄

- [x] Modo semi-automático (clipboard)
- [x] Playwright login persistente
- [x] Apply + verify via API
- [ ] Submit confiável 100% (React input events)
- [ ] Edição de nome via web (UI Meta mudou)

### Fase 5 — Produto comercial 🔄

- [x] Media Kit PDF/HTML luxe
- [x] Portfólio curado por categoria (84 peças)
- [x] Documentação de curadoria (`docs/MEDIA-KIT-CURADORIA.md`)
- [ ] Template de proposta para marcas
- [ ] Curso gravado (material em `docs/`)
- [ ] Landing page / venda do template

---

## Métricas do case study (sync real)

| Métrica | Valor |
|---------|-------|
| Seguidores | ~32,6k |
| Posts totais | 834 |
| Tipo de conta | Creator |
| Posts sincronizados | 30 Reels |
| Taxa engajamento (amostra) | ~0,32% |
| Destaque comercial | shares orgânicos altos |

*Dados de demonstração não são commitados no repositório (privacidade).*

---

## Riscos e mitigações

| Risco | Mitigação |
|-------|-----------|
| Token expira (~60 dias) | Comando `auth` documentado |
| API Meta muda scopes | Changelog + docs atualizados |
| Instagram muda UI web | Seletores centralizados em `instagram_browser.py` |
| Bio > 150 chars | Validação antes de apply (planejado) |
| Secrets no git | `.gitignore` + `.env.example` |

---

## Contato / portfólio

- **GitHub:** [@Tatyssz](https://github.com/Tatyssz)
- **Instagram (case study):** [@tatyzacharias](https://instagram.com/tatyzacharias)
