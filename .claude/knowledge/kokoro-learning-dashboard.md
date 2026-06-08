# Kokoro Learning Dashboard — Control de Plan, Ejecucion y Aprendizaje

> "Lo que se planifica, se ejecuta y se aprende debe vivir en el mismo
> sistema. Si no, Kokoro recuerda por partes y el invitado repite por
> partes."

> LeanStack es un marco creado por Ash Maurya. Kokoro lo usa con
> atribucion explicita en sus artefactos de validacion y experimentacion.

## Proposito

Este artefacto formaliza el sistema de control que Kokoro usa para llevar
memoria de todo lo que se hace con un invitado, una campana, una creacion
o una hipotesis.

No es una UI.
No es un runtime.
No es un almacen de secretos.

Es el modelo de conocimiento que permite ver, en un solo lugar, tres capas:

1. **Plan** - que ibamos a probar
2. **Ejecucion** - que hicimos realmente
3. **Aprendizaje** - que quedo validado y que sigue

## Criterio Central

Kokoro no deberia depender de memoria conversacional para saber:

- que se queria validar
- que se cambio
- que funciono
- que no funciono
- que landing, asset, campaña o tactica estaba activa
- cual es el siguiente paso

Si esa informacion no esta en un artefacto formal, se pierde.

## Las 3 Capas Del Sistema

### 1. Plan

La capa de plan responde a la pregunta:

> "¿Que vamos a probar antes de invertir mas?"

Aqui vive el lenguaje de `Validation Plan` de LeanStack:

- BACKGROUND
- CURRENT CONDITION
- FUTURE CONDITION
- ANALYSIS
- PROPOSAL
- FOLLOW-ON PLANS

Uso:
- antes de una apuesta nueva
- antes de una nueva linea
- antes de una validacion con costo real

### 2. Ejecucion

La capa de ejecucion responde a la pregunta:

> "¿Que hicimos realmente y con que contexto?"

Aqui vive el historial operativo del invitado:

- `session_log`
- cambios realizados
- notas de revision
- cadencia
- tipo de campaña
- landing utilizada
- assets en uso

Esta capa debe ser suficientemente compacta para abrirse en `kokoro-open`
y suficientemente rica para no obligar al invitado a repetir el contexto.

### 3. Aprendizaje

La capa de aprendizaje responde a la pregunta:

> "¿Que sabemos ahora que no sabiamos antes?"

Aqui vive el lenguaje de `Experiment Report` de LeanStack:

- BACKGROUND
- FALSIFIABLE HYPOTHESES
- DETAILS
- RESULTS
- VALIDATED LEARNING
- NEXT ACTION

Uso:
- al cerrar un sprint
- al cerrar una iteracion
- al decidir perseverar, pivotar o pausar

## Fuentes De Verdad

### Fuente publica

El repositorio publico guarda:

- el modelo
- los templates
- las guias de uso
- los campos estandar
- la forma de leer el sistema

### Fuente privada

La ejecucion real vive fuera del repositorio publico:

- MCP
- `.env`
- credenciales
- exports privados
- runtime operacional

El repositorio no debe contener esa capa.

## Entidades Del Dashboard

### Learning Record

Una entrada formal que conecta plan, ejecucion y aprendizaje.

Campos base:
- `date`
- `client_id`
- `type`
- `skill`
- `summary`
- `hallazgos`
- `artifacts`
- `next_action`

Campos opcionales segun el caso:
- `platform`
- `campaign_type`
- `task_group`
- `task`
- `cadence`
- `landing_page`
- `asset_group`
- `change_made`
- `reason`
- `learning_state`
- `status`
- `evidence`

### Validation Plan

Objeto de plan previo a la inversion.

Usa LeanStack con atribucion explicita a Ash Maurya.

### Experiment Report

Objeto de cierre despues del sprint.

Usa LeanStack con atribucion explicita a Ash Maurya.

### Session Log

Historial continuo por invitado.

Es la memoria operativa diaria.

## Vista Operativa

Si el invitado entra a Kokoro, el sistema deberia poder responder:

| Pregunta | Fuente |
|---|---|
| ¿Que se queria validar? | Validation Plan |
| ¿Que se hizo? | Session Log |
| ¿Que se cambio? | Session Log + changes |
| ¿Que se aprendio? | Experiment Report |
| ¿Que sigue? | NEXT ACTION / next_action |

## Reglas Del Sistema

1. No mezclar plan y aprendizaje en un solo bloque.
2. No registrar aprendizaje sin contexto de ejecucion.
3. No guardar secretos, env ni runtime privado.
4. No inventar `learning_state` si no esta claro.
5. No reemplazar el control humano con automatismo opaco.
6. No usar el dashboard como UI; es un modelo de conocimiento.

## Relacion Con Kokoro Google Ads

En Google Ads, este sistema permite registrar:

- tipo de campaña
- tarea revisada
- cadencia de revision
- notas de lo que funciono y no funciono
- landing activa
- assets en uso
- cambios hechos
- aprendizaje acumulado

Eso convierte la operacion en una memoria utilizable, no en notas sueltas.

## Relacion Con LeanStack

Kokoro usa LeanStack para dos momentos canonicos:

- **Validation Plan** antes de invertir
- **Experiment Report** al cierre del sprint

La atribucion a LeanStack y Ash Maurya debe mantenerse visible cuando se use
ese marco.

## Regla Final

Si una decision, aprendizaje o cambio importa para el siguiente paso, no
debe depender de la memoria del chat.

Debe quedar en este sistema.
