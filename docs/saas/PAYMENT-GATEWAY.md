# Gateway de pagamento — ComJuntas (DEC-05)

> **Status:** fechado · 2026-08-19  
> **Decisão:** **Stripe (principal no F1)** · **Mercado Pago PIX (F2+, cursos avulsos)**  
> **Planos / trial:** [`PLANOS-LAUNCH.md`](../produto/PLANOS-LAUNCH.md) · [`TRIAL-POLICY.md`](../produto/TRIAL-POLICY.md)

---

## Decisão

| Fase | Gateway | Uso |
|------|---------|-----|
| **F1** | **Stripe** | Assinaturas Start/Pro · trial 7 dias · webhooks · portal do cliente |
| **F2+** | **Stripe** | Checkout one-time dos cursos C1–C5 |
| **F2+** *(opcional)* | **Mercado Pago** | **PIX** para compra avulsa de curso (quem não quer cartão) |
| **Futuro** | Avaliar MP | Assinatura recorrente via MP só se churn por “não tenho cartão internacional” |

**Não fazer no F1:** integrar dois gateways de assinatura em paralelo (complexidade dobrada).

---

## Por que Stripe no F1

| Critério | Stripe | Mercado Pago |
|----------|--------|--------------|
| Assinatura + **trial 7d** com cartão upfront | ✅ Billing nativo (`trial_period_days`) | ⚠️ Preapproval; trial mais trabalhoso |
| **Um** checkout assinatura + curso avulso | ✅ Products + Prices + Checkout | Dois fluxos (preapproval vs preference) |
| Webhooks (`active`, `past_due`, `canceled`) | ✅ Mature | ✅ Existe, modelo diferente |
| Portal “gerenciar assinatura” | ✅ Customer Portal | Limitado |
| Docs + SDK Next.js | ✅ Excelente | OK |
| BRL + cartão BR | ✅ | ✅ |
| **PIX** assinatura mensal | ❌ | ✅ |
| PIX compra única (curso) | ❌ *(ou Stripe sem PIX)* | ✅ Alta conversão BR |

**Conclusão:** Stripe cobre **90% do F1–F2** com uma integração. MP entra depois como **PIX para curso avulso**, não como segunda assinatura.

---

## Produtos Stripe (nomenclatura)

| Product ID (ex.) | Tipo | Preço |
|------------------|------|-------|
| `comjuntas_start` | Recurring monthly | R$ 69 |
| `comjuntas_pro` | Recurring monthly | R$ 129 |
| `course_c1` … `course_c5` | One-time | ver PLANOS-LAUNCH |
| `bundle_c1_c3` | One-time | R$ 447 |

**Trial:** mesmo Price com `trial_period_days: 7` no subscription create · `payment_behavior: default_incomplete` ou cartão obrigatório no Checkout (`payment_method_collection: always`).

---

## Fluxo técnico (F1)

```
Landing → Stripe Checkout (mode: subscription, plan Start ou Pro)
    → trial 7 dias (contagem interna também após 1º sync — ver TRIAL-POLICY)
    → webhook checkout.session.completed → user.plan = trialing
    → webhook customer.subscription.updated → active | past_due | canceled
    → Customer Portal link em "Minha conta"
```

**Variáveis de ambiente (staging/prod):**

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_START=price_...
STRIPE_PRICE_PRO=price_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

---

## Mercado Pago (F2 — PIX curso avulso)

- **Quando:** primeiro curso avulso no ar (F2-01+)  
- **Escopo:** somente `mode: payment` (Preference API) · **não** assinatura  
- **Motivo:** creator iniciante costuma preferir PIX em compra única R$ 127–447  

Assinatura ComJuntas **permanece Stripe** até dados provarem necessidade de MP recorrente.

---

## Conta e sandbox (ação Taty antes F1 billing)

| Passo | Responsável | Quando |
|-------|-------------|--------|
| Criar conta [Stripe](https://dashboard.stripe.com/register) | Taty | Antes F1-08 |
| Ativar **modo teste** + copiar keys | Taty | F1-08 |
| Criar Products/Prices teste (Start, Pro) | Dev | F1-08 |
| Stripe CLI ou Dashboard → webhook endpoint staging | Dev | F1-08 |
| Conta MP *(opcional)* | Taty | F2 se PIX curso |

**Cartões teste Stripe:** `4242 4242 4242 4242` · qualquer CVC/futuro.

---

## Impacto nos cards

| Card | Gateway |
|------|---------|
| F1-08 Billing Stripe | Stripe Checkout + webhooks |
| F1-09 Trial limits | Flags no DB + Stripe `trialing` |
| F2-03 Checkout curso avulso | Stripe Payment first |
| F2-04 PIX curso *(opcional)* | Mercado Pago |

---

## Próximo passo

**DEC-07** — wireframe F1 (onboarding com passo “Escolher plano → Stripe Checkout”).
