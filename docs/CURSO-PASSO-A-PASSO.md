# Curso: Instagram + Cursor + Meta API para Influenciadoras

**Projeto real:** @tatyzacharias — UGC Beauty & Hair · Baixada Santista  
**Objetivo:** Conectar o Instagram à Meta API, analisar dados reais e otimizar o perfil para receber propostas pagas de marcas.  
**Ferramentas:** Cursor IDE, Python, Meta Graph API, Playwright (opcional).  
**Data de referência:** agosto/2026

---

## Sumário

1. [Visão geral do que construímos](#1-visão-geral-do-que-construímos)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Fase 1 — Criar app na Meta Developers](#3-fase-1--criar-app-na-meta-developers)
4. [Fase 2 — Montar o projeto no Cursor](#4-fase-2--montar-o-projeto-no-cursor)
5. [Fase 3 — OAuth e sincronização de dados](#5-fase-3--oauth-e-sincronização-de-dados)
6. [Fase 4 — Análise do perfil (dados reais)](#6-fase-4--análise-do-perfil-dados-reais)
7. [Fase 5 — Otimizar bio (item por item)](#7-fase-5--otimizar-bio-item-por-item)
8. [Fase 6 — Automação de edição de perfil](#8-fase-6--automação-de-edição-de-perfil)
9. [Erros comuns e como resolver](#9-erros-comuns-e-como-resolver)
10. [O que a API faz e não faz](#10-o-que-a-api-faz-e-não-faz)
11. [Comandos de referência](#11-comandos-de-referência)
12. [Estrutura de arquivos do projeto](#12-estrutura-de-arquivos-do-projeto)
13. [Próximos módulos do curso](#13-próximos-módulos-do-curso)
14. [Checklist para gravar o curso](#14-checklist-para-gravar-o-curso)

---

## 1. Visão geral do que construímos

### Problema inicial

A influenciadora queria **ver tudo do Instagram** (posts, números, audiência, horários) e **enriquecer o perfil** para receber trabalhos pagos — usando o Cursor como “central de agentes”, sem fazer tudo manualmente.

### Solução em camadas (incremental)

| Camada | O que faz | Status |
|--------|-----------|--------|
| **Meta API (oficial)** | Lê perfil, posts recentes, insights | ✅ Funcionando |
| **Análise no chat** | Diagnóstico + recomendações para marcas | ✅ Feito |
| **Otimização de bio** | Um item por vez, com aprovação | 🔄 Em andamento |
| **Automação Playwright** | Edita perfil no browser (API não permite) | 🔄 Em teste |
| **Media Kit automático** | PDF/página com números reais | ⏳ Próximo módulo |

### Resultados já aplicados no perfil @tatyzacharias

| Item | Antes | Depois |
|------|-------|--------|
| **Nome de exibição** | Taty Zacharias | Taty Zacharias \| UGC Beauty & Hair |
| **Bio — linha 1** | Crio histórias AUTÊNTICAS para marcas… | Histórias reais de beleza & cabelo para marcas que valorizam diversidade 🌟 |
| **Bio — linhas 2–4** | (mantidas por enquanto) | Seu cabelo, Suas regras💥 / #lorealistarbr / 📍013 Baixada Santista #sl |

### Números do perfil (sync 11/08/2026)

- **Seguidores:** 32.670
- **Posts totais:** 834
- **Tipo de conta:** Creator (MEDIA_CREATOR)
- **Programa:** L'Oréal Star (#lorealistarbr)
- **Local:** Baixada Santista (013)
- **Posts analisados na API:** 30 Reels mais recentes
- **Insights do período:** reach 889 · views 1.003

---

## 2. Pré-requisitos

### Conta Instagram

- Conta **Creator** ou **Business**
- Idealmente vinculada a uma **Página do Facebook**
- Perfil profissional ativo (no caso: 834 posts, 32k+ seguidores)

### Ferramentas no computador

- **Cursor IDE** instalado
- **Python 3.12+** (instalado via [python.org](https://www.python.org/downloads/) ou `winget install Python.Python.3.12`)
- Marcar **"Add python.exe to PATH"** na instalação
- Conta em [developers.facebook.com](https://developers.facebook.com)

### Conhecimentos úteis (não obrigatório)

- Terminal básico (PowerShell)
- Noções de OAuth / tokens de API
- Copiar/colar comandos no Cursor

---

## 3. Fase 1 — Criar app na Meta Developers

> **Tempo estimado:** 30–60 min (primeira vez)  
> **Frequência:** uma vez só

### Passo 3.1 — Criar o aplicativo

1. Acesse [developers.facebook.com/apps](https://developers.facebook.com/apps)
2. **Criar aplicativo** → tipo **Outros** → **Business**
3. Nome sugerido: `Taty Manager` (ou nome da marca)
4. Portfólio empresarial: vincular ao portfólio da creator

### Passo 3.2 — Adicionar produto Instagram

1. Painel do app → **Adicionar produtos**
2. Escolher **Instagram** → **Configurar**
3. Caso de uso: **Gerenciar mensagens e conteúdo no Instagram**

### Passo 3.3 — Credenciais importantes (dois IDs diferentes!)

| Variável | Onde encontrar | Uso |
|----------|----------------|-----|
| `META_APP_ID` | Configurações do app → Básico | ID do app Facebook |
| `INSTAGRAM_APP_ID` | Instagram → API setup with Instagram login → Business login settings | **Obrigatório para OAuth Instagram** |
| `INSTAGRAM_APP_SECRET` | Mesma tela acima | Troca de código por token |

> ⚠️ **Erro clássico:** usar só o Facebook App ID no OAuth Instagram → `"Invalid platform app"`.  
> **Solução:** usar o **Instagram App ID** separado.

### Passo 3.4 — Redirect URI

Em **Business login settings** (Instagram Login):

```
https://localhost:8765/callback
```

> ⚠️ Meta **rejeita** `http://` — tem que ser **`https://`**.  
> O erro SSL ao abrir `https://localhost:8765/callback` **é esperado** — o código vem na URL.

### Passo 3.5 — Permissões (scopes 2025+)

Scopes atuais (jan/2025+, substituem os antigos):

```
instagram_business_basic
instagram_business_manage_insights
```

Scopes antigos **descontinuados:** `instagram_basic`, `instagram_manage_insights`, etc.

### Passo 3.6 — Testador do Instagram (modo desenvolvimento)

Enquanto o app não está publicado, só testadores autorizam.

1. App → **Funções do app** → **Mais** → **Testadores do Instagram**
2. Adicionar `@tatyzacharias`
3. No Instagram (celular): **Configurações** → **Apps e sites** → **Convites do testador** → **Aceitar**

> ⚠️ Erro **"Função de desenvolvedor insuficiente"** → falta este passo.

### Passo 3.7 — Duplicatas de app

Durante a configuração, podem aparecer **vários apps com o mesmo nome**.  
Usar **apenas um** ID consistente em todo o projeto (ex.: `SEU_META_APP_ID`).

---

## 4. Fase 2 — Montar o projeto no Cursor

> **Pasta do projeto:** `instagram-influencer-agents/`

### Passo 4.1 — Estrutura inicial

```
instagram-influencer-agents/
├── .env                    # credenciais (NÃO commitar)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── scripts/
│   ├── sync_instagram.py   # OAuth + sync API
│   ├── update_profile.py   # editar perfil (semi/auto)
│   └── instagram_browser.py # Playwright
├── data/
│   ├── sync/               # dados da API
│   └── profile/            # alvos de bio + sessão browser
└── docs/
    └── CURSO-PASSO-A-PASSO.md  # este documento
```

### Passo 4.2 — Criar ambiente Python

```powershell
cd "c:\Users\taty_\OneDrive\Desktop\Projetos Cursor\instagram-influencer-agents"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Dependências:**

```
requests>=2.31.0
python-dotenv>=1.0.0
playwright>=1.49.0
```

### Passo 4.3 — Configurar `.env`

Copiar `.env.example` → `.env` e preencher:

```env
META_APP_ID=seu_meta_app_id
INSTAGRAM_APP_ID=seu_instagram_app_id
INSTAGRAM_APP_SECRET=sua_chave_aqui
OAUTH_REDIRECT_URI=https://localhost:8765/callback

# Preenchidos automaticamente após auth:
META_ACCESS_TOKEN=
IG_USER_ID=
```

### Passo 4.4 — Segurança

- `.env` está no `.gitignore`
- **Nunca** commitar tokens ou secrets
- **Nunca** compartilhar prints do `.env` em chat público
- Se expôs o secret em print → **rotacionar** no Meta Developers

---

## 5. Fase 3 — OAuth e sincronização de dados

### Passo 5.1 — Autorizar (primeira vez)

```powershell
.venv\Scripts\python scripts/sync_instagram.py auth
```

**O que acontece:**

1. Abre browser na URL OAuth do Instagram (`instagram.com/oauth/authorize`)
2. Login como @tatyzacharias → **Permitir**
3. Browser mostra erro SSL em `https://localhost:8765/callback?code=...` → **normal**
4. Copiar **URL inteira** da barra de endereço
5. Rodar:

```powershell
.venv\Scripts\python scripts/sync_instagram.py exchange "URL_COPIADA_COM_CODE"
```

6. Token long-lived e `IG_USER_ID` salvos no `.env`

### Passo 5.2 — Sincronizar dados

```powershell
.venv\Scripts\python scripts/sync_instagram.py sync
```

**Arquivos gerados:**

| Arquivo | Conteúdo |
|---------|----------|
| `data/sync/profile_snapshot.json` | Perfil completo + 30 posts + insights |
| `data/sync/resumo.txt` | Resumo legível |

### Passo 5.3 — Endpoints usados (Instagram API with Instagram Login)

| Ação | Endpoint |
|------|----------|
| Perfil | `GET graph.instagram.com/v21.0/{IG_USER_ID}?fields=...` |
| Posts | `GET graph.instagram.com/v21.0/{IG_USER_ID}/media` |
| Insights post | `GET graph.instagram.com/v21.0/{media_id}/insights` |
| Insights conta | `GET graph.instagram.com/v21.0/{IG_USER_ID}/insights` |

### Passo 5.4 — Renovar token (~60 dias)

```powershell
.venv\Scripts\python scripts/sync_instagram.py auth
```

(Repetir fluxo exchange se SSL falhar.)

---

## 6. Fase 4 — Análise do perfil (dados reais)

> **Prompt usado no Cursor:**  
> *"Veja tudo que já fiz no Instagram — posts, números, quem vê, data e horário — para enriquecer meu perfil para propostas pagas."*

### 6.1 — Pilares de conteúdo identificados (30 Reels)

| Pilar | ~% | Exemplos |
|-------|-----|---------|
| **UGC / marcas** | 40% | Elseve, Dailus, Salon Line, KV Makeup, Haskell |
| **Humor / viral** | 35% | Trends, shares altos (1000+ compartilhamentos) |
| **Lifestyle / pessoal** | 25% | Família, autoestima, representatividade |

### 6.2 — Métricas-chave para vender parcerias

- **Taxa de engajamento (amostra):** ~0,32% (curtidas+comentários / seguidores / post)
- **Superpoder:** **shares** (alcance orgânico além dos seguidores)
- **Melhor horário de postagem (inferido):** **12h BRT**, especialmente quinta e sábado
- **Top view:** conteúdo de identidade/representatividade (11k views)
- **Top UGC:** vídeo seletiva Jacobs (462 curtidas, 123 comentários)

### 6.3 — Pontos fortes comerciais

1. L'Oréal Star (#lorealistarbr)
2. 834 posts = consistência
3. 32,6k seguidores = sweet spot para marcas nacionais/regionais
4. Nicho cabelo cacheado + pele negra = representatividade
5. Baixada Santista = regional + Beauty Fair
6. Histórico com Elseve, Dailus, Salon Line, KVMakeup

### 6.4 — O que ainda falta nos dados

| Dado | Como obter |
|------|------------|
| Demografia (idade, gênero, cidades) | Print Insights → Audiência no app |
| Histórico completo (834 posts) | Export Instagram ou paginação API |
| Horário audiência online | Insights do app (não inferido por posts) |

### 6.5 — Frase-resumo para marcas

> *Taty Zacharias — 32,6k | Creator L'Oréal Star | UGC beauty & hair cacheado | Baixada Santista | Reels com alto compartilhamento e campanhas Elseve, Dailus, Salon Line, KV Makeup.*

---

## 7. Fase 5 — Otimizar bio (item por item)

> **Metodologia:** espelhar influenciadoras negras de sucesso (Brasil + referências internacionais).  
> **Regra:** **um item por vez** + **aprovação antes de aplicar**.  
> **Limite Instagram:** bio = **150 caracteres** (inclui quebras de linha e emojis).

### Ordem de otimização do perfil

| # | Item | Campo no Instagram |
|---|------|-------------------|
| 1 | Nome de exibição (negrito acima do @) | Nome |
| 2 | Primeira linha da bio (gancho) | Bio |
| 3 | Segunda linha (credencial / CTA) | Bio |
| 4 | Terceira linha (prova social) | Bio |
| 5 | Quarta linha (local / link) | Bio |
| 6 | Link na bio | Site |
| 7 | Destaques (Highlights) | — |
| 8 | Categoria profissional | — |

---

### Item 1 — Nome de exibição ✅ APROVADO E APLICADO

**Opções apresentadas:**

| Opção | Texto |
|-------|-------|
| A (escolhida) | Taty Zacharias \| UGC Beauty & Hair |
| B | Taty Zacharias \| L'Oréal Star ✨ |
| C | Taty Zacharias \| Beauty 013 🌊 |

**Por quê:** influenciadoras profissionais colocam **nicho + formato** no nome (buscável no Instagram).

**Aplicação:** manual no celular (primeira tentativa de automação ainda não existia).  
**Verificação:** `python scripts/update_profile.py verify name` → ✅ confirmado via API.

---

### Item 2 — Primeira linha da bio ✅ APROVADO E APLICADO

**Bio antes (linha 1):**
> Crio histórias AUTÊNTICAS para marcas que desejam se destacar com seu público🌟

**Opções apresentadas:**

| Opção | Texto |
|-------|-------|
| A | UGC Creator \| Beleza & Cabelo cacheado ✨ |
| B | L'Oréal Star \| Conteúdo que converte para marcas 💄 |
| C (escolhida) | Histórias reais de beleza & cabelo para marcas que valorizam diversidade 🌟 |

**Bio completa após Item 2 (141 caracteres — dentro do limite):**

```
Histórias reais de beleza & cabelo para marcas que valorizam diversidade 🌟
Seu cabelo, Suas regras💥
#lorealistarbr 
📍013 Baixada Santista #sl
```

**Verificação:** `verify biography` → ✅ confirmado via API.

---

### Item 3 — Segunda linha da bio ⏳ PENDENTE APROVAÇÃO

**Proposta inicial (REJEITADA — estourou 150 chars):**

```
L'Oréal Star ✨ | Parcerias e UGC para marcas
```

- Bio total ficaria ~**158–163 caracteres** ❌
- **Lição:** sempre contar caracteres **antes** de aplicar

**Opções corrigidas (≤ 150 chars totais):**

| Opção | Linha 2 | Total estimado |
|-------|---------|----------------|
| A | L'Oréal Star ✨ \| Parcerias | ~148 |
| B | UGC · L'Oréal Star ✨ | ~139 |
| C | Parcerias via DM 💌 | ~138 |
| D | Manter `Seu cabelo, Suas regras💥` | 141 |

**Regra do curso:** IA propõe → aluna aprova → só então aplica.

---

## 8. Fase 6 — Automação de edição de perfil

### Por que precisamos disso?

A **Meta API não permite editar** nome, bio ou link (só leitura).  
Para a creator não colar tudo manualmente no celular, implementamos **duas camadas**:

| Modo | Comando | Quem executa |
|------|---------|--------------|
| **Semi-automático** | `apply --manual` | Copia texto + abre página de edição |
| **Playwright (browser)** | `apply` | Script preenche e clica Enviar no PC |

### Fluxo de aprovação (regra de ouro)

```
1. IA propõe texto + contagem de caracteres
2. Aluna responde "aprovado" ou escolhe opção
3. IA atualiza data/profile/target.json
4. IA roda apply (browser) ou aluna cola no celular
5. IA roda verify e confirma via API
```

### Comandos — update_profile.py

```powershell
# Login 1x no Chrome (sessão salva)
.venv\Scripts\python scripts/update_profile.py login

# Ver o que falta aplicar
.venv\Scripts\python scripts/update_profile.py status

# Aplicar via browser (automático)
.venv\Scripts\python scripts/update_profile.py apply
.venv\Scripts\python scripts/update_profile.py apply biography

# Modo manual (copiar/colar)
.venv\Scripts\python scripts/update_profile.py apply --manual

# Confirmar se salvou no Instagram
.venv\Scripts\python scripts/update_profile.py verify
.venv\Scripts\python scripts/update_profile.py verify name
```

### Arquivo de alvo — `data/profile/target.json`

```json
{
  "name": "Taty Zacharias | UGC Beauty & Hair",
  "biography": "...(bio completa, max 150 chars)...",
  "website": null
}
```

Campos `null` = ainda não definidos.

### Playwright — setup e troubleshooting

**Instalação do Chrome (~200 MB, 1x):**

```powershell
.venv\Scripts\python -m playwright install chromium
```

Chrome instalado em: `%LOCALAPPDATA%\tatyzacharias-playwright\`

**Sessão do browser salva em:** `data/profile/browser_profile/` (não commitar)

**Erros encontrados e soluções:**

| Erro | Causa | Solução |
|------|-------|---------|
| `Executable doesn't exist ... chrome.exe` | Chrome Playwright não instalado no PC da aluna | `python -m playwright install chromium` |
| Clipboard não vai pro celular | Áreas de transferência separadas | Copiar do chat ou OneDrive `apply_pendente.txt` |
| Navigation interrupted | Instagram redireciona via home | Script corrigido com retries em `_goto_edit_page` |
| Campo bio não encontrado | UI nova do Instagram usa `#pepBio` | Seletores atualizados |
| Botão Enviar desabilitado | Instagram exige input real (React) | Usar `press_sequentially` em vez de `fill` |

### Limitações da automação browser

- Funciona no **PC** (Chrome controlado pelo script)
- Instagram pode mudar layout → seletores precisam atualização
- Campo **Nome** na web nova pode não estar em `accounts/edit/` (bio e site funcionam)
- Sempre validar com `verify` via API depois

---

## 9. Erros comuns e como resolver

### Meta / OAuth

| Erro | Solução |
|------|---------|
| Invalid platform app | Usar `INSTAGRAM_APP_ID`, não só `META_APP_ID` |
| Função de desenvolvedor insuficiente | Adicionar Testador do Instagram + aceitar convite no app |
| Redirect URI invalid | Usar `https://localhost:8765/callback` |
| SSL error no callback | Copiar URL com `code=` e rodar `exchange` |
| Token expirado | Rodar `auth` + `exchange` de novo |

### Python / ambiente

| Erro | Solução |
|------|---------|
| `python` não encontrado | Instalar Python + marcar PATH + reiniciar terminal |
| `&&` não funciona no PowerShell | Usar `;` ou comandos separados |
| UnicodeEncodeError no terminal | Script usa `stdout.reconfigure(encoding='utf-8')` |

### Bio / perfil

| Erro | Solução |
|------|---------|
| Bio > 150 caracteres | Contar antes; encurtar linha por linha |
| Colou na Bio em vez do Nome | Nome = 1º campo em Editar perfil |
| API não edita perfil | Usar browser (`apply`) ou manual |

---

## 10. O que a API faz e não faz

### ✅ Faz (com nossos scopes)

- Ler perfil (nome, bio, seguidores, website)
- Listar posts recentes (~30 por sync)
- Insights por post (views, reach, shares, saves)
- Insights parciais da conta (reach, views)

### ❌ Não faz (limitação da Meta)

- Editar nome, bio ou link
- Ler demografia completa da audiência (idade, gênero, cidades) — precisa export/prints ou scopes extras + app review
- Baixar histórico completo de 834 posts em um sync (precisa paginação)
- Publicar posts (precisa scope `instagram_business_content_publish`)

### 🔶 Alternativas

| Necessidade | Alternativa |
|-------------|-------------|
| Editar perfil | Playwright (`update_profile.py apply`) |
| Demografia | Print Insights → Audiência |
| Todos os posts | Export de dados Instagram |
| Publicar Reels | API publish scope (módulo futuro) |

---

## 11. Comandos de referência

```powershell
# Navegar ao projeto
cd "c:\Users\taty_\OneDrive\Desktop\Projetos Cursor\instagram-influencer-agents"

# Ativar venv (opcional)
.venv\Scripts\Activate.ps1

# --- API Meta ---
.venv\Scripts\python scripts/sync_instagram.py auth
.venv\Scripts\python scripts/sync_instagram.py exchange "URL_COM_CODE"
.venv\Scripts\python scripts/sync_instagram.py sync

# --- Perfil ---
.venv\Scripts\python scripts/update_profile.py login
.venv\Scripts\python scripts/update_profile.py status
.venv\Scripts\python scripts/update_profile.py apply
.venv\Scripts\python scripts/update_profile.py apply biography
.venv\Scripts\python scripts/update_profile.py apply --manual
.venv\Scripts\python scripts/update_profile.py verify

# --- Playwright (setup 1x) ---
.venv\Scripts\python -m playwright install chromium
```

---

## 12. Estrutura de arquivos do projeto

```
instagram-influencer-agents/
├── .env                          # secrets (local only)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── docs/
│   └── CURSO-PASSO-A-PASSO.md    # este documento
├── scripts/
│   ├── sync_instagram.py         # OAuth + sync
│   ├── update_profile.py         # status / apply / verify / login
│   └── instagram_browser.py      # Playwright helpers
└── data/
    ├── sync/
    │   ├── profile_snapshot.json # dump completo da API
    │   └── resumo.txt
    └── profile/
        ├── target.json           # o que queremos no perfil
        ├── history.json          # log de verificações
        ├── apply_pendente.txt    # guia manual gerado
        └── browser_profile/      # sessão Chrome (local)
```

---

## 13. Próximos módulos do curso

| Módulo | Conteúdo | Prioridade |
|--------|----------|------------|
| **Media Kit** | PDF/página com números reais + cases UGC | Alta |
| **Item 3–5 da bio** | Linhas 2, 3, 4 + link + CTA parcerias | Alta |
| **Insights audiência** | Print + cruzar com dados API | Média |
| **Sync paginado** | Baixar mais que 30 posts | Média |
| **Agente de conteúdo** | Calendário editorial baseado em horários | Média |
| **Publicar Reels via API** | Scope `content_publish` | Baixa |
| **Pacotes comerciais** | Preços, entregáveis, template proposta | Alta |

---

## 14. Checklist para gravar o curso

### Módulo 1 — Setup (45 min)

- [ ] Criar app Meta Developers (tela a tela)
- [ ] Configurar Instagram Login + Testador
- [ ] Instalar Python + venv
- [ ] Primeiro `auth` + `exchange` + `sync`
- [ ] Mostrar `profile_snapshot.json`

### Módulo 2 — Análise (30 min)

- [ ] Pedir análise no Cursor com dados reais
- [ ] Interpretar pilares, horários, top posts
- [ ] Identificar o que falta (demografia)

### Módulo 3 — Bio profissional (30 min)

- [ ] Explicar ordem: Nome → Bio linha a linha
- [ ] Mostrar referências de influenciadoras negras
- [ ] Aplicar Item 1 (nome) — manual ou browser
- [ ] Aplicar Item 2 (gancho) — com contagem de 150 chars
- [ ] Erro proposital: bio > 150 chars → como corrigir

### Módulo 4 — Automação (30 min)

- [ ] Por que API não edita perfil
- [ ] `update_profile.py login` (1x)
- [ ] `apply` + `verify`
- [ ] Troubleshooting Playwright (chrome.exe, Enviar desabilitado)

### Módulo 5 — Media Kit (próximo)

- [ ] Gerar documento com números do sync
- [ ] Cases UGC + frase comercial
- [ ] Exportar para PDF / Canva

---

## Apêndice — Prompts úteis no Cursor

```
Analise data/sync/profile_snapshot.json e me dê um diagnóstico completo
para receber propostas pagas de marcas de beauty.
```

```
Espelhe influenciadoras negras de sucesso e proponha a linha X da minha bio.
Conte os caracteres (máx 150) e espere minha aprovação antes de aplicar.
```

```
Atualize data/profile/target.json com a opção [X] e rode verify depois de aplicar.
```

```
Monte meu Media Kit com os dados de data/sync/profile_snapshot.json.
```

---

## Apêndice — Linha do tempo do projeto (@tatyzacharias)

| Data | Marco |
|------|-------|
| 11/08/2026 | Projeto criado no Cursor |
| 11/08/2026 | App Meta "Taty Manager" configurado + OAuth OK |
| 11/08/2026 | Primeiro sync — 32.670 seguidores, 30 Reels |
| 11/08/2026 | Análise completa de perfil entregue |
| 11/08/2026 | Item 1 bio: nome → UGC Beauty & Hair ✅ |
| 11/08/2026 | Item 2 bio: linha 1 → diversidade + marcas ✅ |
| 11/08/2026 | Automação Playwright implementada |
| 11/08/2026 | Regra: aprovar antes de aplicar + limite 150 chars |
| Pendente | Item 3 bio: linha 2 (opção A/B/C/D) |
| Pendente | Media Kit automático |

---

*Documento gerado para uso em curso. Projeto: instagram-influencer-agents · @tatyzacharias · Cursor IDE.*
