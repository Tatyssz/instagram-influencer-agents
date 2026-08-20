# Documentação do projeto — índice mestre

> **Repositório:** [`Tatyssz/instagram-influencer-agents`](https://github.com/Tatyssz/instagram-influencer-agents)  
> **Pasta principal:** `docs/` (esta pasta)  
> **Atualizado:** 2026-08-19

Este arquivo é o **mapa**. Qualquer doc novo entra aqui na lista antes (ou logo depois) de ser criado.

---

## Estrutura de pastas

```
docs/
├── README.md                         ← VOCÊ ESTÁ AQUI
├── produto/
│   ├── PRODUTO-SAAS-VISAO.md         ← visão SaaS (negócio, fases, planos)
│   ├── PERSONA-01.md                 ← persona #1 (DEC-02) ✅
│   ├── PLANOS-LAUNCH.md              ← planos e preços (DEC-03) ✅
│   └── TRIAL-POLICY.md               ← trial 7 dias (DEC-04) ✅
├── toolkit/
│   ├── README.md
│   ├── CURSO-PASSO-A-PASSO.md        ← curso / Academy C1–C3
│   └── MEDIA-KIT-CURADORIA.md        ← curadoria portfólio case Taty
└── saas/
    ├── ENTREGAS-FASES.md             ← esqueleto (preencher na F0)
    ├── FRONT-TELAS.md                 ← wireframes F1 (DEC-07) ✅
    ├── ARQUITETURA.md
    ├── SCHEMA-DB.md
    ├── ACADEMY-CATALOGO.md
    ├── META-APP.md
    ├── DEPLOY.md
    ├── RUNBOOK.md
    ├── PAYMENT-GATEWAY.md              ← Stripe + MP (DEC-05) ✅
    ├── ROADMAP-EXECUCAO.md             ← checklist Jira (MD)
    └── ADR/
        └── 001-stack.md
```

**Raiz do repo:** `README.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, `CHANGELOG.md`

---

## Dois projetos, um ecossistema

| Projeto | Repo | Documentação |
|---------|------|--------------|
| **Toolkit + case Taty** | `instagram-influencer-agents` | `docs/toolkit/` + raiz |
| **SaaS (F0+)** | `creator-kit-saas` *(futuro)* | `docs/saas/` → migra para repo novo |

Enquanto o SaaS não existir, **produto + specs ficam aqui**.

---

## Documentos — status

| Doc | Caminho | Status |
|-----|---------|--------|
| Índice mestre | `docs/README.md` | ✅ |
| Visão SaaS | [`produto/PRODUTO-SAAS-VISAO.md`](produto/PRODUTO-SAAS-VISAO.md) | ✅ |
| Curso passo a passo | [`toolkit/CURSO-PASSO-A-PASSO.md`](toolkit/CURSO-PASSO-A-PASSO.md) | ✅ |
| Curadoria media kit | [`toolkit/MEDIA-KIT-CURADORIA.md`](toolkit/MEDIA-KIT-CURADORIA.md) | ✅ |
| Entregas F0–F5 | [`saas/ENTREGAS-FASES.md`](saas/ENTREGAS-FASES.md) | 📋 esqueleto |
| **Roadmap execução (checklist Jira)** | [`saas/ROADMAP-EXECUCAO.md`](saas/ROADMAP-EXECUCAO.md) + `.docx` | ✅ |
| Front / telas | [`saas/FRONT-TELAS.md`](saas/FRONT-TELAS.md) | 📋 esqueleto |
| Arquitetura | [`saas/ARQUITETURA.md`](saas/ARQUITETURA.md) | 📋 esqueleto |
| Schema DB | [`saas/SCHEMA-DB.md`](saas/SCHEMA-DB.md) | 📋 esqueleto |
| Catálogo cursos | [`saas/ACADEMY-CATALOGO.md`](saas/ACADEMY-CATALOGO.md) | 📋 esqueleto |
| Roadmap toolkit | [`../ROADMAP.md`](../ROADMAP.md) | ✅ |

---

## Onde escrever cada coisa nova

| Se decidir… | Escreva em… |
|-------------|-------------|
| Plano, preço, fase, comunidade | `docs/produto/` |
| Tela, wireframe | `docs/saas/FRONT-TELAS.md` |
| Banco, API, deploy | `docs/saas/` |
| Script / media kit Taty | `docs/toolkit/` ou `README` |

**Não usar só o chat** — documentação oficial fica no git.

---

## Links rápidos

- [Visão SaaS](produto/PRODUTO-SAAS-VISAO.md)
- [Curso](toolkit/CURSO-PASSO-A-PASSO.md)
- [Media kit curadoria](toolkit/MEDIA-KIT-CURADORIA.md)
- [Portfólio público Taty](https://tatiana-zacharias-portfolio.netlify.app/ugc/)
