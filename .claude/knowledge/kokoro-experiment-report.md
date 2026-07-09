<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# LeanStack Experiment Report — Canon y Uso en Kokoro

> Guia conceptual. El template copy-ready vive en
> `kokoro-experiment-report-template.md` — este archivo explica por que
> existe, cuando usarlo y como llenarlo sin perder la voz de Kokoro.

## Cuando usar este Experiment Report

Usa un LeanStack Experiment Report al cierre de un sprint 3x3x3 — no
antes. Antes del sprint, el documento canonico es el Validation Plan
(ver `kokoro-validation-plan.md`), que nombra la asuncion mas mortal y
propone el experimento. Durante las tres semanas del sprint, el invitado
ejecuta; al cierre, destila lo ocurrido en este reporte para que el
aprendizaje sobreviva la reunion y quede legible en seis meses.

Momentos tipicos de entrada:

- Una invitada acaba de terminar una campana de prelanzamiento de 3
  semanas y tiene datos crudos que nadie ha ordenado todavia.
- El equipo probo una palanca nueva (una cata, un canal, una cortesia,
  un mensaje) y necesita decidir si mantenerla, cambiarla o archivarla.
- Una oportunidad parecia obvia al arrancar y ahora los datos dicen algo
  matizado — y alguien tiene que ponerlo por escrito antes de que se
  pierda en el ruido operativo.

Si el sprint todavia no ha cerrado — si falta una semana, si falta el
conteo final, si falta el analisis — no abras el Experiment Report
todavia. Se llena una sola vez, al cierre, con todo el material a la mano.

## Reglas (reglas de canon, no sugerencias)

1. **El canon se respeta como canon.** LeanStack fue disenado por Ash
   Maurya con 6 bloques en un orden especifico: BACKGROUND, FALSIFIABLE
   HYPOTHESES, DETAILS, RESULTS, VALIDATED LEARNING, NEXT ACTION. No se
   agrega un septimo bloque "Sorpresas". No se rebautiza RESULTS como
   "Hallazgos". No se fusiona VALIDATED LEARNING con NEXT ACTION. La
   disciplina es lo que mantiene el lenguaje compartido con el mundo
   LeanStack.

2. **Experiment Report y Validation Plan NO son el mismo artefacto.**
   El Validation Plan se llena ANTES del experimento y tiene sus propios
   6 bloques (BACKGROUND / CURRENT CONDITION / FUTURE CONDITION /
   ANALYSIS / PROPOSAL / FOLLOW-ON PLANS). El Experiment Report se llena
   DESPUES y tiene los 6 bloques distintos de arriba. La tentacion de
   "armonizar" ambos canon en un solo set de cabeceras es un error de
   drift — son dos momentos distintos del ciclo de validacion, y el
   canon LeanStack los mantiene separados por una razon.

3. **FALSIFIABLE HYPOTHESES se escribe con umbral, siempre.** Si el
   equipo cerro el sprint sin un umbral de falsificacion pre-acordado,
   el bloque se llena con una nota explicita: "Umbral no definido antes
   del sprint — aprendizaje de proceso: definir umbral ANTES del proximo
   sprint." No se retroactiva el umbral para declarar victoria.

4. **RESULTS son datos crudos, VALIDATED LEARNING es la interpretacion.**
   La tentacion es mezclar "tuvimos 42 catas y aprendimos que la gente
   quiere cafe de especialidad" — eso es mezclar camara con voz. RESULTS
   dice "42 catas, 5 suscriptoras, 760 MXN invertidos". VALIDATED
   LEARNING dice "la cata en persona convierte al 12% cuando esta
   estructurada; el cuello de botella real es el trafico del sabado por
   la manana, no el interes de quien ya llego".

5. **VALIDATED LEARNING es una sola frase.** Es el corazon del reporte.
   Si necesitas un parrafo, todavia no esta destilada. La prueba: puedes
   leerla en voz alta en una reunion en 30 segundos y el equipo entiende
   exactamente que cambia. Si no, sigue cortando.

6. **NEXT ACTION es triadico y se compromete.** Tres opciones, una sola
   elegida: Perseverar, Pivotar, Pausar. No "ver que pasa". No "esperar
   un poco mas". La decision se acompana del diseno del siguiente
   experimento en una frase concreta.

7. **Voz de Kokoro en el contenido, no en la estructura.** Dentro de
   cada bloque escribimos como Kokoro: invitada (nunca cliente),
   inversion (nunca precio), adquirir (nunca comprar), creacion (nunca
   producto), cortesia (nunca gratis). Pero los H2 permanecen en ingles
   canonico — esa es la senal al resto del mundo LeanStack de que
   hablamos el mismo idioma operativo.

## Los 6 bloques canonicos

### 1. BACKGROUND
**Intencion:** dejar por escrito a que Plan de Validacion sirve este
experimento y por que esta palanca se eligio, de modo que cualquiera
que abra el documento en seis meses entienda el momento sin tener que
llamar a nadie.

**Preguntas guia:**
- A cual Validation Plan responde este sprint? En que asuncion aterriza?
- Por que esta palanca — y no otra de las propuestas en el PROPOSAL?
- Que ya sabiamos antes de empezar que nos hizo creer que valia la pena?
- A quien le importa el resultado ademas del invitado directo?

### 2. FALSIFIABLE HYPOTHESES
**Intencion:** escribir la hipotesis en forma falsable con umbral, ANTES
de ejecutar (y si ya se ejecuto sin umbral, nombrar esa deuda).

**Forma canonica:**

```
Creemos que [accion] para [segmento] resultara en [metrica] porque
[razon basada en evidencia]. Criterio de falsificacion: si [metrica
< umbral], hipotesis rechazada.
```

**Preguntas guia:**
- Cual es la accion exacta que vamos a ejecutar? (una sola, no un menu)
- Para que segmento? Descripcion concreta, no abstracta.
- Que metrica vamos a medir? Una sola metrica principal.
- Cual es el umbral por debajo del cual se declara fallida la hipotesis?
- Que evidencia previa nos hace pensar que vale la pena probarlo?

### 3. DETAILS
**Intencion:** describir el diseno del experimento con suficiente
precision para que otra persona pudiera replicarlo sin preguntarte.

**Preguntas guia:**
- Duracion exacta del sprint (fechas de inicio y cierre).
- Canales usados. Si son varios, cual es el canal primario.
- Inversion total (tiempo del equipo en horas + dinero en moneda local).
- Tamano de muestra esperado y como se selecciono.
- Metodo de medicion — con que instrumento, con que frecuencia.
- Atribucion: como vas a saber que la accion causo el movimiento de la
  metrica y no otra cosa del entorno?

### 4. RESULTS
**Intencion:** reportar lo que los datos mostraron, en crudo, sin
interpretar todavia.

**Preguntas guia:**
- Cual fue el numero final contra el umbral?
- Como evoluciono la metrica semana a semana?
- Hubo resultados inesperados — en cualquier direccion?
- Que salio mal en la ejecucion que podria haber afectado los datos?
  (nombrar no desacreditar: si una cata se cancelo por lluvia, eso es
  contexto, no excusa)

### 5. VALIDATED LEARNING
**Intencion:** destilar la interpretacion en una sola frase accionable.
Este es el corazon del artefacto — el resto del documento es andamiaje
para llegar a esta oracion.

**Preguntas guia:**
- En una sola frase: que sabes hoy con certeza que no sabias hace tres
  semanas?
- La frase es accionable — alguien podria actuar sobre ella manana?
- La frase es especifica — menciona el segmento, la metrica, la condicion?
- La frase es honesta — si la hipotesis fallo, lo dice sin rodeos?
- Si la lees a tu equipo en voz alta en 30 segundos, entienden que
  cambia?

**Como suena bien y como suena mal:**
- Mal: "aprendimos mucho de este sprint". (no es aprendizaje, es estado
  de animo)
- Mal: "la cata funciona". (demasiado generica, no accionable)
- Bien: "la cata guiada convierte a invitadas curiosas de cafe de
  especialidad a roughly 12% cuando esta estructurada; el cuello de
  botella real es el trafico del sabado por la manana, no el interes
  de quien ya llego".

### 6. NEXT ACTION
**Intencion:** cerrar el sprint con una decision triadica — Perseverar,
Pivotar o Pausar — y el diseno del siguiente paso en una frase concreta.

**Las tres opciones:**

- **Perseverar.** La hipotesis se valido. El siguiente sprint escala la
  misma palanca, la profundiza o la combina. Nombra la proxima variante.
- **Pivotar.** La hipotesis fallo. El siguiente sprint prueba una
  palanca distinta. Nombra la nueva hipotesis con su propio umbral.
- **Pausar.** Los datos son insuficientes para decidir (no "dudosos" —
  insuficientes). Nombra exactamente que falta y cuando se retoma.

**Preguntas guia:**
- Cual de las tres opciones eliges? (una sola, sin intermedia)
- En una sola frase: cual es el diseno del siguiente experimento?
- Si alguien externo leyera este bloque, sabria manana que hacer?

## Ejemplo trabajado — Invitada: cafeteria de especialidad "cliente_10"

Un cafetero invitado en Guadalajara corre una cafeteria de especialidad
con una suscripcion mensual de granos tostados en casa. La suscripcion
esta estancada en 14 suscriptores activos. En el Plan de Validacion del
2026-03-20, la asuncion mas mortal identificada fue: "las invitadas que
llegan al cafe no saben que tostamos semanalmente aqui mismo". El sprint
de 3 semanas que acaba de cerrar probo una sola palanca: una cata guiada
de cortesia los sabados por la manana como puerta de entrada al ritual
de adquirir granos recien tostados por suscripcion.

```markdown
# Experiment Report: cliente_10 — Cata Sabado Sprint 1

## BACKGROUND
La suscripcion mensual esta en 14 suscriptores activos desde hace tres
meses. El Plan de Validacion del 2026-03-20 nombro como asuncion mas
riesgosa "las invitadas que llegan al cafe no saben que tostamos
semanalmente aqui mismo". Este sprint de 3 semanas prueba una sola
palanca — la cata guiada en persona como puerta de entrada al ritual
de adquirir granos recien tostados por suscripcion. Se eligio sobre
otras propuestas (landing dedicada, campana de prelanzamiento) porque
es la mas cercana al momento de decision real y la mas barata de montar.

## FALSIFIABLE HYPOTHESES
Creemos que ofrecer una cata guiada de cortesia de 30 minutos cada
sabado para invitadas curiosas de cafe de especialidad resultara en al
menos 6 nuevas suscriptoras en 3 semanas porque en las entrevistas
previas 8 de 10 invitadas que pasaron dijeron "no sabia que aqui
tostaban". Criterio de falsificacion: si al cierre de la semana 3 hay
menos de 3 nuevas suscriptoras con fuente atribuida "cata-sabado",
hipotesis rechazada.

## DETAILS
Duracion: 3 sabados consecutivos, del 2026-03-28 al 2026-04-11, de
9:00 a 11:00. Canal primario: presencial unicamente, con un caballete
en la banqueta del cafe. Canal secundario: una historia de Instagram
cada viernes a las 18:00 anunciando la cata del dia siguiente.
Inversion: 800 MXN en granos de muestra (presupuesto tope) y el tiempo
del barista lider (6 horas totales). Muestra: toda invitada que entre
al cafe durante la ventana. Medicion: nuevas suscriptoras con fuente
etiquetada "cata-sabado" en el CRM, con conteo diario al cierre de
cada sabado.

## RESULTS
Sabado 1: 14 catas servidas, 2 nuevas suscriptoras. Sabado 2: 11 catas
servidas, 1 nueva suscriptora. Sabado 3: 17 catas servidas, 2 nuevas
suscriptoras. Total de 3 semanas: 42 catas, 5 nuevas suscriptoras
adjudicadas al tag "cata-sabado". Inversion real en granos de muestra:
760 MXN (por debajo del presupuesto). Dos suscriptoras adicionales
llegaron la semana siguiente citando la cata al registrarse, pero esas
no cuentan para el sprint formal — se registran como senal para el
siguiente ciclo.

## VALIDATED LEARNING
La cata guiada en persona convierte a invitadas curiosas de cafe de
especialidad en suscriptoras a roughly 12% cuando la experiencia esta
estructurada — el cuello de botella real es el trafico peatonal del
sabado por la manana, no el interes de quien ya llego al cafe.

## NEXT ACTION
**Perseverar con ajuste.** Mantener la cata del sabado y sumar una
franja viernes por la tarde para probar la sensibilidad al tipo de
trafico. Proximo sprint de 3 semanas: cata viernes 18:00 a 20:00 vs
cata sabado 9:00 a 11:00, misma estructura, meta de al menos 30 catas
por franja y un criterio de falsificacion paralelo al del sprint 1
(menos de 3 nuevas suscriptoras en cualquiera de las dos franjas
rechaza esa franja especifica).
```

Nota del ejercicio: el template forzo al invitado a separar lo que los
datos mostraron (RESULTS) de lo que aprendio (VALIDATED LEARNING) — algo
que no habia hecho antes por escrito. Tambien lo forzo a no escribirse
"esperar un poco mas" en NEXT ACTION, sino a elegir explicitamente entre
Perseverar, Pivotar y Pausar, con el diseno del siguiente sprint ya
definido.

## Errores comunes al llenar un Experiment Report

1. **Saltarse BACKGROUND** porque "ya sabemos por que lo hicimos". En
   seis meses nadie recordara cual Plan de Validacion le dio origen al
   sprint. Escribelo.

2. **Retroactivar el umbral en FALSIFIABLE HYPOTHESES.** El umbral se
   define antes, no despues. Si no se definio antes, nombralo como deuda
   de proceso — no lo inventes para declarar victoria.

3. **Mezclar RESULTS con VALIDATED LEARNING.** RESULTS es camara, crudo
   de datos. VALIDATED LEARNING es la voz que interpreta. Si en RESULTS
   aparecen frases como "esto significa que...", esa frase pertenece a
   VALIDATED LEARNING.

4. **VALIDATED LEARNING como parrafo.** Si necesitas mas de una oracion,
   todavia no esta destilado. Sigue cortando hasta que quede una frase
   accionable.

5. **NEXT ACTION como "veremos".** No es triadico si eliges "esperar".
   Perseverar, Pivotar o Pausar — una sola, con diseno del siguiente
   experimento.

6. **Harmonizar bloques con el Validation Plan.** Los dos artefactos
   tienen 6 bloques cada uno, pero NO son los mismos 6. Son distintos
   por diseno canonico de LeanStack. No fusiones.

## Conexion con otros skills de Kokoro

- `/kokoro-validate` (Fase 2) produce el Validation Plan que este
  Experiment Report cierra — el Experiment Report responde siempre a un
  Validation Plan nombrado en BACKGROUND.
- `/kokoro-experiment` (Fase 3) es la sesion guiada que ejecuta el
  sprint 3x3x3 y produce este reporte como artefacto de cierre.
- `kokoro-phase3-experiment.md` carga el framework 3x3x3 completo y la
  triad Perseverar/Pivotar/Pausar que este reporte usa en NEXT ACTION.
- `kokoro-validation-plan.md` y `kokoro-validation-plan-template.md`
  son los artefactos hermanos — Validation Plan va antes del
  experimento, Experiment Report va despues. Juntos cierran el ciclo
  completo de validacion LeanStack.
