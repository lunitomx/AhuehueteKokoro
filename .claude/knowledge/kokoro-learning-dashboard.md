# Learning Dashboard — Guía para Invitados

> Tu historial de aprendizaje en Kokoro para Google Ads.

## 1) Qué es

El Learning Dashboard es el registro de sesiones por invitado dentro de `metadata.session_log`. No es una base de datos nueva ni una app separada: es el mismo histórico que ya usa Kokoro, con campos de seguimiento de aprendizaje.

Cuando vuelves a abrir un invitado, Kokoro recuerda lo que se hizo, lo aprendido y el siguiente paso.

## 2) Cómo leerlo

Cada entrada incluye, como mínimo:

- `date`: fecha de la sesión.
- `type`: tipo de trabajo (`gads`, `creative`, `ads`, etc.).
- `summary`: lo hecho (1-2 líneas).
- `hallazgos`: aprendizajes concretos sobre la audiencia, el mercado o el resultado.
- `next_action`: el siguiente paso sugerido.

Cuando aplica Google Ads, también puede incluir:

- `platform`: `google_ads`
- `campaign_type`: `search`, `display`, `pmax`, `shopping`, `other`
- `learning_state`: `learning`, `stable`, `needs_attention`
- `task_group`: `insight`, `optimization`, `launch`
- `task`: tarea concreta de ese bloque
- `cadence`: `72h`, `weekly`, `monthly`, `90d`
- `landing_page`, `asset_group`, `change_made`, `reason`

Regla práctica:
- Si viene `learning_state`, úsalo para decidir si seguimos probando (`learning`) o si estabilizamos (`stable`) o si hay correcciones urgentes (`needs_attention`).

## 3) Flujo de control en 3 capas

### Capa de plan

- Qué se va a trabajar (contexto y objetivo de la sesión).

### Capa de ejecución

- Qué se produjo y se registró (`artifacts`, entregables, cambios recomendados o ejecutados).

### Capa de aprendizaje

- Qué se aprendió y cuál es el siguiente paso natural (`hallazgos` + `next_action`).

## 4) Diferencias clave entre documentos

- **session_log**: resumen histórico de sesiones por invitado (esto es el Learning Dashboard).
- **validation plan**: cómo se piensa y valida una hipótesis.
- **experiment report**: resultados concretos de pruebas y decisiones.

Usa los tres como una secuencia: plan -> ejecutar -> aprender -> repetir.

## 5) Atribución de método

Esta metodología de aprendizaje y mejora iterativa toma base de **LeanStack** y de los principios de estructuración de hipótesis de **Ash Maurya** (`Lean Stack` / `Problem-Solution-Fit`).
