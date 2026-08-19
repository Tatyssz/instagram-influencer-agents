# Schema do banco (Postgres)

> **Status:** esqueleto · rascunho completo em [`../produto/PRODUTO-SAAS-VISAO.md`](../produto/PRODUTO-SAAS-VISAO.md)  
> **Atualizado:** 2026-08-19

## Tabelas core

- `users`
- `subscriptions`
- `instagram_accounts`
- `instagram_sessions`
- `media_kits`
- `portfolio_builds`

## Comunidade

- `circles`, `circle_members`
- `engagement_queue`, `engagement_actions`

## Academy

- `courses`, `course_modules`, `course_lessons`
- `course_enrollments`, `lesson_progress`

## Próximo passo

- [ ] Migrations SQL (Alembic) na F0
- [ ] Diagrama ER
