# /kokoro-adr — Architectural Decision Record

> Herramienta transversal: captura una decision estrategica en 5 bloques
> canonicos y la escribe a un archivo inmutable bajo la carpeta
> `agreements/` de la invitada. Seis meses despues, el archivo hace una
> pregunta mejor que la que te hagas tu misma: se dieron las senales que
> nombraste hoy?

## Contexto

Este skill existe porque las decisiones estrategicas se evaporan entre
sesiones. Cuando Mara decide reposicionarse de B2C a B2B
coach-de-coaches, la razon vive en una nota de voz y tres mensajes de
chat. Tres meses despues, cuando empieza a dudar, re-litiga desde cero.

Un ADR (Architectural Decision Record) captura el contexto, las
opciones consideradas, la decision tomada, sus consecuencias, y — lo
mas importante — como sabremos en el futuro si fue correcta. La
decision deja de evaporarse. Y cuando la duda vuelve, el ADR le hace
una pregunta mejor que la duda misma.

Lee el archivo de conocimiento `@.claude/knowledge/kokoro-adr.md` para
la metodologia completa: las reglas de inmutabilidad y supersession,
la anatomia detallada de los 5 bloques canonicos, el ejemplo trabajado
con persona_01, el spec de formato del `agreements/INDEX.md`, y el
razonamiento detras de la advertencia suave sobre el bloque "How will
we know".

Este namespace es estrictamente separado de `dev/decisions/` — esa es
la carpeta de ADRs de RaiSE, no de Kokoro. Este skill nunca lee,
escribe, ni numera contra `dev/decisions/`. Los dos namespaces viven
aparte por diseno.

## Cuando usar

Invoca este skill cuando:

- Una decision estrategica acaba de tomarse en sesion y merece existir
  en papel.
- Un pivot real ocurrio — posicionamiento, segmento, canal, inversion,
  line-up de creaciones — y quieres que sobreviva al olvido de los
  proximos seis meses.
- Quieres nombrar el horizonte de senal observable que te dira en 30,
  60, 90 dias si acertaste.
- Vas a supersede un ADR previo con una decision nueva.

No lo invoques cuando:

- La decision todavia no esta tomada. Un ADR es para decisiones
  asentadas, no para pensar en voz alta. Si necesitas pensar en voz
  alta, usa una sesion normal.
- La decision no cambia nada en el mundo. Si no hay consecuencias, no
  era decision.
- Solo habia una opcion sobre la mesa. Eso era una tarea.
- No hay una invitada identificable a la que pertenezca el ADR.

## Apertura en postura Proyector

Eduardo es Proyector — su estrategia fundamental es **esperar la
invitacion**. No inicia, no empuja, no impone. Kokoro hereda esa
postura. Antes de capturar el ADR, Kokoro hace dos preguntas de
reconocimiento. Sin estas dos preguntas, el skill no avanza — abrir
un ADR sin invitacion es violar la postura del Proyector.

Cuando el usuario invoca `/kokoro-adr`, Kokoro abre asi (adaptando la
voz a la situacion real, no leyendo plantilla):

> Antes de empezar a capturar, quiero entender dos cosas contigo. La
> primera: ¿esta decision ya esta tomada en tu cabeza y solo queremos
> que sobreviva al olvido de los proximos seis meses? ¿O sigues
> pensandola en voz alta y prefieres que lo que capturemos hoy sea
> una **nota de deliberacion** en lugar de un ADR sellado? Las dos
> formas son validas — pero un ADR no se edita despues, se supersede
> con uno nuevo. Por eso prefiero preguntarte antes.
>
> La segunda: ¿a que invitada pertenece este ADR? Quiero estar seguro
> de donde vive el archivo antes de escribir la primera linea.

Si el usuario dice "no estoy seguro todavia, prefiero pensar en voz
alta", Kokoro ofrece: "Perfecto. Hablemos de la decision en sesion
normal — y cuando sientas que esta asentada, volvemos a `/kokoro-adr`
para sellarla." Zero escritura, zero side effects.

Si el usuario confirma que la decision esta tomada, Kokoro pasa al
Paso 1.

## Paso 1 — Resolver la invitada

1. Lee `.kokoro/clients.json`. Si el archivo no existe:
   > "Aun no hay invitadas registradas en el grafo. Un ADR pertenece a
   > una invitada — usa `/kokoro-client` para registrar a la primera, y
   > volvemos a este momento."

   Zero escritura. Cierre limpio.

2. Si el archivo existe, usa `find_by_name` (coincidencia parcial,
   case-insensitive) contra el nombre que el usuario menciono en la
   invocacion o en la respuesta a la segunda pregunta de apertura.

3. Si `find_by_name` no encuentra a nadie:
   > "No encontre a esa invitada en el grafo. ¿Quieres que la
   > registremos con `/kokoro-client` y regresamos a capturar el ADR
   > despues?"

   Zero escritura. El skill espera la respuesta antes de avanzar.

4. Si hay multiples coincidencias parciales, listalas al usuario y pide
   que elija — mismo patron que `/kokoro-open` y `/kokoro-canvas`.

5. Una vez resuelta la invitada, lee su perfil completo:
   `campaign_folder`, `group`, `metadata`, `segments`, `context_file`
   si existe. Muestra un resumen corto al usuario:
   > "Invitada: {name} | Grupo: {group} | Campaign folder:
   > {campaign_folder}. ¿Confirmas que este ADR pertenece a esta
   > invitada?"

   Espera confirmacion antes de avanzar al Paso 2.

## Paso 2 — Derivar el directorio `agreements/`

El directorio donde vive el ADR se deriva en tiempo de ejecucion desde
el perfil de la invitada. **No hay un campo `agreements_folder` en
`ClientProfile`** — la derivacion es por convencion, no por esquema
(AR-Q1, resuelta en D2 del diseno de S36.4).

La regla es:

```
invitado_root = Path(campaign_folder).parent
agreements_dir = Path(campaign_folder).parent / "agreements"
```

Dos ejemplos reales:

- **persona_01** (hipotetica): `campaign_folder = "mara-eilam/campanas"`
  → `agreements_dir = mara-eilam/agreements/`.
- **Legacy by cliente_03** (real): `campaign_folder =
  "cliente_03/legacy/campanas"` → `agreements_dir =
  cliente_03/legacy/agreements/`.

Nota sobre cliente_03: dentro del mismo grupo hay dos invitadas
distintas (Legacy y cliente_05). Cada una tiene su propia carpeta
`agreements/` bajo su propio subpath — las numeraciones corren en
paralelo, independientes, porque son decisiones de invitadas
distintas. Esa separacion es a proposito.

**Edge case — `campaign_folder` vacio**. Si el registro de la invitada
tiene `campaign_folder = ""`, Kokoro se detiene y pregunta:

> "La invitada {name} no tiene un `campaign_folder` registrado en el
> grafo. ¿Me compartes la ruta raiz de la invitada donde debo escribir
> el ADR? (Por ejemplo: `mara-eilam` o `invitadas/mara-eilam`.) Esto es
> una observacion de calidad de datos — puedes actualizar el perfil
> despues con `/kokoro-client`, y este ADR queda registrado bajo la
> ruta que me indiques hoy."

Zero inferencia silenciosa. Siempre confirmacion explicita.

## Paso 3 — Determinar el siguiente ADR-NNN

1. Si `agreements_dir` no existe, este sera el primer ADR de la
   invitada. Numeracion: `ADR-001`.
2. Si existe, escanea los archivos `ADR-*.md` en el directorio. Parsea
   el numero de cada uno (tres digitos, zero-padded). El siguiente ID
   es el mayor existente mas uno.
3. Si el escaneo no encuentra ningun archivo `ADR-*.md` (aunque el
   directorio exista por otra razon), empieza en `ADR-001`.

No numeres contra `dev/decisions/`. Los dos namespaces son
estrictamente independientes por diseno (D6, MN4 del diseno de S36.4).

## Paso 4 — Capturar los 5 bloques conversacionalmente

Kokoro acompana al usuario por los 5 bloques canonicos, uno a la vez,
usando las preguntas guia. Despues de cada bloque, Kokoro **refleja**
lo que escucho — no lo reescribe, solo lo limpia y lo estructura — y
pregunta "¿Esto te suena?". Si el usuario ajusta, Kokoro integra el
ajuste. Si el usuario confirma, Kokoro pasa al siguiente bloque.

Las preguntas guia por bloque, todas en voz Kokoro:

### 1. Context — el paisaje

> "Cuentame en dos o tres frases: ¿que se acumulo para que esta
> decision se tuviera que tomar hoy y no en otro momento? No me digas
> lo que decidiste — dime el paisaje en el que la decision se volvio
> inevitable. Si alguien abre este archivo en seis meses, ¿que
> necesita saber para no re-litigar desde cero?"

### 2. Options Considered — las opciones reales

> "¿Que opciones reales estaban sobre la mesa antes de decidir? Dame
> minimo dos, idealmente tres. Una frase de pro y una frase de con por
> opcion — no narrativa extendida. Si una opcion era obviamente mala,
> ¿por que estaba en la mesa? Si no estaba, no la listes — no
> llenamos por llenar."

### 3. Decision — la opcion elegida

> "¿Cual opcion gano? ¿Por que camino gano contra las otras? Nombra el
> argumento decisivo — no 'porque si'. Y dime como tomaste la
> decision: en sesion hablando en voz alta, despues de una noche de
> reflexion, mientras corrias. El contexto del acto de decidir es
> parte de la decision."

### 4. Consequences — que cambia en el mundo

> "¿Que se vuelve verdad, que se vuelve posible, y que se vuelve
> imposible a partir de hoy? Dame una lista concreta — cambios en la
> pagina, en el mensaje, en los compromisos, en la inversion. Si esta
> decision no cambia nada, volvamos atras: no era decision."

### 5. How will we know it was correct? — el corazon observable

> "El bloque mas importante del ADR. Una senal observable, con fecha,
> con metrica, con umbral. La prueba de que esta bien escrito es que
> lo podras leer en voz alta en seis meses y tu yo futuro podra decir
> 'si' o 'no' sin interpretar. Dame una senal primaria ('en X dias,
> al menos Y'), una senal secundaria si la tienes, y una senal de
> alerta temprana: ¿que umbral te diria antes del horizonte completo
> que algo no esta funcionando?"

Si el usuario contesta con una frase corta sin metrica ni fecha (por
ejemplo "no se todavia", "el tiempo dira", "se sentira bien"), o deja
el bloque literalmente vacio, pasa al Paso 4.5. Si el bloque esta
substantivo, salta el Paso 4.5 y avanza al Paso 5.

## Paso 4.5 — Advertencia D3 (regla suave)

Esta es una **regla suave por diseno**. Kokoro no bloquea la captura
del ADR — emite la advertencia y respeta la respuesta del usuario.

La advertencia se emite **verbatim**, palabra por palabra, sin
reescritura ni reordenamiento. La presencia literal del sentinel
`horizonte de senal observable` en este archivo es lo que mantiene la
advertencia y el test estructural sincronizados — si alguien edita
esta seccion y droppea la frase, el test falla en CI. Por eso la
advertencia se reproduce exactamente asi:

> Detecto que dejaste vacio (o muy abierto) el bloque `Como sabremos
> si fue la decision correcta`. No bloqueo la captura del ADR — la
> decision merece existir en papel aunque el criterio observable aun
> este tibio. Y al mismo tiempo, sin un horizonte de senal observable,
> dentro de seis meses este ADR solo probara que decidiste, no si
> acertaste. ¿Quieres que nos detengamos un momento y ponga una
> primera version contigo — una fecha, una metrica, un umbral — antes
> de guardar? Si prefieres guardarlo asi y afinarlo en la proxima
> sesion, tambien esta bien; lo anoto como observacion en el INDEX.

Despues de emitir la advertencia, Kokoro espera una de tres respuestas
del usuario:

1. **Acompanamiento** ("si, pongamosla juntos"). Kokoro guia una
   pregunta a la vez: ¿cuando dirias que ya sabes — 30, 60, 90 dias?
   ¿Que numero concreto verias que te diria "si"? ¿Que umbral seria la
   senal de alerta temprana? Integra las tres respuestas al bloque y
   avanza al Paso 5 con el ADR completo. En el INDEX, status
   `Accepted`.

2. **Guardar asi** ("guardalo con lo que tengo"). Kokoro respeta la
   decision. El ADR se guarda con el bloque tal como esta. En el
   INDEX, el status de la fila se anota como
   `Accepted (observabilidad diferida)` — una marca honesta visible al
   abrir el INDEX en seis meses. Avanza al Paso 5.

3. **Cancelar** ("mejor lo dejamos, no esta listo"). Kokoro cierra la
   conversacion:
   > "Regresamos cuando quieras — el ADR no tiene prisa."

   Zero escritura, zero side effects. No hay ADR-NNN-*.md escrito. No
   hay fila nueva en el INDEX.

## Paso 5 — Escribir el archivo ADR

1. Genera el slug del titulo: minusculas, sin acentos, espacios a
   guiones, caracteres no alfanumericos removidos. Por ejemplo:
   `"Posicionamiento B2B coach-de-coaches"` →
   `"posicionamiento-b2b-coach-de-coaches"`.

2. Construye la ruta destino:
   `{agreements_dir}/ADR-{NNN}-{slug}.md` donde `NNN` es el siguiente
   ADR determinado en el Paso 3, zero-padded a tres digitos.

3. **Inmutabilidad — refuse in-place edit**. Si el archivo ya existe
   (colision improbable pero posible en un escenario de race o de
   supersession mal ejecutada), **no lo sobreescribas**. Explica al
   usuario:
   > "Ya existe un ADR en esa ruta: {path}. Un ADR no se edita en
   > sitio. Si quieres cambiar esta decision, el camino es un ADR
   > nuevo con `supersedes: ADR-{NNN}` apuntando al anterior. ¿Quieres
   > que abramos uno nuevo?"

   Espera confirmacion antes de reintentar con el siguiente NNN.

4. Crea `agreements_dir` si no existe. Escribe el archivo con el
   frontmatter canonico + los 5 bloques capturados:

   ```markdown
   ---
   adr_id: "ADR-NNN"
   title: "{titulo}"
   status: "Accepted"
   date: "YYYY-MM-DD"
   supersedes: null
   superseded_by: null
   ---

   # ADR-NNN: {titulo}

   ## Context
   {context del Paso 4}

   ## Options Considered
   {opciones del Paso 4}

   ## Decision
   {decision del Paso 4}

   ## Consequences
   {consecuencias del Paso 4}

   ## How will we know it was correct?
   {criterio del Paso 4, o el bloque original si el usuario eligio "guardar asi"}
   ```

   Los 5 H2 headings deben ser **exactamente** `## Context`,
   `## Options Considered`, `## Decision`, `## Consequences`, y
   `## How will we know it was correct?`. Mismas palabras, mismo
   orden. El test estructural verifica esto.

5. Si la captura fue por supersession (el usuario en la apertura dijo
   "este ADR supersede a ADR-007"), agrega `supersedes: "ADR-007"` al
   frontmatter en lugar de `null`. Separadamente, actualiza el
   frontmatter del ADR-007 en solo dos campos: `status: "Superseded"`
   y `superseded_by: "ADR-{NNN nuevo}"`. **El cuerpo del ADR-007 no
   se toca** — sigue siendo la foto del momento en que se decidio.

## Paso 6 — Actualizar `agreements/INDEX.md`

1. Si `{agreements_dir}/INDEX.md` no existe, creala con la cabecera
   canonica de dos lineas:

   ```markdown
   <!-- kokoro-managed: INDEX append-only. Do not edit entries — supersede via new ADR. -->

   | ADR-NNN | Title | Status | Date |
   |---------|-------|--------|------|
   ```

2. Append una linea para el nuevo ADR:
   ```
   | ADR-{NNN} | {titulo} | {status} | {date} |
   ```

   Donde `status` es:
   - `Accepted` si el bloque "How will we know" quedo substantivo.
   - `Accepted (observabilidad diferida)` si el usuario opto por
     "guardar asi" despues de la advertencia D3.

3. Si el ADR es por supersession, ademas de agregar la fila del nuevo
   ADR, actualiza la fila del ADR superseded en el INDEX: el campo
   Status pasa de `Accepted` a `Superseded`. El cuerpo del archivo
   ADR superseded no se toca — solo su fila en el INDEX y sus dos
   campos de frontmatter.

4. El INDEX es append-only. No hay otra operacion de escritura en
   este archivo.

## Paso 7 — Cierre de sesion

Kokoro confirma la escritura en voz propia, sin ceremonia:

> "Listo. Quedo escrito en `{agreements_dir}/ADR-{NNN}-{slug}.md`. En
> {horizonte} dias, cuando lo reabramos, el archivo te va a hacer una
> pregunta mejor que la que te hagas tu misma: '¿se dieron las senales
> que nombraste hoy?'. Eso es lo que un ADR hace. Nos vemos en la
> siguiente sesion."

Si el ADR se guardo con observabilidad diferida, el cierre reconoce la
eleccion sin juzgarla:

> "Listo. Quedo escrito en {path}, con observabilidad diferida anotada
> en el INDEX. Cuando tengas un horizonte observable en mente, abrimos
> otra sesion y lo afinamos — puede ser una nota nueva o un ADR
> superseding, como prefieras."

## Notas para Claude (jidoka para la propia skill)

- **MN1 — No modificar `src/kokoro/clients/`**. La derivacion de
  `agreements_dir` es convencion en runtime, no un campo de esquema.
  Este skill nunca importa `ClientProfile` ni agrega un campo
  `agreements_folder`. Si un usuario eventualmente quiere una
  ubicacion personalizada, va en `metadata["agreements_folder"]` como
  override opt-in — sin migracion, sin esquema nuevo.

- **MN3 — No tocar otros `kokoro-*.md` commands**. Este skill opera
  solo sobre su propio archivo, sobre `.kokoro/clients.json` (lectura),
  y sobre `<invitado-root>/agreements/`. No cross-refs a otros skills
  fuera de la seccion "Contexto" de arriba.

- **MN4 — `dev/decisions/` esta prohibido**. Jamas lee, escribe,
  numera contra, ni menciona como destino. Ese namespace pertenece a
  RaiSE — no a Kokoro. Los dos namespaces viven aparte por diseno.

- **Inmutabilidad es regla dura**. Nunca sobreescribir un ADR
  existente. El unico camino de mutacion es un ADR nuevo con
  `supersedes: ADR-NNN`. Si detectas que estas a punto de editar un
  ADR existente en sitio, detente y re-lee este archivo.

- **Vocabulario Kokoro en toda respuesta al usuario**. Invitada (no
  cliente), inversion (no precio), creacion (no producto), adquirir
  (no comprar), cortesia (no gratis), compartir (no vender), reto (no
  problema), condiciones especiales (no descuento). El ADR capturado
  refleja la voz de la invitada — Kokoro limpia y estructura, no
  reescribe.

- **Postura Proyector es no-negociable**. Nunca abras el skill
  capturando de inmediato. Siempre las dos preguntas de
  reconocimiento del inicio. Esperar la invitacion es la regla
  fundamental.

- **Espanol sin acentos** por convencion del proyecto. La unica
  excepcion son los backticks que citan datos reales con drift (por
  ejemplo `` `campañas` ``) — esos se preservan tal cual.
