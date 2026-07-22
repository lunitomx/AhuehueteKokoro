# Meta Ads connector setup

Kokoro installs the connector under `~/.claude/kokoro/connectors/meta-ads/`
and creates an empty credential file at `~/.config/kokoro/meta-ads.env` with
permissions `0600`. Fill that local file; never paste its values into an MCP
command or commit it to a repository.

Check readiness:

```bash
~/.claude/kokoro/connectors/meta-ads/doctor.sh
```

Register the same secret-free launcher in Claude Code:

```bash
claude mcp add --scope user meta-ads -- \
  "$HOME/.claude/kokoro/connectors/meta-ads/run.sh"
claude mcp list
```

Register it in Codex:

```bash
codex mcp add meta-ads -- \
  "$HOME/.claude/kokoro/connectors/meta-ads/run.sh"
codex mcp list
```

Registration does not authenticate or query an account. The connector remains
optional and read-only. If Kokoro was installed with a custom package or config
home, use the paths printed by `install.sh`.
