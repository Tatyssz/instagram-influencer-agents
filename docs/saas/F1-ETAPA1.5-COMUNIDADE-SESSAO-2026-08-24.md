# F1 etapa 1.5 — Comunidade (sessão 2026-08-24)

> **Status:** 🔄 piloto funcional local — follow mútuo + fila + alertas de unfollow  
> **Commit:** `bc7c457` (comjuntas-saas)  
> **App:** `comjuntas-saas/apps/web` · **https://localhost:3000/app/community**

---

## O que entregamos nesta sessão

### 1. Follow mútuo do círculo piloto (Beauty Creators)

- Círculo piloto: **todas as contas Instagram conectadas** entram automaticamente (`lib/community/circle.ts`).
- **Gate de follow:** ao entrar na Comunidade, a creator precisa **aprovar** seguir as parceiras (uma vez).
- **Execução automática** após aprovação — a usuária **não** precisa clicar “Tentar seguir de novo” (salvo falha persistente).
- **Login Instagram pelo Chrome** (Playwright, perfil persistente por conta) — necessário porque **2FA não funciona** só pela API privada.
- Follow via **navegador headless** quando há sessão Chrome (`lib/instagram/browser-follow.ts`), contornando HTTP 429 da API.

### 2. Fluxo Chrome (por conta)

1. Entrar pelo Chrome  
2. Login na janela (senha + 2FA se pedir)  
3. “Salvar informações?” → **Agora não**  
4. Voltar ao ComJuntas → **Concluí login**  
5. **Fechar** a janela do Instagram  
6. **Aprovar seguir** (se ainda pendente)  
7. Sistema segue sozinho (fila + intervalo entre ações)

### 3. Detecção de unfollow manual

- Se a creator **deixa de seguir** uma parceira no Instagram, o sistema:
  1. **Detecta** (API + fallback leitura do botão no Chrome: Seguir / Seguir de volta / Seguindo)
  2. **Refaz o follow** automaticamente (recoloca job na fila)
  3. **Notifica a ADM** (log + `/admin` + e-mail opcional via Resend)
  4. **Mostra alerta vermelho** para a usuária (até clicar **Entendi**)
  5. **Mostra verde “Follows do círculo em dia”** quando o follow já foi refeito (mesmo com alerta vermelho aberto)

**Texto do alerta (usuária):**

- “O follow **foi refeito** automaticamente.”
- “Em caso de recorrência, você pode ser **banida** da comunidade **sem devolução de valores**.”
- Vários unfollows pendentes aparecem **na mesma lista** (@a, @b e @c).

### 4. UI Comunidade

| Tela | Rota | Função |
|------|------|--------|
| Fila para engajar | `/app/community` | Pedidos de engajamento das parceiras |
| Meus posts | `/app/community/my-posts` | Marcar Reel/post para pedir engajamento (1/dia piloto) |
| Admin alertas | `/admin` | Lista unfollows manuais detectados |

**Banners:**

- Verde — follows em dia  
- Branco — seguindo contas / login Chrome  
- Vermelho — infração de regra (unfollow manual)

---

## Contas piloto (teste local)

| Instagram | E-mail Clerk | Clerk ID |
|-----------|--------------|----------|
| `@tatianaugc` | `taty_ssz@hotmail.com` | `user_3ICGRI0b6cMo0ERi6sKQOVEkdiY` |
| `@tatyzacharias` | `ugctatianazacharias@gmail.com` | `user_3IBT8GZcQKhrUKVqmLHCkVhcZqV` |

**Admin:** `ugctatianazacharias@gmail.com` → `/admin`

---

## Onde os dados ficam hoje (piloto — **sem Postgres**)

Tudo em arquivos JSON em `apps/web/.data/` ( **não commitar** ):

| Pasta / arquivo | Conteúdo |
|-----------------|----------|
| `.data/instagram/user_*.json` | Conta IG conectada + quem entra no círculo |
| `.data/instagram/web-session/*.json` | Cookies API (criptografados) |
| `.data/instagram/browser/<username>/` | Perfil Chrome Playwright |
| `.data/community/follow-gate.json` | Obrigações de follow (pending/approved) |
| `.data/community/follow-jobs.json` | Fila de execução de follows |
| `.data/community/unfollow-violations.json` | Unfollows manuais + recorrência |
| `.data/community/engagement-requests.json` | Pedidos de engajamento em posts |

**Login:** Clerk (nuvem).  
**Postgres:** existe no `api/` (Alembic) mas **não está ligado** ao app Comunidade ainda.

---

## Arquivos principais (código)

| Área | Caminhos |
|------|----------|
| Círculo | `lib/community/circle.ts` |
| Gate + aprovar | `lib/community/follow-gate.ts`, `follow-gate-panel.tsx` |
| Fila follow | `lib/community/follow-jobs.ts` |
| Unfollow + alertas | `lib/community/unfollow-violations.ts`, `lib/notifications/admin-unfollow-alert.ts` |
| Chrome login | `browser-session-setup.tsx`, `browser-session-manager.ts` |
| Follow browser | `lib/instagram/browser-follow.ts`, `follow-runner.ts` |
| UI | `community-client.tsx`, `follow-progress-banner.tsx`, `unfollow-violation-banner.tsx` |
| APIs | `/api/community/follow-gate`, `/api/community/unfollow-violation`, `/api/community/follow-retry` |

---

## Variáveis de ambiente (`.env.local`)

```env
ADMIN_EMAILS=ugctatianazacharias@gmail.com

# Opcional — e-mail automático de unfollow para ADM
RESEND_API_KEY=
RESEND_FROM=ComJuntas <onboarding@resend.dev>

# Instagram OAuth + Clerk (já existentes)
```

Ver `apps/web/.env.example`.

---

## Bugs corrigidos nesta sessão

| Problema | Causa | Correção |
|----------|-------|----------|
| Follow falhava com “Botão Seguir não encontrado” | Botão era **Seguir de volta**; busca só no `<header>` | Regex + busca em `main` e página inteira |
| Unfollow manual não refazia follow | Jobs ficavam `done`; API atrasada | `requeueUnfollowedDoneJobs` + check Chrome |
| Alerta não aparecia na tela | API lenta / campo não chegava no client | GET dedicado `/api/community/unfollow-violation` + merge no client |
| Verde “em dia” sumia com alerta vermelho | Condição escondia um ou outro | Mostrar **os dois** quando follow já concluído |

---

## O que ainda falta (etapa 1.5 completa)

- [ ] Migrar `.data/community/*` → **PostgreSQL** (círculos, membros, fila, violações)
- [ ] Lista explícita de membros do círculo (hoje = “quem conectou IG”)
- [ ] Execução Playwright de **curtir + comentar** após aprovação na fila
- [ ] Sync automático populando fila quando parceira posta (Meta API)
- [ ] Cotas Pro (1 pedido/dia, 10 ações/dia) + reciprocidade
- [ ] Deploy staging / domínio

---

## Como testar de novo

1. `cd apps/web && npm run dev` → https://localhost:3000  
2. Login com conta piloto → **Comunidade**  
3. Unfollow manual no Instagram → **F5** no ComJuntas  
4. Esperar: alerta vermelho + verde “em dia” + follow refeito  
5. ADM: https://localhost:3000/admin  

---

## Referências

- Regras produto: [`COMUNIDADE-REGRAS.md`](COMUNIDADE-REGRAS.md)  
- Ordem F1: [`F1-ORDEM-EXECUCAO.md`](F1-ORDEM-EXECUCAO.md)  
- Repo: [`comjuntas-saas/README.md`](../../../comjuntas-saas/README.md)
