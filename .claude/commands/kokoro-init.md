# /kokoro-init — Inicializar Kokoro en un Proyecto

> Instalacion de Kokoro knowledge files en un proyecto nuevo.
> Ejecutar una sola vez por proyecto.

> "Antes de sembrar, prepara la tierra."

## Contexto

Kokoro necesita archivos de conocimiento (knowledge files) para funcionar a
profundidad. Este skill copia los archivos desde la fuente central al proyecto
actual.

**Fuente:** `AhuehueteKokoro/.claude/knowledge/` (este repo)
**Destino:** `.claude/knowledge/` del proyecto actual

### Cuando usar

- Primera vez que usas Kokoro en un proyecto nuevo
- Despues de clonar un repo que no tiene los knowledge files

### Cuando NO usar

- Si el proyecto ya tiene knowledge files instalados — usa `/kokoro-update`
- Si estas en el repo de AhuehueteKokoro (ya los tiene)

## Instrucciones

### Paso 1: Detectar contexto

1. Verificar el directorio actual (pwd)
2. Si es el repo AhuehueteKokoro:
   > "Estas en el repo de AhuehueteKokoro — aqui ya estan los knowledge
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

Verificar que el directorio actual tiene los archivos de conocimiento (son parte del repo):
```bash
ls .claude/knowledge/
```

Si no existen, indicar al usuario que clone el repo correctamente:
> "No encuentro los knowledge files. Asegúrate de haber clonado AhuehueteKokoro — los knowledge files están incluidos en el repo."

### Paso 3: Crear estructura

```bash
mkdir -p .claude/knowledge
```

### Paso 4: Copiar archivos

Copiar TODOS los archivos .md de la fuente al destino:

```bash
# Los knowledge files ya están en .claude/knowledge/ dentro del repo.
# Si necesitas copiarlos a otro proyecto, usa:
# cp -r .claude/knowledge/*.md /ruta/a/tu/proyecto/.claude/knowledge/
# cp -r .claude/knowledge/*/ /ruta/a/tu/proyecto/.claude/knowledge/ 2>/dev/null
```

### Paso 5: Verificar y reportar

Contar archivos copiados y presentar resumen:

```
Kokoro inicializado en: {directorio actual}

Archivos instalados:
- {N} knowledge files copiados
- Subdirectorios: {lista de subdirectorios si hay}

Fuente: AhuehueteKokoro/.claude/knowledge/
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
cp .claude/AGENTS.md ./AGENTS.md
```

El `AGENTS.md` contiene la identidad Kokoro + referencia a los skills.
Codex CLI lo lee automaticamente al abrir el proyecto.

---

## Arquitectura multi-agente — Que va donde

Kokoro funciona en 3 CLIs: Claude Code, Hermes (Nous) y Codex (OpenAI).
Cada uno tiene su mecanismo de identidad y skills:

### Identidad global (una vez por maquina)

| CLI | Archivo | Cuando se carga |
|-----|---------|-----------------|
| Claude Code | `~/.claude/CLAUDE.md` | Siempre, en todo proyecto |
| Hermes | `~/.hermes/SOUL.md` | Siempre, en todo proyecto |
| Codex | No tiene global de identidad | — |

Estos archivos YA estan configurados con la identidad Kokoro en la maquina de Eduardo.
No hay que tocarlos por proyecto.

### Skills globales (una vez por maquina)

| CLI | Directorio | Como se invocan |
|-----|-----------|-----------------|
| Claude Code | `~/.claude/commands/kokoro-*.md` | `/kokoro-*` como slash command |
| Hermes | `~/.hermes/config.yaml` → `quick_commands` | `/kokoro-*` como quick command |
| Codex | No tiene mecanismo equivalente | — |

Los skills de Claude Code YA estan en `~/.claude/commands/` (65 skills).
Los quick_commands de Hermes YA estan en `~/.hermes/config.yaml` (28 skills principales).

### Por proyecto

| Archivo | Para quien | Que contiene |
|---------|-----------|--------------|
| `.claude/knowledge/` | Todos los CLIs | Knowledge files de dominio |
| `CLAUDE.md` | Claude Code + Hermes | Identidad Kokoro + RaiSE context |
| `AGENTS.md` | Codex CLI | Identidad Kokoro + instrucciones proyecto |
| `.hermes.md` | Hermes (alternativo) | Solo si necesitas override especifico |

**Regla:** `kokoro-init` instala knowledge files + crea AGENTS.md.
Los skills y la identidad global ya estan en la maquina — no van en el proyecto.

---

## Notas para Claude

- No copiar archivos que contengan datos personales de clientes
- No copiar `.kokoro/` (datos del grafo de invitados)
- Solo copiar archivos de knowledge (metodologia, frameworks, guias)
- Si el usuario tiene dudas, explicar que los knowledge files son las
  "instrucciones" que Kokoro necesita para guiar bien — como un libro
  de recetas que el chef necesita tener en la cocina
- Hermes lee CLAUDE.md automaticamente (fallback chain), por lo que
  en proyectos que ya tienen CLAUDE.md, Hermes funciona sin pasos extra
- Para agregar un skill nuevo a Hermes, agregar entrada en
  `~/.hermes/config.yaml` bajo `quick_commands`
