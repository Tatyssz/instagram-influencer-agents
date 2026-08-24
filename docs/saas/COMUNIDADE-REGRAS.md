# Comunidade — regras de produto (DEC-2026-08-20)

> **Decisões Tatiana · atualizado 2026-08-20**  
> Complementa [`F1-ORDEM-EXECUCAO.md`](F1-ORDEM-EXECUCAO.md) e [`../produto/PLANOS-LAUNCH.md`](../produto/PLANOS-LAUNCH.md)

---

## Decisões fechadas

| # | Regra |
|---|--------|
| 1 | **Seguir todas:** ao entrar no círculo, premissa fixa — sistema segue todas as creators do grupo (aprovação **uma vez**, em lote no onboarding). |
| 2 | **Quais Reels recebem engajamento:** **Opção A** — a creator marca no app quais posts pedem engajamento (`☑ Pedir engajamento da comunidade`). Nada entra na fila das parceiras sem isso. |
| 3 | **Admin:** cria círculo, convida, modera — **não** escolhe post por post. |
| 4 | **Execução:** parceiras **aprova** curtir/comentar (nunca automático sem aprovação). |
| 5 | **Unfollow manual:** proibido deixar de seguir integrante do círculo. Sistema **refaz o follow** automaticamente. Usuária recebe alerta; ADM é notificada. **Recorrência → banimento sem devolução.** |

---

## Unfollow manual (implementado 2026-08-24)

| O quê | Comportamento |
|-------|----------------|
| Detecção | Ao abrir Comunidade (API + leitura do botão no Chrome) |
| Follow | Refeito automaticamente (fila Playwright) |
| Usuária | Banner vermelho até clicar **Entendi**; banner verde “em dia” quando follow já refeito |
| ADM | Lista em `/admin` + log; e-mail opcional (`RESEND_API_KEY`) |
| Vários alvos | Todos os unfollows pendentes na mesma mensagem |
| Dados | `.data/community/unfollow-violations.json` (piloto) |

Detalhe técnico: [`F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md`](F1-ETAPA1.5-COMUNIDADE-SESSAO-2026-08-24.md)

## Dois lados da moeda (limites = negócio)

A comunidade tem **dois tipos de limite** — confundir os dois quebra o produto.

| Lado | Pergunta | Quem paga Pro |
|------|----------|----------------|
| **Pedir** | Quantos posts **eu** posso marcar “quero engajamento” por dia? | Creator que **publicou** |
| **Dar** | Quantas curtidas/comentários **eu** posso **aprovar e executar** nos posts das parceiras por dia? | Creator que **engaja** |

**Analogia:** pedir = “colocar na vitrine do círculo”. Dar = “ir lá apoiar as parceiras”.

---

## Limites propostos — launch (Pro R$ 129)

> **Estes números são só para o início** (piloto + primeiras pagantes).  
> Visão: **milhares de usuárias** — via **muitos círculos**, não um grupo gigante.

| Limite | Pro (launch) | Por quê |
|--------|--------------|---------|
| **Pedidos de engajamento** | **1 post/dia** | Evita spam no círculo; 1 Reel “oficial” por dia é realista para UGC; diferencia valor do Pro |
| **Executar (curtir + comentar)** | **até 10 ações/dia** | Protege conta Instagram; cobre círculo ~10–15 pessoas com 1 pedido/dia cada |
| **Seguir (onboarding + novas membros)** | **fora da cota diária** de engajamento | Evento raro (entrada no círculo); intervalo 3–5 min entre follows |
| **Círculos** | **1** | Já definido em PLANOS-LAUNCH |
| **Tamanho do círculo** | **5–20 creators** | Qualidade > volume |

### Escala — milhares de usuárias

| Início | Escala |
|--------|--------|
| 1 círculo piloto (~10 pessoas) | **Centenas de círculos** (beauty, hair, fitness…) |
| 1 pedido/dia · 10 ações/dia | Cotas **maiores por plano** ou **dinâmicas** por tamanho do círculo |
| Moderação manual | Admin + score automático + match por nicho |

**1.000 usuárias ≠ 1 grupo de 1.000.**  
**1.000 usuárias ≈ 50–100 círculos de 10–20** — engajamento real, particionado.

### Reciprocidade (regra de ouro)

Quem **pede** engajamento hoje deve **dar** engajamento nas filas das parceiras (score de reciprocidade). Quem só pede e nunca aprova/executa → aviso → pausa ou remoção do círculo.

---

## Planos e dinheiro

| Plano | Comunidade | Pedir engajamento | Executar |
|-------|------------|-------------------|----------|
| **Start R$ 69** | ❌ | — | — |
| **Pro R$ 129** | ✅ 1 círculo | **1 post/dia** | **10 ações/dia** |
| **Plus** *(futuro)* | 2 círculos? | **2–3 posts/dia**? | **20 ações/dia**? | *Upsell quando existir* |

**Trial:** comunidade **fora** do trial ([`TRIAL-POLICY.md`](../produto/TRIAL-POLICY.md)) — só paga Pro ativo entra no círculo.

**Copy de venda Pro:**  
*“1 pedido de engajamento por dia no seu Reel + fila organizada para apoiar suas parceiras — sem grupo caótico no WhatsApp.”*

---

## Fluxo completo (referência)

```
ENTRADA NO CÍRCULO
  → Aceita regra “seguir todas”
  → Aprova lote único de follows
  → Sistema executa follows (intervalo)

PUBLICOU REEL
  → Sync lista posts
  → Creator marca ☑ “Pedir engajamento” (máx. 1/dia no Pro)
  → Entra na fila das parceiras

PARCEIRA
  → Vê na fila Comunidade
  → Aprova curtir + comentário (editável)
  → Sistema executa (conta na cota de 10/dia)

SCORE
  → Pediu vs deu → reciprocidade
```

---

## O que construir (ordem técnica)

1. ✅ Onboarding círculo + follow em lote — [`follow-gate.ts`](../../comjuntas-saas/apps/web/lib/community/follow-gate.ts) · login Chrome · fila Playwright  
2. ✅ Unfollow manual → refollow + alertas — [`unfollow-violations.ts`](../../comjuntas-saas/apps/web/lib/community/unfollow-violations.ts)  
3. 🔄 Tela **Meus posts** — marcar pedido (com contador 1/dia)  
4. 🔄 Fila Comunidade — só posts pedidos (estrutura pronta; sync pendente)  
5. ⬜ Cotas por plano + reciprocidade  
6. ⬜ Execução Playwright curtir/comentar (1.5e)  
7. ⬜ Postgres no lugar de `.data/community/*.json`

---

## Pendente (decidir depois — escala)

- Plus: 2 ou 3 pedidos/dia?  
- Reset da cota: meia-noite horário Brasil?  
- Post extra avulso (ex.: R$ 9 por pedido adicional)? — monetização extra  
- **Revisão de cotas** quando passar de ~100 creators ativas (métrica, não data fixa)  
- Match automático em círculos por nicho + tier de seguidores  
- Limite dinâmico de ações/dia baseado no tamanho real do círculo (ex.: `min(10, membros_ativos - 1)` no launch → fórmula maior no Plus)
