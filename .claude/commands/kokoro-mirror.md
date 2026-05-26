# /kokoro-mirror — Espejo del Perfil Scout

> Herramienta transversal: Relee y presenta el perfil generado por `/kokoro-scout`
> con voz de Eduardo, desde la montaña.

> "Un espejo no inventa, no juzga, no aconseja. Solo muestra lo que ya está ahí."

## Contexto

Este skill lee el `profile.md` que `/kokoro-scout` generó y lo presenta con la
voz de Eduardo — un resumen narrativo desde la montaña, no una lista mecánica
de secciones.

Úsalo cuando:
- Quieras ver cómo Scout ve tu negocio sin volver a ejecutar el discovery
- Quieras compartir el perfil con alguien en una conversación
- Quieras confirmar que el perfil sigue vigente antes de iniciar un onboarding

### Dependencias

- **Input:** `.kokoro/scout/{slug}/profile.md` (generado por `/kokoro-scout`)
- **Slug:** misma cadena de derivación que `/kokoro-scout`

---

## Paso 1 — Derivar el Slug

Usa la misma cadena de prioridad que `/kokoro-scout`:

1. **`.claude/knowledge/kokoro-cliente.md`** — campo `slug` o `nombre` en el frontmatter
2. **Otros knowledge files** — campo `nombre` en cualquier `kokoro-*.md`
3. **Nombre del directorio del repo** — `basename $(pwd)` en kebab-case
4. **Preguntar al usuario** — solo si las opciones anteriores son ambiguas

---

## Paso 2 — Buscar el Profile

```bash
# Ruta esperada
.kokoro/scout/{slug}/profile.md
```

### Caso A — El archivo existe

Leer el archivo completo y proceder al Paso 3.

### Caso B — El archivo no existe

Responder con:

> "No encontré un perfil Scout para este negocio. Ejecuta `/kokoro-scout`
> primero para generar uno. Si ya lo ejecutaste, verifica que el slug sea
> correcto."

### Caso C — Múltiples slugs en `.kokoro/scout/`

Si hay más de un directorio bajo `.kokoro/scout/`, listar los disponibles:

```bash
ls .kokoro/scout/
```

Y pedir selección:

> "Encontré perfiles Scout para varios negocios en este repo. ¿Cuál quieres ver?"
> {lista numerada}

---

## Paso 3 — Presentar con Voz de Eduardo

La presentación es un **espejo narrativo** de las 8 secciones del perfil.
No es una lista — es una lectura interpretativa desde la montaña.

### Apertura obligatoria

> "Mirando el perfil de {nombre del negocio} que Scout construyó desde tu repo..."

### Cuerpo

Recorre las secciones del perfil en orden, pero no como enumeración.
Cada sección se menciona con una frase de transición natural:

- **Negocio:** "Lo que hace: ..."
- **Audiencia:** "Para quienes es: ..."
- **Propuesta de Valor:** "Lo que los distingue: ..."
- **Voz de Marca:** "Cómo lo comunican: ..."
- **Actividad de Marketing:** "Dónde están hoy: ..."
- **Diagnóstico de Fase:** "**Fase {N}** — {justificación}"
- **Fuentes Usadas:** (mencionar solo si hay 1-2 fuentes, omitir si son muchas)
- **Gaps Detectados:** "Lo que no se pudo inferir: ..."

Si una sección dice "No detectado", menciónalo con naturalidad:

> "Sobre su propuesta de valor, el repo no tenía suficiente información
> para que Scout la infiriera. Eso es una pista en sí misma."

### Cierre

> "Eso es lo que el repo dice de tu negocio. ¿Quieres actualizar este perfil
> ejecutando `/kokoro-scout` de nuevo, o prefieres ir directo a `/kokoro-onboard`?"

### Reglas de voz

- Vocabulario Eduardo: inversión, invitado, creación, compartir, reto/oportunidad
- Sin emojis, sin tono de influencer, sin "10 tips"
- La presentación es un espejo — no agrega opiniones ni recomendaciones nuevas
- Si el perfil está desactualizado (fecha de generación antigua), mencionarlo:
  > "Este perfil se generó el {fecha}. Si hubo cambios en el repo desde entonces,
  > considera ejecutar `/kokoro-scout` de nuevo."

---

## Notas para Claude

- No modificar `profile.md` — solo leerlo y presentarlo
- No ejecutar discovery — eso es trabajo de `/kokoro-scout`
- Si el perfil no existe, indicarlo claramente — no inventar ni sugerir contenido
- Responde en el idioma del usuario, manteniendo nombres de secciones en español
