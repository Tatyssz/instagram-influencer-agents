# F1 etapa 1.5 — Comunidade (sessão 2026-08-28)

> **Status:** 🔄 piloto local — comentários v13, moderação off-topic, admin cancelar fila  
> **Commits:** `f728ead`, `6bc55a9` (comjuntas-saas)  
> **App:** `comjuntas-saas/apps/web` · **https://localhost:3000/app/community**

Continuação de [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-27.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-27.md).

---

## O que entregamos nesta sessão

### 1. Comentários sugeridos v13 (tom humano)

| Regra | Detalhe |
|-------|---------|
| Mínimo | **4 palavras** (emoji não conta) |
| Contexto | Lê legenda + hashtags; comentário precisa ancorar no assunto |
| Tom | Seguidora no Instagram — ecoa frases do post («não vão nos abalar», «autoestima em dia») |
| Bloqueio | Elogios vazios («Uau!!», «Que incrível!»), marketing, tom de PR |
| Regeneração | `COMMENT_GENERATOR_VERSION=13` — pendentes antigos atualizam ao abrir a fila |
| IA | OpenAI opt-in; validação local sempre (`isValidEngagementComment`) |

Arquivos: `suggest-comment.ts`, `suggest-comment-ai.ts`, `comment-golden-fixtures.ts`

### 2. Moderação off-topic corrigida

| Problema | Correção |
|----------|----------|
| UGC genérico passava na fila | Keyword `ugc` isolado removido; match contextual em `ugc_beauty` |
| Posts de estabelecimento/viagem | Expandido `OFF_TOPIC_REVIEW` (estabelecimento, #viagem, gastronomia, etc.) |
| Ordem de checagem | Off-topic **antes** de allow beauty |

Arquivos: `beauty-taxonomy.ts`, `content-moderation.ts`, `content-moderation.test.mjs`

### 3. Admin — cancelar pedidos na fila

| URL | Ação |
|-----|------|
| `/admin/alerts/engagement-requests` | Lista pedidos ativos · **Cancelar pedido na fila** |

Efeito: remove da fila das parceiras; owner vê status `rejected`; pedido não conta em limite diário/duplicata.

Arquivos: `requests.ts`, `admin/alerts/engagement-requests/`, nav + card no painel ADM.

### 4. Revisão de conteúdo ADM — layout

Botões Aprovar / Motivo / Recusar alinhados na mesma barra (`content-review/page.tsx`).

---

## Testes

```powershell
cd comjuntas-saas/apps/web
npm run test:comments      # 20 golden (incl. autoestima/anti-racismo)
npm run test:moderation
npm run test:community     # comments + moderation + reel-watch
```

---

## Arquivos principais

| Área | Caminhos |
|------|----------|
| Comentários | `lib/community/suggest-comment.ts`, `suggest-comment-ai.ts` |
| Moderação | `beauty-taxonomy.ts`, `content-moderation.ts` |
| Admin fila | `admin/alerts/engagement-requests/` |
| Docs | `comjuntas-saas/docs/COMUNIDADE-PILOTO.md` |

---

## Próximo passo

- Estabilizar execução IG no piloto local.
- Migrar Comunidade para PostgreSQL (`api/` + migrations).
