# /kokoro-feed-audit — Auditoria del Corpus Meta Ads (Fase D)

> Herramienta transversal: Audita el corpus activo de Meta Ads por angulo
> Aplica en Fase D del pipeline Parrilla de Contenido Comercial
>
> "No hay ads buenos o malos — hay angulos sembrados y angulos por explorar."

## Contexto

Este skill ejecuta la Fase D del pipeline Parrilla de Contenido Comercial:
audita el corpus activo de Meta Ads de un invitado clasificando cada ad
por **angulo narrativo y cluster de Andromeda**, no por desempenio.
El output es un `corpus.json` con cobertura de angulos, angulos ausentes,
y anti-patrones detectados.

**Este skill NUNCA produce listas de "ads a pausar". Solo produce listas
de "angulos a explorar".**

Lee el archivo de conocimiento `kokoro-feed-audit.md` para la metodologia
completa, el schema de `corpus.json`, y el vocabulario canonico de angulos.

### Diferencia con otros skills

- `/kokoro-creative-review` analiza creativos INDIVIDUALES por cluster →
  este skill analiza el CORPUS COMPLETO
- `/kokoro-analytics` consulta metricas numericas → este skill produce
  un catalogo estructurado de angulos
- `/kokoro-parrilla` orquesta las 6 fases → este skill es una fase del pipeline

### Resolucion de invitado

Antes de auditar, resuelve el invitado desde el grafo:

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
2. Si encuentra al invitado:
   - Lee `metadata["platform_accounts"]` para confirmar Meta Ads
   - Lee `metadata.get("context_file")` para enriquecer el analisis
3. Si NO encuentra al invitado:
   - Pide confirmacion de cuenta Meta Ads y export CSV

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Confirma que el usuario quiere ejecutar Fase D:

> "Vamos a auditar tu corpus activo de Meta Ads para entender que angulos
> tienes cubiertos y cuales faltan por explorar. Necesito acceso al feed
> (via MCP o CSV export) y screenshots de los creativos activos.
> ¿Tienes eso disponible? Toma unos 15-20 minutos."

Si el usuario ya confirmo, actua directamente.

### Pipeline de auditoria

#### Paso 1: Obtener datos del feed

Intenta MCP primero:
```
mcp__meta-ads__get_campaign_performance(
  account_id="{act_XXXX}",
  level="ad",
  time_range_since="{YYYY-MM-DD}",
  time_range_until="{YYYY-MM-DD}"
)
mcp__meta-ads__get_ad_creative_details(ad_id="{ad_id_confirmado}")
```

`get_ad_creative_details` requiere un ad ID, no un account ID. Si el reporte
no aporta los IDs necesarios, pidelos mediante exportacion y no inventeslos.

Si MCP no esta disponible (fallback default):
1. Pide al usuario exportar CSV desde Ads Manager
2. Espera a que proporcione el archivo
3. Procesa el CSV

Solicita screenshots: "Comparte los creativos activos (screenshots o
enlaces) para que pueda clasificar cada ad por angulo visual."

#### Paso 2: Clasificar cada ad por angulo y cluster

Siguiendo la metodologia en `kokoro-feed-audit.md`, clasifica cada ad.

Para cada ad, determina:
- **Angulo narrativo:** que historia cuenta este ad
- **Cluster de Andromeda:** donde lo clasifica el sistema de IA
- **Formato:** video, image, carousel, story, stop_motion
- **Fase de delivery:** exploration, learning, optimization

#### Paso 3: Compilar corpus.json

Genera el archivo estructurado con angles_covered, angles_absent,
antipatterns_detected.

#### Paso 4: Presentar resultados

```
## Auditoria de Corpus — {Nombre del Invitado}
**Fuente:** MCP / CSV
**Periodo:** ultimos 30 dias
**Ads analizados:** {N}

### Angulos cubiertos
{lista de angulos con conteo de ads por angulo}

### Angulos ausentes
{lista de angulos que el corpus no toca — estos son los angulos a explorar}

### Anti-patrones detectados
{lista de anti-patrones con descripcion}

### Proximos pasos
- **Angulos a explorar:** {angulos prioritarios}
- **Sugerencia:** usa `/kokoro-ads` para sembrar el cluster ausente con nuevo copy
- **Siguiente fase:** `/kokoro-parrilla` para integrar en la parrilla completa
```

### Persistencia

Guarda el corpus.json en:
```
invitados/{grupo}/feed-audit/corpus-{fecha}.json
```

## Anti-patrones

- **NUNCA producir "ads a pausar"** — solo "angulos a explorar"
- **NUNCA clasificar ads como "ganador" o "perdedor"** — solo cobertura
- **NUNCA recomendar pausa** — si un cluster esta saturado, sugerir diversificar
- **NUNCA usar "funciono", "no funciono", "mejor ad", "peor ad"**
- **No auditar sin screenshots** — el analisis visual es esencial para
  clasificar por angulo
- **No mezclar fuentes** — corpus.json debe indicar si los datos vienen
  de MCP o CSV, no ambos en el mismo archivo

## Notas para Claude

- Usa voz de Eduardo: precision tecnica sin jerga, metaforas agricolas
- El output corpus.json es consumido por `/kokoro-parrilla` (Fase E-F)
- Clasifica por angulo narrativo, no por metrica numerica
- Los anti-patrones son descriptivos, no prescriptivos
- "Angulos a explorar" es el unico output accionable — nunca "ads a pausar"
