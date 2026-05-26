# /kokoro-tracking-check — Verificacion de Tracking (Fase 0)

> Herramienta transversal: Audita la salud de medicion digital de un invitado
> Aplica ANTES de cualquier parrilla de contenido (Fase 0 del pipeline)
>
> "Si el tracking miente, los datos no son datos — son ruido con formato."

## Contexto

Este skill ejecuta la Fase 0 del pipeline Parrilla de Contenido Comercial:
verifica que el tracking digital del invitado este sano antes de invertir
tiempo en analisis de datos o creacion de contenido. Puede correr standalone
(herramienta transversal) o como pre-check de `/kokoro-parrilla`.

Lee el archivo de conocimiento `kokoro-tracking-checklist.md` para la
metodologia completa de los 5 dominios de verificacion.

### Resolucion de invitado

Antes de ejecutar, resuelve el invitado desde el grafo:

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
2. Si encuentra al invitado:
   - Lee `metadata["platform_accounts"]` para saber que plataformas tiene
   - Lee `metadata.get("landing_url")` para la URL de prueba
3. Si NO encuentra al invitado:
   - Pide la URL de la landing page manualmente
   - Pide confirmacion de plataformas activas (Meta Ads, Google Ads, CRM)

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Confirma que el usuario quiere ejecutar Fase 0 antes de empezar:

> "Vamos a revisar la salud del tracking de tu invitado antes de construir
> cualquier cosa. Esto implica verificar pixel, UTMs, llegada a CRM y
> compliance Google. Toma entre 10-15 minutos. ¿Te parece? ¿Tienes acceso
> a la landing, al CRM y al Events Manager?"

Si el usuario ya incluyo el nombre y confirmacion, actua directamente.

### Pipeline de verificacion

#### Paso 1: Ejecutar los 5 dominios

Para cada dominio, sigue la metodologia en `kokoro-tracking-checklist.md`.
Si hay MCP disponible para alguna plataforma (GA4 para verificar eventos,
Pipedrive para verificar llegada de leads), intenta validacion automatica.
Si no, guia al usuario paso a paso con instrucciones claras.

##### D1 — Pixel: submit vs page-view

Pregunta al usuario si puede abrir la landing en una pestana de incognito
y compartir lo que ve en la pestana Network. Si hay MCP GA4, verifica
eventos registrados.

##### D2 — Duplicados generate_lead

Pregunta si puede enviar un lead de prueba y revisar Events Manager.
Alternativamente, si hay MCP GA4, revisar eventos duplicados.

##### D3 — Llegada a CRM + closer visibility

Si hay MCP Pipedrive, verifica automaticamente la llegada del lead.
Si no, pide al usuario que verifique manualmente y comparta el resultado.

##### D4 — UTM persistence

Guia al usuario en la prueba de UTMs. Si hay MCP GA4, verificar que
las UTMs aparecen en los parametros de eventos.

##### D5 — Google Ads compliance

Si hay MCP Google Ads, verifica estado de verificacion de anunciante.
Si no, pregunta al usuario si ha completado el proceso.

#### Paso 2: Generar gap-list priorizada

Para cada dominio, reporta:

```
## D{N} — {Nombre del dominio}
**Estado:** OK / CRITICO / WARNING
**Evidencia:** {que se vio / que se confirmo}
**Recomendacion:** {que hacer si es critico/warning}
```

#### Paso 3: Verdicto final

```
---
## Verdicto Fase 0
**Resultado:** GO / WAIT
**Criticos:** {N}
**Warnings:** {N}

{Si GO:} El tracking esta sano. Puedes proceder a Fase A del pipeline.
{Si WAIT:} Hay {N} criticos que reparar antes de continuar.
  Prioridad de reparacion:
  1. {critico mas grave}
  2. {siguiente critico}
```

### Plantilla de Salida

```
## Fase 0 — Tracking Check para {Nombre del Invitado}

| Dominio | Estado |
|---------|--------|
| D1 Pixel (submit vs page-view) | OK / CRITICO / WARNING |
| D2 Duplicados generate_lead | OK / CRITICO / WARNING |
| D3 CRM + closer visibility | OK / CRITICO / WARNING |
| D4 UTM persistence | OK / CRITICO / WARNING |
| D5 Google Ads compliance | OK / CRITICO / WARNING |

---

### D1 — Pixel: submit vs page-view
**Estado:** {OK / CRITICO / WARNING}
**Evidencia:** {detalle de lo verificado}
**Recomendacion:** {accion si aplica}

### D2 — Duplicados generate_lead
**Estado:** {OK / CRITICO / WARNING}
**Evidencia:** {detalle}
**Recomendacion:** {accion si aplica}

### D3 — CRM + closer visibility
**Estado:** {OK / CRITICO / WARNING}
**Evidencia:** {detalle}
**Recomendacion:** {accion si aplica}

### D4 — UTM persistence
**Estado:** {OK / CRITICO / WARNING}
**Evidencia:** {detalle}
**Recomendacion:** {accion si aplica}

### D5 — Google Ads compliance
**Estado:** {OK / CRITICO / WARNING}
**Evidencia:** {detalle}
**Recomendacion:** {accion si aplica}

---
## Verdicto Fase 0
**Resultado:** GO / WAIT
```

### Siguiente paso

- Si GO y hay pipeline Parrilla activo → "Puedes continuar con `/kokoro-parrilla`"
- Si GO standalone → "Tracking verificado. Guarda este reporte como baseline."
- Si WAIT → "Repara los criticos primero. Usa `/kokoro-tracking-check` para re-verificar."

## Anti-patrones

- **No saltarse dominios** — ejecutar los 5 siempre, aunque algunos sean
  automaticos y otros manuales
- **No asumir tracking sano** — verificar cada dominio, no confiar en
  configuraciones previas
- **No minimizar criticos** — un CRITICO es bloqueante, no un "lo revisamos despues"
- **No usar "cliente", "producto", "precio"** — vocabulario Kokoro siempre

## Notas para Claude

- Usa voz de Eduardo: precision tecnica sin jerga, metaforas agricolas
- Cuando MCP no esta disponible, guia al usuario paso a paso
- Distingue claramente entre CRITICO (bloqueante) y WARNING (riesgo documentado)
- El output gap-list es el input gate para Fase A del pipeline Parrilla
- Si el lead de prueba es un invitado real, usar datos anonimizados
  ("Test Fase 0", email test@tracking-check.local)

## Persistencia

Guarda el reporte en:
```
invitados/{grupo}/tracking/fase-0-{fecha}.md
```
