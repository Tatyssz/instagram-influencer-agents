# F1 — Etapa 1: Conectar Instagram + Dashboard (2026-08-20)

> **Para:** Tatiana · **Repo:** `comjuntas-saas` (local)  
> **Commit:** `c22b6b0` — *Initial commit: ComJuntas SaaS through Instagram connect (F0 + etapa 1)*

---

## Critério de saída (atingido)

- [x] Creator conecta Instagram via OAuth (Meta API)
- [x] Dashboard mostra dados reais (seguidores, posts, alcance, views 28d)
- [x] Perfil no dashboard (foto, nome, @, bio)
- [x] Fluxo em nova aba + cancelamento tratado com copy profissional
- [x] Testado com @tatyzacharias
- [x] Commit local + docs atualizados

**Fora desta etapa (depois):** visual luxe/glow, gráficos, preview de posts, Postgres em produção.

---

## O que fizemos

### Meta / OAuth

- App **Taty Manager** (Instagram App ID no `.env.local`)
- Redirect: `https://localhost:3000/api/instagram/callback`
- Dev server: `npm run dev` → **HTTPS** (`--experimental-https`)

### Telas e APIs

| Peça | Caminho |
|------|---------|
| Conectar | `/app/connect-instagram` |
| Dashboard | `/app` |
| Callback OAuth | `/api/instagram/callback` |
| Sync | `/api/instagram/sync` |
| Cancelamento | `/oauth-cancelled` |

### UX (decisões Tatiana)

- Instagram abre em **outra aba**; ComJuntas permanece aberta
- Textos **profissionais** e **honestos** (leitura agora; engajamento depois, com aprovação)
- Dashboard: cabeçalho de perfil + seções “Sua conta” e “Desempenho · 28 dias”

### Dados de teste (@tatyzacharias, 2026-08-20)

- Seguidores: 32.450 · Posts: 835 · Alcance 28d: 52 · Views 28d: 107

---

## Arquivos principais (código)

```
apps/web/lib/instagram/     config, graph, sync, storage
apps/web/app/api/instagram/ connect, callback, sync, disconnect
apps/web/app/app/dashboard-client.tsx
apps/web/app/app/connect-instagram/
```

Dados por usuária: `apps/web/.data/instagram/` (gitignored).

---

## Lições (não-dev)

1. **Preview do Cursor** costuma dar tela branca com HTTPS local — usar **Chrome/Edge**.
2. **Ctrl + Shift + R** recarrega sem cache.
3. Cancel no Instagram às vezes mostra tela da Meta — não controlamos; ComJuntas fica na outra aba.

---

## Próxima etapa

**F1 etapa 1.5 — Comunidade + engajamento mútuo** (fila + aprovar curtir/comentar/seguir).

Ver [`F1-ORDEM-EXECUCAO.md`](F1-ORDEM-EXECUCAO.md), [`RITUAL-FIM-ETAPA.md`](RITUAL-FIM-ETAPA.md).
