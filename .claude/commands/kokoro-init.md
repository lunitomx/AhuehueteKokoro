# /kokoro-init — Inicializar Kokoro en un Proyecto

> Instalacion de Kokoro knowledge files en un proyecto nuevo.
> Ejecutar una sola vez por proyecto.

> "Antes de sembrar, prepara la tierra."

## Contexto

Kokoro necesita archivos de conocimiento (knowledge files) para funcionar a
profundidad. Este skill copia los archivos desde la fuente central al proyecto
actual.

**Fuente:** `/Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/`
**Destino:** `.claude/knowledge/` del proyecto actual

### Cuando usar

- Primera vez que usas Kokoro en un proyecto nuevo
- Despues de clonar un repo que no tiene los knowledge files

### Cuando NO usar

- Si el proyecto ya tiene knowledge files instalados — usa `/kokoro-update`
- Si estas en el repo fuente `RaizAncestral` (ya los tiene)

## Instrucciones

### Paso 1: Detectar contexto

1. Verificar el directorio actual (pwd)
2. Si es `/Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral`:
   > "Estas en el repo fuente de Kokoro — aqui ya estan los knowledge
   > files. Este skill es para otros proyectos. Si quieres actualizar
   > los archivos existentes, no necesitas hacer nada aqui."
   → Terminar

3. Verificar si `.claude/knowledge/` ya existe y tiene archivos kokoro-*:
   - Si tiene archivos: avisar y preguntar
     > "Este proyecto ya tiene {N} knowledge files de Kokoro instalados.
     > ¿Quieres reinstalar desde cero (sobreescribe todo) o prefieres
     > usar `/kokoro-update` para sincronizar solo lo nuevo?"
   - Si no tiene archivos: continuar con instalacion

### Paso 2: Verificar fuente

Verificar que la fuente existe:
```bash
ls /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/
```

Si no existe, informar:
> "No encuentro la fuente de knowledge files. Verifica que el repo
> RaizAncestral este en /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral"

### Paso 3: Crear estructura

```bash
mkdir -p .claude/knowledge
```

Para la memoria compartida v2, `kokoro init` también crea las superficies
`.kokoro/shared/events/` y `.kokoro/shared/views/`, además de los tiers
ignorados `local/`, `secrets/`, `cache/` y `raw/`. Mantén una sola sección
marcada de Kokoro en `CLAUDE.md` y `AGENTS.md`; el renderer conserva todo el
texto fuera de sus marcadores y apunta a `.kokoro/shared/views/context.md`.

### Paso 4: Copiar archivos

Copiar TODOS los archivos .md de la fuente al destino:

```bash
# Archivos en raiz de knowledge/
cp /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/*.md .claude/knowledge/

# Subdirectorios (lux/, google-ads/, etc.)
cp -r /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/*/ .claude/knowledge/ 2>/dev/null
```

### Paso 5: Verificar y reportar

Contar archivos copiados y presentar resumen:

```
Kokoro inicializado en: {directorio actual}

Archivos instalados:
- {N} knowledge files copiados
- Subdirectorios: {lista de subdirectorios si hay}

Fuente: RaizAncestral/extension/.claude/knowledge/
Destino: .claude/knowledge/

Para actualizar en el futuro: /kokoro-update
```

### Paso 6: Detectar contexto del proyecto (opcional)

Si el proyecto tiene archivos que sugieren un tipo de negocio, mencionarlo:
- `package.json` → proyecto web/Node
- `astro.config.*` → sitio Astro
- `wp-content/` → WordPress
- `.kokoro/clients.json` → ya tiene invitados registrados

> "Detecte que este es un proyecto {tipo}. Los knowledge files estan
> listos. Puedes empezar con `/kokoro-onboard` para tu primera sesion
> o `/kokoro` para un diagnostico rapido."

### Paso 7: Crear AGENTS.md para Codex CLI (opcional)

Si el proyecto va a ser usado con OpenAI Codex CLI, crear `AGENTS.md` en la raiz:

```bash
# Verificar si ya existe
ls AGENTS.md 2>/dev/null
```

Si no existe, copiar la plantilla base del repo:
```bash
cp /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/AGENTS.md ./AGENTS.md
```

El `AGENTS.md` contiene la identidad Kokoro + referencia a los skills.
Codex CLI lo lee automaticamente al abrir el proyecto.

---

## Notas para Claude

- No copiar archivos que contengan datos personales de clientes
- No copiar `.kokoro/` (datos del grafo de invitados)
- Solo copiar archivos de knowledge (metodologia, frameworks, guias)
- Si el usuario tiene dudas, explicar que los knowledge files son las
  "instrucciones" que Kokoro necesita para guiar bien — como un libro
  de recetas que el chef necesita tener en la cocina
