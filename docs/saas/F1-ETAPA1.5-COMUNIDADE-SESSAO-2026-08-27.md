# F1 etapa 1.5 — Comunidade (sessão 2026-08-27)

> **Status:** 🔄 piloto local — fila inbox, histórico compacto, catálogo de posts, comentários v11, performance  
> **Commit:** *(comjuntas-saas — ver `git log` após push)*  
> **App:** `comjuntas-saas/apps/web` · **https://localhost:3000/app/community**

Continuação de [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-26.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-26.md).

---

## O que entregamos nesta sessão

### 1. Fila estilo inbox (triagem escalável)

| Item | Detalhe |
|------|---------|
| UI | Lista compacta à esquerda + detalhe à direita (`QueueInbox`) |
| Navegação | Anterior / Próximo · **Aprovar e próximo** |
| Objetivo | Escalar quando houver muitos pedidos pendentes |

### 2. «O que você já fez» — compacto e paginado

| Item | Detalhe |
|------|---------|
| Preview | 5 linhas compactas (estilo inbox), não cards grandes |
| Ver tudo | Expande na mesma página com scroll (`max-h`) |
| API | `GET /api/community/queue/history?limit=&offset=` |
| Fila | `historyPreview` + `historyTotal` em `/api/community/queue` |

### 3. Meus posts — catálogo completo + paginação na UI

| Item | Detalhe |
|------|---------|
| Backend | `fetchAllRecentMedia()` — busca todos os posts (lotes de 25, até 500) |
| UI | 15 posts/página · **Primeiro** · Anterior · Próxima · **Último** |
| Thumbnails | `media_url` + `children` do carrossel (não só `thumbnail_url` de Reels) |

### 4. Comentários sugeridos v11

Arquivo: `lib/community/suggest-comment.ts` · `COMMENT_GENERATOR_VERSION = 11`.

| Regra | Detalhe |
|-------|---------|
| Maquiagem vs skincare | Post de blush KV → não sugerir «rotina de pele» |
| Golden | Fixture KV Makeup blush em `comment-golden-fixtures.ts` |
| UI | Botão renomeado para **Outro texto** |

### 5. Performance e erros amigáveis

| Item | Detalhe |
|------|---------|
| Gate leve | `assertCommunityUnlockedLight()` no PATCH de aprovar — sem sync IG pesado |
| Fila | `ensurePendingComments` só em pendentes do usuário; queue + members em paralelo |
| Gate UI | Fila renderiza enquanto follow-gate carrega |
| Erros | `user-facing-error.ts` — não expor TypeError na UI |

---

## APIs novas/alteradas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/community/queue` | `historyPreview`, `historyTotal` (substitui `history`) |
| GET | `/api/community/queue/history` | Histórico paginado `{ items, total, hasMore }` |
| GET | `/api/community/my-posts` | Todos os posts + `postsTotal`, `postsTruncated` |

---

## Arquivos principais

| Área | Caminhos |
|------|----------|
| Fila inbox + histórico | `community-client.tsx`, `requests.ts`, `queue/route.ts`, `queue/history/route.ts` |
| Meus posts | `my-posts-client.tsx`, `my-posts/route.ts`, `lib/instagram/graph.ts` |
| Comentários v11 | `suggest-comment.ts`, `comment-golden-fixtures.ts` |
| Performance / erros | `follow-gate.ts`, `community-follow-gate.tsx`, `actions/[id]/route.ts`, `user-facing-error.ts` |

---

## Testes

```powershell
cd apps/web
npm run test:comments
```

---

## Próximo passo

- Push do piloto quando Tatiana pedir.
- Migrar Comunidade para PostgreSQL (`api/` + migrations).
