# F1 etapa 1.5 — Comunidade (sessão 2026-08-26)

> **Status:** 🔄 piloto local — comentários humanos v10 + reprovar/regenerar + testes golden  
> **Commit:** *(comjuntas-saas — ver `git log` após push)*  
> **App:** `comjuntas-saas/apps/web` · **https://localhost:3000/app/community**

Continuação de [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-25.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-25.md) (`541e4dc`).

---

## O que entregamos nesta sessão

### 1. Botão «Reprovar e gerar texto»

| Item | Detalhe |
|------|---------|
| UI | Ao lado de «Aprovar e executar» na fila (`community-client.tsx`) |
| API | `PATCH /api/community/actions/[id]` com `action: "regenerate_comment"` |
| Backend | `regenerateEngagementComment()` — guarda textos rejeitados, gera outro sem aprovar |
| Comportamento | Textarea atualiza na hora; pode repetir até gostar; não executa no Instagram |

### 2. Comentários sugeridos v10 (tom de seguidora)

Arquivo: `lib/community/suggest-comment.ts` · `COMMENT_GENERATOR_VERSION = 10`.

| Regra | Detalhe |
|-------|---------|
| **Proibido** | Pitch de marketing: «Quero conhecer», «Preciso testar», «arrasa demais» |
| **Proibido** | Elogio vazio quando legenda é rica («Que finalização no cabelo!» no post Widi Care) |
| **Proibido** | «Qual produto?» quando legenda já cita produto/marca |
| **Prioridade** | Linha citada na legenda → contexto (pós-química, rotina, fios) → tema |
| **Exemplo** | Widi Care Pré e Pós Química → *«Amei a linha Pré e Pós Química!»* ou *«Amo ver cuidado pós-química!»* |
| **Exemplo** | Só `#ugc #parfum` → pergunta sobre perfume (ok — legenda não nomeia produto) |

Funções novas: `suggestReplacementComment`, `contextualCommentsFromCaption`, `isMarketingComment`, `isValidEngagementComment`.

### 3. IA opt-in (sem custo por padrão)

| Modo | Config |
|------|--------|
| **Regras locais** | Padrão — zero config, zero custo |
| **OpenAI** | `OPENAI_COMMENT_ENABLED=true` + `OPENAI_API_KEY` (`suggest-comment-ai.ts`) |

Wrapper async: `suggestCommentsForMembersAsync` — usado na fila e ao criar pedido.

### 4. Testes golden (legendas reais do piloto)

| Arquivo | Função |
|---------|--------|
| `comment-golden-fixtures.ts` | 3 legendas reais + frases proibidas |
| `suggest-comment.golden.test.mjs` | 12 testes — regressão de tom robótico |

Casos travados:

1. **@tatyzacharias** — Widi Care Pré e Pós Química  
2. **@tatianaugc** — `#ugc #parfum`  
3. **@tatyzacharias** — Phállebeauty Meline + Seduction Woman  

```powershell
cd apps/web
npm run test:comments
```

---

## Arquivos principais (código novo/alterado)

| Área | Caminhos |
|------|----------|
| Reprovar/regenerar | `requests.ts`, `actions/[id]/route.ts`, `community-client.tsx` |
| Comentários v10 | `suggest-comment.ts`, `suggest-comment-ai.ts` |
| Testes golden | `comment-golden-fixtures.ts`, `suggest-comment.golden.test.mjs` |
| Script | `package.json` → `test:comments` |

---

## Bugs / dores corrigidos

| Problema | Correção |
|----------|----------|
| «Quero conhecer a Widi Care!» | Removido gerador de pitch; filtro `isMarketingComment` |
| «Que finalização no cabelo!» em legenda rica | Contextual + bloqueio de elogio genérico |
| Sem como pedir outra sugestão | Botão «Reprovar e gerar texto» |
| Medo de regressão | Fixtures golden + `npm run test:comments` |
| «Que tratamento caprichado!» bloqueado | Falso positivo em `/caprichad/` corrigido |

---

## Como testar

1. `cd apps/web && npm run dev` → https://localhost:3000/app/community  
2. Abrir item pendente → se comentário não servir → **Reprovar e gerar texto**  
3. Editar se quiser → **Aprovar e executar**  
4. `npm run test:comments` — deve passar 12/12  

---

## Referências

- Resumo local: [`comjuntas-saas/docs/COMUNIDADE-PILOTO.md`](../../../comjuntas-saas/docs/COMUNIDADE-PILOTO.md)  
- Regras: [`COMUNIDADE-REGRAS.md`](COMUNIDADE-REGRAS.md)  
- Sessão anterior: [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-25.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-25.md)
