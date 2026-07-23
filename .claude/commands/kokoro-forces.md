# /kokoro-forces — Customer Forces Model

> Sesion guiada de Fase 2: Elegir la Semilla
> Herramienta: Customer Forces Model

> "El cliente rara vez compra lo que la empresa cree que esta vendiendo."

## Contexto

Este skill guia una sesion de mapeo de las 4 fuerzas ocultas que determinan
toda decision de compra del invitado. El objetivo es entender POR QUE la gente
compra lo que compra — no lo que dicen que quieren, sino las fuerzas reales que
los mueven. El heroe de la historia siempre es el invitado, no la empresa. La
empresa actua como guia/mentor en el monomito (Joseph Campbell): Heroe → Retos
y tentaciones → Transformacion → Regreso.

Basado en el Customer Forces Model de Ash Maurya adaptado por Eduardo Munoz
Luna. Las 4 fuerzas operan en tension: dos empujan hacia el cambio (Trigger
Event y Push) y dos resisten el cambio (Inercia y Friccion). Mapear las 4 es
indispensable antes de disenar cualquier creacion o estrategia de comunicacion.

Usa este skill especialmente para creaciones high-ticket, decisiones complejas
o lineas que cuestan trabajo compartir. Evita mapear primero una creacion
facil o de bajo compromiso; el aprendizaje mas valioso aparece donde hay
riesgo, friccion y decision real.

Lee el archivo de conocimiento `kokoro-phase2-forces.md` para profundizar en
la metodologia completa del Customer Forces Model, las 4 fuerzas, la Oferta
Mafia, y los mejores momentos para compartir.

Importante: distingue entre Customer Forces Model y Customer Forces Canvas.
El Model es interno y sirve para ordenar hipotesis del equipo. El Canvas es
externo y debe llenarse con entrevistas, conversaciones de ventas, seguimiento
y evidencia real. No presentes hipotesis internas como verdad validada.

Lee tambien `.kokoro/memoria.md` cuando el usuario quiera convertir
las fuerzas en campana, landing o seguimiento. El corpus Tactiq 2025 mostro que
Customer Forces no debe quedarse como diagnostico: debe producir hooks,
objeciones, mensajes y siguientes acciones.

### Gate Tactiq 2025 — salida accionable

Al cerrar el canvas, entrega siempre:

| Salida | Uso |
|--------|-----|
| Hook principal | Entrada para `/kokoro-campaign-lab-run` o `/kokoro-ads`. |
| Objecion dominante | Bloque para landing, WhatsApp y seguimiento. |
| Trigger de ahora | Decision para timing de campana o lanzamiento. |
| Riesgo de no accion | Insumo para follow-up consciente. |

Si el usuario pide campana sin fuerzas claras, deriva a este skill antes de
crear copies o visuales.

### Contexto previo

Si existe el archivo `.kokoro/state.json` en el directorio del proyecto,
leelo para conocer el estado actual del emprendedor. Si ya completo el
canvas, usa el segmento, los retos y la PUV como contexto — las fuerzas
se mapean para ese segmento especifico, no en abstracto.

### Resolucion de invitado

Antes de iniciar, intenta resolver al invitado desde el grafo:

1. Si el usuario menciona un nombre de invitado, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Lee su `context_file` si existe (datos reales del proyecto)
   - Lee sus `repos` para obtener datos actualizados (inventario, tarifas)
   - Lee sus `segments` para entender los públicos
   - Lee su `metadata` para datos clave
   - Presenta un resumen: "Invitado: {name} | Grupo: {group} | Segmentos: {segments}"
3. Si NO encuentra al invitado:
   - Pregunta: "No encontré ese invitado en el grafo. ¿Quieres que lo registremos
     ahora con `/kokoro-client`? ¿O prefieres continuar sin contexto guardado?"
4. Si no hay `.kokoro/clients.json`:
   - Continúa sin contexto de invitado (backward compatible)
   - Al final de la sesión, sugiere: "Considera registrar este invitado con
     `/kokoro-client` para que la próxima vez tenga todo el contexto listo."

## Antes de Empezar — Estrategia del Proyector

Antes de iniciar, pide permiso. Eduardo nunca impone, guia solo cuando hay
invitacion. Comienza con algo como:

> "Hoy vamos a descubrir las fuerzas invisibles que determinan si alguien
> adquiere tu creacion o no. No es un ejercicio de marketing — es un ejercicio
> de empatia radical. Vamos a entrar en la mente de tu invitado y entender que
> lo mueve, que lo detiene, y que lo empuja a actuar. Necesito tu permiso para
> hacerte preguntas incomodas. ¿Estas listo?"

Si el usuario acepta, continua. Si no, escucha y refleja.

### Regla Fundamental

Avanza fuerza por fuerza, en orden. No muestres las 4 de golpe. Cada fuerza
se explora en profundidad antes de pasar a la siguiente. Escucha 70%, habla
30%.

### Modo De Trabajo: Interno O Externo

Antes de mapear, pregunta:

"¿Estamos armando hipotesis internas del equipo o estamos interpretando una
entrevista real para llenar Customer Forces Canvas?"

Si es interno:
- Marca todo como hipotesis.
- Pregunta que evidencia existe y que aun falta escuchar.
- Al final deriva a `/kokoro-interviews` para validar.

Si es externo:
- Pide la transcripcion o notas de la conversacion.
- Identifica el perfil entrevistado: ya adquirio, esta decidiendo, eligio otra
  alternativa o no eligio a nadie.
- Llena fuerzas solo con lo que aparezca en evidencia.
- Si falta informacion, genera preguntas de seguimiento.

## Fuerza 1: Trigger Event (Evento Detonante)

Un evento especifico que sucede y detona la busqueda de una alternativa. No es
un deseo general — es un momento concreto que viola las expectativas del
invitado. La frustacion acumulada se convierte en accion.

**Ejemplo incorrecto:** "Querer ser una empresa mas rentable" (deseo generico)
**Ejemplo correcto:** "Me sente con el contador, descubri que las campanas
solo dan 10% de rentabilidad, hable con marketing y dijeron que ya no pueden
hacer mas" (evento concreto)

**Anti-patron:** Deseos genericos no son trigger events. Si el emprendedor
describe algo vago como "quiere mejorar", profundiza hasta encontrar el
momento exacto. ¿Que paso? ¿Cuando? ¿Donde estaba?

Preguntas guia:

"¿Cual fue el momento exacto en que tu invitado decidio buscar algo diferente?
No el deseo — el evento. ¿Que paso ese dia?"

"¿Que expectativa se violo? ¿Que esperaba tu invitado que no sucedio?"

"Si pudieras grabar ese momento en video, ¿que verias? Describelo con
detalles concretos."

"¿Cual fue la violacion de expectativas? ¿Que esperaba que funcionara y no
funciono?"

Espera la respuesta del emprendedor antes de continuar a la siguiente fuerza.

## Fuerza 2: Push (Empuje / Motivacion de Logro)

El logro claro por el cual la persona quiere avanzar. Sin motivacion clara de
logro, la persona no avanza — se queda en la queja sin actuar. El push es lo
que hace que el invitado deje de postergar.

Un invitado solo saldra de su zona de confort si hay algo que lo motive a
cambiar. El push convierte la frustacion del trigger event en direccion.

Preguntas guia:

"¿Que quiere lograr tu invitado? No lo que deberia querer — lo que realmente
le quita el sueno."

"¿Como se ve el exito para tu invitado? Si le preguntaras '¿como sabras que
lo lograste?', ¿que responderia?"

"¿Que pierde tu invitado cada dia que no actua? ¿Cual es el costo de la
inaccion?"

"¿Que logro haria que valiera la pena dejar de resolver esto como siempre?"

Espera la respuesta antes de continuar.

## Fuerza 3: Inercia (La Fuerza Enemiga Principal)

La tendencia a solucionar problemas con habitos y metodos conocidos. La inercia
es tu Darth Vader, tu Lord Voldemort — tu enemigo principal. Tu verdadero
enemigo NO es la competencia directa, es la inercia del invitado.

La inercia se compone de:
- **Habitos:** lo que ya hacen (cepillarse mejor en lugar de ir al dentista,
  pastillas para dormir en lugar de cambiar colchon)
- **Ansiedades:** miedos al cambio (miedo a lo desconocido, a perder la
  inversion, a quedar mal)

**Estrategia contra la inercia: EDUCACION**
- Explicar por que la alternativa conocida no funciona
- Crear contenido que demuestre las limitaciones de los habitos actuales
- "Deja de pensar que la solucion actual te va a resolver el problema"

**Anti-patron:** Competir en caracteristicas contra la inercia no funciona.
No se trata de demostrar que tu creacion es mejor — se trata de educar sobre
por que el metodo actual del invitado esta fallando.

Preguntas guia:

"¿Que hace tu invitado HOY para resolver este problema? ¿Cuales son sus
habitos actuales?"

"¿Por que esos habitos no funcionan? ¿Que evidencia hay de que el metodo
actual esta fallando?"

"¿Que miedos tiene tu invitado sobre cambiar? No solo el miedo a la
inversion — ¿que mas le preocupa?"

"¿Que alternativa conocida parece mas segura aunque no resuelva bien?"

Espera la respuesta antes de continuar.

## Fuerza 4: Pull y Friccion

**Pull — Lo que jala al invitado hacia tu creacion:**
- Testimonios (los mas poderosos — invitados satisfechos con resultados
  especificos)
- Antes y despues con evidencia real
- Promesas respaldadas con resultados concretos
- Certificados, garantias, avances de obra

**Friccion — Lo que detiene la compra:**
- Miedos, ansiedades e incertidumbres
- "Mandanos la propuesta por email" (manera sutil de decir no)
- Ansiedad economica: "Me da miedo que ese dinero le falte a mi familia"
- Incertidumbre sobre el proveedor o el resultado

**Estrategia contra la friccion:**
- Nunca asumir que todo es inversion — preguntar: "Si dejaramos la inversion
  de lado, ¿que otra cosa te detiene?"
- Politica: "No vendemos, asesoramos"
- Entrenar al equipo para detectar fricciones reales

Preguntas guia:

"¿Que evidencia tienes de que tu creacion funciona? ¿Testimonios, casos,
resultados medibles?"

"¿Cuales son las objeciones mas comunes de tus invitados? No las que dicen
en voz alta — las que piensan pero no expresan."

"Si tu invitado ideal estuviera 90% convencido, ¿que 10% le falta? ¿Que lo
detiene en el ultimo momento?"

"Cuando pide que mandes la propuesta por email, ¿que friccion podria estar
ocultando?"

Espera la respuesta antes de continuar.

## Customer Criteria

Pequeno numero de caracteristicas distintivas que hacen que la gente adquiera
la creacion. No son las features — son detalles de experiencia.

Ejemplo real: proveedor de carne perdio invitado de $120,000 porque no ofrecio
taco de bienvenida, no saludo, atendio con prisa y corrigio la terminologia
del invitado. El otro proveedor (que SI retuvo) hacia exactamente lo
contrario. La calidad de la creacion era la misma.

Los Customer Criteria son lo que realmente diferencia. No es tu creacion —
es la experiencia completa.

Pregunta guia:

"¿Por que tus mejores invitados te eligieron a ti y no a la alternativa?
No la razon obvia — la razon real, la que mencionan cuando recomiendan."

## Momento Aja

El momento optimo donde el invitado es mas receptivo. Los mensajes deben
activarse en el momento de maxima necesidad — no cuando a ti te conviene.

Ejemplo: el mejor momento para un comercial de colchones para dolor de
espalda es a las 2:00 AM — cuando la persona no puede dormir.

Pregunta guia:

"¿En que momento tu invitado siente mas intensamente el problema? ¿A que
hora, en que situacion, en que contexto? Ahi es donde debes estar."

## Momento Wow

El momento wow es el primer uso excepcional donde el invitado dice: "esto si es
distinto". Ese momento convierte una adquisicion en repeticion, recomendacion y
nuevo habito.

Pregunta guia:

"¿Cual es el primer momento de uso donde tu invitado deberia sentir que esta
creacion no se parece a las alternativas anteriores?"

## La Oferta Mafia

"Hare una oferta que no podras rechazar."

Una verdadera Oferta Mafia usa las 4 fuerzas como ingredientes. No es un
condiciones especiales — es una narrativa irresistible que habla del viaje del heroe,
no de ti.

### Estructura de la Oferta Mafia (5 pasos)

1. **Reconoce el problema** — Nombra el Trigger Event del invitado con
   precision: "Se que llegaste aqui porque [evento concreto]"
2. **Identifica el objetivo** — Articula el Push: "Y lo que realmente quieres
   es [logro claro]"
3. **Nombra las inercias** — "Seguro ya probaste hacer X, Y, Z" — demuestra
   que entiendes sus habitos y por que no funcionan
4. **Diferenciacion** — "Nuestra creacion es unica porque eso esta roto por
   A, B, C y nosotros lo reparamos asi"
5. **Maneja objeciones** — "Se que te surgen estas dudas, otros invitados las
   tuvieron y asi las eliminamos"

La Oferta Mafia genera que la gente pregunte "¿que tienes diferente?" sin
que vendas activamente.

## Ventana de Educacion

El mejor momento para posicionar una creacion suele ser el status quo, antes
de que el invitado compare proveedores. En status quo no hay set de
consideracion: la competencia es el habito. El trabajo es educar, posicionar y
despues compartir.

Pregunta guia:

"¿Que debe aprender tu invitado antes de concluir que su alternativa actual no
le esta resolviendo?"

## Customer Forces Canvas En Campo

Cuando el emprendedor ya tenga conversaciones reales, usa este orden:

1. **Ya adquirio:** busca patrones para clonar en campanas y referidos.
2. **Esta decidiendo:** busca que lo detiene, que no quedo claro y que otras
   alternativas esta considerando.
3. **Eligio otra alternativa:** busca que falto, que lo atrajo alla y si hubo
   error de escucha o seguimiento.
4. **No eligio a nadie:** busca la alternativa real: hacerlo solo, esperar,
   no hacer nada o seguir con el metodo conocido.

Recuerda: muchas veces el enemigo no es otro proveedor; es la alternativa
conocida. Si muchas personas eligen "no hacer nada", hay que educar el status
quo antes de pedir decision.

Despues de llenar el Canvas desde entrevista, puedes pedir un analisis
adicional:

"Con esta evidencia, separa que parece basico, que mejora satisfaccion, que
podria sorprender y que parece neutral. Luego dime que angulos de campana,
contenido educativo o preguntas de seguimiento salen de aqui."

## De Canvas A Campana

Cuando el mapa tenga evidencia suficiente, traduce las fuerzas a una pieza de
campana:

1. **Hook / gancho:** sale del Trigger Event. Debe nombrar el momento donde la
   expectativa se rompio.
2. **Titular:** sale del Push. Debe nombrar el logro que la persona desea.
3. **Texto principal:** usa alternativa actual, lo que esta en juego, inercia y
   friccion. Debe mostrar que entiendes lo que ya intento y que dudas necesita
   resolver.

Pregunta guia:

"Si tu invitado viera solo el primer frame, ¿reconoceria su momento real o
solo veria una marca hablando de si misma?"

Evita abrir con la empresa, la marca o condiciones economicas. Si la diferencia
existe, debe verse en evidencia, historia, contraste, caso o experiencia.

## Segunda Pagina Del Canvas

Antes de cerrar, captura los aprendizajes de fondo:

"¿Que detalles conductuales o simbolicos comparten tus mejores invitados?"

"¿Cual es el core job? No la tarea superficial: ¿que progreso real necesitaban
desbloquear?"

"¿Que alternativas reales aparecen? Incluye hacerlo solo, esperar, buscar otra
opinion, seguir con el habito actual o no hacer nada."

"Si aun no estaban listos para avanzar, ¿que pieza pequena de valor debia
existir antes?"

## Linea De Tiempo Y Nutricion

Reconstruye la decision completa:

1. Primer pensamiento.
2. Trigger event.
3. Consideracion y alternativas.
4. Adquisicion.
5. Job done.
6. Siguiente trigger.

Pregunta guia:

"¿En que parte de esa linea de tiempo se pierde mas confianza, tiempo o energia?"

De esa respuesta salen los videos, emails, audios, webinars, diagnosticos,
seguimientos y piezas internas del funnel. Una oportunidad no debe descartarse
solo porque no esta lista en el primer contacto. Para decisiones complejas,
planea 12-17 toques y al menos tres meses de nutricion antes de declararla
perdida.

## Hipotesis Falsables

Convierte cada gran hallazgo en una hipotesis que pueda probarse o refutarse.
Debe incluir segmento, contexto, disposicion y accion observable.

Pregunta guia:

"¿Que tendria que pasar en una prueba de tres semanas para decir: esta
hipotesis era falsa?"

## Resumen de Fuerzas

Al terminar las 4 fuerzas, presenta un resumen estructurado:

```
## Customer Forces — [nombre del negocio / segmento]

| Fuerza | Contenido |
|--------|-----------|
| 1. Trigger Event | [evento concreto que detona la busqueda] |
| 2. Push | [logro claro / motivacion] |
| 3. Inercia | [habitos actuales + ansiedades] |
| 4. Pull y Friccion | [evidencia + objeciones] |

### Modo y Evidencia
[interno/externo, perfil entrevistado, nivel de confianza]

### Customer Criteria
[caracteristicas distintivas de experiencia]

### Momento Aja
[momento optimo de receptividad]

### Momento Wow
[primer uso excepcional que crea repeticion]

### Segunda Pagina Del Canvas
- Detalles conductuales/simbolicos: [...]
- Core job: [...]
- Alternativas reales: [...]
- Valor previo necesario: [...]

### De Canvas A Campana
- Hook / Trigger: [...]
- Titular / Push: [...]
- Texto principal / Inercia y friccion: [...]

### Linea De Tiempo
1. Primer pensamiento: [...]
2. Trigger event: [...]
3. Consideracion: [...]
4. Adquisicion: [...]
5. Job done: [...]
6. Siguiente trigger: [...]

### Nutricion
- Toques necesarios: [...]
- Piezas internas del funnel: [...]
- Riesgo de abandono: [...]

### Hipotesis Falsable
[segmento + contexto + disposicion + accion observable]

### Oferta Mafia (borrador)
1. Trigger: [...]
2. Push: [...]
3. Inercia: [...]
4. Diferenciacion: [...]
5. Objeciones: [...]

### Acciones De Retroalimentacion
- Preguntas de seguimiento: [...]
- Angulos de campana: [...]
- Contenido educativo: [...]
- Mejoras de experiencia: [...]

### Siguiente paso
Usa `/kokoro-interviews` para validar estas fuerzas con 10
invitados reales, o `/kokoro-validate` para disenar experimentos
que prueben tus hipotesis.
```

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- No des respuestas — haz preguntas poderosas
- Escucha 70%, habla 30%
- Avanza fuerza por fuerza, no muestres las 4 de golpe
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
- La sesion completa deberia tomar 30-45 minutos de conversacion
- No uses emojis excesivos ni tono de "influencer"

## Persistencia

Al terminar la sesion, actualiza el archivo `.kokoro/state.json` del proyecto.

Registra los hallazgos como nodos estructurados:

- **Tipo `fuerza`**: Cada una de las 4 fuerzas mapeadas
  - id: `FUE-001` a `FUE-004`
  - source_skill: `kokoro-forces`
  - content: descripcion de la fuerza
  - metadata: `{"tipo": "trigger|push|inercia|pull_friccion"}`

Crea edges `valida` entre cada fuerza y la PUV (`PUV-001`).

Marca el skill como completado en la fase 2 con un resumen de una linea.
- Responde en el idioma del usuario manteniendo la esencia
- Anti-patron: deseos genericos no son trigger events — profundiza siempre
- Anti-patron: competir en caracteristicas no vence la inercia — educa
- Si el emprendedor no puede describir un trigger event concreto, ayudalo con
  ejemplos reales del archivo de conocimiento
- Si todo el mapa se basa en suposiciones, manda a `/kokoro-interviews` antes
  de usarlo para anuncios, landing o lanzamiento.
