# ComJuntas — visão e plano (SaaS)

> **Status:** planejamento · não iniciado  
> **Marca:** **ComJuntas** (*Comunidade Juntas*)  
> **Autora / fundadora / case zero:** Tatiana Zacharias (@tatyzacharias)  
> **Instagram produto:** [@comjuntas](https://www.instagram.com/comjuntas/) ✅  
> **Data do registro:** 2026-08-19  
> **Última atualização:** 2026-08-19 — Persona #1 (DEC-02) fechada  
> **Contexto:** portfólio UGC v1 pronto em https://tatiana-zacharias-portfolio.netlify.app/ugc/

---

## O que é

Empacotar o fluxo já construído no `instagram-influencer-agents` (sync Instagram, métricas, media kit PDF, portfólio web, análise comercial, deploy) como **SaaS multi-usuário com assinatura mensal** para outros creators/influenciadores.

**Modelo de negócio:** a pessoa paga por mês (pacote recorrente) para ter acesso a:

- Gerar **media kit** a partir do Instagram dela
- **Portfólio web** público (link para marcas)
- **IA analisando** o perfil: o que está bom, o que melhorar
- **Comunidade / Círculos** — grupo de creators que se apoiam mutuamente
- **Engajamento assistido** — curtir/comentar nos posts da comunidade **somente após a usuária aprovar** (nível 3 com gate humano)
- **Cursos (Academy)** — material educacional da Taty: **incluso em alguns pacotes** ou **vendido avulso**

**Diferencial vs painéis SMM (InstaBarato etc.):** contas reais, engajamento real, reciprocidade — não bots nem métricas falsas.

**Receita:** assinatura recorrente (SaaS) + **venda avulsa de cursos** (compra única).

---

## Módulo Comunidade (Círculos)

### Conceito

Várias influenciadoras cadastradas no sistema formam um **círculo fechado**. Cada uma engaja nas outras de forma mútua:

```
        A (Taty)
       /        \
   curte/comenta  curte/comenta
     /              \
   B ←────────────→ C
     \              /
   curte/comenta  curte/comenta
```

- **A** engaja nos posts de **B** e **C**
- **B** engaja em **A** e **C**
- **C** engaja em **A** e **B**

Hoje isso acontece manualmente em grupos de WhatsApp/Telegram (“fulana postou, vai lá dar amor”). O **ComJuntas** **organiza, lembra, equilibra reciprocidade e executa após aprovação**.

### O que o sistema faz

| Função | Descrição |
|--------|-----------|
| **Círculo / comunidade** | Grupo fechado de creators (ex.: UGC beauty, 5–20 pessoas) |
| **Detectar posts novos** | Sync OAuth de cada membro → “B publicou Reel” |
| **Fila de engajamento** | “Hoje você deve engajar: post da B, post da C” |
| **Notificações** | E-mail, push ou WhatsApp: “2 posts da comunidade esperando” |
| **Sugestão de comentário (IA)** | Texto autêntico para revisar/editar antes de aprovar |
| **Aprovação explícita** | Usuária revisa → clica “Aprovar e executar” |
| **Execução** | Worker curte/comenta no Instagram **só após aprovação** |
| **Reciprocidade** | Score: quem deu X / quem recebeu Y; quem só recebe perde acesso |

### Regras da comunidade (anti-pod tóxico)

- Comentários **variados** — IA sugere, humano revisa
- Limite diário por plano (ex.: 10 engajamentos/dia no Pro)
- Intervalo mínimo entre ações (ex.: 2–5 min)
- Grupos **pequenos** (5–20) > grupos enormes
- Mesmo nicho quando possível (beauty UGC = comentários naturais)
- Opt-in explícito + consentimento nos Termos de Uso
- Quem não engaja → score cai / removida do círculo

### InstaBarato vs ComJuntas

| | InstaBarato / SMM | ComJuntas |
|---|-------------------|-------------|
| Quem engaja | Bots / contas fake | Creators reais da comunidade |
| Motivação | Compra | Reciprocidade + pacote mensal |
| Execução | Automática invisível | **Aprovação humana** + execução |
| Valor para marcas | Nenhum (métrica falsa) | Rede real + conteúdo autêntico |
| Risco | Alto (ToS, legal) | Médio (mitigado com limites + aprovação) |

---

## Autenticação — três camadas distintas

“Estar logada no sistema” envolve **três conexões separadas**:

### 1) Login no ComJuntas (conta SaaS)

Identifica quem é a usuária, plano ativo, pagamento, dashboard.

- E-mail + senha, **Google**, ou **magic link**
- Ferramentas candidatas: Clerk, Supabase Auth, Auth0, NextAuth
- Resultado: `user_id`, sessão JWT, acesso ao painel

### 2) Conectar Instagram — OAuth Meta (dados)

Leitura oficial via Graph API: posts, insights, métricas, media kit.

- Botão “Conectar Instagram” → redirect Meta → token de longa duração
- Token **criptografado em repouso**, por usuária
- Serve para: sync, media kit, portfólio, **detectar posts novos da comunidade**

**Limitação:** a API Meta **não** permite curtir/comentar no feed de outras contas.

### 3) Conectar para engajamento — sessão Instagram (execução)

Necessário para executar curtir/comentar após aprovação.

- Fluxo único: “Autorizar engajamento”
- Janela segura (Playwright / browser isolado)
- Usuária faz login no **instagram.com** (2FA se tiver)
- Salvamos **cookies de sessão criptografados** — nunca a senha em texto
- Renovar quando expirar (aviso no painel: “Reconecte o Instagram para engajamento”)

```
Login ComJuntas     →  quem paga, quem aprova
OAuth Meta            →  ler dados, detectar posts
Sessão Instagram      →  executar curtir/comentar (só após aprovar)
```

---

## Fluxo de engajamento (aprovar → executar)

```
1. B publica Reel
2. Sync (OAuth Meta) detecta post novo de membro do círculo
3. Sistema notifica A: preview + sugestão de comentário (IA)
4. A entra no painel, revisa/edita comentário, marca ☑ curtir
5. A clica "Aprovar e executar" (ou aprova lote de N itens)
6. Worker Playwright usa sessão criptografada de A
7. Executa curtir + publicar comentário no post de B
8. Painel registra: feito ✓ / falhou / sessão expirada
9. Reciprocidade atualizada no score do círculo
```

**Princípio:** não é bot invisível. É **assistente com consentimento explícito** por ação (ou lote aprovado).

**Estados de `engagement_actions`:** `pending` → `approved` → `executing` → `done` | `failed` | `session_expired`

---

## Módulo Academy (Cursos)

### Modelo de venda

Dois caminhos de monetização — **podem coexistir**:

| Modelo | Como funciona | Exemplo |
|--------|-----------------|---------|
| **No pacote (mensal)** | Assinante do plano X tem acesso aos cursos Y enquanto pagar | Pro inclui Curso 1 + 2 |
| **Avulso (compra única)** | Paga uma vez → acesso ao curso (permanente ou por X meses) | Curso Media Kit R$ 197 |
| **Upsell** | Quem já é assinante compra avulso com desconto | -30% no checkout |

**Regra de produto:** quem **só compra curso avulso** não ganha sync automático / comunidade / execução — isso fica no SaaS. Quem **só assina** pode não ter todos os cursos (depende do plano).

### Material já mapeado

Fonte principal no toolkit (case Taty): [`docs/toolkit/CURSO-PASSO-A-PASSO.md`](../toolkit/CURSO-PASSO-A-PASSO.md) — 15 fases + 5 módulos para gravação.

**Catálogo sugerido** (cada linha = produto vendável avulso **ou** bundle no pacote):

| ID | Curso | Conteúdo (do mapeamento) | Material | Incluso no pacote (rascunho) |
|----|-------|--------------------------|----------|------------------------------|
| **C1** | **Instagram + Meta API do zero** | App Meta, OAuth, sync, `profile_snapshot.json` (Módulos 1–2) | ✅ doc completo | Starter (intro) |
| **C2** | **Bio profissional + automação** | Otimizar bio item a item, Playwright, aprovação (Módulos 3–4) | ✅ doc completo | Pro |
| **C3** | **Media Kit & Portfólio UGC** | PDF glow, portfólio luxe, curadoria de parcerias (Módulo 5 / Fase 7) | ✅ case @tatyzacharias | Pro |
| **C4** | **Fechar parcerias pagas** | Pacotes comerciais, proposta, preços, CTA marcas (ROADMAP v0.7+) | 📋 planejado | Creator+ |
| **C5** | **Comunidade & engajamento mútuo** | Círculos, fila, aprovar + executar, reciprocidade | 📋 junto com Fase C SaaS | Creator+ |

**Formato de entrega (a definir na implementação):** vídeo-aulas + PDFs + templates + (opcional) área de membros no próprio ComJuntas.

### Fluxo de acesso ao curso

```
Compra avulsa OU plano ativo
        ↓
course_enrollments (user_id + course_id)
        ↓
Área "Meus cursos" no painel
        ↓
Módulos / aulas (progresso opcional: lesson_completed)
```

**Integração billing:** Stripe/Mercado Pago — produtos separados (`price_course_c3`) + assinaturas (`price_plan_pro`).

---

## Personas e planos — fechado (DEC-03)

Detalhes completos: [`PLANOS-LAUNCH.md`](PLANOS-LAUNCH.md)

| Plano | Preço | Persona | Venda desde |
|-------|-------|---------|-------------|
| **ComJuntas Start** | R$ 69/mês | A — 500–3k | F1 · só ferramenta |
| **ComJuntas Pro** ⭐ | R$ 129/mês | B/C — 3k+ | F1 · **+ comunidade + cursos** |
| **Plus** | *TBD* | — | ⏸ decidir depois (engajamento auto?) |

**F1 cobra:** Start + Pro · **Hero:** Pro · Comunidade/cursos: **só Pro** (por enquanto)

*(Billing: [`PAYMENT-GATEWAY.md`](../saas/PAYMENT-GATEWAY.md) ✅ · Trial: [`TRIAL-POLICY.md`](TRIAL-POLICY.md) ✅)*

---

## É projeto novo?

| | |
|---|---|
| **Não do zero** | Reutiliza scripts, pipelines e aprendizado do toolkit atual |
| **Sim como produto** | Multi-tenant, login, billing, onboarding, painel, escala, suporte |

**Recomendação de repos:**

- Manter `instagram-influencer-agents` = toolkit / case Taty (não quebrar o que está aprovado)
- Criar repo novo (ex.: `creator-kit-saas`) que consome o toolkit como lib ou workers

---

## O que já existe (case Taty — motor do produto)

| Peça | Status |
|------|--------|
| OAuth + sync Instagram (Meta API) | ✅ |
| Métricas + diagnóstico comercial | ✅ |
| Media kit PDF (layout glow aprovado) | ✅ |
| Portfólio web luxe + deploy | ✅ |
| Curadoria parcerias / cases / feedbacks | ✅ |
| Deploy Netlify (`sync_portfolio_netlify.ps1`) | ✅ |
| Automação Playwright (perfil) | ✅ parcial — base para worker de engajamento |
| Curso passo a passo (`docs/toolkit/CURSO-PASSO-A-PASSO.md`) | ✅ material mapeado (5 módulos + Fase 7) |
| Licença MIT (vender curso/template) | ✅ no repo toolkit |

**Links de referência:**

- Portfólio UGC: https://tatiana-zacharias-portfolio.netlify.app/ugc/
- Repo toolkit: `Tatyssz/instagram-influencer-agents`
- Repo deploy portfólio: `Tatyssz/portifolio` (pasta `ugc/`)

---

## MVP sugerido (v1 — 4–6 semanas focadas)

Mínimo para **primeira cobrança** (Fase A — ver roadmap):

1. **Login ComJuntas** (email/Google)
2. **Assinatura** (Stripe ou Mercado Pago)
3. **Conectar Instagram** (OAuth Meta)
4. **Sync automático** (posts + insights)
5. **Media kit** gerado (PDF + link público)
6. **Portfólio web** (1 template fixo — estilo luxe aprovado)
7. **Relatório IA** simples: o que está bom / o que melhorar

**Fora do MVP v1 (Fases B e C):**

- Módulo Comunidade / Círculos
- Fila de engajamento + aprovação + execução Playwright
- Múltiplos templates visuais
- Domínio customizado
- Agendamento / publicação de posts
- White-label agências

---

## Arquitetura mínima

```
[Web app]     login, onboarding, dashboard, fila de aprovação, área de cursos
     ↓
[API]         usuários, assinaturas, cursos, círculos, engagement_actions
     ↓
[Workers]     sync IG, build mediakit, análise IA, executor Playwright
     ↓
[Storage]     HTML/PDF/assets por creator + vídeos/PDFs de cursos (S3 ou similar)
     ↓
[CDN/Netlify] hosting estático por tenant (subpath ou subdomínio)
```

**Stack sugerida** (alinhada ao que já existe):

| Camada | Tecnologia |
|--------|------------|
| Backend | Python FastAPI (reaproveita scripts) |
| Frontend | Next.js ou React (dashboard) |
| DB | Postgres (ver schema abaixo) |
| Filas | Redis + Celery (ou equivalente) |
| Pagamento | Stripe ou Mercado Pago — **assinatura + compra avulsa de cursos** |
| IA | API Claude/GPT — prompt + dados do sync + sugestão de comentários |
| Executor | Playwright (sessão isolada, só `approved`) |

---

## Schema do banco (rascunho)

### Core SaaS

| Tabela | Campos principais |
|--------|-------------------|
| `users` | id, email, name, created_at |
| `subscriptions` | user_id, plan, stripe_customer_id, status, current_period_end |
| `instagram_accounts` | user_id, ig_user_id, oauth_token_enc, token_expires_at |
| `instagram_sessions` | user_id, cookies_enc, valid_until, last_used_at |
| `media_kits` | user_id, pdf_url, public_slug, generated_at |
| `portfolio_builds` | user_id, html_url, template, built_at |

### Comunidade + engajamento

| Tabela | Campos principais |
|--------|-------------------|
| `circles` | id, name, niche, max_members, created_by |
| `circle_members` | circle_id, user_id, joined_at, reciprocity_score, status |
| `engagement_queue` | id, circle_id, post_owner_id, post_id, post_url, detected_at |
| `engagement_actions` | id, queue_id, actor_user_id, like, comment_text, status, approved_at, executed_at, error |

### Academy (cursos)

| Tabela | Campos principais |
|--------|-------------------|
| `courses` | id, slug, title, description, price_cents, included_in_plans[], status |
| `course_modules` | id, course_id, title, sort_order |
| `course_lessons` | id, module_id, title, content_type, content_url, duration_min |
| `course_enrollments` | user_id, course_id, source (`subscription` \| `purchase`), stripe_payment_id, expires_at |
| `lesson_progress` | user_id, lesson_id, completed_at |

**Lógica de acesso:** usuária vê curso se `course_enrollments` ativo **ou** plano atual inclui o curso em `included_in_plans`.

**Índices úteis:** `(actor_user_id, status)`, `(circle_id, detected_at)`, `(user_id, status)` em subscriptions.

---

## Decisões legais / Meta (crítico antes de escala)

- [ ] App Meta em **modo produção** + revisão de permissões
- [ ] Termos de uso, privacidade, **LGPD**
- [ ] Tokens Instagram **por usuário**, criptografados em repouso
- [ ] Cookies de sessão para engajamento: consentimento explícito + deletar ao cancelar
- [ ] Termos: automação **autorizada pela usuária**; ela responde pelo conteúdo dos comentários
- [ ] Rate limits e quotas da Graph API
- [ ] Limites de execução Playwright (anti-abuso, anti-ban)
- [ ] Política de retenção/deleção de dados ao cancelar

---

## Ordem de lançamento recomendada

| Fase | Entrega | Cobrança |
|------|---------|----------|
| **A** | Login + Stripe + media kit + portfólio + IA | ✅ Começar a cobrar |
| **A+** | **Academy v1** — C1–C3 no painel (material do `CURSO-PASSO-A-PASSO.md`) + venda avulsa | Paralelo ou logo após A |
| **B** | Círculos + fila + **só lembretes** (abre Instagram manualmente) | Incluído no Starter |
| **C** | Aprovar + executar (Playwright pós-aprovação) + Curso C5 | Pro / Creator+ |

Assim o produto **monetiza cedo**; engajamento automático entra como upgrade, sem bloquear o go-live.

---

## Fluxo do primeiro entregável (prototipar antes de cobrar)

1. Creator cria conta → escolhe plano → **paga**
2. **Conectar Instagram** (OAuth)
3. Sync roda → **dashboard** com métricas
4. Botão **Gerar media kit** → PDF + URL pública
5. Botão **Ver análise IA** → pontos fortes + melhorias

**Beta:** 2–3 creators UGC (sem cobrança ou trial) antes de escala.

---

## Roadmap técnico (histórico)

| Fase | Objetivo |
|------|----------|
| **0** | Product brief + MVP scope (este doc) |
| **1** | Multi-tenant: 1 creator = 1 IG = 1 media kit |
| **2** | Assinatura + limites por plano |
| **3** | Templates de portfólio (2–3 estilos) |
| **4** | IA coach (melhorias + benchmarks nicho beauty) |
| **5** | Comunidade: círculos + fila + lembretes |
| **6** | Engajamento: aprovação + execução Playwright |
| **7** | Academy: LMS + checkout avulso |
| **8** | White-label / agências |

> **Entregas operacionais (F0–F5):** ver seção abaixo — é a ordem que seguimos na prática.

---

## Entregas por fase (ordem fixa — não pular)

> **Regra:** cada fase só começa quando a anterior está **no ar e validada**. Uma entrega = um marco testável.

| Fase | Nome | Duração ref. | Objetivo | Cobrança |
|------|------|--------------|----------|----------|
| **F0** | Fundação | 1–2 sem | Repo, DB, auth, shell front + admin | Não |
| **F1** | Core SaaS | 4–6 sem | IG + media kit + portfólio + IA + billing | **Sim** |
| **F2** | Academy | 2–3 sem | Cursos C1–C3 + avulso | Sim (+ upsell) |
| **F3** | Comunidade | 3–4 sem | Círculos + fila + lembretes (manual) | No plano |
| **F4** | Engajamento | 4–6 sem | Aprovar + executar + C5 | Pro+ |
| **F5** | Escala | contínuo | Templates, agency, domínio | Planos top |

### F0 — Fundação

- Repo `creator-kit-saas`, Postgres, auth, layout front vazio
- Admin: login Taty + lista usuários (leitura)
- **Saída:** login app + admin em staging

### F1 — Core SaaS (primeiro dinheiro)

**Usuária:** onboarding → pagamento → OAuth IG → dashboard → gerar media kit + portfólio + relatório IA  
**Admin:** usuárias, planos, re-sync, suporte  
**Fora:** círculos, Playwright engajamento, cursos  
**Saída:** 2–3 betas pagantes geram kit sozinhas

### F2 — Academy

**Usuária:** Meus cursos, C1–C3, checkout avulso  
**Admin:** CRUD cursos, matrículas  
**Saída:** 1 compra avulsa ou acesso via Pro

### F3 — Comunidade

**Usuária:** círculo, fila, link manual pro Instagram, score reciprocidade  
**Admin:** CRUD círculos, moderar  
**Saída:** piloto 5–10 pessoas, 2 semanas  
**Fora:** auto curtir/comentar (F4)

### F4 — Engajamento

**Usuária:** autorizar sessão IG, aprovar + executar, histórico  
**Admin:** logs, limites globais  
**Saída:** engajamento aprovado estável 1 semana

### F5 — Escala

Templates, domínio próprio, Agency, app Meta produção, C4 gravado

---

## Front funcional — 3 superfícies

Um projeto **Next.js** com rotas e roles separados:

| URL | Quem | Fase |
|-----|------|------|
| `comjuntas.com.br` | Marketing (landing, preços, cursos) | F1 mínimo: 1 página |
| `app.comjuntas.com.br` | Usuária creator | F0 shell → F1 completo |
| `admin.comjuntas.com.br` | Taty / suporte | F0 mínimo → evolui |

### App usuária — telas por fase

| Área | F1 | F2+ |
|------|----|-----|
| Onboarding (plano + IG) | ✅ | — |
| Dashboard métricas | ✅ | gráficos |
| Media kit + portfólio | ✅ | histórico |
| Relatório IA | ✅ | chat coach |
| Minha conta / billing | ✅ | sessão engajamento |
| Cursos | — | F2 |
| Comunidade / fila | — | F3–F4 |

### Admin — telas por fase

| Tela | Fase |
|------|------|
| Dashboard (MRR, ativos) | F1 |
| Usuárias + assinaturas | F1 |
| Cursos + matrículas | F2 |
| Círculos + moderação | F3 |
| Logs execução IG | F4 |

**Stack:** Next.js + shadcn/ui + Tailwind · Auth Clerk/Supabase · API FastAPI (Python)

---

## Nome do produto — fechado

| Campo | Valor |
|-------|--------|
| **Marca** | **ComJuntas** |
| **Significado** | **Com**unidade + **Juntas** (creators que se apoiam mutuamente) |
| **Instagram** | `@comjuntas` ✅ criado 2026-08-19 |
| **Fundadora** | Tatiana Zacharias — case zero UGC beauty/hair |
| **Bio sugerida** | *ComJuntas · comunidade UGC beauty · media kit, portfólio e apoio mútuo · by Tatiana Zacharias* |
| **Domínio alvo** | `comjuntas.com.br` · `app.` · `admin.` *(registrar — pendente DEC-01)* |
| **Planos (DEC-03)** | Start R$69 · Pro R$129 (+ comunidade + cursos) · Plus TBD — [`PLANOS-LAUNCH.md`](PLANOS-LAUNCH.md) |
| **App Meta** | Pode permanecer técnico (*Taty Manager*); nome comercial é ComJuntas |

**Posicionamento de marca (DEC-06 — parcial):** ComJuntas é a marca; Tatiana é a **fundadora e face** do movimento, não sigla nas iniciais.

**Alternativas descartadas:** Glow Circle (IG ocupado), Lume/Brilho/Círculo (tom poético), TAZ/TZK (sigla forçada), nomes inventados (Kora, Velvi…).

---

## O que mais decidir (checklist mestre)

**Negócio:** ~~Persona~~ ✅ · ~~Planos~~ ✅ · ~~Trial~~ ✅ · ~~Stripe (DEC-05)~~ ✅  
**Legal:** Termos + LGPD (F1); consentimento engajamento (F4); Meta dev vs produção  
**Marca:** logo/cores (derivar do luxe?), ComJuntas + Tatiana como fundadora  
**Ops:** hosting (Vercel + Railway?), suporte (WhatsApp/e-mail), quem modera círculos  
**Métricas:** F1 = 10 pagantes; F2 = vendas curso; F3 = 1 círculo ativo; F4 = 50 engajamentos/semana ok

---

## Posicionamento

- Nicho inicial: **influencer de beleza** (cabelo, makeup, skincare) — UGC **e** creator tradicional
- Persona launch (aquisição F1): **micro 3k–10k** — ver [`PERSONA-01.md`](PERSONA-01.md)
- Proposta: media kit + portfólio + IA + comunidade + cursos (ferramenta + educação)
- Naming: **ComJuntas** (ver seção [Nome do produto — fechado](#nome-do-produto--fechado))

---

## Próximos passos quando retomar

**Agora (F0 — escolher 1 por vez):**

1. ~~**Decidir nome**~~ → **ComJuntas** ✅ · ~~`@comjuntas`~~ ✅ · registrar domínio
2. ~~**Wireframe F1**~~ ✅ — [`FRONT-TELAS.md`](../saas/FRONT-TELAS.md)
3. **Criar repo** `comjuntas-saas` + schema F0/F1
4. **Landing 1 página** + waitlist (opcional antes do billing)

Depois:

5. MVP spec detalhado por fase (este doc = base)
6. Schema SQL completo
7. Spike Playwright (só antes de F4)

---

## Regras herdadas do case Taty (não esquecer)

- PDF media kit: **estrutura aprovada** — não alterar sem pedido explícito
- Hero / layout luxe do portfólio web: idem
- Separar sempre **dados pessoais** (`.env`, `data/sync/`) de código deployável
- Commit/push só quando Taty pedir

---

*Documento criado para retomada futura. Atualizar conforme decisões forem tomadas.*
