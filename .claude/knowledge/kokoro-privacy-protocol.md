# Protocolo de Privacidad — Datos de Invitados

> Regla madre: el repositorio publico contiene metodologia, contratos de
> skills, ejemplos anonimizados y artefactos de trabajo no sensibles. Los datos
> reales de invitados viven en workspaces privados y nunca se publican.

## Principio

Los nombres reales de invitados NUNCA aparecen en archivos trackeados por git.
Usamos slugs anonimizados (`cliente_NN`) en todo artefacto que vive en el
repositorio.

Kokoro puede hablar de procesos de marketing, ventas, Google Ads, Meta Ads,
GA4, Search Console, parrillas, landings y analitica. Pero no debe publicar
los datos reales que hacen identificable a un invitado, una cuenta o una
campana.

## Public repo vs private workspace

| Espacio | Puede contener | Nunca debe contener |
|---|---|---|
| Repositorio publico | Skills, knowledge, gates, ejemplos fake, slugs `cliente_NN`, placeholders | Nombres reales, tokens, exports, reportes reales, account IDs reales |
| Workspace privado | Contextos de invitados, mappings de cuentas, exports, reportes, sesiones | Archivos que se vayan a compartir publicamente sin revisar |
| Runtime MCP | Credenciales en config local del servidor MCP | Credenciales copiadas a markdown, commits o ejemplos |

## Dónde viven los nombres reales

Estos directorios son gitignored y pueden contener nombres reales:

- `.kokoro/` — datos de invitados, sesiones, contextos
- `.raise/rai/personal/` — lista de nombres para el hook, datos personales
- `clientes/` o `clients/` — carpetas privadas de trabajo si existen localmente
- `exports/` — descargas de plataformas
- `reports/` — reportes generados para invitados
- `generated/` — creativos, imagenes o video generados para un invitado

## Dónde NUNCA deben aparecer

- `work/` — epics, stories, retrospectivas
- `dev/` — parking lot, decisiones, problem briefs
- `governance/` — PRD, vision, backlog
- `.claude/` — skills, knowledge files, CLAUDE.md
- `src/` — código fuente
- `tests/` — tests (usar slugs en fixtures)
- `extension/` — distribución pública
- `README.md` — ejemplos publicos solamente
- `AGENTS.md` — identidad y protocolo, nunca datos de invitado

## Identificadores de plataformas

Los IDs reales de plataformas pueden identificar cuentas o propiedades. En el
repositorio publico usa placeholders:

| Plataforma | Placeholder publico | Dato real vive en |
|---|---|---|
| Meta Ads | `act_123456789` | `.kokoro/clients.json` o workspace privado |
| Google Ads | `1234567890` | `.kokoro/clients.json` o workspace privado |
| GA4 | `properties/123456` | `.kokoro/clients.json` o workspace privado |
| Search Console | `https://ejemplo.com` | `.kokoro/clients.json` o workspace privado |

Si un orquestador necesita mostrar cuentas descubiertas via MCP, debe hacerlo
en la sesion de trabajo y no persistir la lista completa en archivos publicos.

## Credenciales y MCP

Las credenciales de MCP nunca pertenecen al repo:

- tokens de Meta
- developer tokens de Google Ads
- OAuth refresh tokens
- client secrets
- service account JSON
- API keys de OpenAI, Gemini u otros proveedores

Los skills pueden documentar nombres de variables y placeholders, pero no
valores reales. La conexion se verifica en runtime con el servidor MCP local.

## Salida de orquestadores

Los orquestadores Kokoro deben separar tres niveles:

1. **Diagnostico publico:** metodologia, gates, estructura, ejemplos fake.
2. **Lectura privada de sesion:** metricas reales consultadas via MCP o archivos privados.
3. **Artefacto compartible:** resumen anonimizando nombres, IDs y datos que no deban salir.

Antes de guardar cualquier reporte, el orquestador debe aplicar el gate
`GATE-NO-SENSITIVE-DATA`.

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

## Checklist relacionado

Antes de compartir o publicar el repo, ejecutar:

- `kokoro-share-readiness.md`
