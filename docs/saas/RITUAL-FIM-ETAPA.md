# Ritual ao finalizar cada etapa

> **Decisão (Tatiana, 2026-08-20):** toda etapa concluída → **commit local** + **documentos atualizados**.

---

## Quando fazer

Quando a etapa atingir o **critério de saída** (funciona na máquina da Taty, testado, ela aprova).

---

## Checklist (agente / dev)

1. **Validar** com Tatiana que a etapa está ok.
2. **Atualizar documentos** (toolkit `docs/saas/`):
   - [`ENTREGAS-FASES.md`](ENTREGAS-FASES.md) — status da entrega
   - [`F1-ORDEM-EXECUCAO.md`](F1-ORDEM-EXECUCAO.md) — se for F1
   - Criar ou atualizar `F1-ETAPA*-SESSAO-YYYY-MM-DD.md` (registro da sessão)
   - [`comjuntas-saas/README.md`](../../../comjuntas-saas/README.md) — tabela de status
3. **Commit local** em `comjuntas-saas/`:
   ```powershell
   cd comjuntas-saas
   git status
   git diff
   ```
   - Confirmar que **`.env.local`**, **`.data/`** e secrets **não** entram no commit.
   - Mensagem: 1–2 frases no **porquê**, não só lista de arquivos.
4. **Registrar** o hash do commit no arquivo de sessão da etapa.
5. **Não fazer push** nem publicar na internet — salvo pedido explícito da Tatiana.

---

## Commits por etapa (histórico)

| Etapa | Commit | Data | Notas |
|-------|--------|------|-------|
| F0 + F1 etapa 1 | `c22b6b0` | 2026-08-20 | Monorepo + OAuth IG + dashboard |

---

## Próxima etapa

Só iniciar a etapa seguinte **depois** do ritual completo.
