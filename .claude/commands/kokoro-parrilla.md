# /kokoro-parrilla — Orquestador del Pipeline Parrilla (6 Fases)

> Herramienta orquestadora: Ejecuta las 6 fases del pipeline Parrilla
> de Contenido Comercial end-to-end, desde Fase 0 (tracking check) hasta
> Fase F (xlsx + verificacion pre-delivery)
>
> "No construyes una parrilla — cultivas un ecosistema de angulos."

## Contexto

Este skill es el **orquestador** del pipeline Parrilla de Contenido Comercial.
Coordina la ejecucion de las 6 fases, verifica los gates entre fases, y
produce el xlsx final. NO reemplaza las skills individuales — las invoca
o guia al operador para ejecutarlas.

Lee el archivo de conocimiento `kokoro-parrilla-method.md` para la
metodologia completa de las 6 fases, gates, loop de feedback, y esquema
del xlsx.

### Skills que orquesta

| Fase | Skill/Herramienta | Tipo |
|------|------------------|------|
| Fase 0 | `/kokoro-tracking-check` | Skill existente (S38.1) |
| Fase A | `/kokoro-listen`, `/kokoro-research`, `/kokoro-audit` | Skills humanas existentes |
| Fase B | `/kokoro-onboard` + lectura de landing | Skill humana existente |
| Fase C | Metodologia CUR | Humana (skill futura E39) |
| Fase D | `/kokoro-feed-audit` | Skill existente (S38.2) |
| Fase E | Propuesta v1 + loop feedback | Orquestador |
| Fase F | `scripts/generate-parrilla-xlsx.py` + verificacion | Script + checks |

### Resolucion de invitado

Antes de orquestar, resuelve el invitado desde el grafo:

1. Busca en `.kokoro/clients.json` el nombre mencionado
2. Si encuentra al invitado:
   - Lee `metadata["platform_accounts"]` para plataformas disponibles
   - Lee `metadata.get("context_file")` para contexto del proyecto
   - Lee `metadata.get("landing_url")` para la landing page
3. Si NO encuentra: registrar con `/kokoro-client` primero

### Checklist de inputs requeridos

Antes de empezar, confirma que el operador tiene:

- [ ] Landing page del invitado (URL)
- [ ] Acceso a Meta Ads account (o CSV export reciente)
- [ ] Acceso a CRM (o screenshots de leads recientes)
- [ ] Transcripts o notas de sesiones con el invitado
- [ ] Screenshots de creativos activos
- [ ] Confirmacion de buyer personas (o tiempo para definirlas en Fase B)

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Voy a guiarte por las 6 fases del pipeline Parrilla para tu invitado.
> Desde verificar tracking hasta generar el xlsx final. El proceso completo
> toma entre 45-90 minutos dependiendo de cuanta informacion tengas lista.
> ¿Quieres empezar? Primero confirmemos que tienes los inputs minimos."

### Pipeline completo

#### Fase 0 — Tracking Check

Invoca `/kokoro-tracking-check` para el invitado.

**Gate:** Ver resultado. Si WAIT (hay CRITICOS), detener pipeline y
recomendar reparacion. Si GO, continuar.

```
## Fase 0 — Tracking Check
**Resultado:** GO / WAIT
**Detalles:** [referencia al reporte de tracking-check]
```

#### Fase A — Inteligencia base

Guia al operador para ejecutar inteligencia base:
- Sugiere `/kokoro-listen` para escuchar a la audiencia
- Sugiere `/kokoro-research` para investigacion de mercado
- Sugiere `/kokoro-audit` para auditoria de sitio web

Recopila los outputs en un brief de inteligencia.

**Gate:** Confirmar al menos 3 insights de audiencia utilizables.

```
## Fase A — Inteligencia base
**Insights:** {3+ insights clave}
**Fuentes:** {que skills/herramientas se usaron}
```

#### Fase B — Alma de marca

Guia al operador para conectar con la identidad del invitado:
- Revisar landing page y materiales de marca
- Definir voz, tono y personalidad
- Definir buyer personas (al menos 2)

**Gate:** Confirmar al menos 2 buyer personas con necesidades especificas.

```
## Fase B — Alma de marca
**Buyer Personas:** {lista de personas con necesidades}
**Voz de marca:** {descripcion breve}
```

#### Fase C — CUR (Contenido Util Relevante)

Guia al operador para definir pilares de contenido:
- Que informacion necesita la audiencia (util)
- Que temas sirven al negocio (relevante)
- Donde se cruzan (sweet spot)

**Gate:** Confirmar al menos 3 pilares de contenido validados.

```
## Fase C — CUR
**Pilares de contenido:** {3+ pilares}
**Temas por pilar:** {lista de temas}
```

#### Fase D — Feed Audit

Invoca `/kokoro-feed-audit` para auditar el corpus Meta Ads.

**Gate:** corpus.json debe tener angles_absent con al menos 2 entradas.

```
## Fase D — Feed Audit
**Angulos cubiertos:** {lista}
**Angulos ausentes:** {lista}
**Anti-patrones:** {lista}
```

#### Fase E — Propuesta v1 + loop feedback

Sintetiza los inputs de Fases A-D en una propuesta de parrilla:

1. **v1 strawman:** Propuesta inicial de 12 piezas basada en los datos
   recopilados. Incluir justificacion de cada pieza desde las Bases de
   Aprendizaje.
2. **Feedback elevation:** Pide al operador que eleve la parrilla al
   CMO/invitado para feedback dirigido. Cada pieza de feedback se eleva
   a regla global, no se aplica como cambio puntual.
3. **v2 (max 2 pasadas):** Segunda version incorporando reglas elevadas.

```
## Fase E — Propuesta v1 + Loop
**Version actual:** v1 / v2
**Reglas elevadas del feedback:** {lista de reglas R nuevas}
**Estado:** strawman / feedback pendiente / v2 completo
```

#### Fase F — Parrilla xlsx + verificacion

1. Ejecutar `scripts/generate-parrilla-xlsx.py` para generar el xlsx
   con los datos de las fases previas
2. Ejecutar verificacion pre-delivery (7 checks deterministicos)
3. Si pasa: entregar xlsx + verification-report.md
4. Si falla: reportar errores al operador para reparacion

```
## Fase F — Entrega
**xlsx:** marketing/content/parrillas/parrilla-{slug}-v{N}-piloto-{YYYY-MM}.xlsx
**Verificacion:** {PASS / FAIL — detalle de cada check}
**Estado:** entregado / requiere reparacion
```

### Verificacion pre-delivery (7 checks)

El orquestador ejecuta estos checks ANTES de marcar la parrilla como entregable:

1. **Vocabulario commodity** — grep contra lista de palabras prohibidas
2. **Vocabulario binario** — grep contra lista del binary_framing.txt
3. **Referencias internas** — grep contra lista provista por operador
4. **Hoja 3 minima** — assert >= 15 filas
5. **Citas verificables** — assert columna Fuente no vacia
6. **Fechas absolutas** — regex contra fechas relativas
7. **Typos nombres propios** — comparar contra lista confirmada

Output: `verification-report.md`. Si FAIL, el xlsx NO se entrega.

### Plantilla de cierre

```
---
## Resumen del Pipeline — {Nombre del Invitado}

| Fase | Estado | Artefacto |
|------|--------|-----------|
| Fase 0 Tracking Check | {Completo / Saltado} | {link al reporte} |
| Fase A Inteligencia | {Completo} | {brief} |
| Fase B Alma de Marca | {Completo} | {brief} |
| Fase C CUR | {Completo} | {matriz} |
| Fase D Feed Audit | {Completo} | {corpus.json} |
| Fase E Propuesta | {v1 / v2} | {brief} |
| Fase F Entrega | {Entregado / Pendiente} | {xlsx + verification-report} |

**Tiempo total:** ~{N} minutos
**Pasadas de feedback:** {N} (max 2)
**Verificacion:** PASS / FAIL

### Siguientes pasos
- La parrilla es una hipotesis fundamentada — candidata a
  `/kokoro-validate` para destilar plan de validacion
- Usa `/kokoro-experiment` cuando el primer resultado del piloto entre
- Para la siguiente parrilla, repite desde Fase 0
```

## Anti-patrones

- **No saltarse Fase 0** — el tracking check es obligatorio
- **No entregar xlsx sin verificacion** — los 7 checks son obligatorios
- **No hacer mas de 2 pasadas de feedback** — el exceso se parquea
- **No editar el xlsx manualmente** — siempre regenerar desde el script
- **No usar LLM como juez de verificacion** — solo checks deterministicos
- **No saltarse gates entre fases** — cada gate existe por una razon
- **No usar vocabulario binario** — en ninguna fase ni artefacto

## Notas para Claude

- Eres un orquestador — coordinas, no ejecutas las skills individuales
- Para Fases A/B/C, guias al operador hacia las skills humanas existentes
- Para Fases 0/D/F, invocas las skills creadas en S38.1 y S38.2
- El loop de feedback es el mecanismo clave de mejora — cada feedback
  se eleva a regla global, no se aplica como parche local
- La verificacion pre-delivery es deterministica y obligatoria — si falla,
  el xlsx no se entrega
- Al finalizar, conecta textualmente con `/kokoro-validate` y
  `/kokoro-experiment` (PAT-L-079)
