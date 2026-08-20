# Dados do roadmap de execução — fonte única para MD + DOCX
# Atualizado: 2026-08-19

from __future__ import annotations

from dataclasses import dataclass, field

# Metadados do documento
AUTHOR = "Tatiana Zacharias"
DOC_VERSION = "V0"
VERSION_DATE = "2026-08-19"

STATUS_LABEL = {
    "todo": "⬜ A fazer",
    "in_progress": "🔄 Em progresso",
    "done": "✅ Concluído",
}


@dataclass
class Task:
    id: str
    title: str
    description: str
    expected_result: str
    acceptance_criteria: list[str]
    dependencies: list[str] = field(default_factory=list)
    status: str = "todo"  # todo | in_progress | done
    criteria_checked: list[bool] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.criteria_checked:
            self.criteria_checked = [False] * len(self.acceptance_criteria)
        elif len(self.criteria_checked) != len(self.acceptance_criteria):
            raise ValueError(f"{self.id}: criteria_checked length mismatch")


@dataclass
class Epic:
    id: str
    title: str
    goal: str
    duration: str
    tasks: list[Task]


EPICS: list[Epic] = [
    Epic(
        id="EPIC-0",
        title="Organização do projeto",
        goal="Workspace e documentação prontos para desenvolver o SaaS.",
        duration="Imediato",
        tasks=[
            Task(
                id="ORG-01",
                title="Abrir pasta oficial no Cursor",
                description="Usar instagram-influencer-agents como workspace principal (código + docs + git).",
                expected_result="Cursor aberto na pasta com scripts/, docs/, .git visíveis.",
                acceptance_criteria=[
                    "Pasta instagram-influencer-agents contém scripts/, docs/, .git",
                    "Árvore contém docs/produto/, docs/saas/, docs/toolkit/",
                    "Cursor aberto nesta pasta (File → Open Folder)",
                ],
                dependencies=[],
                status="in_progress",
                criteria_checked=[True, True, False],
            ),
            Task(
                id="ORG-02",
                title="Limpar pastas duplicadas",
                description="Remover instagram-influencer-agents-github e instagram-influencer-agents-old após confirmar que a pasta principal está completa.",
                expected_result="Apenas uma pasta de projeto no disco.",
                acceptance_criteria=[
                    "Backup -old removido ou arquivado conscientemente",
                    "Cópia -github removida se redundante",
                ],
                dependencies=["ORG-01"],
                status="todo",
                criteria_checked=[False, False],
            ),
            Task(
                id="ORG-03",
                title="Publicar documentação no GitHub",
                description="Commit e push da estrutura docs/ reorganizada e ROADMAP-EXECUCAO.",
                expected_result="GitHub reflete docs/README.md, produto/, saas/, ROADMAP-EXECUCAO.",
                acceptance_criteria=[
                    "docs/ reorganizado localmente (README, produto, saas, toolkit)",
                    "ROADMAP-EXECUCAO.md + .docx gerados (V0)",
                    "git push concluído sem erro",
                    "Arquivos visíveis no repo Tatyssz/instagram-influencer-agents",
                ],
                dependencies=["ORG-01"],
                status="in_progress",
                criteria_checked=[True, True, False, False],
            ),
            Task(
                id="ORG-04",
                title="Documentar visão SaaS e roadmap",
                description="PRODUTO-SAAS-VISAO.md, fases F0–F5, checklist Jira (este documento).",
                expected_result="Planejamento completo versionado em docs/produto/ e docs/saas/.",
                acceptance_criteria=[
                    "docs/produto/PRODUTO-SAAS-VISAO.md completo",
                    "docs/saas/ROADMAP-EXECUCAO com épicos e cards",
                    "docs/README.md índice mestre atualizado",
                ],
                dependencies=[],
                status="done",
                criteria_checked=[True, True, True],
            ),
            Task(
                id="ORG-05",
                title="Sincronizar pasta local com GitHub (Opção B)",
                description="Copiar repo completo para instagram-influencer-agents; eliminar pasta incompleta.",
                expected_result="Uma pasta local com código + git + docs.",
                acceptance_criteria=[
                    "scripts/ e .git presentes na pasta principal",
                    "SYNC-LOCAL.md com instruções",
                ],
                dependencies=[],
                status="done",
                criteria_checked=[True, True],
            ),
        ],
    ),
    Epic(
        id="EPIC-1",
        title="Decisões pré-SaaS",
        goal="Decisões de produto e negócio tomadas antes de codar.",
        duration="1–2 dias",
        tasks=[
            Task(
                id="DEC-01",
                title="Definir nome do produto e domínio",
                description=(
                    "Nome fechado: ComJuntas (Comunidade Juntas). "
                    "Reservar @comjuntas no Instagram e domínio comjuntas.com.br (app. + admin.)."
                ),
                expected_result="Nome fechado + @ Instagram + domínio registrado ou em processo.",
                acceptance_criteria=[
                    "Nome ComJuntas documentado em docs/produto/",
                    "@comjuntas reservado no Instagram",
                    "Domínio comjuntas.com.br definido/reservado",
                ],
                dependencies=["ORG-01"],
                status="in_progress",
                criteria_checked=[True, True, False],
            ),
            Task(
                id="DEC-02",
                title="Definir persona #1",
                description=(
                    "Beauty influencer BR (UGC + creator tradicional). "
                    "Três faixas: A 500–3k, B 3k–10k (prioridade launch), C 10k+."
                ),
                expected_result="Persona escrita com dores, objetivo e willingness to pay.",
                acceptance_criteria=[
                    "1 persona primária escolhida",
                    "Registrada no doc de produto",
                ],
                dependencies=[],
                status="done",
                criteria_checked=[True, True],
            ),
            Task(
                id="DEC-03",
                title="Definir planos no launch",
                description=(
                    "Start R$69 (só ferramenta) + Pro R$129 (hero: + comunidade + cursos). "
                    "Plano Plus/intermediário TBD depois."
                ),
                expected_result="Tabela de planos fechada para F1.",
                acceptance_criteria=[
                    "Planos e limites por plano definidos",
                    "Preços de referência validados",
                ],
                dependencies=["DEC-02"],
                status="done",
                criteria_checked=[True, True],
            ),
            Task(
                id="DEC-04",
                title="Definir modelo de trial",
                description=(
                    "Trial 7 dias com limitações (Start + Pro). "
                    "Cartão obrigatório. Pro+ sem trial. Ver TRIAL-POLICY.md."
                ),
                expected_result="Política de trial documentada.",
                acceptance_criteria=["Decisão única registrada", "Impacto no billing descrito"],
                dependencies=["DEC-03"],
                status="done",
                criteria_checked=[True, True],
            ),
            Task(
                id="DEC-05",
                title="Escolher gateway de pagamento",
                description=(
                    "Stripe principal F1 (assinatura + trial + cursos). "
                    "Mercado Pago PIX opcional F2 para curso avulso. Ver PAYMENT-GATEWAY.md."
                ),
                expected_result="Gateway escolhido + conta criada ou em criação.",
                acceptance_criteria=[
                    "Decisão documentada em docs/saas/PAYMENT-GATEWAY.md",
                    "Conta Stripe teste criada antes de F1-08 (checklist no doc)",
                ],
                dependencies=["DEC-03"],
                status="done",
                criteria_checked=[True, False],
            ),
            Task(
                id="DEC-06",
                title="Definir posicionamento de marca",
                description=(
                    "ComJuntas como marca; Tatiana Zacharias como fundadora/case zero "
                    "(não sigla forçada nas iniciais)."
                ),
                expected_result="Diretriz de marca para landing e comunicação.",
                acceptance_criteria=["Decisão registrada", "Tom de voz definido em 3 bullets"],
                dependencies=["DEC-01"],
                status="in_progress",
                criteria_checked=[True, False],
            ),
            Task(
                id="DEC-07",
                title="Wireframe F1 (app + admin)",
                description="Wireframes textuais: onboarding (Stripe+IG), 5 telas app, 2 admin.",
                expected_result="Wireframes em docs/saas/FRONT-TELAS.md ou Figma link.",
                acceptance_criteria=[
                    "Onboarding, dashboard, media kit, portfólio, conta mapeados",
                    "Admin: lista usuárias + detalhe mapeados",
                ],
                dependencies=["DEC-02", "DEC-03"],
                status="done",
                criteria_checked=[True, True],
            ),
            Task(
                id="DEC-08",
                title="Rascunho legal LGPD",
                description="Termos de Uso e Política de Privacidade mínimos para cobrança.",
                expected_result="Rascunho revisável antes do go-live F1.",
                acceptance_criteria=[
                    "Termos cobrem dados Instagram e cancelamento",
                    "Privacidade cobre LGPD básico",
                ],
                dependencies=["DEC-01"],
            ),
        ],
    ),
    Epic(
        id="EPIC-2",
        title="F0 — Fundação",
        goal="Infra, auth e shell do front em staging. Ainda não cobra.",
        duration="1–2 semanas",
        tasks=[
            Task(
                id="F0-01",
                title="Criar repo comjuntas-saas",
                description="Repositório separado do toolkit Taty; consome scripts como lib ou workers.",
                expected_result="Repo no GitHub com README e estrutura monorepo ou api+web.",
                acceptance_criteria=[
                    "Repo criado e clonável",
                    "README explica relação com instagram-influencer-agents",
                ],
                dependencies=["DEC-01", "DEC-07"],
            ),
            Task(
                id="F0-02",
                title="Postgres + migrations iniciais",
                description="Schema users, subscriptions; Alembic ou equivalente.",
                expected_result="DB provisionado + migration v1 aplicada.",
                acceptance_criteria=[
                    "Tabelas users e subscriptions existem",
                    "Migration versionada no repo",
                ],
                dependencies=["F0-01"],
            ),
            Task(
                id="F0-03",
                title="Auth usuária",
                description="Login email/Google ou magic link (Clerk, Supabase Auth, etc.).",
                expected_result="Usuária cria conta e acessa /app.",
                acceptance_criteria=[
                    "Signup e login funcionam",
                    "Sessão persiste entre reloads",
                ],
                dependencies=["F0-01"],
            ),
            Task(
                id="F0-04",
                title="Auth admin",
                description="Role admin para Taty; rota /admin protegida.",
                expected_result="Apenas admin acessa painel administrativo.",
                acceptance_criteria=[
                    "Usuária comum não acessa /admin",
                    "Admin loga com credencial separada ou role",
                ],
                dependencies=["F0-03"],
            ),
            Task(
                id="F0-05",
                title="Shell Next.js (marketing + app + admin)",
                description="Layout base, navegação, rotas vazias com placeholder.",
                expected_result="3 superfícies routáveis em staging.",
                acceptance_criteria=[
                    "Landing 1 página renderiza",
                    "/app e /admin com layout sidebar",
                ],
                dependencies=["F0-03", "F0-04"],
            ),
            Task(
                id="F0-06",
                title="API FastAPI esqueleto",
                description="Health check, auth middleware, estrutura de routers.",
                expected_result="API responde /health em staging.",
                acceptance_criteria=["Deploy API funcional", "Auth integrado com front"],
                dependencies=["F0-01"],
            ),
            Task(
                id="F0-07",
                title="Deploy staging",
                description="Vercel (front) + Railway/Fly (API) + Postgres managed.",
                expected_result="URLs staging compartilháveis.",
                acceptance_criteria=[
                    "Front e API acessíveis via HTTPS",
                    "Variáveis de ambiente documentadas",
                ],
                dependencies=["F0-05", "F0-06", "F0-02"],
            ),
            Task(
                id="F0-08",
                title="Critério de saída F0",
                description="Validação end-to-end do foundation.",
                expected_result="Taty loga app + admin em staging.",
                acceptance_criteria=[
                    "Demo gravada ou checklist assinado",
                    "docs/saas/ARQUITETURA.md preenchido",
                ],
                dependencies=["F0-07"],
            ),
        ],
    ),
    Epic(
        id="EPIC-3",
        title="F1 — Core SaaS (primeira cobrança)",
        goal="Creator paga e gera media kit + portfólio + IA sozinha.",
        duration="4–6 semanas",
        tasks=[
            Task(
                id="F1-01",
                title="Onboarding + seleção de plano",
                description="Fluxo criar conta → escolher Starter/Pro → checkout.",
                expected_result="Nova usuária completa onboarding sem suporte manual.",
                acceptance_criteria=["Fluxo < 5 minutos", "Erros tratados com mensagem clara"],
                dependencies=["F0-08", "DEC-05"],
            ),
            Task(
                id="F1-02",
                title="Integração billing recorrente",
                description="Stripe ou MP webhooks: active, canceled, past_due.",
                expected_result="Assinatura ativa libera features; cancelada bloqueia.",
                acceptance_criteria=[
                    "Webhook testado em sandbox",
                    "Status sync com tabela subscriptions",
                ],
                dependencies=["F1-01"],
            ),
            Task(
                id="F1-03",
                title="OAuth Instagram multi-tenant",
                description="Cada usuária conecta IG; token criptografado por tenant.",
                expected_result="Botão Conectar Instagram funciona por usuária.",
                acceptance_criteria=[
                    "Token salvo criptografado",
                    "Reconectar fluxo documentado",
                ],
                dependencies=["F0-08"],
            ),
            Task(
                id="F1-04",
                title="Worker sync automático",
                description="Job sync posts + insights após OAuth ou agendado.",
                expected_result="Dashboard mostra dados reais do IG conectado.",
                acceptance_criteria=[
                    "Sync completa em < 5 min para perfil típico",
                    "Falha registrada e visível no admin",
                ],
                dependencies=["F1-03"],
            ),
            Task(
                id="F1-05",
                title="Dashboard métricas",
                description="Seguidores, alcance, engajamento resumido.",
                expected_result="Usuária vê métricas após sync.",
                acceptance_criteria=["Métricas batem com API Meta", "Estado vazio se sem IG"],
                dependencies=["F1-04"],
            ),
            Task(
                id="F1-06",
                title="Gerar media kit PDF + link",
                description="Reutilizar pipeline mediakit do toolkit por tenant.",
                expected_result="PDF gerado + URL pública única.",
                acceptance_criteria=[
                    "PDF abre e números correspondem ao sync",
                    "Regenerar sobrescreve versão ou versiona",
                ],
                dependencies=["F1-04"],
            ),
            Task(
                id="F1-07",
                title="Gerar portfólio web + link",
                description="Template luxe fixo; hosting por tenant (subpath/subdomínio).",
                expected_result="Link público do portfólio funcional.",
                acceptance_criteria=["Mobile responsive", "Link compartilhável"],
                dependencies=["F1-04"],
            ),
            Task(
                id="F1-08",
                title="Relatório IA",
                description="Análise pontos fortes + melhorias a partir do sync.",
                expected_result="Texto estruturado gerado sob demanda.",
                acceptance_criteria=[
                    "Relatório em português",
                    "Baseado em dados reais do sync",
                ],
                dependencies=["F1-04"],
            ),
            Task(
                id="F1-09",
                title="Página Minha conta",
                description="Plano, billing portal, cancelar, reconectar IG.",
                expected_result="Usuária autogere assinatura e conexão IG.",
                acceptance_criteria=[
                    "Link para portal de pagamento",
                    "Desconectar IG remove token",
                ],
                dependencies=["F1-02", "F1-03"],
            ),
            Task(
                id="F1-10",
                title="Admin — lista e detalhe usuárias",
                description="Suporte: ver plano, sync, reprocessar jobs.",
                expected_result="Admin resolve 80% tickets sem código.",
                acceptance_criteria=[
                    "Lista paginada de usuárias",
                    "Botão re-sync funcional",
                ],
                dependencies=["F1-04", "F0-04"],
            ),
            Task(
                id="F1-11",
                title="Publicar Termos + Privacidade",
                description="Páginas legais linkadas no signup e footer.",
                expected_result="Compliance mínimo LGPD no ar.",
                acceptance_criteria=["Links no onboarding", "DEC-08 incorporado"],
                dependencies=["DEC-08", "F1-01"],
            ),
            Task(
                id="F1-12",
                title="Beta pago 2–3 creators",
                description="Recrutar UGC beauty; cobrar preço beta.",
                expected_result="2–3 pagantes usando produto sem você operar manual.",
                acceptance_criteria=[
                    "Cada beta gera kit + portfólio sozinha",
                    "Feedback coletado",
                ],
                dependencies=["F1-06", "F1-07", "F1-08", "F1-02"],
            ),
            Task(
                id="F1-13",
                title="Critério de saída F1 — 10 pagantes",
                description="North star F1: escala inicial de receita.",
                expected_result="10 assinantes pagantes ativos.",
                acceptance_criteria=[
                    "MRR registrado",
                    "Churn documentado",
                ],
                dependencies=["F1-12"],
            ),
        ],
    ),
    Epic(
        id="EPIC-4",
        title="F2 — Academy",
        goal="Cursos C1–C3 no painel + venda avulsa.",
        duration="2–3 semanas",
        tasks=[
            Task(
                id="F2-01",
                title="Área Meus cursos",
                description="Listagem de cursos matriculados + progresso.",
                expected_result="Usuária vê cursos do plano ou comprados.",
                acceptance_criteria=["Estado vazio amigável", "Progresso % se habilitado"],
                dependencies=["F1-13"],
            ),
            Task(
                id="F2-02",
                title="Conteúdo C1 — Meta API",
                description="Migrar módulos 1–2 do CURSO-PASSO-A-PASSO para aulas.",
                expected_result="C1 navegável no painel.",
                acceptance_criteria=["≥5 aulas", "Markdown ou vídeo embed"],
                dependencies=["F2-01"],
            ),
            Task(
                id="F2-03",
                title="Conteúdo C2 — Bio + automação",
                description="Módulos 3–4 do curso em aulas.",
                expected_result="C2 navegável no painel.",
                acceptance_criteria=["≥4 aulas", "Links para toolkit quando relevante"],
                dependencies=["F2-01"],
            ),
            Task(
                id="F2-04",
                title="Conteúdo C3 — Media Kit & Portfólio",
                description="Módulo 5 / Fase 7 do curso em aulas.",
                expected_result="C3 navegável no painel.",
                acceptance_criteria=["Case Taty referenciado", "Passo a passo reproduzível"],
                dependencies=["F2-01"],
            ),
            Task(
                id="F2-05",
                title="Checkout avulso + bundle",
                description="Compra one-time por curso; bundle C1+C2+C3.",
                expected_result="Não-assinante compra curso e acessa.",
                acceptance_criteria=[
                    "Webhook compra avulsa",
                    "course_enrollments criado",
                ],
                dependencies=["F2-01", "DEC-05"],
            ),
            Task(
                id="F2-06",
                title="Admin cursos e matrículas",
                description="CRUD cursos; ver quem comprou o quê.",
                expected_result="Taty publica/despublica curso sem deploy.",
                acceptance_criteria=["CRUD mínimo funcional", "Lista matrículas exportável"],
                dependencies=["F2-02"],
            ),
            Task(
                id="F2-07",
                title="Critério de saída F2",
                description="1 compra avulsa OU Pro acessa C1–C3.",
                expected_result="Receita de curso ou upsell comprovado.",
                acceptance_criteria=["1 transação avulsa real ou 3 Pro com acesso"],
                dependencies=["F2-05", "F2-02", "F2-03", "F2-04"],
            ),
        ],
    ),
    Epic(
        id="EPIC-5",
        title="F3 — Comunidade (lembretes)",
        goal="Círculos + fila; engajamento manual no Instagram.",
        duration="3–4 semanas",
        tasks=[
            Task(
                id="F3-01",
                title="CRUD círculos (admin)",
                description="Criar círculo, nicho, limite de membros, convites.",
                expected_result="Admin gerencia círculos fechados.",
                acceptance_criteria=["Círculo criado", "Convite por link ou e-mail"],
                dependencies=["F1-13"],
            ),
            Task(
                id="F3-02",
                title="Entrada e saída de membros",
                description="Usuária aceita convite; admin remove membro.",
                expected_result="Membros vinculados a circle_members.",
                acceptance_criteria=["Opt-in explícito", "Saída imediata"],
                dependencies=["F3-01"],
            ),
            Task(
                id="F3-03",
                title="Detectar posts da comunidade",
                description="Sync identifica post novo de membro do círculo.",
                expected_result="engagement_queue populada automaticamente.",
                acceptance_criteria=[
                    "Post detectado em < 24h",
                    "Não duplica mesmo post",
                ],
                dependencies=["F3-02", "F1-04"],
            ),
            Task(
                id="F3-04",
                title="Fila Engajar hoje + deep link",
                description="Lista posts pendentes; botão abre Instagram.",
                expected_result="Usuária sabe o que engajar hoje.",
                acceptance_criteria=["Link abre post correto", "Marcar como feito manual"],
                dependencies=["F3-03"],
            ),
            Task(
                id="F3-05",
                title="Score de reciprocidade",
                description="Quem deu X / recebeu Y; alerta desequilíbrio.",
                expected_result="Dashboard reciprocidade por membro.",
                acceptance_criteria=[
                    "Score atualiza ao marcar feito",
                    "Regra documentada para remoção",
                ],
                dependencies=["F3-04"],
            ),
            Task(
                id="F3-06",
                title="Notificações",
                description="E-mail ou WhatsApp: posts esperando engajamento.",
                expected_result="Membro avisado sem abrir painel.",
                acceptance_criteria=["Opt-in notificação", "Rate limit diário"],
                dependencies=["F3-04"],
            ),
            Task(
                id="F3-07",
                title="Piloto 5–10 creators — 2 semanas",
                description="Círculo real UGC beauty monitorado.",
                expected_result="Grupo usa fila consistentemente.",
                acceptance_criteria=[
                    "≥80% membros engajaram na semana",
                    "Feedback qualitativo coletado",
                ],
                dependencies=["F3-05", "F3-06"],
            ),
        ],
    ),
    Epic(
        id="EPIC-6",
        title="F4 — Engajamento com aprovação",
        goal="Aprovar → executar curtir/comentar via Playwright.",
        duration="4–6 semanas",
        tasks=[
            Task(
                id="F4-01",
                title="Autorizar sessão Instagram",
                description="Fluxo seguro; cookies criptografados; nunca senha em texto.",
                expected_result="Usuária autoriza engajamento uma vez.",
                acceptance_criteria=[
                    "Consentimento nos Termos",
                    "Renovar sessão quando expirar",
                ],
                dependencies=["F3-07"],
            ),
            Task(
                id="F4-02",
                title="Sugestão IA de comentário",
                description="IA gera comentário variado; usuária edita antes de aprovar.",
                expected_result="Comentário editável na fila.",
                acceptance_criteria=["Não repetitivo", "Tom beauty/UGC"],
                dependencies=["F3-04"],
            ),
            Task(
                id="F4-03",
                title="Aprovar e executar",
                description="Estados pending → approved → executing → done/failed.",
                expected_result="Ação executada após clique explícito.",
                acceptance_criteria=[
                    "Sem execução sem approved",
                    "Lote opcional limitado",
                ],
                dependencies=["F4-01", "F4-02"],
            ),
            Task(
                id="F4-04",
                title="Worker Playwright",
                description="Executor isolado; limites diários e intervalo entre ações.",
                expected_result="Curtir + comentar no post alheio.",
                acceptance_criteria=[
                    "Log completo por ação",
                    "Para em session_expired",
                ],
                dependencies=["F4-03"],
            ),
            Task(
                id="F4-05",
                title="Admin logs e limites globais",
                description="Auditoria; caps por plano; alertas falha em massa.",
                expected_result="Ops consegue investigar incidentes.",
                acceptance_criteria=["Logs 30 dias", "Limites configuráveis"],
                dependencies=["F4-04"],
            ),
            Task(
                id="F4-06",
                title="Curso C5 + critério de saída F4",
                description="Material comunidade; 1 semana estável sem ban.",
                expected_result="50 engajamentos/semana ok no piloto.",
                acceptance_criteria=[
                    "C5 publicado ou outline",
                    "Zero incidentes críticos 7 dias",
                ],
                dependencies=["F4-04", "F4-05"],
            ),
        ],
    ),
    Epic(
        id="EPIC-7",
        title="F5 — Escala",
        goal="PMF: templates, agency, domínio, Meta produção.",
        duration="Contínuo",
        tasks=[
            Task(
                id="F5-01",
                title="Múltiplos templates portfólio",
                description="2–3 estilos além do luxe.",
                expected_result="Usuária escolhe template no painel.",
                acceptance_criteria=["Preview antes de publicar"],
                dependencies=["F1-13"],
            ),
            Task(
                id="F5-02",
                title="Domínio customizado",
                description="Creator usa domínio próprio no portfólio.",
                expected_result="DNS + SSL automatizado.",
                acceptance_criteria=["Plano superior only", "Doc setup usuária"],
                dependencies=["F5-01"],
            ),
            Task(
                id="F5-03",
                title="Plano Agency / white-label",
                description="N contas; círculos privados agência.",
                expected_result="Oferta B2B documentada e vendável.",
                acceptance_criteria=["Pricing agency", "Multi-tenant agency role"],
                dependencies=["F4-06"],
            ),
            Task(
                id="F5-04",
                title="App Meta modo produção",
                description="Review Meta; escala além de testadores.",
                expected_result="App aprovado produção.",
                acceptance_criteria=["Business verification se exigido"],
                dependencies=["F1-13"],
            ),
            Task(
                id="F5-05",
                title="Curso C4 — Fechar parcerias",
                description="Pacotes comerciais, proposta, pricing para marcas.",
                expected_result="C4 no Academy.",
                acceptance_criteria=["Alinhado a template proposta marcas"],
                dependencies=["F2-07"],
            ),
            Task(
                id="F5-06",
                title="IA coach avançada",
                description="Benchmarks nicho beauty; chat coach.",
                expected_result="Diferencial Pro+ claro.",
                acceptance_criteria=["Respostas grounded em sync"],
                dependencies=["F1-08"],
            ),
        ],
    ),
    Epic(
        id="EPIC-P",
        title="Toolkit Taty (paralelo — case pessoal)",
        goal="Manter case @tatyzacharias; motor do produto.",
        duration="Paralelo ao SaaS",
        tasks=[
            Task(
                id="TK-01",
                title="Bio linhas 2–4 + link + CTA",
                description="Completar otimização bio case Taty item a item.",
                expected_result="Bio comercial completa aprovada.",
                acceptance_criteria=["≤150 chars", "Aplicado no IG"],
                dependencies=[],
            ),
            Task(
                id="TK-02",
                title="Validador 150 chars no update_profile",
                description="Bloquear apply se bio exceder limite Instagram.",
                expected_result="CLI valida antes de Playwright.",
                acceptance_criteria=["Teste unitário ou manual documentado"],
                dependencies=[],
            ),
            Task(
                id="TK-03",
                title="Playwright submit confiável",
                description="100% sucesso em apply bio/nome quando UI Meta estável.",
                expected_result="apply + verify passam consistentemente.",
                acceptance_criteria=["3 runs seguidos OK"],
                dependencies=[],
            ),
            Task(
                id="TK-04",
                title="Template proposta para marcas",
                description="Documento/PDF proposta comercial UGC.",
                expected_result="Template reutilizável para C4.",
                acceptance_criteria=["Usado em 1 outreach real"],
                dependencies=[],
            ),
            Task(
                id="TK-05",
                title="Gravar curso em vídeo (C1–C3)",
                description="Opcional; complementa material texto.",
                expected_result="Vídeos hospedados e linkados no Academy.",
                acceptance_criteria=["≥1 módulo gravado"],
                dependencies=["F2-01"],
            ),
            Task(
                id="TK-06",
                title="Regra: media kit Taty layout bloqueado",
                description="Não alterar PDF/portfólio aprovado sem pedido explícito Taty.",
                expected_result="Zero regressão visual case pessoal.",
                acceptance_criteria=[
                    "Regra documentada em PRODUTO-SAAS-VISAO e user rules",
                    "Checklist release inclui regra",
                ],
                dependencies=[],
                status="done",
                criteria_checked=[True, True],
            ),
        ],
    ),
]

# Concluído no toolkit antes do SaaS (pré-requisitos — não são cards de épico)
PREREQUISITES_DONE: list[str] = [
    "Meta API — OAuth + sync Instagram (instagram-influencer-agents)",
    "Media kit PDF layout glow + portfólio web luxe (@tatyzacharias)",
    "Deploy portfólio: tatiana-zacharias-portfolio.netlify.app/ugc/",
    "docs/toolkit/CURSO-PASSO-A-PASSO.md (material Academy C1–C3)",
    "docs/toolkit/MEDIA-KIT-CURADORIA.md",
    "Nome/bio otimizados parcialmente (itens 1–2 da bio)",
    "Automação Playwright perfil (parcial — base F4)",
]
