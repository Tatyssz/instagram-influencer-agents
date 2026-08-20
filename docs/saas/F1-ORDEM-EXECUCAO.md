# F1 — Ordem de execução (revisão 2026-08-20)

> **Decisão:** engajamento mútuo entra **antes** do media kit.  
> **Princípio:** creators reais se apoiam — **não** bot invisível (InstaBarato).

---

## Nova ordem (o que construímos)

| # | Nome | O que a creator vê | Diferença vs InstaBarato |
|---|------|-------------------|--------------------------|
| **1** | Conectar Instagram | Dashboard com números reais | Dados oficiais (Meta API) |
| **1.5** | **Comunidade + engajamento** | Fila de posts das parceiras; aprovar curtir / comentar / seguir | **Você aprova cada ação**; comentário editável; contas reais |
| **2** | Media kit PDF | Gera PDF glow | — |
| **3** | Portfólio luxe | Link público | — |
| **4** | IA + Stripe + visual | Pro completo + cobrança | — |
| **5** | Publicar na internet | Staging / domínio | Só quando 1–4 funcionarem |

---

## Status por etapa

| # | Status | Commit / doc |
|---|--------|----------------|
| **1** | ✅ Concluída 2026-08-20 | `c22b6b0` · [`F1-ETAPA1-SESSAO-2026-08-20.md`](F1-ETAPA1-SESSAO-2026-08-20.md) |
| **1.5** | 🔄 Em andamento | — |
| **2–5** | ⬜ | — |

**Ritual ao fechar cada etapa:** [`RITUAL-FIM-ETAPA.md`](RITUAL-FIM-ETAPA.md)

---

## Como funciona o engajamento (1.5)

```
Parceira B publica Reel
        ↓
Sync detecta post novo (Meta API)
        ↓
Você recebe na fila: preview + sugestão de comentário (IA)
        ↓
Você revisa, marca ☑ curtir ☑ seguir (se quiser), edita o texto
        ↓
Clica "Aprovar e executar"
        ↓
Sistema executa NA SUA CONTA — com limites (ex.: 10/dia, intervalo entre ações)
        ↓
Registro: feito ✓ / falhou / reconectar Instagram
```

**Nunca executa sozinho** sem você ter aprovado. Isso é o oposto de painel SMM.

### Três ações possíveis (todas opcionais por post)

| Ação | Quem decide | Como executa |
|------|-------------|--------------|
| **Curtir** | Você marca ☑ e aprova | Playwright após aprovação |
| **Comentar** | Você edita o texto e aprova | Playwright após aprovação |
| **Seguir** | Você marca ☑ e aprova *(só se ainda não segue)* | Playwright após aprovação |

Seguir tem limite mais baixo que curtir (risco de parecer bot) — regra no produto.

---

## Fases técnicas (por trás)

| Sub-etapa | Entrega |
|-----------|---------|
| **1.5a** | Banco: círculos + fila + ações |
| **1.5b** | Tela Comunidade no app (fila + aprovar) |
| **1.5c** | Sync popula fila quando parceira posta |
| **1.5d** | Autorizar sessão IG para executar |
| **1.5e** | Worker: curtir + comentar + seguir após `approved` |
| **1.5f** | Piloto: 2 creators (ex.: Taty + 1 beta) |

---

## Referência

Detalhes completos: [`../produto/PRODUTO-SAAS-VISAO.md`](../produto/PRODUTO-SAAS-VISAO.md) (fluxo § aprovar → executar)
