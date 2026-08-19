# Deploy

> **Status:** esqueleto — preencher na F0  
> **Atualizado:** 2026-08-19

## Candidatos

| Componente | Onde |
|------------|------|
| Front (Next.js) | Vercel |
| API (FastAPI) | Railway / Fly.io |
| Postgres | Supabase / Neon |
| Workers | Mesmo host API ou fila separada |
| Assets (PDF/HTML) | S3 / R2 |
| Portfólios públicos | CDN / Netlify por tenant |

## Secrets

- Meta app credentials
- Stripe/MP keys
- Encryption key (tokens IG)
