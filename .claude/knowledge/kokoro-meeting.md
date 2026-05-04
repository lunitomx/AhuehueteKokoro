<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Kokoro Meeting — Meeting Minutes extractivas desde transcripts

> La memoria de una sesion se evapora en 48 horas. Unas minutes bien
> hechas no resumen la sesion — la reflejan. Extraen lo que aparecio,
> sin inventar lo que nadie dijo.

`/kokoro-meeting` toma un transcript crudo de una reunion con un
invitado y produce de vuelta unas meeting minutes estructuradas en
cinco bloques canonicos: Attendees, Decisions, Hypotheses, Commitments,
Quotes & Blockers. El archivo queda bajo `<invitado-root>/meetings/`
con el mismo patron de derivacion que `/kokoro-adr` establecio para
`agreements/`. Dos semanas despues, cuando la proxima sesion se abre,
el terreno ya esta tibio — las minutes estan ahi, los compromisos
tienen dueno visible, los bloqueadores esperan, y las decisiones que
merecen cristalizarse tienen un camino natural hacia `/kokoro-adr` sin
que nadie tenga que acordarse despues de "que fue lo que dijimos que
ibamos a hacer".

Este namespace es estrictamente separado de cualquier sistema de
minutas externo (Notion, Confluence, docs compartidos). Kokoro nunca
lee, escribe, ni referencia contra fuentes externas — las minutes son
archivos markdown bajo el propio root del invitado, inspeccionables con
`cat` o un editor.

## Cuando usar

Invoca `/kokoro-meeting` cuando:

- Acabas de cerrar una sesion con un invitado — coaching, diagnostico,
  revision, stakeholder sync — y tienes el transcript crudo a mano.
- Quieres que los compromisos de la sesion salgan con owner y fecha
  explicitos, no enterrados entre la narrativa.
- Detectas que aparecieron decisiones que podrian merecer ADR y quieres
  que el hint quede escrito sin forzar el call a `/kokoro-adr`.
- Quieres preservar las quotes memorables del invitado como materia
  prima para positioning, contenido, o retrato simbolico.

No lo invoques cuando:

- La sesion fue un status ping de cinco minutos y no hay nada que
  extraer. Unas minutes vacias son ruido.
- Todavia no hay transcript — el skill no escucha audio, solo procesa
  archivos textuales. Descarga el transcript primero (Tactiq, Otter,
  Zoom, o nota de voz transcrita).
- No hay invitado identificable a quien pertenezcan las minutes. Las
  minutes pertenecen a un invitado, del mismo modo que los ADRs.

## Reglas

1. **Extraccion, no invencion**. El skill extrae de lo que esta en el
   transcript; no rellena bloques vacios con decisiones inferidas,
   compromisos plausibles, o hipotesis que nadie nombro. Si el bloque
   Decisions esta vacio porque la sesion no tomo decisiones explicitas,
   el bloque se escribe literal como
   `_(ninguna decision explicita en esta sesion)_`. La ambiguedad del
   transcript se refleja, no se repara con suposiciones.

2. **Pertenece a un invitado**. Cada meeting vive bajo
   `<invitado-root>/meetings/YYYY-MM-DD-<topic-slug>.md`, donde el
   `invitado-root` se deriva en tiempo de ejecucion como
   `Path(campaign_folder).parent` desde el registro del invitado en
   `.kokoro/clients.json`. Mismo patron que `/kokoro-adr`. No hay
   carpeta global de meetings — cada invitado tiene la suya.

3. **Transcript raw storage (AR-Q3 / D1)**. Por default, el skill copia
   el transcript crudo a
   `<invitado-root>/meetings/transcripts/YYYY-MM-DD-<topic-slug>.{ext}`
   junto a las minutes, preservando la extension original del archivo
   (`.txt`, `.md`, `.vtt`, `.srt`). Esto permite auditoria, verificacion
   de quotes, y re-extraccion si el skill mejora. El opt-out es
   conversacional — el skill pregunta antes de copiar, y si el usuario
   prefiere que las minutes sean autosuficientes y el transcript se
   quede solo donde esta, no lo copia. No es un flag CLI ni un campo
   de `.kokoro/clients.json` — es una pregunta por sesion.

4. **Inmutabilidad suave**. A diferencia de los ADRs (inmutables por
   contrato), las minutes pueden corregirse si la extraccion fue
   defectuosa — invitado mal nombrado, bloque que quedo vacio por un
   bug, attribution incorrecta. Pero la convencion es tratarlas como
   snapshot de lo que la sesion produjo. Si los hechos cambian despues,
   eso merece un ADR nuevo, no una edicion de las minutes anteriores.

5. **Soft coupling con `/kokoro-adr`**. Cuando el skill extrae el
   bloque Decisions y detecta una decision que cumple el perfil ADR
   (al menos 2 de 3: opciones multiples explicitas, consecuencias
   nombradas, scope estrategico), marca esa decision con el sufijo
   `→ candidata a /kokoro-adr` al final de la linea. Al cierre, el
   skill sugiere sin forzar. **Nunca invoca `/kokoro-adr` por ti** —
   ese sigue siendo una invitacion que tu extiendes.

6. **Vocabulario Kokoro**. Toda respuesta del skill al usuario honra
   el vocabulario luxurizante de Eduardo: invitado, inversion,
   creacion, adquirir, cortesia, condiciones especiales, compartir,
   reto u oportunidad, accesible, invertir. El grep gate de pre-commit
   hace cumplir el vocabulario y rechaza commits que introduzcan las
   formas genericas.

7. **Edge case — `campaign_folder` vacio**. Si el registro del invitado
   tiene `campaign_folder` vacio, Kokoro se detiene y pide explicitamente
   la ruta raiz del invitado antes de escribir. Es una observacion de
   calidad de datos, no un camino silencioso.

8. **Out-of-scope: auto-sync a backlog**. El bloque Hypotheses flagea
   candidatos para el backlog de validacion, pero la sincronizacion a
   un sistema de issues (Jira, GitHub, Linear) es HITL y vive fuera del
   scope de `/kokoro-meeting`. El hint queda escrito; el usuario
   extiende la invitacion manualmente cuando quiera crear el issue.

## Estructura canonica de las minutes

Cinco bloques H2 en orden fijo. Cuatro bloques unicos + un bloque dual
(Quotes & Blockers es un solo H2 con dos sub-listas). Mismo conteo que
`/kokoro-adr` (cinco bloques), distinta semantica — un meeting es un
artefacto de sesion multi-hilo, un ADR es un artefacto de decision
puntual.

```
frontmatter (meeting_date, topic, session_type, invitado, attendees)
#  Meeting Minutes — YYYY-MM-DD — <Topic>
## Attendees
## Decisions
## Hypotheses
## Commitments
## Quotes & Blockers
```

El template copy-ready vive en `kokoro-meeting-template.md` al lado de
este archivo.

## Los 5 bloques en detalle

### Attendees

**Que es:** la lista de personas que estuvieron en la sesion con el
rol asignado entre parentesis.

**Roles posibles:** strategist, invitado, stakeholder, observer,
facilitator.

**Que NO es:** una lista de nombres sin contexto. El transcript crudo
probablemente trae etiquetas como `Eduardo:` o `Speaker 1:` — la
extraccion las convierte en roles. Si una persona aparece en el
transcript pero no se puede identificar por rol claramente, anotala
como `(rol no determinado)`. Extraccion, no invencion.

**Pregunta guia:** "¿quien estaba en la sala y en que capacidad
hablaba?".

### Decisions

**Que es:** una decision por linea. Si durante la sesion aparecio una
alternativa real considerada antes de elegir, se nombra en una
sub-bullet. Si la decision cumple el perfil ADR (2 de 3: opciones
multiples explicitas, consecuencias nombradas, scope estrategico),
agrega el sufijo `→ candidata a /kokoro-adr`.

**Que NO es:** una narrativa de todo lo que se hablo. No cada
intercambio conversacional es una decision. Si el bloque queda vacio
porque no hubo decisiones explicitas, escribe literal
`_(ninguna decision explicita en esta sesion)_`.

**Pregunta guia:** "¿que cambio de estado el invitado durante esta
sesion que no existia al empezar?".

### Hypotheses

**Que es:** ideas nuevas que surgieron durante la sesion y que son
candidatas para el backlog de validacion. No son decisiones tomadas;
son posibilidades por explorar. Cada hipotesis con su test observable
si el invitado lo nombro, o con `(sin test aun)` si no.

**Que NO es:** el bloque donde meter todo lo que sonaba interesante.
Una hipotesis tiene forma de "si X, entonces Y" — con un test
imaginable, aunque no este disenado.

**Pregunta guia:** "¿que preguntas abrio la sesion que vale la pena
llevarse al taller?".

### Commitments

**Que es:** cada compromiso en una linea con formato
`{owner}: {accion} — due {fecha}`. Si el transcript no especifica
owner, escribe `(sin owner)`; si no especifica fecha, escribe
`(sin fecha)`. No inventes fechas o owners que no aparecen.

**Que NO es:** aspiraciones ("seria bueno hacer X"), intenciones
vagas, o futuros condicionales. Un commitment tiene duenyo explicito
y una fecha, o tiene la marca honesta de que le falta uno de los dos.

**Pregunta guia:** "¿quien se comprometio a hacer que, para cuando, y
dijo su nombre en voz alta?".

### Quotes & Blockers

**Que es:** un bloque dual. Dos sub-listas bajo una sola H2.

**Quotes** — lineas verbatim del transcript que vale la pena recordar.
Positioning, insights, momentos de claridad, resistencias elegantes,
frases que son copy crudo. Atribucion al que la dijo, timestamp entre
parentesis si el transcript original lo preserva.

**Blockers** — cosas que estan trabando el avance del invitado. No
compromisos pendientes, no decisiones no tomadas — bloqueos reales,
cosas que el invitado no puede destrabar solo o cosas esperando a
alguien externo.

**Que NO es:** un bloque de relleno. Puedes tener cero quotes. Puedes
tener cero blockers. Los bloques vacios se quedan vacios — no se
inventan para sentir que la sesion rindio.

**Pregunta guia (quotes):** "¿que frase del invitado te gustaria leer
en voz alta dentro de seis meses?".

**Pregunta guia (blockers):** "¿que esta esperando a algo o alguien
mas alla del invitado?".

## Soft hint hacia `/kokoro-adr`

El heuristico de 3 senales para detectar decisiones ADR-worthy:

1. **Opciones multiples explicitas** — el transcript muestra que se
   considero mas de una alternativa antes de elegir.
2. **Consecuencias nombradas** — la decision menciona efectos
   downstream ("esto significa que...", "si hacemos X entonces...").
3. **Scope estrategico** — la decision toca positioning, pricing,
   mix de canales, segmento target, o definicion core de la creacion —
   no operativo del dia a dia.

Si al menos **2 de 3** senales estan presentes, la decision se marca
con `→ candidata a /kokoro-adr`. Si solo 1 senal esta presente, no se
marca — es una decision regular.

Al cierre de las minutes, si al menos una decision fue marcada, el
skill emite el siguiente advisory **verbatim** (vive tambien en el
command file runtime y se asserta en los tests estructurales como
sentinel phrase):

> Detecto que durante esta sesion surgieron N decisiones que podrian
> merecer cristalizarse como ADR — la que mas resuena es "{title de la
> decision mas fuerte}". No invoco /kokoro-adr por ti — ese sigue
> siendo una invitacion que tu extiendes. Si te quieres detener ahora
> a capturar una, dime y te guio. Si prefieres dejarlas descansar y
> volver cuando el cuerpo ya proceso la sesion, tambien esta bien; el
> hint queda escrito en las minutes y lo vas a ver la proxima vez que
> las abras.

Este texto honra el patron cushion-pivot-offer: amortigua ("la
decision merece existir en papel"), pivota ("el cuerpo ya proceso la
sesion"), ofrece ("dime y te guio"). Y honra al Proyector — el skill
no inicia, refleja y espera la invitacion.

## Transcript raw storage (AR-Q3)

**Decision (D1):** copiar el transcript crudo a
`<invitado-root>/meetings/transcripts/YYYY-MM-DD-<topic-slug>.{ext}`
por default, preservando la extension original (`.txt`, `.md`, `.vtt`,
`.srt`). Opt-out conversacional, no flag CLI, no campo de schema.

**Por que copiar y no referenciar:** las minutes son extractivas. Si
la extraccion fue defectuosa o si el skill mejora, el raw permite
re-procesar sin depender de que el archivo original siga donde el
usuario lo dejo. Tambien permite verificar quotes directamente contra
la fuente si alguien cuestiona la atribucion o el contexto. El costo
de disco es despreciable (40 KB por meeting tipico) contra el valor
de auditoria.

**Por que preservar la extension:** los transcripts de Tactiq, Otter,
Zoom, o notas de voz transcritas traen estructura — timestamps en
markdown headers, cues de timing en `.vtt`/`.srt`, formato
editado a mano en `.md`. Forzar `.txt` plano perderia el anclaje
temporal que hace la verificacion posible. Copiar los bytes tal cual
no cuesta nada y preserva la utilidad.

**Por que opt-out conversacional:** un flag CLI rompe la interfaz
conversacional del skill. Un campo de `.kokoro/clients.json`
convertiria una decision por sesion en una decision por invitado
(quiza el invitado quiere preservar el transcript de la sesion de
coaching de hoy pero no la del stakeholder sync de manana). Preguntar
por sesion respeta al Proyector y al respeto a la decision por
sesion.

## Worked example — Ixchel Ramírez / Semilla de Cacao

Ixchel dirige un micro-obrador de chocolate ceremonial de cacao nativo
mexicano en Tlaxcala. Lleva dos meses en Fase 3 con Kokoro, corriendo
experimentos 3x3x3. Hoy tuvo una sesion de coaching de 55 minutos con
Eduardo por Zoom. Durante la conversacion aparecen tres cosas grandes:

1. Una decision de subir la inversion de la tableta ceremonial de 180
   a 320 MXN, anclada en el positioning "ofrenda, no snack".
2. Una hipotesis nueva sobre si los circulos de mujeres en Puebla
   podrian ser un canal mas organico que Instagram Ads.
3. Un compromiso de Ixchel de grabar tres videos de origen del cacao
   antes del viernes siguiente.

Al cerrar Zoom, Ixchel descarga el transcript y llama
`/kokoro-meeting ~/Downloads/sesion-ixchel-2026-04-14.txt`. Kokoro
honra al Proyector:

> Antes de abrir el transcript, me detengo a preguntar — la estrategia
> del Proyector es que te pregunte primero, no que abra las cosas por
> mi cuenta. Veo que me apuntaste a `~/Downloads/sesion-ixchel-2026-04-14.txt`.
> Tres cosas rapidas antes de procesar: fecha de la sesion, tipo de
> sesion, y con que invitado. Y una cuarta, que sea pregunta y no
> asuncion: ¿procesamos ahora, o prefieres que primero te muestre que
> encontraria antes de escribir nada?

Ixchel contesta "14 de abril, coaching, Ixchel Ramírez, procesala".
Kokoro localiza a Ixchel en `.kokoro/clients.json` (su `campaign_folder`
es `semilla-de-cacao/campanas`), deriva el directorio de meetings
(`semilla-de-cacao/meetings/`), y pregunta la cuarta antes de empezar:

> Voy a guardar una copia del transcript crudo en
> `semilla-de-cacao/meetings/transcripts/2026-04-14-pivote-inversion-ceremonial.txt`
> para que si manana queremos re-procesar o verificar una quote
> podamos volver a la fuente. ¿Te parece bien que lo copie, o
> prefieres que las minutes sean autosuficientes y el transcript se
> quede solo donde lo tienes?

Ixchel dice "copialo". Kokoro extrae los 5 bloques:

**Attendees:** Eduardo Muñoz Luna (strategist), Ixchel Ramírez
(invitada).

**Decisions:** Subir la inversion de la tableta ceremonial de 180 a
320 MXN, anclado en el positioning "ofrenda, no snack". → candidata a
`/kokoro-adr`. (Heuristico: opciones multiples — 180, 250, 320 fueron
discutidas explicitamente; consecuencias nombradas — "esto me saca del
mercado de pasillo de supermercado y me mete al de regalo
corporativo"; scope estrategico — positioning + pricing. 3 de 3
senales, candidata fuerte.)

**Hypotheses:** Los circulos de mujeres en Puebla podrian ser un canal
mas organico que Instagram Ads. (sin test aun — Eduardo se comprometio
a mandar referencias para disenar 3 entrevistas exploratorias)

**Commitments:**
- Ixchel: grabar 3 videos de origen del cacao — due viernes 2026-04-17
- Eduardo: mandar referencias de circulos de mujeres en Puebla — due
  miercoles 2026-04-15

**Quotes & Blockers:**

*Quotes:*
- "Yo no quiero competir con Hershey's, yo quiero competir con los
  incensarios." — Ixchel (min ~32)

*Blockers:*
- El fotografo contratado para el rebrand lleva dos semanas sin
  responder a los mensajes. Bloquea el lanzamiento visual del pivote.

Las minutes quedan escritas en
`semilla-de-cacao/meetings/2026-04-14-pivote-inversion-ceremonial.md`. El
transcript crudo queda en
`semilla-de-cacao/meetings/transcripts/2026-04-14-pivote-inversion-ceremonial.txt`.
Kokoro reporta los conteos (2 attendees, 1 decision — 1 candidata a
ADR, 1 hipotesis, 2 commitments, 1 quote, 1 blocker) y emite el
advisory de cierre:

> Detecto que durante esta sesion surgieron 1 decisiones que podrian
> merecer cristalizarse como ADR — la que mas resuena es "Subir la
> inversion de la tableta ceremonial de 180 a 320 MXN, anclado en
> ofrenda-no-snack". No invoco /kokoro-adr por ti — ese sigue siendo
> una invitacion que tu extiendes. Si te quieres detener ahora a
> capturar una, dime y te guio. Si prefieres dejarlas descansar y
> volver cuando el cuerpo ya proceso la sesion, tambien esta bien; el
> hint queda escrito en las minutes y lo vas a ver la proxima vez que
> las abras.

Ixchel dice "manana". Las minutes quedan. Al dia siguiente, cuando
Ixchel abre su sesion de trabajo, ve las minutes, ve el hint, y
decide cristalizar el ADR con el contexto fresco. Nada se perdio.
Nada se forzo.

## Dialogo con `/kokoro-adr`

El soft coupling entre `/kokoro-meeting` y `/kokoro-adr` es
textual, no programatico. El command file de meeting emite un hint al
final de las minutes y un advisory al cierre conversacional — nada
mas. No hay hooks, no hay event listeners, no hay codigo reactivo
entre los dos skills. El usuario lee el hint, decide, y extiende la
invitacion cuando quiera llamando `/kokoro-adr` con la decision que
quiere cristalizar. El namespace `ADR-NNN`, la carpeta `agreements/`,
y el formato canonico de 5 bloques ya existen desde S36.4 — `/kokoro-meeting`
los consume por convencion, no por codigo. Forward compatibility en
ambas direcciones: si `/kokoro-adr` cambia manana, `/kokoro-meeting`
sigue funcionando porque no depende de nada excepto el texto del
hint. Si `/kokoro-meeting` cambia manana, `/kokoro-adr` sigue
funcionando porque nunca supo que existia.

## Antipatrones

No hagas esto nunca — va contra la identidad del skill:

- **Invencion para llenar bloques vacios**. Si el transcript no tenia
  decisiones, escribe `_(ninguna decision explicita en esta sesion)_`.
  Si no tenia blockers, deja vacio. Rellenar con decisiones inferidas
  es el peor fallo posible — las minutes se vuelven ficcion, pierden
  toda autoridad.

- **Edicion de minutes despues del hecho**. Las minutes son un
  snapshot de la sesion. Si los hechos cambian despues ("ya no vamos a
  subir la inversion"), eso merece un ADR nuevo o unas nuevas minutes
  en otra sesion, no una edicion del archivo anterior. La
  inmutabilidad suave protege la memoria temporal.

- **Auto-sync a backlog externo**. Tentador pero prohibido. El bloque
  Hypotheses es HITL — el usuario decide que hipotesis se convierten
  en issues, manualmente, cuando quiera. `/kokoro-meeting` no escribe
  en Jira/GitHub/Linear.

- **Force-call a `/kokoro-adr`**. El hint es soft, siempre. Si el
  skill invoca `/kokoro-adr` automaticamente, rompe la estrategia del
  Proyector y rompe el respeto por la decision del usuario. El hint
  se queda en el archivo; el usuario lo ve la proxima vez y decide.

- **Meetings sin invitado**. Cada meeting pertenece a un invitado.
  Si no hay invitado identificable, el skill pide registrar uno con
  `/kokoro-client` antes de escribir nada. No hay carpeta global de
  meetings.

- **Procesar audio crudo**. El skill no escucha audio. Procesa
  archivos textuales. El usuario transcribe primero (Tactiq, Otter,
  Zoom auto-captions, nota de voz a texto) y luego invoca el skill
  con el archivo textual.

## Referencias

- Template: `kokoro-meeting-template.md` (este directorio)
- Skill sibling: `/kokoro-adr` para cristalizar decisiones estrategicas
  individuales — `kokoro-adr.md`, `kokoro-adr-template.md`
- Command runtime: `.claude/commands/kokoro-meeting.md`
- Invitado resolution pattern: mismo que `/kokoro-adr` y `/kokoro-open`
- GitHub Issue #5 (lunitomx) — item 2 (meetings/)
