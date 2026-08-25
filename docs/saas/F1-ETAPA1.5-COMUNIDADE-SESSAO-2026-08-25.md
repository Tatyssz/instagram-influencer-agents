# F1 etapa 1.5 — Comunidade (sessão 2026-08-25)

> **Status:** 🔄 piloto local — fila de engajamento + execução IG + sininho + comentários contextuais  
> **Commit:** `541e4dc` (comjuntas-saas)  
> **App:** `comjuntas-saas/apps/web` · **https://localhost:3000/app/community**

Continuação de [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md) (`bc7c457`, `8d637ed`).

---

## O que entregamos nesta sessão

### 1. Fila para engajar (UI + regras)

| Regra | Implementação |
|-------|----------------|
| **Curtir** | Sempre marcado e **desabilitado** (curtida automática ao aprovar) |
| **Seguir** | Removido da fila de engajamento por post (follow só no gate do círculo) |
| **Ignorar pedido** | Bloqueado — cada pedido precisa ser aprovado e executado |
| **Comentário** | Editável antes de «Aprovar e executar» |

### 2. Execução real no Instagram

- Após aprovação: **curtir + comentar** na conta da parceira que aprovou.
- Caminho: API web privada (`private-api.ts`) → fallback **Playwright** (`browser-engagement.ts`, `engagement-runner.ts`).
- Execução **assíncrona** (não trava a UI): status `executing` → poll a cada 3s → `done` ou `failed`.
- Timeout **90s**; recuperação de jobs `executing` órfãos após 90s.
- Erro exibido na fila + botão **«Tentar de novo»**.

### 3. Sininho de avisos (header)

- Ícone **sempre visível** ao lado do e-mail.
- **Badge vermelho** só com aviso **não lido**.
- Painel: mensagem de pedido pendente + **«Abrir Fila para engajar»** + **«Excluir aviso»**.
- «Excluir aviso» = dismiss do lembrete (pedido **permanece na fila**).
- Novo pedido → badge volta (`notification-read.json` + `markEngagementRequestUnreadForRecipients`).
- API: `GET/POST /api/community/notifications`.

### 4. Comentários sugeridos (v7)

Arquivo: `lib/community/suggest-comment.ts` · `COMMENT_GENERATOR_VERSION = 7`.

| Regra | Detalhe |
|-------|---------|
| Tom | Seguidora no Instagram — curto, casual |
| Contexto | Hashtags (`#parfum`) e produtos citados na legenda |
| Proibido | «UGC caprichado», «conteúdo», elogio vazio («Tá lindo!») quando há assunto |
| Proibido | Perguntar «qual produto?» quando a legenda **já nomeia** o produto |
| Exemplo | Legenda com Serum Meline → *«Amei o Serum Meline!»* |
| Exemplo | Só `#ugc #parfum` → *«Me passa o nome do perfume!»* |
| Distinto | Cada parceira do círculo recebe comentário diferente no mesmo pedido |

Regeneração automática de pendentes quando muda `COMMENT_GENERATOR_VERSION` ou detecta comentário robótico/genérico.

### 5. Meus posts — status do pedido

| Badge | Quando |
|-------|--------|
| **Na fila** (amarelo) | Pedido criado; parceiras ainda não concluíram todas |
| **Concluído** (verde) | Todas as parceiras executaram (`status === done`) |

API `GET /api/community/my-posts` → `engagementStatus`: `none` | `in_queue` | `completed`.

### 6. Correções de UX / auth

- `fetchCommunityApi` com retry (evita falso «Conecte Instagram» por race do Clerk).
- Comunidade não marca mais todos os avisos como lidos ao abrir a página.
- Gate follow: mensagem honesta quando sessão ainda carrega.

---

## Contas piloto (atualizado)

| Instagram | E-mail Clerk | Clerk ID |
|-----------|--------------|----------|
| `@tatianaugc` | `taty_ssz@hotmail.com` | `user_3ICGRI0b6cMo0ERi6sKQOVEkdiY` |
| `@tatyzacharias` | `ugctatianazacharias@gmail.com` | `user_3IBT8GZcQKhrUKVqmLHCkVhcZqV` |
| `@favoritosdataty` | *(conta piloto)* | `user_3IBU3bYU617dZm6y6a0wja9Mbu3` |

**Admin:** `ugctatianazacharias@gmail.com`

---

## Dados locais (`.data/` — não commitar)

| Arquivo | Conteúdo |
|---------|----------|
| `community/engagement-requests.json` | Pedidos + ações (`pending` / `executing` / `done` / `failed`) |
| `community/notification-read.json` | Avisos lidos/dismissed por usuária |
| `instagram/web-session/*.json` | Sessão web IG por @ |

---

## Arquivos principais (código novo/alterado)

| Área | Caminhos |
|------|----------|
| Fila + approve | `lib/community/requests.ts`, `app/api/community/actions/[id]/route.ts` |
| Comentários | `lib/community/suggest-comment.ts` |
| Notificações | `lib/community/notification-read.ts`, `components/community-notifications-bell.tsx`, `app/api/community/notifications/` |
| Execução IG | `lib/instagram/engagement-runner.ts`, `browser-engagement.ts`, `private-api.ts` |
| UI fila | `app/app/community/community-client.tsx` |
| Meus posts | `app/app/community/my-posts/my-posts-client.tsx`, `app/api/community/my-posts/route.ts` |
| Fetch client | `lib/community/client-fetch.ts` |

---

## Bugs corrigidos nesta sessão

| Problema | Correção |
|----------|----------|
| Aprovar só gravava `approved`, não curtia/comentava | Runner IG + status `done`/`failed` |
| Sininho sumia ou não avisava novo pedido | Sem auto-mark na Comunidade; unread por request id |
| «Excluir aviso» não funcionava | Aviso ≠ fila; painel usa snapshot até dismiss |
| Comentários genéricos / «UGC caprichado» | Gerador v7 + refresh de pendentes |
| «Qual produto usou?» com produto na legenda | Prioriza menção ao produto; filtra perguntas vazias |
| UI travava em «Executando no Instagram…» | Execução async + poll; import do runner corrigido |
| Falso «Conecte Instagram» | Retry Clerk + gate honesto |

---

## O que ainda falta (etapa 1.5 completa)

- [ ] Migrar `.data/community/*` → **PostgreSQL**
- [ ] Sync automático populando fila quando parceira posta (Meta API)
- [ ] Estabilidade execução IG em staging (sessões, rate limit)
- [ ] Cotas Pro formais (10 ações/dia) + reciprocidade
- [ ] Deploy staging

---

## Como testar

1. `cd apps/web && npm run dev` → https://localhost:3000  
2. Conta A → **Meus posts** → pedir engajamento (1/dia)  
3. Conta B → sininho com badge → **Fila para engajar** → editar comentário → **Aprovar e executar**  
4. Verificar no Instagram se curtiu/comentou; na fila → `done` ou erro + **Tentar de novo**  
5. Conta A → **Meus posts** → badge **Concluído** quando todas executarem  

---

## Referências

- Resumo local: [`comjuntas-saas/docs/COMUNIDADE-PILOTO.md`](../../../comjuntas-saas/docs/COMUNIDADE-PILOTO.md)  
- Regras: [`COMUNIDADE-REGRAS.md`](COMUNIDADE-REGRAS.md)  
- Convites turma: [`DEC-11-TURMA-FUNDADORA-CONVITE.md`](../produto/DEC-11-TURMA-FUNDADORA-CONVITE.md)
