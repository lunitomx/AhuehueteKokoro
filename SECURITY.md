# Security policy

Kokoro's public distribution contains methodology, runtime code, connector
source, and empty configuration templates. It must never contain credentials,
advertising account data, private machine paths, or exports from a real account.

## Advertising connector boundary

- The Meta Ads connector distributed here is a clean, read-only implementation.
- Do not copy a working connector directory, `.env`, token file, report, debug
  script, or Git history into this repository.
- Private methodology sources named `*-formal-source.md` and
  `kokoro-tactiq-field-patterns.md` never cross the public export boundary.
- Authentication values belong only in the user's ignored local file at
  `~/.config/kokoro/meta-ads.env` or in the parent process environment.
- MCP configuration may contain variable names and launcher paths, never token,
  app-secret, OAuth-secret, private-key, or account-ID values.
- Missing credentials are an `unconfigured` optional capability, not a broken
  Kokoro installation.

## Reporting a secret exposure

Use the repository's private GitHub security-advisory channel. Do not paste the
credential into a public issue. A committed credential must be revoked or
rotated at its provider even after the current file is removed.
