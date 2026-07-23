# /kokoro-feed-audit — Metodologia de auditoria del corpus Meta Ads (Fase D)

> Metodologia para auditar el corpus activo de Meta Ads de un invitado
> por **angulo y cluster**, no por desempenio binario. Fase D del pipeline
> Parrilla de Contenido Comercial.
>
> "No hay ads buenos o malos — hay angulos sembrados y angulos por explorar."

## Principio fundacional

El corpus activo de Meta Ads de un invitado es un **ecosistema de angulos**.
Cada ad siembra uno o mas clusters (identidad, progreso, dolor_operativo,
inversion_numerica, comunidad, autoridad, etc.). La auditoria de feed no
clasifica ads por "rendimiento" sino por **cobertura de angulos** — que
clusters estan cubiertos, cuales estan ausentes, y que anti-patrones de
senal se detectan en la distribucion.

**El output NUNCA es una lista de "ads a pausar". El output es una lista de
"angulos a explorar".**

## Input

La auditoria acepta dos fuentes de entrada:

### Fast path: MCP `meta-ads`
Si el MCP Meta Ads esta disponible y responde, usa
`get_campaign_performance` para datos de rendimiento y
`get_ad_creative_details` sólo cuando ya tengas un ad ID confirmado. El
conector no sustituye screenshots ni inventa IDs ausentes.

### Default path: CSV export manual
Si MCP no esta disponible, el operador exporta un CSV manual desde
Ads Manager:
1. Ir a Ads Manager → seleccionar cuenta
2. Exportar → CSV (no Excel)
3. Columnas requeridas: Ad Name, Ad ID, Format, Impressions, CTR, CPC,
   CPM, Frequency, Amount Spent (MXN), Results, Cost per Result
4. Rango: ultimos 30-90 dias

### Screenshots
Adicionalmente, el operador debe proporcionar screenshots de los creativos
activos para analisis visual. Sin screenshots, la auditoria no puede
evaluar el formato ni el hook visual.

## Output: `corpus.json`

La auditoria produce un archivo `corpus.json` con el siguiente schema:

```json
{
  "invitado_slug": "cliente_NN",
  "snapshot_date": "YYYY-MM-DD",
  "source": "mcp" | "csv",
  "ads": [
    {
      "ad_id": "string",
      "ad_name": "string",
      "format": "video" | "image" | "carousel" | "story" | "stop_motion",
      "angle": "identidad" | "dolor_operativo" | "inversion_numerica" | "progreso" | "comunidad" | "autoridad" | "string",
      "cluster": "string",
      "metrics": {
        "impressions_30d": "int",
        "ctr_30d": "float",
        "cpa_30d": "float",
        "frequency_30d": "float"
      },
      "screenshot_path": "string | null",
      "delivery_phase": "exploration" | "learning" | "optimization",
      "notes": "string"
    }
  ],
  "angles_covered": ["array of angle strings"],
  "angles_absent": ["array of angle strings the corpus does NOT touch"],
  "antipatterns_detected": ["string descriptions"]
}
```

### Campos clave

- **angle**: el angulo narrativo que el ad intenta sembrar. Usar una de las
  categorias canonicas o extender con una nueva si es necesario.
- **cluster**: el cluster de Andromeda donde este ad probablemente se clasifica.
- **delivery_phase**: fase de delivery actual del ad segun Meta.
- **angles_covered**: lista de angulos unicos presentes en el corpus.
- **angles_absent**: lista de angulos del vocabulario canonico que NO aparecen
  en ningun ad del corpus. Estos son los **angulos a explorar**.
- **antipatterns_detected**: patrones problematicos observados en la
  distribucion del corpus (ej: concentracion excesiva en un solo angulo,
  formato unico, frecuencia alta en un cluster, etc.).

## Proceso de auditoria

### Paso 1: Recopilar datos
- Intentar MCP primero. Si falla, pedir CSV export.
- Pedir screenshots de cada ad activo (o al menos de los principales).

### Paso 2: Clasificar cada ad por angulo y cluster
Para cada ad en el corpus:
1. Mirar el screenshot (o el ad_name si no hay screenshot)
2. Identificar el **angulo narrativo** principal que comunica
3. Identificar el **cluster de Andromeda** probable
4. Registrar metricas de 30 dias (impressions, CTR, CPA, frequency)
5. Anotar fase de delivery
6. Determinar si el ad introduce un angulo NUEVO o repite uno ya cubierto

### Paso 3: Generar cobertura del corpus
- Compilar `angles_covered` de todos los ads analizados
- Compilar `angles_absent` contra el vocabulario canonico de angulos

### Paso 4: Detectar anti-patrones
Buscar estos anti-patrones en la distribucion del corpus:
- **Concentracion excesiva** (>60% de ads en un solo angulo)
- **Canibalizacion de cluster** (multiple ads con mismo angulo y mismo cluster)
- **Formato unico** (todos los ads son del mismo formato)
- **Frecuencia alta** (frequency >3 en algun cluster — saturacion)
- **Exploration perpetua** (ads en learning phase por >7 dias)
- **Angulo sin cobertura de video** (si el cluster requiere formato video
  pero solo hay imagenes estaticas)

### Paso 5: Compilar corpus.json
Escribir el archivo `corpus.json` en la carpeta del invitado.

## Anti-patrones de la auditoria

- **NUNCA producir "ads a pausar"** — solo "angulos a explorar"
- **NUNCA clasificar ads como "buenos" o "malos"** — solo describir cobertura
- **NUNCA recomendar pausa sin referencias** — si un cluster tiene frecuencia
  alta, sugerir diversificar, no pausar el ad
- **NUNCA usar "funciono", "no funciono", "ganador", "perdedor"** —
  vocabulario prohibido

## Vocabulario canonico de angulos

| Angulo | Descripcion | Cluster tipico |
|--------|-------------|----------------|
| identidad | "Esto es quien eres / quien puedes ser" | identidad |
| dolor_operativo | "Este problema te esta costando tiempo/dinero" | necesidad |
| inversion_numerica | "Esto cuesta X pero vale Y" | logica |
| progreso | "Mira como cambia la situacion" | transformacion |
| comunidad | "No estas solo, otros ya lo hicieron" | pertenencia |
| autoridad | "Expertos confian / datos respaldan" | credibilidad |
| escasez | "Oportunidad limitada en el tiempo" | urgencia |
| aspiracion | "Este es el futuro que puedes tener" | aspiracional |

## Referencias

- `kokoro-meta-ai-ecosystem.md` — sistemas de IA de Meta (GEM, Andromeda, Lattice, Sequence)
- `kokoro-creative-review.md` — analisis de creativos individuales por cluster
- `kokoro-analytics.md` — consulta de metricas con voz corpus-unificada
- `kokoro-quality-gates.md` — gates de calidad pre-delivery
