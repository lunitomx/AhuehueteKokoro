---
name: kokoro
description: Route Kokoro requests to the packaged command and knowledge surface.
kokoro_owned: true
---

# Kokoro Router

Kokoro package root resolution:

1. Use `KOKORO_HOME` when present.
2. Otherwise, if this skill is inside an installed package, use that package
   root.
3. Otherwise, when running inside a Kokoro checkout, use the repository root.

Before responding:

1. Read `IDENTITY_kokoro.md` from the package root.
2. Inside a public Kokoro checkout, route explicit command requests to
   `.claude/commands/kokoro*.md`.
3. Inside an installed package, route explicit command requests to
   `commands/kokoro*.md`.
4. Inside a public Kokoro checkout, resolve knowledge under `.claude/knowledge/`,
   `.claude/knowledge/google-ads/`, and `.claude/knowledge/lux/`.
5. Inside an installed package, resolve knowledge under `knowledge/`,
   `knowledge/google-ads/`, and `knowledge/lux/`.
6. If identity, command source, or required knowledge is missing, stop and ask
   the user to run Kokoro verify/update.

Never assume the current working directory is the Kokoro package.
