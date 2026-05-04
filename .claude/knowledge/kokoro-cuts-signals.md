# Senales de Corte — Referencia Tecnica para /kokoro-cuts

> Skill: `/kokoro-cuts`
> Herramienta transversal: aplica en cualquier fase

> "El ojo entrenado no busca contenido — encuentra los momentos
> donde la verdad se concentra."

## Proposito

Referencia tecnica para el skill `/kokoro-cuts`. Documenta las senales que
identifican momentos de alto valor en una transcripcion, el formato de
transcripcion esperado, las reglas de escalamiento por duracion, y el
esquema JSON de salida.

## Las 5 Senales de Corte

Cada senal representa una dimension de valor para contenido corto. Un buen
corte tipicamente puntua alto en 2-3 senales simultaneamente.

### 1. Densidad de Contenido (peso: 25%)

Una idea completa expresada en pocas oraciones, sin divagacion. El hablante
va al punto y entrega valor en espacio compacto.

**Indicadores positivos:**
- Definiciones claras ("X es cuando...")
- Frameworks expresados en una frase ("Los 3 pilares de...")
- Datos concretos con contexto ("El 70% de las personas...")
- Consejos accionables y especificos

**Indicadores negativos:**
- Repeticion de la misma idea con diferentes palabras
- Muletillas y relleno ("bueno, como te decia, este...")
- Contexto excesivo antes de llegar al punto

### 2. Potencial de Hook (peso: 25%)

La frase de apertura del segmento funciona como gancho en los primeros
3 segundos de un short. Captura atencion inmediata.

**Patrones de hook efectivo:**
- Pregunta provocadora: "¿Sabias que el 90% de los negocios...?"
- Afirmacion contracultural: "El marketing de contenido esta muerto"
- Promesa concreta: "Esto cambio completamente mi manera de..."
- Anecdota personal: "Cuando perdi mi primer negocio..."
- Dato impactante: "Solo 3 de cada 100 emprendedores..."

**Hooks debiles (evitar):**
- Generalidades: "Hoy vamos a hablar de..."
- Saludos: "Hola, bienvenidos al canal..."
- Transiciones suaves sin fuerza propia

### 3. Transicion Tematica (peso: 10%)

Cambios claros de tema que marcan limites naturales de segmento. Utiles
para determinar donde empieza y termina un corte.

**Indicadores:**
- Frases de transicion: "Ahora bien...", "Pasemos a...", "Otro punto..."
- Cambio de tono o ritmo en la conversacion
- Pregunta del entrevistador que abre nuevo tema
- Pausa natural seguida de tema diferente

### 4. Pico Emocional (peso: 20%)

Momentos de intensidad que generan conexion humana. El contenido con
emocion se comparte mas y retiene mejor.

**Indicadores:**
- Anecdotas personales con vulnerabilidad
- Humor natural (no forzado)
- Pasion evidente en la voz (detectable por exclamaciones,
  enfasis, repeticion intencional)
- Momentos de revelacion o insight inesperado
- Conflicto o tension narrativa

### 5. Valor Autonomo (peso: 20%)

El segmento se entiende completamente solo, sin necesitar contexto del
resto del video. Critico para shorts que se distribuyen independientemente.

**Indicadores positivos:**
- El segmento tiene inicio, desarrollo y cierre propio
- No depende de "como decia antes..." o "volviendo al tema..."
- Los referentes son universales, no internos al video
- Funciona si alguien lo ve sin haber visto nada mas

**Indicadores negativos:**
- Referencias a algo dicho anteriormente
- Pronombres ambiguos ("eso que mencionamos")
- Depende de contexto visual no presente en audio

## Formato de Transcripcion Esperado

El skill `/kokoro-cuts` consume transcripciones generadas por `/kokoro-listen`.
El formato tiene un header de metadata seguido del texto:

```
============================
TRANSCRIPCION
Fuente: {url}
Titulo: {titulo del video}
Duracion: {duracion en formato M:SS o H:MM:SS}
Fecha: {YYYY-MM-DD}
Idioma: {es/en}
Costo: ~${costo} USD
============================

{transcripcion completa como texto plano}
```

### Parseo del header

1. Buscar las lineas entre los delimitadores `====`
2. Extraer campos por prefijo: `Fuente:`, `Titulo:`, `Duracion:`, etc.
3. Todo despues del segundo delimitador `====` es la transcripcion
4. Si el formato no coincide, pedir al usuario que confirme la metadata
   manualmente

### Parseo de duracion

La duracion viene en formato libre del video original. Convertir a segundos:
- `3:43` → 223 segundos
- `1:05:30` → 3930 segundos
- `45` → 45 segundos (asumido como segundos)

## Reglas de Escalamiento por Duracion

La cantidad de cortes sugeridos se escala con la duracion del video fuente
para evitar sobre-segmentacion de videos cortos o sub-representacion de
videos largos.

| Duracion del video | Rango de cortes | Logica |
|--------------------|-----------------|--------|
| < 5 minutos | 1-3 | Video corto, pocos momentos diferenciados |
| 5-30 minutos | 3-7 | Rango tipico de entrevistas y charlas |
| > 30 minutos | 5-10 | Videos largos, mas oportunidades |

**Regla de calidad:** Nunca llenar la cuota solo por llenar. Si un video
de 20 minutos solo tiene 2 momentos con score >= 6, sugerir 2 cortes.
La honestidad es mas valiosa que la cantidad.

**Umbral minimo de score:** 6/10. Cortes debajo de este umbral no se
presentan al usuario.

## Esquema JSON de Salida

El archivo JSON se guarda junto a la transcripcion como `{basename}-cuts.json`.

```json
{
  "source_transcript": "/path/to/transcript.txt",
  "video_title": "Titulo original del video",
  "video_duration": "3:43",
  "video_url": "https://...",
  "cuts_count": 2,
  "cuts": [
    {
      "rank": 1,
      "score": 9,
      "title": "Titulo sugerido para el short",
      "hook": "Frase de apertura para overlay de texto",
      "excerpt": "Texto completo del segmento seleccionado",
      "start_sentence": "Primera oracion del corte...",
      "end_sentence": "Ultima oracion del corte...",
      "estimated_duration_seconds": 45,
      "rationale": "Explicacion de por que este momento fue seleccionado"
    }
  ]
}
```

### Campos del corte

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| rank | int | Posicion en el ranking (1 = mejor) |
| score | int | Puntuacion final 1-10 |
| title | string | Titulo sugerido para YouTube Short / IG Reel |
| hook | string | Frase de apertura (~10 palabras) |
| excerpt | string | Texto completo del segmento |
| start_sentence | string | Primera oracion (para localizar en video) |
| end_sentence | string | Ultima oracion (para localizar en video) |
| estimated_duration_seconds | int | Duracion estimada (~150 palabras/min) |
| rationale | string | Justificacion del corte |

### Estimacion de duracion

Calcular basandose en velocidad promedio de habla:
- ~150 palabras por minuto (habla natural en espanol)
- Contar palabras del excerpt
- `duracion_segundos = (palabra_count / 150) * 60`
- Redondear a multiplos de 5 segundos

## Flujo con Otros Skills

```
/kokoro-listen → transcripcion.txt
/kokoro-cuts   → transcripcion-cuts.json
/kokoro-shorts → extraccion de segmentos de video (futuro)
/kokoro-creative → thumbnails para cada short
```

El JSON de cortes es el contrato entre `/kokoro-cuts` y `/kokoro-shorts`.
Los campos `start_sentence` y `end_sentence` permiten localizar el segmento
en el video original.
