# /kokoro-campaign-lab-run — Laboratorio de Campana desde Customer Forces

> Orquestador E48 basado en Tactiq 2025.
> Uso: convertir una intencion de campana en hooks, angulos creativos,
> landing, prueba y seguimiento sin saltarse la raiz estrategica.

## Contexto

Lee primero `.kokoro/memoria.md`, `kokoro-phase2-forces.md`,
`kokoro-elevator-pitch-storytelling.md` y `kokoro-phase3-launch.md`.

Lee tambien `kokoro-video-script-method.md` cuando la campana incluya video,
Reel, Short, anuncio hablado, toma a camara o hook verbal. En ese caso este
run es el orquestador: primero ordena trigger events, oferta/creacion, ICP y
ELF; despues deriva a `/kokoro-video-script` para guion base; solo con guion
aprobado pasa a `/kokoro-creative` o `/kokoro-ads`.

Este run existe porque el corpus Tactiq muestra un patron repetido: los mejores
anuncios no empiezan en el formato; empiezan en el evento detonante, el lenguaje
del invitado, la promesa y la friccion que lo mantiene en el status quo.

## Entrada Minima

- Creacion que se quiere compartir.
- Invitado especifico.
- Evento detonante o situacion que lo hace buscar cambio.
- ICP, edad, canal y quien habla.
- Logro deseado.
- Objecion principal.
- Objetivo ELF: engagement, lead o followers/fans.
- Canal inicial: organic, Meta, Google, email, WhatsApp, landing u otro.
- Sistema de seguimiento disponible.

## Gates

No produzcas assets de campana si falta:

| Gate | Pregunta |
|------|----------|
| Suelo | Que objetivo de negocio debe mover esta campana? |
| Semilla | Que hipotesis de oferta o modelo ya esta validada? |
| Fuerzas | Que empuja al invitado a cambiar y que lo frena? |
| Mensaje | Que frase diria el invitado, no la empresa? |
| Seguimiento | Que pasa despues del clic, mensaje o formulario? |
| Medicion | Que metrica dira que aprendimos algo real? |

Si faltan fuerzas, manda a `/kokoro-forces`. Si falta validacion, manda a
`/kokoro-validate` o `/kokoro-experiment`. Si falta landing, usa
`/kokoro-landing`. Si falta pauta especifica, usa `/kokoro-ads` o
`/kokoro-gads` despues de este laboratorio.

### Gate RAW-E48-017 — orquestacion de video

Si el pedido es de video, no saltes directo a Creative Corpus, produccion ni
copy. El orden obligatorio es:

1. **Trigger events** — lista 5-10 eventos detonantes reales por ICP/canal.
2. **Hook candidates** — convierte los mejores triggers en hooks de 3-5
   segundos.
3. **Creacion/oferta** — define que se quiere invitar a elegir y que
   transformacion promete, sin sonar a venta.
4. **ICP + ELF** — separa por edad/canal y define la accion esperada.
5. **Guion base** — usa `/kokoro-video-script` para Hook / Interes / Deseo /
   Accion.
6. **Aprobacion** — espera validacion del angulo.
7. **Produccion + pauta** — solo despues usa `/kokoro-creative` o
   `/kokoro-ads`.

Si el usuario pide "haz todo", entrega primero el Campaign Lab con el bloque
Video Script Handoff y pregunta si aprueba el angulo antes de producir.

## Flujo

1. **Forces Snapshot**
   - Push: que lo mueve hacia la nueva solucion.
   - Pull: que atrae de la creacion.
   - Anxiety: que teme perder o arriesgar.
   - Habit: que lo mantiene en lo conocido.

2. **Hook Bank**
   Crea 20 hooks clasificados:
   - Evento detonante.
   - Dolor cotidiano.
   - Deseo especifico.
   - Objecion.
   - Prueba social.
   - Contraste status quo vs nueva manera.

3. **Offer + ELF Check**
   Antes de armar guion, aclara:
   - Que creacion/oferta se quiere compartir.
   - Que transformacion promete.
   - Que no debe sonar a venta.
   - Que accion ELF esperamos.

4. **Story Spine**
   Convierte el mejor hook en historia:
   - Antes: situacion reconocible.
   - Tension: costo de seguir igual.
   - Giro: nueva manera.
   - Invitacion: siguiente accion.

5. **Video Script Handoff**
   Si el formato es video o hook hablado:
   - Selecciona 1-3 hooks.
   - Resume trigger event, chismecito, ICP, ELF y oferta.
   - Deriva a `/kokoro-video-script`.
   - No generes produccion, B-roll, thumbnails ni copy de pauta hasta que el
     guion base este aprobado.

6. **Creative Corpus**
   Define 5 angulos creativos:
   - Testimonio.
   - Educativo.
   - Contraste.
   - Autoridad.
   - Demostracion o caso.

7. **Landing + Follow-up**
   - Hero: logro + diferencia.
   - Secciones: reto, consecuencia, solucion, prueba, proceso, inversion, CTA.
   - Seguimiento: primer mensaje, segundo toque, objecion y cierre.

8. **Experiment Brief**
   - Hipotesis.
   - Canal.
   - Metrica principal.
   - Duracion.
   - Criterio de perseverar, pivotar o pausar.

## Salida

```markdown
## Campaign Lab

### Forces Snapshot
| Fuerza | Insight | Evidencia |
|--------|---------|-----------|

### Hook Bank
| Tipo | Hook |
|------|------|

### Story Spine
[historia breve]

### Offer + ELF
| Punto | Decision |
|-------|----------|

### Video Script Handoff
| Campo | Valor |
|-------|-------|

### Creative Corpus
| Angulo | Asset | Razon |
|--------|-------|-------|

### Landing + Follow-up
| Punto | Mensaje |
|-------|---------|

### Experimento
| Hipotesis | Metrica | Duracion | Decision |
|-----------|---------|----------|----------|
```

## Reglas

- No uses hooks genericos; cada hook debe venir de una fuerza o una objecion.
- No propongas pauta si no hay seguimiento.
- No propongas landing sin CTA unico.
- No confundas formato con estrategia: primero fuerzas, luego assets.
- Si el formato es video, `/kokoro-campaign-lab-run` orquesta y
  `/kokoro-video-script` escribe el guion base antes de produccion.
