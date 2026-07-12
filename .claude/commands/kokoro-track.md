---
name: kokoro-track
description: "Herramienta transversal: Guia al usuario a CONFIGURAR la medicion de lo que necesita medir — desde hojas de calculo hasta GA4 y Meta Pixel"
version: 1.0.0
metadata:
  hermes:
    tags: [kokoro, track, medicion, analytics, cuantitativo]
    related_skills: [kokoro-finance, kokoro-connect, kokoro-analytics]
---
# Herramienta transversal: Guia de Medicion (kokoro-track)

> "No puedes mejorar lo que no mides. Y no puedes medir lo que no has configurado."

## Contexto

Este skill existe para cerrar la breca entre "necesito medir X" y "como configuro la medicion de X". Los skills de Fase 1 y 2 identifican QUE medir (margen por canal, CAC, LTV, tasa de activacion). Este skill dice COMO hacerlo.

Tres niveles de sofisticacion:
1. **Hoja de calculo** — manual, sin herramientas, arranque inmediato
2. **Google Analytics + Meta Pixel** — automatico pero requiere configuracion
3. **Pipeline completo** — GA4 + Meta CAPI + CRM + dashboard

Dependiendo del nivel del emprendedor, guia al adecuado. No todos necesitan el nivel 3.

## Input

Este skill LEE el archivo `.kokoro/memoria.md` y `.kokoro/outputs/` para saber QUE necesita medir el negocio.

Si no existe contexto previo, pregunta: "¿Que necesitas medir que hoy no estas midiendo?"

## Instrucciones

### Paso 1: Identificar que medir

Lee `memoria.md` y extrae automaticamente lo que los skills previos identificaron como "necesito medir":

| Fuente | Que dijo que necesita medir |
|--------|---------------------------|
| kokoro-diagnose | Margen, CAC, LTV por canal |
| kokoro-mountain (OKRs) | Engagement IG, recompra, visitas Shopify |
| kokoro-finance | CPA real, ROI, conversion por canal |
| kokoro-funnel | Tasa de conversion por etapa del embudo |

Si no hay contexto: preguntar "¿Que 3 numeros necesitas ver cada semana para saber si tu negocio esta sano?"

### Paso 2: Elegir nivel

Preguntar:
> "Hay 3 formas de medir esto. Cada una requiere distinto nivel de herramientas y tiempo:
>
> 1. **Hoja de calculo** — hoy mismo, gratis, manual (15 min/semana)
> 2. **GA4 + Pixel** — configuracion unica, automatico, requiere cuenta Google (1-2 horas)
> 3. **Pipeline completo** — GA4 + Meta CAPI + CRM + dashboard (2-3 dias, asistencia tecnica)
>
> ¿Con cual arrancamos?"

### Paso 3: Guiar la configuracion

Dependiendo del nivel elegido:

**Nivel 1 — Hoja de calculo:**
- Generar plantilla CSV con columnas: Semana, Canal, Impresiones, Clics, Inversion, Leads, Clientes, Ingresos, Margen, CAC, LTV
- Instrucciones: "Cada lunes llenas la fila de la semana anterior. En 4 semanas tienes datos para decidir."

**Nivel 2 — GA4 + Pixel:**
- Pasos: 1) Crear propiedad GA4 2) Instalar gtag en Shopify 3) Configurar eventos (page_view, view_item, add_to_cart, purchase) 4) Instalar Meta Pixel 5) Configurar conversion en Meta
- Referencia: skill kokoro-connect + kokoro-meta-capi

**Nivel 3 — Pipeline completo:**
- Derivar a: skill kokoro-connect para cuentas, skill kokoro-meta-capi para CAPI, y configurar dashboard

### Paso 4: Persistir

Guardar en `.kokoro/outputs/sNN-track.md` con:
- Que se va a medir
- En que nivel
- Proximos pasos concretos
- Fecha de la primera revision de datos

Actualizar `memoria.md` y `state.json`.

## Contrato con otros skills

- **kokoro-finance** necesita metricas de margen, CAC, LTV → este skill le da el como
- **kokoro-funnel** necesita metricas por etapa → este skill configura el tracking
- **kokoro-connect** conecta las cuentas → este skill dice cuales y para que
