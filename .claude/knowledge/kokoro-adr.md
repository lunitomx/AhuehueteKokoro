<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Kokoro ADR — Architectural Decision Records para invitadas

> Las decisiones se evaporan entre sesiones. Un ADR no decide — protege la
> decision del olvido y mantiene abierto el bucle epistemologico.

Un ADR de Kokoro captura la forma completa de una decision estrategica
(contexto + opciones + decision + consecuencias + como sabremos) en una
sola conversacion, y la escribe a un archivo inmutable bajo la carpeta
`agreements/` de la invitada a la que pertenece. Seis meses despues,
cuando la decision se cuestione, el archivo hace una mejor pregunta que
la duda — porque contiene el criterio observable que se nombro el dia
que la decision se tomo.

Este namespace es estrictamente separado de `dev/decisions/` — esa es la
carpeta de ADRs de RaiSE, no de Kokoro. Kokoro nunca lee, escribe, ni
numera contra `dev/decisions/`.

## Cuando usar

Invoca `/kokoro-adr` cuando:

- Una decision estrategica acaba de tomarse en sesion y merece
  sobrevivir al olvido de los proximos seis meses.
- Un pivot real ha ocurrido — posicionamiento, segmento, canal,
  inversion, line-up de creaciones — y quieres que exista en papel.
- Quieres nombrar el criterio observable que, dentro de un horizonte
  concreto, te dira si la decision fue correcta.
- Vas a supersede un ADR previo con una decision nueva que aprendio de
  la anterior.

No lo invoques cuando:

- La decision todavia no esta tomada y prefieres una nota de
  deliberacion. Un ADR es para decisiones asentadas, no para pensar en
  voz alta.
- La "decision" no cambia nada en el mundo (la pagina, el mensaje, los
  compromisos, la inversion). Si no cambia nada, no era decision.
- Solo habia una opcion sobre la mesa. Eso era una tarea, no una
  decision — no necesita ADR.
- No hay una invitada identificable a la que pertenezca el ADR.

## Reglas

1. **Inmutabilidad**. Un ADR no se edita en sitio. Una vez escrito,
   queda. Si cambia el entendimiento, el camino es un ADR nuevo con
   `supersedes: ADR-NNN` apuntando al anterior, y el anterior se marca
   `superseded_by: ADR-MMM`. El INDEX refleja ambos.

2. **Pertenece a una invitada**. Cada ADR vive bajo
   `<invitado-root>/agreements/ADR-NNN-<slug>.md`, donde el
   `invitado-root` se deriva en tiempo de ejecucion como
   `Path(campaign_folder).parent` desde el registro de la invitada en
   `.kokoro/clients.json`. No hay carpeta global de ADRs — cada
   invitada tiene la suya.

3. **Numeracion por invitada**. La proxima ADR es la mayor numeracion
   existente en `<invitado-root>/agreements/` mas uno, empezando en
   `ADR-001`. Si dos invitadas del mismo grupo (por ejemplo Legacy by
   cliente_03 y cliente_05, ambas bajo `cliente_03/`) numeran en
   paralelo, es correcto — son decisiones independientes en espacios
   independientes.

4. **Edge case — `campaign_folder` vacio**. Si el registro de la
   invitada tiene `campaign_folder` vacio, Kokoro se detiene y pide
   explicitamente la ruta raiz de la invitada antes de escribir. Es
   una observacion de calidad de datos, no un camino silencioso.

5. **Observacion no bloqueante — acentos en `campañas`**. Tres de las
   cuatro invitadas actualmente registradas tienen el valor
   `campaign_folder` con tilde (`campañas`) mientras que la convencion
   del proyecto es espanol sin acentos. Esta es una deriva
   preexistente en los datos, no en el codigo. `Path(...).parent`
   funciona identico con o sin acento, asi que la derivacion es
   robusta. No la arreglamos aqui — se deja registrada para una
   limpieza futura.

6. **Vocabulario Kokoro**. Toda respuesta del skill al usuario honra
   el vocabulario: invitada (no cliente), inversion (no precio),
   creacion (no producto), adquirir (no comprar), cortesia (no
   gratis), compartir (no vender), reto (no problema), condiciones
   especiales (no descuento). El ADR capturado refleja la voz de la
   invitada — Kokoro la limpia y la estructura, no la reescribe.

## Los 5 bloques canonicos

Un ADR tiene exactamente estos 5 bloques, en este orden, con estas
palabras. El orden y la nomenclatura son contrato estructural — si
alguien edita el archivo y renombra "How will we know it was correct?"
a "Metrics", el test estructural falla en CI y nadie puede hacer
merge. Esa rigidez es a proposito: la memoria institucional se
corrompe en silencio cuando los bloques derivan.

### Context

Intent: El paisaje. El terreno en el que la decision se volvio
inevitable.

Preguntas guia:

- Que se acumulo — observaciones, senales, conversaciones — para que
  la decision se tuviera que tomar hoy y no en otro momento?
- Si alguien abre este archivo en seis meses, que necesita saber para
  no re-litigar desde cero?
- Que estaba en juego si la decision no se tomaba?

### Options Considered

Intent: Las opciones reales que estaban sobre la mesa, con pros y
cons honestos.

Preguntas guia:

- Que opciones reales considero la mente antes de decidir? Minimo 2,
  idealmente 3.
- Una frase de pro y una frase de con por opcion. No narrativa
  extendida — una frase por lado.
- Si una opcion era obviamente mala, por que estaba en la mesa? (Si
  no estaba, no la listes — no llenes por llenar.)

### Decision

Intent: La opcion elegida, con el razonamiento explicito — no "porque
si".

Preguntas guia:

- Cual opcion gano?
- Por que camino gano contra las otras? Nombra el argumento decisivo.
- Como se tomo la decision? En sesion hablando en voz alta? Despues de
  una noche de reflexion? El contexto del acto de decidir es parte de
  la decision.

### Consequences

Intent: Que se vuelve verdad, posible, e imposible a partir de hoy.

Preguntas guia:

- Que cambia concretamente en la pagina, en el mensaje, en los
  compromisos, en la inversion?
- Que se cierra — que caminos dejan de estar abiertos?
- Que se abre — que oportunidades nuevas aparecen gracias a haber
  elegido esta direccion?
- Si nada cambia tras esta decision, vuelve al paso anterior. No era
  decision.

### How will we know it was correct?

Intent: El corazon del ADR. Una senal observable, con fecha, con
metrica, con umbral. La prueba de que el criterio esta bien escrito
es que lo puedes leer en voz alta en seis meses y tu yo futuro puede
decir "si" o "no" sin interpretar.

Preguntas guia:

- Cuando dirias que ya sabes si la decision fue correcta? Nombra un
  horizonte en dias.
- Que numero verias que te diria "si"? Nombra una metrica.
- Que umbral seria la senal de alerta temprana para abrir un
  superseding antes del horizonte completo?
- Senales primaria, secundaria y de alerta — tres lineas, no un
  parrafo de narrativa.

## How will we know — el corazon observable

De los 5 bloques, este es el que mas se salta la gente apurada. Y es
el que mas vale. Un ADR sin criterio observable es un monumento al
acto de decidir — prueba que decidiste, no si acertaste. Seis meses
despues, el yo futuro lee "el tiempo dira" y no aprende nada.

Por eso Kokoro, cuando detecta que dejaste vacio o muy abierto este
bloque, emite esta advertencia en voz propia — sin bloquear la
captura, porque la decision merece existir en papel aunque el
criterio aun este tibio:

> Detecto que dejaste vacio (o muy abierto) el bloque `Como sabremos
> si fue la decision correcta`. No bloqueo la captura del ADR — la
> decision merece existir en papel aunque el criterio observable aun
> este tibio. Y al mismo tiempo, sin un horizonte de senal observable,
> dentro de seis meses este ADR solo probara que decidiste, no si
> acertaste. Quieres que nos detengamos un momento y ponga una
> primera version contigo — una fecha, una metrica, un umbral — antes
> de guardar? Si prefieres guardarlo asi y afinarlo en la proxima
> sesion, tambien esta bien; lo anoto como observacion en el INDEX.

Tres caminos posibles despues de la advertencia:

1. **El usuario acepta acompanamiento.** Kokoro le pregunta una
   pregunta a la vez: cuando, que numero, que umbral de alerta. El
   bloque se completa con tres lineas concretas.
2. **El usuario prefiere guardar asi.** Kokoro respeta. El ADR se
   guarda con el bloque tal como esta. En `agreements/INDEX.md` la
   fila se anota con status `Accepted (observabilidad diferida)` —
   una marca honesta visible al abrir el INDEX dentro de seis meses.
3. **El usuario cancela.** Nada se escribe. Zero side effects.

Esta es una **regla suave** por diseno. La version v1 no bloquea. Si
el dogfooding muestra que los ADRs sin observabilidad se acumulan y
no aportan valor, la regla se puede endurecer en v2 — es una decision
empirica para despues, no una decision de arquitectura ahora.

## Supersession e inmutabilidad

Un ADR no se edita. El campo `status` puede pasar de `Accepted` a
`Superseded` cuando otro ADR lo reemplace, pero el cuerpo del archivo
queda intacto. El flujo de supersession es:

1. La decision original vive como `ADR-007`, status `Accepted`.
2. Seis semanas despues, las senales observables contradicen la
   decision. La invitada abre una nueva sesion y decide pivotar.
3. Kokoro captura la decision nueva como `ADR-012`, con
   `supersedes: ADR-007` en el frontmatter.
4. Kokoro actualiza el bloque de frontmatter de `ADR-007` solo en dos
   campos: `status: "Superseded"` y `superseded_by: "ADR-012"`. El
   cuerpo del ADR-007 no se toca — sigue siendo la foto de lo que se
   pensaba en ese momento.
5. El `agreements/INDEX.md` refleja ambos — ADR-007 marcado
   Superseded, ADR-012 marcado Accepted.

Esta es la unica forma de mutar un ADR. No hay edit en sitio. La
razon es sencilla: la memoria institucional se conserva cuando los
ADRs son fotos del momento en que se decidio, no ediciones posteriores
que reescriben la historia.

## Ejemplo trabajado — persona_01

persona_01 es una terapeuta de marca personal en Cuernavaca. Tres meses
en Fase 2 con Kokoro, su Lean Canvas quedo ambivalente entre dos
segmentos: profesionistas en transicion de carrera (B2C) y coaches que
buscan diferenciacion (B2B). Tres entrevistas con coaches revelaron
una urgencia operativa que ninguna de las profesionistas habia
expresado. En sesion, Mara decide pivotar el posicionamiento hacia B2B
coach-de-coaches. Invoca `/kokoro-adr "posicionamiento B2B coach de
coaches"` y Kokoro la acompana por los 5 bloques. Asi queda guardado
en `mara-eilam/agreements/ADR-001-posicionamiento-b2b-coach-de-coaches.md`:

```markdown
---
adr_id: "ADR-001"
title: "Posicionamiento B2B coach-de-coaches"
status: "Accepted"
date: "2026-04-13"
supersedes: null
superseded_by: null
---

# ADR-001: Posicionamiento B2B coach-de-coaches

## Context

Tres meses en Fase 2 con Kokoro. El Lean Canvas quedo ambivalente
entre dos segmentos: profesionistas en transicion (B2C) y coaches que
buscan diferenciacion (B2B). En las tres ultimas entrevistas de
validacion, las coaches describieron una urgencia operativa concreta
— "me siento intercambiable con otras coaches del mismo nicho,
necesito una voz que me distinga este trimestre" — que las
profesionistas jamas mencionaron. La inversion en energia de
posicionamiento se estaba dispersando por servir a los dos segmentos
a la vez. La decision no puede posponerse mas sin comprometer la
siguiente ronda de entrevistas.

## Options Considered

1. **Mantener B2C profesionistas.** Pros: mercado teoricamente mas
   amplio, narrativa de transformacion personal mas resonante con mi
   historia propia. Cons: ciclo de adquisicion lento (6-9 meses),
   urgencia apenas percibida en entrevistas, competencia saturada con
   coaches de carrera.
2. **Pivotar a B2B coach-de-coaches.** Pros: urgencia validada en
   campo (3 de 3 entrevistas), inversion tipo superior, ciclo de
   adquisicion corto (semanas), posicionamiento diferenciado en un
   nicho donde mi formacion en marca personal es escasa. Cons:
   mercado mas estrecho en volumen, necesito retirar con dignidad a
   las tres invitadas profesionistas actualmente activas, mi propia
   narrativa publica necesita reescribirse.
3. **Hibrido — seguir con ambos segmentos.** Pros: hedge contra el
   riesgo del nicho estrecho. Cons: dilucion de mensaje, manto
   estrategico sin borde, el mismo patron que me trajo aqui — no
   resuelve el reto de fondo.

## Decision

Opcion 2 — pivotar a B2B coach-de-coaches. La urgencia validada en
entrevistas pesa mas que el tamano teorico del mercado B2C. La
diferenciacion estructural (formacion en marca personal + tres anos
de clinica con invitadas en transicion de identidad profesional) es
una ventaja injusta que no puedo activar mientras el mensaje apunta
a dos segmentos a la vez. Eduardo y yo hablamos esto en voz alta
durante la sesion y la decision se sintio asentada, no forzada.

## Consequences

- La pagina principal cambia a voz coach-de-coaches — se reescribe en
  los proximos 10 dias.
- El Lean Canvas se reescribe para el nuevo segmento en la proxima
  sesion (no antes de que la pagina exista en borrador).
- Las tres invitadas profesionistas actualmente activas reciben una
  carta de cierre con dignidad: se les ofrece una sesion de cortesia
  para cerrar el proceso y una recomendacion a dos coaches de
  confianza cuyos servicios si encajan con su momento.
- Las proximas 5 creaciones de contenido (posts, newsletter, podcast
  invitado) pivotan al lenguaje coach-de-coaches — terminologia de
  posicionamiento profesional, no de transicion personal.
- La inversion publicitaria en Meta Ads se pausa 14 dias mientras la
  pagina y el mensaje se reajustan. Se reactiva solo con el nuevo
  copy.

## How will we know it was correct?

En 60 dias a partir de hoy (plazo: 2026-06-12):

- **Senal primaria**: al menos 5 conversaciones de descubrimiento con
  coaches generadas organicamente a partir del nuevo posicionamiento
  (origen rastreado: web directa, referencia, contenido organico —
  no trafico pagado).
- **Senal secundaria**: al menos una invitada coach que adquiera la
  sesion Raiz (inversion 3,500 MXN) o equivalente.
- **Senal de alerta temprana a los 30 dias** (2026-05-13): si tengo
  menos de 3 conversaciones de descubrimiento, no espero los 60 dias
  — abro un ADR superseding con aprendizajes de las primeras cuatro
  semanas y reviso si el diagnostico del segmento fue correcto o si
  el mensaje aun no esta afinado.

Si al cumplir 60 dias la senal primaria y la secundaria se dieron,
este ADR se queda como Accepted y la siguiente decision sera sobre
escala, no sobre segmento. Si solo una se dio, hay aprendizaje pero
no validacion — documento los matices en una nota y decido con
Eduardo en sesion si profundizo o si abro un superseding. Si ninguna
se dio, la hipotesis de segmento queda rechazada y el siguiente ADR
cambia la palanca.
```

Nota sobre el ejemplo: persona_01 es una invitada inventada para
didactica. No es una invitada real registrada en el grafo. El ejemplo
ilustra la textura y densidad que un ADR real debe tener — especial
atencion al bloque "How will we know", que es el unico con fechas,
metricas y umbrales concretos.

## INDEX.md format spec

Cada carpeta `<invitado-root>/agreements/` tiene un `INDEX.md` que
lista todos los ADRs de esa invitada en orden cronologico de
creacion. El formato es de tabla, con exactamente estas cuatro
columnas, y esta linea de cabecera es parte del contrato estructural:

```markdown
<!-- kokoro-managed: INDEX append-only. Do not edit entries — supersede via new ADR. -->

| ADR-NNN | Title | Status | Date |
|---------|-------|--------|------|
| ADR-001 | Posicionamiento B2B coach-de-coaches | Accepted | 2026-04-13 |
| ADR-002 | Pausar linea creacion accesorios | Accepted (observabilidad diferida) | 2026-04-18 |
```

El INDEX es append-only. No se edita una fila existente — si un ADR
pasa de Accepted a Superseded, se escribe una fila nueva para el ADR
que lo supersede y la fila del ADR original se actualiza solamente
en el campo Status (de `Accepted` a `Superseded`). El cuerpo del
archivo ADR jamas se edita.

Si el bloque "How will we know" quedo tibio y el usuario opto por
guardarlo asi, el campo Status de la fila se anota como
`Accepted (observabilidad diferida)` — una marca honesta que
alguien que abre el INDEX puede ver de un vistazo y decidir si
quiere revisar el ADR antes de que el tiempo afile el criterio.

S36.3 (`/kokoro-meeting`) leera este INDEX para ligar actas de
reunion a los ADRs que discuten — por eso el formato se documenta
aqui exactamente una vez, para que no haya renegociacion cuando
`/kokoro-meeting` llegue.

## See also

- `/kokoro-adr` — el skill que captura estos archivos. Vive en
  `.claude/commands/kokoro-adr.md`.
- `kokoro-adr-template.md` — la plantilla canonica con los 5 bloques
  en orden. Usala como referencia si prefieres escribir el ADR a mano
  en un editor antes de que el skill lo capture en sesion.
