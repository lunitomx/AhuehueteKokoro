# /kokoro-diagnose-anclas — Mapa de Anclas: Causas Raiz

> Sub-skill de /kokoro-diagnose — NO invocar directamente
> Produce: `.kokoro/diagnostics/anclas.md`

## Contexto

Guia al emprendedor paso a paso por el ejercicio del Mapa de Anclas para
identificar causas raiz de los problemas del negocio.

El negocio es un barco. Hay fuerzas que lo impulsan y fuerzas que lo frenan.

Lee tambien `kokoro-dinamicas-vivas.md`. La base de dinamicas vivas de Kokoro
esta inspirada en la lectura privada del libro de referencia y en practicas
publicas de facilitacion visual. Es una adaptacion Kokoro, no una
implementacion de esa metodologia. Refuerza cuatro reglas: capturar anclas por escrito, no
defenderse durante la sesion, conservar la disposicion visual de las anclas y
procesar despues por area, severidad y prioridad.

## Instrucciones

### Paso 1 — Vientos (fortalezas)

Pregunta: "Si tu negocio es un barco, ¿que vientos lo estan impulsando
ahora mismo? ¿Que esta funcionando bien?"

Escucha. Profundiza. No saltes a los problemas todavia.

### Paso 2 — Anclas (obstaculos)

Pregunta: "Ahora dime, ¿que anclas estan frenando tu barco? ¿Que te
esta deteniendo de avanzar a la velocidad que quieres?"

Para cada ancla, profundiza:
- "¿Eso es la causa raiz o es un sintoma de algo mas profundo?"
- "¿Desde cuando tienes esta ancla?"
- "¿Que has intentado para cortarla?"
- "Si cortaras esta ancla, ¿cuanto mas rapido avanzaria el barco?"
- "¿Esta ancla te afecta a ti solo o tambien a otros invitados/equipo?"

### Paso 3 — Rocas bajo el agua (riesgos)

Pregunta: "¿Que rocas ves debajo del agua? Riesgos que podrian hundir
el barco si no los atiendes."

### Paso 3B — Fricciones operativas

Cuando un ancla describe un recorrido que se repite, entiende primero como
funciona hoy. No propongas una solucion ni una automatizacion todavia. Pregunta
de una en una:

- "Muéstrame el recorrido actual, desde que empieza hasta que termina."
- "¿Cuánto tiempo ocupa cada vez y cuántas veces sucede en una semana normal?"
- "¿A quiénes carga o involucra este recorrido?"
- "¿Qué sistemas, hojas o mensajes intervienen?"
- "¿Qué consecuencia visible tiene cuando se retrasa o se repite?"
- "¿Qué hecho, ejemplo o patrón repetido sostiene esta lectura?"
- "¿Qué dato todavía no conocemos?"

Registra lo observado sin completar datos faltantes:

| Campo | Qué registrar |
|-------|---------------|
| Recorrido actual | Inicio, pasos y cierre; `Pendiente` si no se conoce. |
| Evidencia | Frase, hecho, métrica, ejemplo o patrón repetido. |
| Tiempo y frecuencia | Minutos por vez y veces por semana, o `Pendiente`. |
| Personas y sistemas | Quién participa y qué herramientas intervienen. |
| Consecuencia | Efecto observable sobre seguimiento, carga, experiencia o confianza. |
| Riesgo | Bajo, medio, alto o `Pendiente`, con la razón disponible. |
| Por aclarar | Preguntas que necesitan evidencia antes de decidir. |

No inventes números ni uses cero como sustituto de lo desconocido. Si el
recorrido toca credenciales, inversión, datos personales, permisos o una
acción externa, marca el riesgo como alto: el diagnóstico sólo lo entiende y
no realiza cambios en CRM, Ads Manager, calendarios ni otras herramientas.

### Paso 4 — Priorizacion

De todas las anclas y rocas identificadas, pregunta:
- "Si pudieras cortar UNA sola ancla esta semana, ¿cual tendria mas
  impacto en la velocidad de tu barco?"
- "¿Que ancla te quita el sueno?"
- "¿Cual es urgente por dolor y cual es importante por estrategia?"

### Regla de Facilitacion — No Defender

Si una ancla parece injusta, incompleta o equivocada, no corrijas en tiempo
real. Primero entiende. Pregunta:

- "Ayudame a entender que viste para escribir esta ancla."
- "Que experiencia concreta la hizo sentir pesada?"
- "Que impacto tuvo en tu avance?"

La respuesta o plan se prepara despues, en el reporte. Si respondes durante el
juego, la persona aprende a negociar contigo en vez de mostrarte la verdad de
su experiencia.

### Procesamiento

Al terminar, clasifica cada ancla o grupo de anclas:

| Campo | Opciones |
|-------|----------|
| Area | Oferta, operacion, seguimiento, medicion, equipo, experiencia, confianza |
| Severidad | Critica, alta, media, baja |
| Prioridad | Inmediata, urgente, antes del siguiente ciclo, cuando haya capacidad, diferir |
| Evidencia | Frase, hecho, metrica, ejemplo o patron repetido |

Si la energia de la sala empieza a proponer soluciones, captura motores
posibles, pero no cambies el foco antes de entender las anclas. Si el objetivo
ya es crear alternativas, deriva despues a `/kokoro-caja-creativa`,
`/kokoro-prune` o `/kokoro-dinamicas-vivas`.

### Output: anclas.md

Crear `.kokoro/diagnostics/anclas.md`:

```markdown
# Mapa de Anclas — Diagnostico de Causas Raiz

Invitado: {nombre}
Fecha: {fecha}

## Vientos (fortalezas)
- {viento 1}
- {viento 2}
- {viento 3}

## Anclas (obstaculos)
- {ancla 1 — priorizada}
- {ancla 2}
- {ancla 3}

## Rocas (riesgos)
- {roca 1}
- {roca 2}

## Ancla Prioritaria
{ancla con mayor impacto — la que cortaria primero}

## Matriz de Anclas
| Ancla | Area | Severidad | Prioridad | Evidencia |
|-------|------|-----------|-----------|-----------|
| {ancla} | {area} | {critica/alta/media/baja} | {prioridad} | {evidencia} |

## Fricciones operativas observadas

| Fricción | Recorrido actual | Evidencia | Tiempo y frecuencia | Personas y sistemas | Consecuencia | Riesgo | Por aclarar |
|----------|------------------|-----------|---------------------|---------------------|--------------|--------|-------------|
| {fricción} | {recorrido o Pendiente} | {evidencia} | {dato o Pendiente} | {dato o Pendiente} | {consecuencia} | {bajo/medio/alto/Pendiente} | {preguntas} |

Esta sección captura contexto. La propuesta de una oportunidad se presenta
después, con evidencia visible y confirmación de la persona.

## Motores Posibles
- {motor opcional que podria contrarrestar una ancla}

## Observaciones
{notas adicionales del facilitador}
```

Crear directorios si no existen. Confirmar: "Complete el Mapa de Anclas."

## Notas para Claude

- Voz de Eduardo: metaforas, profundidad, sprezzatura
- No des respuestas — haz preguntas poderosas
- Escucha 70%, habla 30%
- Si el emprendedor se desvia, redirige con elegancia desde la montana
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
