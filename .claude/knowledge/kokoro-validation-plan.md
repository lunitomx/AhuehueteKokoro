<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# LeanStack Validation Plan — Canon y Uso en Kokoro

> Guia conceptual. El template copy-ready vive en
> `kokoro-validation-plan-template.md` — este archivo explica por que
> existe, cuando usarlo y como llenarlo sin perder la voz de Kokoro.

## Cuando usar este Plan de Validacion

Usa un LeanStack Validation Plan cada vez que, en Fase 2, el invitado
este a punto de invertir tiempo, inversion o reputacion en una hipotesis
que todavia no tiene evidencia. No antes — antes primero escucha con
`/kokoro-interviews` o mapea fuerzas con `/kokoro-forces`. No despues —
despues de validar, pasas a disenar el experimento con
`/kokoro-experiment` (Fase 3).

Momentos tipicos de entrada:

- Una invitada quiere abrir una linea nueva y hay dudas reales sobre
  si la demanda existe o fue cortesia en una conversacion.
- El modelo de negocio asume que cierto segmento adquirira a cierta
  inversion, y nadie ha verificado si ese segmento siquiera escucha a
  la invitada.
- Una oportunidad parece obvia pero la asuncion que la sostiene no ha
  sido puesta a prueba — y el costo de equivocarse es alto.

Si la situacion todavia no llega a "estoy a punto de invertir X", no
abras un Validation Plan. Sigue escuchando. El plan se llena **antes**
del experimento, no en paralelo.

## Reglas (reglas de canon, no sugerencias)

1. **El canon se respeta como canon.** LeanStack fue disenado por Ash
   Maurya con 6 bloques en un orden especifico. No se agrega un
   septimo bloque "Voz de Kokoro". No se rebautiza BACKGROUND como
   "Raices". No se divide FOLLOW-ON PLANS en tres H2. La disciplina
   es lo que mantiene el lenguaje compartido entre Kokoro, el
   invitado y cualquier otro practicante LeanStack del mundo.

2. **Riesgoso primero, siempre.** La asuncion mas mortal del modelo
   se ataca en el primer experimento de PROPOSAL. No la mas facil,
   no la mas barata — la mas mortal. Si la riesgosa sobrevive, el
   resto del plan tiene sentido; si no, ahorraste semanas.

3. **FUTURE CONDITION es falsificable o no es.** No "queremos crecer",
   no "esperamos validar": numero, fecha, condicion observable. Si no
   puedes escribir la meta como una oracion que cualquiera pudiera
   verificar sin preguntarte, todavia no es una meta.

4. **FOLLOW-ON PLANS se escribe antes de ver los datos.** La tentacion
   es posponerlo: "ya veremos." El plan pierde su poder si los
   compromisos post-experimento se improvisan con los datos en la
   mano. Exito / fracaso / mezcla — los tres preacordados.

5. **Voz de Kokoro en el contenido, no en la estructura.** Dentro de
   cada bloque, escribimos como Kokoro: invitado (nunca cliente),
   inversion (nunca precio), elegir/adquirir (nunca comprar),
   creacion (nunca producto). Pero los H2 permanecen en ingles
   canonico — esa es la senal al resto del mundo de que estamos
   hablando el mismo idioma operativo.

6. **Un Validation Plan, un tema.** No mezcles tres hipotesis en el
   mismo documento. Si hay tres, hay tres planes — cada uno con su
   asuncion mas riesgosa, su experimento, sus follow-ons.

## Los 6 bloques canonicos

### 1. BACKGROUND
**Intencion:** dejar por escrito por que existe esta validacion, de
modo que cualquiera que abra el documento en seis meses entienda el
momento sin tener que llamar a nadie.

**Preguntas guia:**
- Que detono esta validacion? Fue una solicitud espontanea de tres
  invitadas? Una caida en metricas? Una oportunidad externa?
- Que ya sabemos — cualitativamente — que nos hace creer que vale la
  pena mirar esto?
- A quien le importa el resultado ademas del invitado directo?

### 2. CURRENT CONDITION
**Intencion:** dibujar el presente con numeros duros. No impresiones,
no "parece que" — lo observable hoy.

**Preguntas guia:**
- Cuantos invitados activos hay hoy? Cual es la inversion promedio?
- Cual es la tasa actual del indicador que esta validacion tocara?
- Si no tenemos el numero, lo decimos: "sin medicion todavia" es
  informacion tambien.

### 3. FUTURE CONDITION
**Intencion:** declarar, antes de correr ningun experimento, la
condicion observable que nos permitira decir "validado".

**Preguntas guia:**
- En N dias (con fecha concreta), que debe ser cierto?
- Como lo mediremos — y con que instrumento?
- Si alguien externo leyera la meta, podria decir si se cumplio o no
  sin consultarnos? Si no, reescribela.

### 4. ANALYSIS
**Intencion:** cerrar los ojos al instinto de "ya sabemos" y nombrar
la brecha entre el presente y el futuro, con sus riesgos y, sobre
todo, con la asuncion mas mortal del plan.

**Preguntas guia:**
- Que separa el estado actual del estado futuro?
- Cuales son las 3 asunciones principales que sostienen el plan?
- De esas tres, cual — si resulta falsa — mata todo el plan? Esa es
  la que se ataca primero en PROPOSAL.

### 5. PROPOSAL
**Intencion:** disenar experimentos concretos, en orden de riesgo,
para atacar la asuncion mas mortal primero.

**Preguntas guia:**
- Cual es el experimento mas pequeno posible que puede falsificar la
  asuncion mas mortal?
- Cuanta inversion, tiempo y reputacion cuesta cada experimento?
- Si el primer experimento mata la hipotesis, existe un experimento
  2 que todavia vale la pena correr?

### 6. FOLLOW-ON PLANS
**Intencion:** preacordar, antes de ver los datos, que haremos en
cada escenario — exito, fracaso, mezcla.

**Preguntas guia:**
- Si el experimento tiene exito (umbral alcanzado), cual es el
  siguiente paso concreto y en que plazo?
- Si fracasa, pausamos la linea? Redoblamos en otra direccion?
  Cerramos la hipotesis?
- Si los resultados son mixtos — "la gente dice si pero no paga"
  es el clasico — que iteramos: mensaje, canal, segmento, inversion?

## Ejemplo trabajado — Invitada: marca de joyeria "cliente_08"

Una invitada platera en CDMX corre una marca de joyeria ceremonial
hecha a mano. En los ultimos dos meses, tres invitadas distintas le
pidieron piezas de uso diario con una inversion mas accesible. Hoy
el 100% de su catalogo es ceremonial, con piezas arriba de 6,000 MXN.
Antes de disenar una capsula everyday completa, quiere saber si el
deseo es real o fue conversacion de cortesia. Abrimos un Validation
Plan.

```markdown
# Validation Plan: cliente_08 — Linea Everyday (2,500-4,000 MXN)

## BACKGROUND
Tres invitadas distintas pidieron por DM, en los ultimos 60 dias,
piezas de uso diario por debajo de 4,000 MXN. La linea actual es
100% ceremonial (>6,000 MXN). Antes de disenar una capsula everyday,
necesitamos saber si el deseo es real o fue una conversacion de
cortesia. El costo de equivocarnos no es solo tiempo de taller: es
el riesgo de diluir la historia ceremonial que ya funciona.

## CURRENT CONDITION
- 100% del catalogo es ceremonial (>6,000 MXN por pieza).
- Inversion promedio mensual por invitada activa: 7,200 MXN.
- 0 SKUs en el rango 2,500-4,000 MXN.
- 3 solicitudes espontaneas por DM en los ultimos 60 dias.
- Base activa: 42 invitadas con al menos una pieza adquirida en
  los ultimos 12 meses.

## FUTURE CONDITION
En 30 dias desde hoy:
- Al menos 12 de 30 invitadas encuestadas dicen que elegirian una
  pieza everyday en el rango 2,500-4,000 MXN dentro de los proximos
  30 dias, Y
- Al menos 3 invitadas pre-reservan (con anticipo del 30%) una pieza
  everyday antes de que exista el SKU fisico.

Si ambas condiciones se cumplen, consideramos la linea everyday
validada para disenar una capsula de 5 piezas.

## ANALYSIS
La brecha es de datos, no de deseo intuido. La asuncion mas riesgosa
no es que nadie quiera adquirir — es que las mismas invitadas que hoy
adquieren piezas ceremoniales adquiririan ademas piezas everyday, en
lugar de en sustitucion. Si canibaliza la linea ceremonial, incluso
un "exito" en pre-reservas seria un fracaso real: cambiariamos
margen alto por volumen con margen menor sin crecer el total.

Riesgos secundarios: dilucion de la narrativa de marca, presion
sobre el taller con un segundo tipo de produccion, tiempos de
entrega en el rango accesible.

La asuncion mas mortal: "las invitadas actuales adquiriran everyday
ademas de ceremonial, no en vez de". La atacamos primero.

## PROPOSAL
Experimentos en orden de riesgo — lo mas mortal primero.

1. **Pre-reserva anclada a invitadas activas (ataca la asuncion
   canibalizacion).** Enviar por canal privado a las 42 invitadas
   activas una pieza editorial de boceto (un diseno everyday y un
   diseno ceremonial nuevo, lado a lado), con dos llamados a la
   accion: "reserva tu pieza everyday" (anticipo 30%) o "reserva tu
   proxima ceremonial". Duracion: 7 dias. Meta: al menos 3
   pre-reservas everyday Y al menos 2 ceremoniales. Si las
   ceremoniales caen a cero, la senal de canibalizacion es real,
   no importa cuantas everyday se pre-reserven.
   Inversion estimada: 4 horas de diseno + 1 hora de envio.

2. **Encuesta anclada con inversion, 30 invitadas.** Seis preguntas
   cortas, con pregunta ancla: "Si tuvieras una pieza everyday en
   2,500-3,500 MXN, la elegirias este mes? Y por que si/no?"
   Complementa los datos duros del experimento 1 con razones.
   Inversion estimada: 2 horas de diseno de encuesta + 3 horas
   de seguimiento.

## FOLLOW-ON PLANS
- **Exito (>=3 pre-reservas everyday, >=2 ceremoniales, >=12
  respuestas positivas en encuesta):** disenamos capsula de 5
  SKUs everyday, lanzamos en 21 dias con las pre-reservadoras
  como embajadoras y narrativa clara de complementariedad con
  ceremonial. Siguiente plan de validacion: retencion de invitadas
  everyday a 90 dias.

- **Fracaso (0-2 pre-reservas, canibalizacion visible en
  ceremoniales, encuesta tibia):** pausamos la linea everyday.
  Abrimos tres conversaciones de una hora con las invitadas que
  pidieron everyday originalmente para entender que buscaban — es
  posible que el reto no sea "una pieza mas accesible" sino "una
  pieza que pueda usar todos los dias sin miedo", y eso podria
  resolverse dentro del canon ceremonial con una subcoleccion
  "everyday ceremonial".

- **Mezcla (respuestas positivas pero pre-reservas debiles):** el
  interes existe, pero el mensaje del prelanzamiento no esta
  convirtiendo. Iteramos el mensaje y el canal (no la creacion).
  Re-test en 14 dias con la misma inversion, mensaje distinto.
```

Nota del ejercicio: el template forzo a la invitada a pensar en
orden de riesgo y a comprometerse con criterios observables antes
de invertir — dos cosas que nunca habia hecho por escrito.

## Errores comunes al llenar un Validation Plan

1. **Saltarse BACKGROUND** porque "todos lo sabemos". En seis meses,
   nadie va a recordar el detonador. Escribelo.

2. **Confundir CURRENT CONDITION con historia emocional.** "Hemos
   crecido mucho" no es CURRENT CONDITION. "Inversion promedio
   mensual 7,200 MXN, 42 invitadas activas" si.

3. **FUTURE CONDITION vaga.** Si no puedes verificarla sin
   preguntarle al invitado, reescribela.

4. **ANALYSIS sin asuncion mortal nombrada.** El bloque no sirve si
   solo lista riesgos. Lo que importa es cual es la mas mortal.

5. **PROPOSAL ordenado por facilidad, no por riesgo.** El instinto
   humano elige el experimento facil primero. El canon LeanStack
   pide lo contrario.

6. **FOLLOW-ON PLANS solo con "exito".** Los tres escenarios
   (exito, fracaso, mezcla) son obligatorios — el plan pierde su
   poder si no pre-acuerdas el fracaso.

## Conexion con otros skills de Kokoro

- `/kokoro-canvas` (Fase 2) identifica las asunciones riesgosas
  desde el Lean Canvas que luego ANALYSIS nombra y PROPOSAL ataca.
- `/kokoro-interviews` (Fase 2) alimenta BACKGROUND y CURRENT
  CONDITION con material cualitativo real.
- `/kokoro-forces` (Fase 2) ayuda a detectar cual de las fuerzas
  (empuje, tiron, ansiedad, habito) esta detras de la asuncion
  mas mortal.
- `/kokoro-validate` (Fase 2) es la sesion guiada que usa este
  canon como forma canonica del output.
- `/kokoro-experiment` (Fase 3) toma el PROPOSAL y lo ejecuta
  como experimento 3x3x3 con su propio reporte (ver
  `kokoro-experiment-report.md`).
