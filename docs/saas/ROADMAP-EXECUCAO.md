# Roadmap de execução — ComJuntas SaaS

> **Autora:** Tatiana Zacharias  
> **Versão:** V0  
> **Data V0:** 2026-08-19  
> **Formato:** Épico (bloco) = história Jira · Tarefa = card  
> **Fonte:** `scripts/roadmap_execucao_data.py` → regenere com `python scripts/generate_roadmap_execucao.py`  
> **Índice geral:** [docs/README.md](../README.md)

---

## Como usar

1. Marque `[x]` nos critérios de aceite conforme concluir.
2. **Status** do card: ⬜ A fazer · 🔄 Em progresso · ✅ Concluído
3. Não pule épico sem critério de saída do anterior (F0→F1→…).

---

## Pré-requisitos concluídos (toolkit @tatyzacharias)

*Motor do SaaS — feito antes deste roadmap.*

- [x] Meta API — OAuth + sync Instagram (instagram-influencer-agents)
- [x] Media kit PDF layout glow + portfólio web luxe (@tatyzacharias)
- [x] Deploy portfólio: tatiana-zacharias-portfolio.netlify.app/ugc/
- [x] docs/toolkit/CURSO-PASSO-A-PASSO.md (material Academy C1–C3)
- [x] docs/toolkit/MEDIA-KIT-CURADORIA.md
- [x] Nome/bio otimizados parcialmente (itens 1–2 da bio)
- [x] Automação Playwright perfil (parcial — base F4)
## EPIC-0 — Organização do projeto

**Objetivo:** Workspace e documentação prontos para desenvolver o SaaS.  
**Duração:** Imediato  
**Progresso épico:** 🔄 2/5

### [ORG-01] Abrir pasta oficial no Cursor

| Campo | Conteúdo |
|-------|----------|
| **Status** | 🔄 Em progresso |
| **Dependências** | Nenhuma |

**Descrição:** Usar instagram-influencer-agents como workspace principal (código + docs + git).

**Resultado esperado:** Cursor aberto na pasta com scripts/, docs/, .git visíveis.

**Critérios de aceite:**

  - [x] Pasta instagram-influencer-agents contém scripts/, docs/, .git
  - [x] Árvore contém docs/produto/, docs/saas/, docs/toolkit/
  - [ ] Cursor aberto nesta pasta (File → Open Folder)

---

### [ORG-02] Limpar pastas duplicadas

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | ORG-01 |

**Descrição:** Remover instagram-influencer-agents-github e instagram-influencer-agents-old após confirmar que a pasta principal está completa.

**Resultado esperado:** Apenas uma pasta de projeto no disco.

**Critérios de aceite:**

  - [ ] Backup -old removido ou arquivado conscientemente
  - [ ] Cópia -github removida se redundante

---

### [ORG-03] Publicar documentação no GitHub

| Campo | Conteúdo |
|-------|----------|
| **Status** | 🔄 Em progresso |
| **Dependências** | ORG-01 |

**Descrição:** Commit e push da estrutura docs/ reorganizada e ROADMAP-EXECUCAO.

**Resultado esperado:** GitHub reflete docs/README.md, produto/, saas/, ROADMAP-EXECUCAO.

**Critérios de aceite:**

  - [x] docs/ reorganizado localmente (README, produto, saas, toolkit)
  - [x] ROADMAP-EXECUCAO.md + .docx gerados (V0)
  - [ ] git push concluído sem erro
  - [ ] Arquivos visíveis no repo Tatyssz/instagram-influencer-agents

---

### [ORG-04] Documentar visão SaaS e roadmap

| Campo | Conteúdo |
|-------|----------|
| **Status** | ✅ Concluído |
| **Dependências** | Nenhuma |

**Descrição:** PRODUTO-SAAS-VISAO.md, fases F0–F5, checklist Jira (este documento).

**Resultado esperado:** Planejamento completo versionado em docs/produto/ e docs/saas/.

**Critérios de aceite:**

  - [x] docs/produto/PRODUTO-SAAS-VISAO.md completo
  - [x] docs/saas/ROADMAP-EXECUCAO com épicos e cards
  - [x] docs/README.md índice mestre atualizado

---

### [ORG-05] Sincronizar pasta local com GitHub (Opção B)

| Campo | Conteúdo |
|-------|----------|
| **Status** | ✅ Concluído |
| **Dependências** | Nenhuma |

**Descrição:** Copiar repo completo para instagram-influencer-agents; eliminar pasta incompleta.

**Resultado esperado:** Uma pasta local com código + git + docs.

**Critérios de aceite:**

  - [x] scripts/ e .git presentes na pasta principal
  - [x] SYNC-LOCAL.md com instruções

---

## EPIC-1 — Decisões pré-SaaS

**Objetivo:** Decisões de produto e negócio tomadas antes de codar.  
**Duração:** 1–2 dias  
**Progresso épico:** ⬜ 0/8

### [DEC-01] Definir nome do produto e domínio

| Campo | Conteúdo |
|-------|----------|
| **Status** | 🔄 Em progresso |
| **Dependências** | ORG-01 |

**Descrição:** Nome fechado: ComJuntas (Comunidade Juntas). Reservar @comjuntas no Instagram e domínio comjuntas.com.br (app. + admin.).

**Resultado esperado:** Nome fechado + @ Instagram + domínio registrado ou em processo.

**Critérios de aceite:**

  - [x] Nome ComJuntas documentado em docs/produto/
  - [x] @comjuntas reservado no Instagram
  - [ ] Domínio comjuntas.com.br definido/reservado

---

### [DEC-02] Definir persona #1

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | Nenhuma |

**Descrição:** Quem paga primeiro: UGC beauty iniciante, micro creator 5–10k, ou 10k+.

**Resultado esperado:** Persona escrita com dores, objetivo e willingness to pay.

**Critérios de aceite:**

  - [ ] 1 persona primária escolhida
  - [ ] Registrada no doc de produto

---

### [DEC-03] Definir planos no launch

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-02 |

**Descrição:** Quantos planos no go-live (recomendado Starter + Pro) e preços de referência.

**Resultado esperado:** Tabela de planos fechada para F1.

**Critérios de aceite:**

  - [ ] Planos e limites por plano definidos
  - [ ] Preços de referência validados

---

### [DEC-04] Definir modelo de trial

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-03 |

**Descrição:** Trial 7 dias vs pagamento direto vs freemium limitado.

**Resultado esperado:** Política de trial documentada.

**Critérios de aceite:**

  - [ ] Decisão única registrada
  - [ ] Impacto no billing descrito

---

### [DEC-05] Escolher gateway de pagamento

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-03 |

**Descrição:** Stripe, Mercado Pago ou ambos para assinatura BR.

**Resultado esperado:** Gateway escolhido + conta criada ou em criação.

**Critérios de aceite:**

  - [ ] Conta sandbox/teste acessível
  - [ ] Documentado em docs/saas/

---

### [DEC-06] Definir posicionamento de marca

| Campo | Conteúdo |
|-------|----------|
| **Status** | 🔄 Em progresso |
| **Dependências** | DEC-01 |

**Descrição:** ComJuntas como marca; Tatiana Zacharias como fundadora/case zero (não sigla forçada nas iniciais).

**Resultado esperado:** Diretriz de marca para landing e comunicação.

**Critérios de aceite:**

  - [x] Decisão registrada
  - [ ] Tom de voz definido em 3 bullets

---

### [DEC-07] Wireframe F1 (app + admin)

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-02, DEC-03 |

**Descrição:** Esboço das 5 telas usuária + 2 admin para Core SaaS.

**Resultado esperado:** Wireframes em docs/saas/FRONT-TELAS.md ou Figma link.

**Critérios de aceite:**

  - [ ] Onboarding, dashboard, media kit, portfólio, conta mapeados
  - [ ] Admin: lista usuárias + detalhe mapeados

---

### [DEC-08] Rascunho legal LGPD

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-01 |

**Descrição:** Termos de Uso e Política de Privacidade mínimos para cobrança.

**Resultado esperado:** Rascunho revisável antes do go-live F1.

**Critérios de aceite:**

  - [ ] Termos cobrem dados Instagram e cancelamento
  - [ ] Privacidade cobre LGPD básico

---

## EPIC-2 — F0 — Fundação

**Objetivo:** Infra, auth e shell do front em staging. Ainda não cobra.  
**Duração:** 1–2 semanas  
**Progresso épico:** ⬜ 0/8

### [F0-01] Criar repo comjuntas-saas

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-01, DEC-07 |

**Descrição:** Repositório separado do toolkit Taty; consome scripts como lib ou workers.

**Resultado esperado:** Repo no GitHub com README e estrutura monorepo ou api+web.

**Critérios de aceite:**

  - [ ] Repo criado e clonável
  - [ ] README explica relação com instagram-influencer-agents

---

### [F0-02] Postgres + migrations iniciais

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-01 |

**Descrição:** Schema users, subscriptions; Alembic ou equivalente.

**Resultado esperado:** DB provisionado + migration v1 aplicada.

**Critérios de aceite:**

  - [ ] Tabelas users e subscriptions existem
  - [ ] Migration versionada no repo

---

### [F0-03] Auth usuária

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-01 |

**Descrição:** Login email/Google ou magic link (Clerk, Supabase Auth, etc.).

**Resultado esperado:** Usuária cria conta e acessa /app.

**Critérios de aceite:**

  - [ ] Signup e login funcionam
  - [ ] Sessão persiste entre reloads

---

### [F0-04] Auth admin

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-03 |

**Descrição:** Role admin para Taty; rota /admin protegida.

**Resultado esperado:** Apenas admin acessa painel administrativo.

**Critérios de aceite:**

  - [ ] Usuária comum não acessa /admin
  - [ ] Admin loga com credencial separada ou role

---

### [F0-05] Shell Next.js (marketing + app + admin)

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-03, F0-04 |

**Descrição:** Layout base, navegação, rotas vazias com placeholder.

**Resultado esperado:** 3 superfícies routáveis em staging.

**Critérios de aceite:**

  - [ ] Landing 1 página renderiza
  - [ ] /app e /admin com layout sidebar

---

### [F0-06] API FastAPI esqueleto

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-01 |

**Descrição:** Health check, auth middleware, estrutura de routers.

**Resultado esperado:** API responde /health em staging.

**Critérios de aceite:**

  - [ ] Deploy API funcional
  - [ ] Auth integrado com front

---

### [F0-07] Deploy staging

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-05, F0-06, F0-02 |

**Descrição:** Vercel (front) + Railway/Fly (API) + Postgres managed.

**Resultado esperado:** URLs staging compartilháveis.

**Critérios de aceite:**

  - [ ] Front e API acessíveis via HTTPS
  - [ ] Variáveis de ambiente documentadas

---

### [F0-08] Critério de saída F0

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-07 |

**Descrição:** Validação end-to-end do foundation.

**Resultado esperado:** Taty loga app + admin em staging.

**Critérios de aceite:**

  - [ ] Demo gravada ou checklist assinado
  - [ ] docs/saas/ARQUITETURA.md preenchido

---

## EPIC-3 — F1 — Core SaaS (primeira cobrança)

**Objetivo:** Creator paga e gera media kit + portfólio + IA sozinha.  
**Duração:** 4–6 semanas  
**Progresso épico:** ⬜ 0/13

### [F1-01] Onboarding + seleção de plano

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-08, DEC-05 |

**Descrição:** Fluxo criar conta → escolher Starter/Pro → checkout.

**Resultado esperado:** Nova usuária completa onboarding sem suporte manual.

**Critérios de aceite:**

  - [ ] Fluxo < 5 minutos
  - [ ] Erros tratados com mensagem clara

---

### [F1-02] Integração billing recorrente

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-01 |

**Descrição:** Stripe ou MP webhooks: active, canceled, past_due.

**Resultado esperado:** Assinatura ativa libera features; cancelada bloqueia.

**Critérios de aceite:**

  - [ ] Webhook testado em sandbox
  - [ ] Status sync com tabela subscriptions

---

### [F1-03] OAuth Instagram multi-tenant

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F0-08 |

**Descrição:** Cada usuária conecta IG; token criptografado por tenant.

**Resultado esperado:** Botão Conectar Instagram funciona por usuária.

**Critérios de aceite:**

  - [ ] Token salvo criptografado
  - [ ] Reconectar fluxo documentado

---

### [F1-04] Worker sync automático

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-03 |

**Descrição:** Job sync posts + insights após OAuth ou agendado.

**Resultado esperado:** Dashboard mostra dados reais do IG conectado.

**Critérios de aceite:**

  - [ ] Sync completa em < 5 min para perfil típico
  - [ ] Falha registrada e visível no admin

---

### [F1-05] Dashboard métricas

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-04 |

**Descrição:** Seguidores, alcance, engajamento resumido.

**Resultado esperado:** Usuária vê métricas após sync.

**Critérios de aceite:**

  - [ ] Métricas batem com API Meta
  - [ ] Estado vazio se sem IG

---

### [F1-06] Gerar media kit PDF + link

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-04 |

**Descrição:** Reutilizar pipeline mediakit do toolkit por tenant.

**Resultado esperado:** PDF gerado + URL pública única.

**Critérios de aceite:**

  - [ ] PDF abre e números correspondem ao sync
  - [ ] Regenerar sobrescreve versão ou versiona

---

### [F1-07] Gerar portfólio web + link

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-04 |

**Descrição:** Template luxe fixo; hosting por tenant (subpath/subdomínio).

**Resultado esperado:** Link público do portfólio funcional.

**Critérios de aceite:**

  - [ ] Mobile responsive
  - [ ] Link compartilhável

---

### [F1-08] Relatório IA

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-04 |

**Descrição:** Análise pontos fortes + melhorias a partir do sync.

**Resultado esperado:** Texto estruturado gerado sob demanda.

**Critérios de aceite:**

  - [ ] Relatório em português
  - [ ] Baseado em dados reais do sync

---

### [F1-09] Página Minha conta

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-02, F1-03 |

**Descrição:** Plano, billing portal, cancelar, reconectar IG.

**Resultado esperado:** Usuária autogere assinatura e conexão IG.

**Critérios de aceite:**

  - [ ] Link para portal de pagamento
  - [ ] Desconectar IG remove token

---

### [F1-10] Admin — lista e detalhe usuárias

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-04, F0-04 |

**Descrição:** Suporte: ver plano, sync, reprocessar jobs.

**Resultado esperado:** Admin resolve 80% tickets sem código.

**Critérios de aceite:**

  - [ ] Lista paginada de usuárias
  - [ ] Botão re-sync funcional

---

### [F1-11] Publicar Termos + Privacidade

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | DEC-08, F1-01 |

**Descrição:** Páginas legais linkadas no signup e footer.

**Resultado esperado:** Compliance mínimo LGPD no ar.

**Critérios de aceite:**

  - [ ] Links no onboarding
  - [ ] DEC-08 incorporado

---

### [F1-12] Beta pago 2–3 creators

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-06, F1-07, F1-08, F1-02 |

**Descrição:** Recrutar UGC beauty; cobrar preço beta.

**Resultado esperado:** 2–3 pagantes usando produto sem você operar manual.

**Critérios de aceite:**

  - [ ] Cada beta gera kit + portfólio sozinha
  - [ ] Feedback coletado

---

### [F1-13] Critério de saída F1 — 10 pagantes

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-12 |

**Descrição:** North star F1: escala inicial de receita.

**Resultado esperado:** 10 assinantes pagantes ativos.

**Critérios de aceite:**

  - [ ] MRR registrado
  - [ ] Churn documentado

---

## EPIC-4 — F2 — Academy

**Objetivo:** Cursos C1–C3 no painel + venda avulsa.  
**Duração:** 2–3 semanas  
**Progresso épico:** ⬜ 0/7

### [F2-01] Área Meus cursos

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-13 |

**Descrição:** Listagem de cursos matriculados + progresso.

**Resultado esperado:** Usuária vê cursos do plano ou comprados.

**Critérios de aceite:**

  - [ ] Estado vazio amigável
  - [ ] Progresso % se habilitado

---

### [F2-02] Conteúdo C1 — Meta API

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-01 |

**Descrição:** Migrar módulos 1–2 do CURSO-PASSO-A-PASSO para aulas.

**Resultado esperado:** C1 navegável no painel.

**Critérios de aceite:**

  - [ ] ≥5 aulas
  - [ ] Markdown ou vídeo embed

---

### [F2-03] Conteúdo C2 — Bio + automação

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-01 |

**Descrição:** Módulos 3–4 do curso em aulas.

**Resultado esperado:** C2 navegável no painel.

**Critérios de aceite:**

  - [ ] ≥4 aulas
  - [ ] Links para toolkit quando relevante

---

### [F2-04] Conteúdo C3 — Media Kit & Portfólio

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-01 |

**Descrição:** Módulo 5 / Fase 7 do curso em aulas.

**Resultado esperado:** C3 navegável no painel.

**Critérios de aceite:**

  - [ ] Case Taty referenciado
  - [ ] Passo a passo reproduzível

---

### [F2-05] Checkout avulso + bundle

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-01, DEC-05 |

**Descrição:** Compra one-time por curso; bundle C1+C2+C3.

**Resultado esperado:** Não-assinante compra curso e acessa.

**Critérios de aceite:**

  - [ ] Webhook compra avulsa
  - [ ] course_enrollments criado

---

### [F2-06] Admin cursos e matrículas

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-02 |

**Descrição:** CRUD cursos; ver quem comprou o quê.

**Resultado esperado:** Taty publica/despublica curso sem deploy.

**Critérios de aceite:**

  - [ ] CRUD mínimo funcional
  - [ ] Lista matrículas exportável

---

### [F2-07] Critério de saída F2

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-05, F2-02, F2-03, F2-04 |

**Descrição:** 1 compra avulsa OU Pro acessa C1–C3.

**Resultado esperado:** Receita de curso ou upsell comprovado.

**Critérios de aceite:**

  - [ ] 1 transação avulsa real ou 3 Pro com acesso

---

## EPIC-5 — F3 — Comunidade (lembretes)

**Objetivo:** Círculos + fila; engajamento manual no Instagram.  
**Duração:** 3–4 semanas  
**Progresso épico:** ⬜ 0/7

### [F3-01] CRUD círculos (admin)

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-13 |

**Descrição:** Criar círculo, nicho, limite de membros, convites.

**Resultado esperado:** Admin gerencia círculos fechados.

**Critérios de aceite:**

  - [ ] Círculo criado
  - [ ] Convite por link ou e-mail

---

### [F3-02] Entrada e saída de membros

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-01 |

**Descrição:** Usuária aceita convite; admin remove membro.

**Resultado esperado:** Membros vinculados a circle_members.

**Critérios de aceite:**

  - [ ] Opt-in explícito
  - [ ] Saída imediata

---

### [F3-03] Detectar posts da comunidade

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-02, F1-04 |

**Descrição:** Sync identifica post novo de membro do círculo.

**Resultado esperado:** engagement_queue populada automaticamente.

**Critérios de aceite:**

  - [ ] Post detectado em < 24h
  - [ ] Não duplica mesmo post

---

### [F3-04] Fila Engajar hoje + deep link

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-03 |

**Descrição:** Lista posts pendentes; botão abre Instagram.

**Resultado esperado:** Usuária sabe o que engajar hoje.

**Critérios de aceite:**

  - [ ] Link abre post correto
  - [ ] Marcar como feito manual

---

### [F3-05] Score de reciprocidade

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-04 |

**Descrição:** Quem deu X / recebeu Y; alerta desequilíbrio.

**Resultado esperado:** Dashboard reciprocidade por membro.

**Critérios de aceite:**

  - [ ] Score atualiza ao marcar feito
  - [ ] Regra documentada para remoção

---

### [F3-06] Notificações

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-04 |

**Descrição:** E-mail ou WhatsApp: posts esperando engajamento.

**Resultado esperado:** Membro avisado sem abrir painel.

**Critérios de aceite:**

  - [ ] Opt-in notificação
  - [ ] Rate limit diário

---

### [F3-07] Piloto 5–10 creators — 2 semanas

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-05, F3-06 |

**Descrição:** Círculo real UGC beauty monitorado.

**Resultado esperado:** Grupo usa fila consistentemente.

**Critérios de aceite:**

  - [ ] ≥80% membros engajaram na semana
  - [ ] Feedback qualitativo coletado

---

## EPIC-6 — F4 — Engajamento com aprovação

**Objetivo:** Aprovar → executar curtir/comentar via Playwright.  
**Duração:** 4–6 semanas  
**Progresso épico:** ⬜ 0/6

### [F4-01] Autorizar sessão Instagram

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-07 |

**Descrição:** Fluxo seguro; cookies criptografados; nunca senha em texto.

**Resultado esperado:** Usuária autoriza engajamento uma vez.

**Critérios de aceite:**

  - [ ] Consentimento nos Termos
  - [ ] Renovar sessão quando expirar

---

### [F4-02] Sugestão IA de comentário

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F3-04 |

**Descrição:** IA gera comentário variado; usuária edita antes de aprovar.

**Resultado esperado:** Comentário editável na fila.

**Critérios de aceite:**

  - [ ] Não repetitivo
  - [ ] Tom beauty/UGC

---

### [F4-03] Aprovar e executar

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F4-01, F4-02 |

**Descrição:** Estados pending → approved → executing → done/failed.

**Resultado esperado:** Ação executada após clique explícito.

**Critérios de aceite:**

  - [ ] Sem execução sem approved
  - [ ] Lote opcional limitado

---

### [F4-04] Worker Playwright

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F4-03 |

**Descrição:** Executor isolado; limites diários e intervalo entre ações.

**Resultado esperado:** Curtir + comentar no post alheio.

**Critérios de aceite:**

  - [ ] Log completo por ação
  - [ ] Para em session_expired

---

### [F4-05] Admin logs e limites globais

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F4-04 |

**Descrição:** Auditoria; caps por plano; alertas falha em massa.

**Resultado esperado:** Ops consegue investigar incidentes.

**Critérios de aceite:**

  - [ ] Logs 30 dias
  - [ ] Limites configuráveis

---

### [F4-06] Curso C5 + critério de saída F4

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F4-04, F4-05 |

**Descrição:** Material comunidade; 1 semana estável sem ban.

**Resultado esperado:** 50 engajamentos/semana ok no piloto.

**Critérios de aceite:**

  - [ ] C5 publicado ou outline
  - [ ] Zero incidentes críticos 7 dias

---

## EPIC-7 — F5 — Escala

**Objetivo:** PMF: templates, agency, domínio, Meta produção.  
**Duração:** Contínuo  
**Progresso épico:** ⬜ 0/6

### [F5-01] Múltiplos templates portfólio

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-13 |

**Descrição:** 2–3 estilos além do luxe.

**Resultado esperado:** Usuária escolhe template no painel.

**Critérios de aceite:**

  - [ ] Preview antes de publicar

---

### [F5-02] Domínio customizado

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F5-01 |

**Descrição:** Creator usa domínio próprio no portfólio.

**Resultado esperado:** DNS + SSL automatizado.

**Critérios de aceite:**

  - [ ] Plano superior only
  - [ ] Doc setup usuária

---

### [F5-03] Plano Agency / white-label

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F4-06 |

**Descrição:** N contas; círculos privados agência.

**Resultado esperado:** Oferta B2B documentada e vendável.

**Critérios de aceite:**

  - [ ] Pricing agency
  - [ ] Multi-tenant agency role

---

### [F5-04] App Meta modo produção

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-13 |

**Descrição:** Review Meta; escala além de testadores.

**Resultado esperado:** App aprovado produção.

**Critérios de aceite:**

  - [ ] Business verification se exigido

---

### [F5-05] Curso C4 — Fechar parcerias

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-07 |

**Descrição:** Pacotes comerciais, proposta, pricing para marcas.

**Resultado esperado:** C4 no Academy.

**Critérios de aceite:**

  - [ ] Alinhado a template proposta marcas

---

### [F5-06] IA coach avançada

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F1-08 |

**Descrição:** Benchmarks nicho beauty; chat coach.

**Resultado esperado:** Diferencial Pro+ claro.

**Critérios de aceite:**

  - [ ] Respostas grounded em sync

---

## EPIC-P — Toolkit Taty (paralelo — case pessoal)

**Objetivo:** Manter case @tatyzacharias; motor do produto.  
**Duração:** Paralelo ao SaaS  
**Progresso épico:** 🔄 1/6

### [TK-01] Bio linhas 2–4 + link + CTA

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | Nenhuma |

**Descrição:** Completar otimização bio case Taty item a item.

**Resultado esperado:** Bio comercial completa aprovada.

**Critérios de aceite:**

  - [ ] ≤150 chars
  - [ ] Aplicado no IG

---

### [TK-02] Validador 150 chars no update_profile

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | Nenhuma |

**Descrição:** Bloquear apply se bio exceder limite Instagram.

**Resultado esperado:** CLI valida antes de Playwright.

**Critérios de aceite:**

  - [ ] Teste unitário ou manual documentado

---

### [TK-03] Playwright submit confiável

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | Nenhuma |

**Descrição:** 100% sucesso em apply bio/nome quando UI Meta estável.

**Resultado esperado:** apply + verify passam consistentemente.

**Critérios de aceite:**

  - [ ] 3 runs seguidos OK

---

### [TK-04] Template proposta para marcas

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | Nenhuma |

**Descrição:** Documento/PDF proposta comercial UGC.

**Resultado esperado:** Template reutilizável para C4.

**Critérios de aceite:**

  - [ ] Usado em 1 outreach real

---

### [TK-05] Gravar curso em vídeo (C1–C3)

| Campo | Conteúdo |
|-------|----------|
| **Status** | ⬜ A fazer |
| **Dependências** | F2-01 |

**Descrição:** Opcional; complementa material texto.

**Resultado esperado:** Vídeos hospedados e linkados no Academy.

**Critérios de aceite:**

  - [ ] ≥1 módulo gravado

---

### [TK-06] Regra: media kit Taty layout bloqueado

| Campo | Conteúdo |
|-------|----------|
| **Status** | ✅ Concluído |
| **Dependências** | Nenhuma |

**Descrição:** Não alterar PDF/portfólio aprovado sem pedido explícito Taty.

**Resultado esperado:** Zero regressão visual case pessoal.

**Critérios de aceite:**

  - [x] Regra documentada em PRODUTO-SAAS-VISAO e user rules
  - [x] Checklist release inclui regra

---

## Legenda de dependências

- IDs referem-se a cards (ex.: `F0-08`, `DEC-01`)
- Épico paralelo **EPIC-P** não bloqueia SaaS; **TK-05** depende de **F2-01**

