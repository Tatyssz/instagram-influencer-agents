# Arquitetura SaaS

> **Status:** esqueleto  
> **Atualizado:** 2026-08-19

```
[Next.js]     marketing + app + admin
     ↓
[FastAPI]     auth, billing, tenants, jobs
     ↓
[Workers]     sync IG, mediakit, IA, Playwright
     ↓
[Postgres]    users, subscriptions, …
     ↓
[S3/R2]       PDF, HTML, assets
     ↓
[CDN]         portfólios públicos
```

## Stack candidata

| Camada | Tecnologia |
|--------|------------|
| Front | Next.js 14+, shadcn/ui |
| API | Python FastAPI |
| DB | Postgres |
| Filas | Redis + Celery |
| Auth | Clerk ou Supabase |
| Pagamento | **Stripe** (F1) · MP PIX cursos (F2 opcional) — [`PAYMENT-GATEWAY.md`](saas/PAYMENT-GATEWAY.md) |

Ver também: [`SCHEMA-DB.md`](SCHEMA-DB.md), [`../produto/PRODUTO-SAAS-VISAO.md`](../produto/PRODUTO-SAAS-VISAO.md)
