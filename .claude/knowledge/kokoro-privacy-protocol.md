# Protocolo de Privacidad — Datos de Invitados

## Principio

Los nombres reales de invitados (clientes) NUNCA aparecen en archivos
trackeados por git. Usamos slugs anonimizados (`cliente_NN`) en todo
artefacto que vive en el repositorio.

## Dónde viven los nombres reales

Estos directorios son gitignored y pueden contener nombres reales:

- `.kokoro/` — datos de invitados, sesiones, contextos
- `.raise/rai/personal/` — lista de nombres para el hook, datos personales

## Dónde NUNCA deben aparecer

- `work/` — epics, stories, retrospectivas
- `dev/` — parking lot, decisiones, problem briefs
- `governance/` — PRD, vision, backlog
- `.claude/` — skills, knowledge files, CLAUDE.md
- `src/` — código fuente
- `tests/` — tests (usar slugs en fixtures)
- `extension/` — distribución pública

## Cómo funciona el hook

El pre-commit hook (`.githooks/pre-commit`) bloquea commits que contengan
nombres de la lista `.raise/rai/personal/real-clients.txt`.

- **Word-boundary matching** (`grep -w`): un nombre corto no matchea palabras más largas que lo contienen
- **Case-insensitive** (`grep -i`): matchea independientemente de mayúsculas/minúsculas
- **Accent stripping** (`sed` transliteration): matchea variantes con y sin acentos
- **Fail-open**: si la lista no existe, el hook permite el commit (clones frescos no se rompen)

## Cómo añadir un nuevo invitado

1. Agregar el nombre real a `.raise/rai/personal/real-clients.txt` (una línea por nombre)
2. No es necesario agregar variantes con acentos — el hook las maneja
3. El nombre debe tener 3+ caracteres
4. Verificar que no haya duplicados en la lista

## Qué hacer si el hook bloquea un commit legítimo

Si el hook bloquea un commit donde el nombre aparece en contexto legítimo
(ej: documentando el propio protocolo de privacidad):

1. Reemplazar el nombre real con el slug `cliente_NN` correspondiente
2. Si es imposible evitar el nombre (raro), usar `git commit --no-verify`
3. Documentar por qué se usó `--no-verify` en el mensaje de commit

## Política de slugs

| Formato | Ejemplo | Uso |
|---------|---------|-----|
| `cliente_NN` | `cliente_01`, `cliente_05` | Identificador del invitado |
| `Cliente{NN}ProyectoRepo` | `Cliente05ProyectoRepo` | Nombre de repo ficticio |

Los slugs se asignan secuencialmente. El mapeo slug → nombre real vive
solo en `.kokoro/` (gitignored).
