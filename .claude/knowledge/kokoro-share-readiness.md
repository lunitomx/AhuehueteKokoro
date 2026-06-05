# Kokoro Share Readiness Checklist

Use this checklist before sharing Ahuehuete Kokoro publicly, inviting a collaborator, or packaging a workspace for a guest.

## Decision

| Status | Meaning |
|---|---|
| Pass | Safe to share after normal review |
| Hold | Fix the listed items before sharing |
| Private Only | Do not publish; use a private workspace |

## 1. Secrets

- [ ] No `.env` files are tracked.
- [ ] No API keys, access tokens, refresh tokens, OAuth client secrets, service account JSON, or private keys are tracked.
- [ ] MCP credentials live only in local MCP/server configuration.
- [ ] Documentation uses placeholders only.

Verification:

```bash
git status --short
rg -n --hidden --glob '!/.git/**' --glob '!/.agents/**' --glob '!/.claude/skills/**' \
  '(sk-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{20,}|EAA[A-Za-z0-9]{20,}|access[_-]?token|refresh[_-]?token|client[_-]?secret)' .
```

## 2. Guest Identity

- [ ] No real guest names appear in public files.
- [ ] Public examples use `cliente_NN`.
- [ ] Slug-to-name mappings live only in `.kokoro/` or a private workspace.
- [ ] Meeting notes, transcripts, and context files are not tracked.

Verification:

```bash
git status --short
rg -n "cliente real|nombre real|@gmail|@hotmail|@outlook" . --hidden --glob '!/.git/**'
```

## 3. Platform Accounts

- [ ] Real Meta account IDs are not committed.
- [ ] Real Google Ads customer IDs are not committed.
- [ ] Real GA4 property IDs are not committed.
- [ ] Real Search Console properties are not committed unless intentionally public and non-sensitive.
- [ ] Platform mappings live in `.kokoro/clients.json` or private workspace files.

Allowed public examples:

```text
act_123456789
1234567890
properties/123456
https://ejemplo.com
```

## 4. Exports, Reports, and Generated Assets

- [ ] `exports/` is not tracked.
- [ ] `reports/` is not tracked.
- [ ] `generated/` is not tracked.
- [ ] Spreadsheet exports, CSVs, generated images, generated videos, and rendered reports are private by default.
- [ ] Any deliverable intended for a guest is reviewed before sharing outside git.

Verification:

```bash
git check-ignore -v exports/cliente_01/test.csv reports/cliente_01/pulse.md generated/cliente_01/ad.png
```

## 5. RaiSE and Kokoro Runtime State

- [ ] `.kokoro/` is ignored.
- [ ] `.raise/rai/` runtime state is ignored.
- [ ] `.raise/artifacts/` may be tracked only for public typed artifacts.
- [ ] `.rai/` is ignored if created locally.
- [ ] Session output with private details is not tracked.

Verification:

```bash
git check-ignore -v .kokoro/clients.json .raise/rai/personal/real-clients.txt
git check-ignore -v .raise/artifacts/s40.1-design.yaml || true
```

The second command should return no ignore rule for public artifacts.

## 6. MCP Boundaries

- [ ] The repo documents MCP names and placeholders, not credentials.
- [ ] Orchestrators check MCP registration and health at runtime.
- [ ] If MCP is unavailable, output says "not connected" instead of inventing data.
- [ ] Actions that mutate ad accounts require explicit invitation.

## 7. Share Decision

Use the strictest applicable result:

| Result | Condition | Action |
|---|---|---|
| Pass | Only public methodology, placeholders, and safe artifacts are present | Share |
| Hold | Untracked private files are safe locally but docs or ignore rules need cleanup | Fix before sharing |
| Private Only | Real guest data, exports, credentials, or account mappings are required | Move work to private workspace |

## Operator Note

Kokoro can guide with elegance, but privacy is not aesthetic. If a file helps a guest because it contains their real data, it belongs outside the public repo unless explicitly anonymized.
