# Entregas por fase (F0–F5)

> **Status:** F0 local validado · F1 etapa 1 ✅ · F1 etapa 1.5 piloto local 🔄 · staging pendente  
> **Atualizado:** 2026-08-24

## Resumo

| Fase | Nome | Cobrança | Critério de saída |
|------|------|----------|-------------------|
| F0 | Fundação | Não | Login app + admin em staging |
| F1 | Core SaaS | Sim | 2–3 betas pagantes geram kit sozinhas |
| F2 | Academy | Upsell | 1 compra avulsa ou acesso Pro |
| F3 | Comunidade | No plano | Círculo piloto 2 semanas |
| F4 | Engajamento | Pro+ | Aprovar+executar estável 1 semana |
| F5 | Escala | — | Templates, agency, domínio |

**Registros de sessão:** [`F0-SESSAO-2026-08-20.md`](F0-SESSAO-2026-08-20.md) · [`F1-ETAPA1-SESSAO-2026-08-20.md`](F1-ETAPA1-SESSAO-2026-08-20.md) · [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md)  
**Ritual fim de etapa (commit + docs):** [`RITUAL-FIM-ETAPA.md`](RITUAL-FIM-ETAPA.md)  
**Regras comunidade (DEC-2026-08-20):** [`COMUNIDADE-REGRAS.md`](COMUNIDADE-REGRAS.md)

## F0 — Fundação

Repo local: `comjuntas-saas/` · git commit `c22b6b0` ✅ · GitHub remoto pendente

### Concluído (local)

- [x] Repo `comjuntas-saas` (local + README)
- [x] Migration Alembic `users` + `subscriptions` (arquivo no repo)
- [x] Clerk configurado + login testado (e-mail / Google)
- [x] Admin: `ugctatianazacharias@gmail.com` → `/admin` OK
- [x] Shell Next.js: landing, `/app/*`, `/admin/*`
- [x] API FastAPI `/api/v1/health` (testado local)
- [x] Validação manual: landing → app → admin (2026-08-20)

### Pendente (fecha F0)

- [ ] Postgres rodando + `alembic upgrade head` (Docker ou DB na nuvem)
- [ ] Push GitHub repo `comjuntas-saas`
- [ ] Deploy staging (F0-07)
- [ ] Critério saída F0-08 (login app + admin **em staging**)

## F1 — Core SaaS (ordem revisada)

Ver [`F1-ORDEM-EXECUCAO.md`](F1-ORDEM-EXECUCAO.md).

| # | Entrega | Status |
|---|---------|--------|
| 1 | OAuth IG + sync + dashboard | ✅ testado @tatyzacharias · commit `c22b6b0` |
| **1.5** | **Comunidade: follow mútuo + fila + alertas unfollow** | 🔄 piloto local · [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md) |
| 2 | Media kit PDF | ⬜ |
| 3 | Portfólio luxe | ⬜ |
| 4 | IA + Stripe + visual | ⬜ |

### Engajamento (1.5) — detalhe

- [x] Plano e ordem documentados (≠ InstaBarato)
- [x] Migration `circles`, `circle_members`, `engagement_queue`, `engagement_actions`
- [x] Menu **Comunidade** no app (shell)
- [x] Conectar Instagram (etapa 1) — ver [`F1-ETAPA1-SESSAO-2026-08-20.md`](F1-ETAPA1-SESSAO-2026-08-20.md)
- [x] Gate follow círculo + login Chrome + fila Playwright (piloto)
- [x] Detecção unfollow manual + refollow + alerta ADM/usuária
- [x] Tela **Meus posts** — marcar pedido (contador 1/dia piloto)
- [ ] Fila engajamento populada pelo sync
- [ ] Executar curtir/comentar após aprovação
- [ ] Dados da comunidade no Postgres (hoje JSON em `.data/`)
- [ ] Piloto 2 creators em staging

## F1 — itens originais (depois)

- [ ] Billing (Stripe)
- [ ] OAuth IG multi-tenant
- [ ] Media kit + portfólio + IA

## F2 — Academy

- [ ] C1–C3 no painel
- [ ] Checkout avulso

## F3 — Comunidade

- [ ] Círculos + fila lembretes

## F4 — Engajamento

- [ ] Sessão IG + aprovar + executar

## F5 — Escala

- [ ] Backlog pós-PMF
