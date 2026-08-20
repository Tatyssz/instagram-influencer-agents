# Política de trial — ComJuntas (DEC-04)

> **Status:** fechado · 2026-08-19  
> **Decisão:** **Trial 7 dias com limitações** (Start e Pro) · plano Plus (futuro) sem trial  
> **Planos:** [`PLANOS-LAUNCH.md`](PLANOS-LAUNCH.md)

---

## Regra geral

| Item | Política |
|------|----------|
| **Duração** | 7 dias corridos a partir do **primeiro sync** bem-sucedido |
| **Planos com trial** | Start e Pro |
| **Plus** *(futuro)* | Sem trial — quando existir |
| **Cartão** | **Obrigatório** no cadastro (cobrança automática ao fim do trial se não cancelar) |
| **Cancelamento** | A qualquer momento no painel · sem cobrança se cancelar antes do dia 7 |
| **Conversão** | Dia 7 → cobra plano escolhido (Start R$ 69 ou Pro R$ 129) |
| **Re-trial** | 1 trial por CPF/e-mail/IG — bloqueio por `instagram_user_id` |

---

## Limitações durante o trial

### ComJuntas Start (trial)

| Recurso | Trial | Após pagar |
|---------|-------|------------|
| Conectar Instagram | ✅ 1 conta | ✅ |
| Sync | **1×** (máx. 30 posts) | 1×/semana |
| Media kit PDF | **Preview HTML** com marca d'água · **sem download PDF** | 1×/mês PDF final |
| Portfólio web | **Não publica** — só preview interno (5 peças) | Link básico público |
| Relatório IA | ❌ | ❌ |
| Cursos | ❌ | ❌ *(avulso ok)* |
| Comunidade | ❌ | ❌ |

### ComJuntas Pro (trial)

| Recurso | Trial | Após pagar |
|---------|-------|------------|
| Conectar Instagram | ✅ 1 conta | ✅ |
| Sync | **1×** (máx. 50 posts) | 1×/dia |
| Media kit PDF | **1 PDF** com footer *“Versão trial ComJuntas”* | Fair use 5×/mês |
| Portfólio web | **Publicado** · slug trial · **máx. 12 peças** · badge *Trial* no header | Luxe completo |
| Relatório IA | **Resumo** (3 insights, sem benchmarks) | Relatório completo mensal |
| Cursos | ❌ | ✅ **C1–C5** (F2) |
| Comunidade | ❌ | ✅ círculo + fila (F3) |

---

## O que NÃO entra no trial (anti-abuso)

- Segunda conta Instagram no mesmo trial  
- Regenerar kit ilimitado  
- Export PDF final sem watermark (Start)  
- Segundo sync antes de pagar  
- **Comunidade e cursos** (mesmo no Pro — só após assinar)  
- Fila de engajamento / execução automática (Plus / F4, futuro)  
- Download em lote de assets do portfólio  

---

## Fluxo billing (implementação F1)

```
Cadastro → escolhe Start ou Pro trial
    → cartão (Stripe/MP)
    → OAuth Instagram
    → primeiro sync (inicia contagem 7 dias)
    → usa recursos com limites acima
    → dia 5: e-mail "trial acaba em 2 dias"
    → dia 7: cobrança automática OU conta read-only se cartão falhar
```

### Estados da assinatura

| Status | Comportamento |
|--------|----------------|
| `trialing` | Limites trial ativos |
| `active` | Plano pago — limites completos do plano |
| `past_due` | Cartão falhou — 3 dias grace · só leitura |
| `canceled` | Fim do período pago · export dados 30 dias (LGPD) |

### Impacto no gateway (DEC-05 ✅)

- **Stripe:** `subscription` com `trial_period_days: 7` + cartão no Checkout  
- Detalhes: [`PAYMENT-GATEWAY.md`](../saas/PAYMENT-GATEWAY.md)

---

## UX — mensagens-chave

**Banner no app (trial):**  
*Você está no trial Pro · 4 dias restantes · [Assinar agora]*

**Start — bloqueio PDF:**  
*No trial você vê o preview. Assine para baixar o PDF final.*

**Pro — footer PDF trial:**  
*Gerado no trial ComJuntas · Assine para remover esta marca.*

---

## Métricas

| Métrica | Meta F1 |
|---------|---------|
| Trial → pago (Start) | ≥ 25% |
| Trial → pago (Pro) | ≥ 35% |
| Cancelamento antes do dia 7 | monitorar (> 60% = preço ou valor trial baixo) |

---

## Próximo passo

**DEC-07** — wireframe F1 (checkout Stripe no onboarding).
