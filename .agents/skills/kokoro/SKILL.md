---
name: kokoro
description: Route Kokoro requests to the packaged command and knowledge surface.
kokoro_owned: true
---

# Kokoro Router

## Step 1 — Resolve the package root (preflight)

Resolve the Kokoro package root **before** answering anything, in this order:

1. `KOKORO_HOME` when set.
2. `KOKORO_PACKAGE_HOME` when set.
3. The installed package home `~/.claude/kokoro`.
4. The Kokoro checkout that contains this skill — walk up from this file until
   a directory with `IDENTITY_kokoro.md` is found.

Then run the guard, which performs exactly that resolution:

```sh
bash "$(dirname "<this SKILL.md>")/preflight.sh"
```

- **Exit 0** → the first line of stdout is the package root. Use it.
- **Exit 1** → **STOP. Do not answer the request.** This `SKILL.md` was
  installed without the Kokoro package, and copying this file alone is
  **not a valid installation**. Show the user the guard message, which names the
  supported command:

  ```sh
  git clone https://github.com/lunitomx/AhuehueteKokoro.git
  cd AhuehueteKokoro
  ./install/install.sh
  ```

If the harness cannot execute `preflight.sh`, apply the resolution order above
yourself and verify that `<package root>/IDENTITY_kokoro.md` exists. If it does
not, stop and show the same `install/install.sh` command.

## Step 2 — Route the request

Once the package root is resolved:

1. Read `<package root>/IDENTITY_kokoro.md`.
2. Inside a Kokoro checkout, route explicit command requests to
   `.claude/commands/kokoro*.md`; inside an installed package, to
   `commands/kokoro*.md`.
3. Inside a Kokoro checkout, resolve knowledge under `.claude/knowledge/`,
   `.claude/knowledge/google-ads/` and `.claude/knowledge/lux/`; inside an
   installed package, under `knowledge/`, `knowledge/google-ads/` and
   `knowledge/lux/`.
4. If identity, command source or required knowledge is missing, stop and ask
   the user to run `<package root>/install/verify.sh` or to reinstall with
   `install/install.sh`.

Never assume the current working directory is the Kokoro package.
