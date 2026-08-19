# ADR 001 — Stack inicial

> **Status:** proposto  
> **Data:** 2026-08-19

## Contexto

SaaS ComJuntas reutiliza scripts Python do toolkit; precisa front app+admin e billing.

## Decisão (proposta)

- **Front:** Next.js + shadcn/ui
- **API:** FastAPI
- **DB:** Postgres
- **Auth:** Clerk ou Supabase Auth

## Consequências

- Workers Python compartilham código com `instagram-influencer-agents`
- Monorepo ou lib Python publicada internamente

## Alternativas consideradas

- Django full-stack — descartado (front separado preferido)
- Streamlit admin — descartado (UX limitada)
