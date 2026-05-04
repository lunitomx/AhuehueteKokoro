# /kokoro-scorecard — Vista Unificada del Invitado

> Herramienta transversal: Scorecard ejecutivo cross-platform
> Aplica en Fase 4 (Cosechar) — complementa /kokoro-analytics

> "Los numeros no mienten, pero tampoco hablan solos. Necesitan un
> interprete que los convierta en direccion."

## Contexto

Este skill genera un scorecard ejecutivo unificado que consulta TODAS
las plataformas conectadas del invitado (Meta Ads, Google Ads, GA4,
Search Console) y presenta una vista consolidada con tendencias,
indicadores de salud, e insights accionables.

Complementa a `/kokoro-analytics` — analytics responde preguntas
puntuales, scorecard da la vista panoramica.

Lee `kokoro-analytics-metrics.md` para traducciones de metricas.

### Dependencias

- **MCP servers**: facebook-ads, google-ads, google-analytics, google-search-console
- **Invitado conectado**: metadata["platform_accounts"] con al menos 1 plataforma

### Resolucion de invitado

1. Busca en `.kokoro/clients.json` via `find_by_name`
2. Lee `metadata["platform_accounts"]` para plataformas conectadas
3. Si no tiene plataformas → sugiere `/kokoro-connect` primero
4. Presenta: "Invitado: {name} | Plataformas: {lista}"

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Un buen scorecard no te dice que hacer — te muestra donde mirar.
> Es la vista desde la montana de tus numeros. Generemos tu panorama."

### Proceso — 4 pasos

### Paso 1: Consultar todas las plataformas

Para cada plataforma conectada, ejecutar tools de resumen:

**Meta Ads** (si conectado):
```
mcp__facebook-ads__get_account_insights_summary(account_id, date_preset="last_7d")
mcp__facebook-ads__get_campaign_performance(account_id, date_preset="last_7d")
```

**Google Ads** (si conectado):
```
mcp__google-ads__get_campaign_performance(customer_id, date_range="LAST_7_DAYS")
```

**GA4** (si conectado):
```
mcp__google-analytics__run_report(property_id, dimensions=["date","sessionDefaultChannelGroup"], metrics=["sessions","totalUsers","bounceRate","averageSessionDuration"], date_range="last7days")
```

**Search Console** (si conectado):
```
mcp__google-search-console__get_performance_overview(site_url, days=7)
```

Consultar tambien el periodo anterior (7 dias previos) para tendencias.

### Paso 2: Calcular indicadores de salud

Para cada plataforma, asignar semaforo:

| Indicador | Verde | Amarillo | Rojo |
|-----------|:-----:|:--------:|:----:|
| **Meta Ads CTR** | > 2% | 1-2% | < 1% |
| **Meta Ads CPC** | < $5 MXN | $5-15 MXN | > $15 MXN |
| **Google Ads Quality Score** | > 7 | 5-7 | < 5 |
| **GA4 Bounce Rate** | < 40% | 40-60% | > 60% |
| **GSC Click-through Rate** | > 3% | 1-3% | < 1% |

Adaptar umbrales segun la industria del invitado si es posible.

### Paso 3: Generar insights cross-platform

Buscar patrones entre plataformas:
- ¿El trafico de ads se convierte en sesiones GA4?
- ¿Las keywords de GSC coinciden con los keywords de Google Ads?
- ¿El costo por resultado de Meta se refleja en conversiones de GA4?
- ¿Hay canales que generan trafico pero no conversion?

### Paso 4: Presentar scorecard

## Plantilla de Salida

```
## Scorecard — {invitado}
Periodo: {fecha_inicio} a {fecha_fin} (7 dias)
Plataformas: {lista de conectadas}
Generado: {YYYY-MM-DD}

### Resumen Ejecutivo

{2-3 lineas: como le va al invitado en general, tendencia principal}

### Meta Ads {semaforo}

| Metrica | Valor | vs Anterior | Tendencia |
|---------|:-----:|:-----------:|:---------:|
| Inversion total | ${X} MXN | {+/-}% | {up/down} |
| Alcance | {N} personas | {+/-}% | {up/down} |
| Impresiones | {N} veces | {+/-}% | {up/down} |
| CTR | {X}% | {+/-}pp | {up/down} |
| CPC | ${X} MXN | {+/-}% | {up/down} |
| Resultados | {N} | {+/-}% | {up/down} |

Campanas activas: {N}
Mejor campana: {nombre} (CTR {X}%, {N} resultados)

### Google Ads {semaforo}

| Metrica | Valor | vs Anterior | Tendencia |
|---------|:-----:|:-----------:|:---------:|
| Inversion | ${X} MXN | {+/-}% | {up/down} |
| Clics | {N} | {+/-}% | {up/down} |
| CTR | {X}% | {+/-}pp | {up/down} |
| CPC | ${X} MXN | {+/-}% | {up/down} |

Top keywords: {keyword1}, {keyword2}, {keyword3}

### GA4 — Sitio Web {semaforo}

| Metrica | Valor | vs Anterior | Tendencia |
|---------|:-----:|:-----------:|:---------:|
| Sesiones | {N} | {+/-}% | {up/down} |
| Usuarios | {N} | {+/-}% | {up/down} |
| Bounce rate | {X}% | {+/-}pp | {up/down} |
| Duracion promedio | {X} min | {+/-}% | {up/down} |

Top canales: {canal1} ({X}%), {canal2} ({X}%), {canal3} ({X}%)

### Search Console — SEO {semaforo}

| Metrica | Valor | vs Anterior | Tendencia |
|---------|:-----:|:-----------:|:---------:|
| Impresiones | {N} | {+/-}% | {up/down} |
| Clics | {N} | {+/-}% | {up/down} |
| CTR | {X}% | {+/-}pp | {up/down} |
| Posicion promedio | {X} | {+/-} | {up/down} |

Top queries: {query1}, {query2}, {query3}

### Insights Cross-Platform

{3-5 observaciones que conectan datos entre plataformas}

1. {insight — ej: "El trafico de Meta Ads representa el X% de las
   sesiones en GA4, pero el bounce rate de ese canal es alto"}
2. {insight — ej: "Las keywords con mejor rendimiento en Google Ads
   coinciden con las que posicionan organicamente en GSC"}
3. {insight}

### Indicadores de Salud

| Plataforma | Estado | Nota |
|------------|:------:|------|
| Meta Ads | {verde/amarillo/rojo} | {1 linea} |
| Google Ads | {verde/amarillo/rojo} | {1 linea} |
| GA4 | {verde/amarillo/rojo} | {1 linea} |
| Search Console | {verde/amarillo/rojo} | {1 linea} |

### Acciones Recomendadas

1. {accion concreta basada en los datos}
2. {accion concreta}
3. {accion concreta}

### Siguiente paso

- `/kokoro-analytics` para profundizar en una plataforma especifica
- `/kokoro-ads` para generar creativos si Meta necesita contenido nuevo
- `/kokoro-intel` para analizar competencia en contenido
- `/kokoro-rhythm` para integrar estas metricas en tu ritmo semanal
```

## Plataformas no conectadas

Si una plataforma no esta en platform_accounts, mostrar:
```
### {Plataforma} — No conectada
Conecta esta plataforma con `/kokoro-connect` para incluirla
en tu scorecard.
```

No omitir la seccion — mostrar que existe y que se puede conectar.

## Notas para Claude

- Usa la voz de Eduardo: "vista desde la montana", "los numeros hablan"
- "Inversion" no "gasto", "invitado" no "cliente", "creacion" no "producto"
- Los semaforos son guia, no juicio — adaptar a la industria
- Insights cross-platform son el VALOR PRINCIPAL — no solo listar numeros
- Si una plataforma falla, mostrar las demas sin bloquear
- Consulta kokoro-analytics-metrics.md para traducciones de metricas
- IMPORTANTE: Siempre comparar vs periodo anterior — tendencia > valor absoluto
- IMPORTANTE: Acciones recomendadas deben ser CONCRETAS y basadas en datos

## Persistencia

### Session Log

```python
entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "scorecard",
    "skill": "/kokoro-scorecard",
    "client_id": client.id,
    "summary": "Scorecard {periodo}: {N} plataformas, {resumen_salud}",
    "hallazgos": ["{insights cross-platform principales}"],
    "artifacts": [],
    "next_action": "{accion prioritaria basada en datos}"
}
```
