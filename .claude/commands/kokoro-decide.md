---
name: kokoro-decide
description: "Herramienta transversal: Consolida los outputs de skills previos y FUERZA una decision explicita antes de avanzar a la siguiente fase"
version: 1.0.0
metadata:
  hermes:
    tags: [kokoro, decide, decision, estrategia, consolidacion]
    related_skills: [kokoro-adr, kokoro-mountain]
---
# Herramienta transversal: Decision Estrategica (kokoro-decide)

> "La informacion sin decision es ruido. La decision sin accion es ilusion."

## Contexto

Este skill se ejecuta entre fases o despues de un bloque de skills. Su unico proposito es impedir que el emprendedor acumule informacion sin actuar.

Lee TODOS los outputs de `.kokoro/outputs/`, los consolida en un solo cuadro, y fuerza UNA decision concreta. Despues de este skill, el emprendedor sabe exactamente que va a hacer.

## Input

Lee automaticamente:
- `.kokoro/memoria.md` — sintesis viva
- `.kokoro/outputs/*.md` — todos los outputs de skills ejecutados

Si no hay contexto: preguntar cual es la decision que necesita tomar.

## Instrucciones

### Paso 1: Consolidar

Presenta un cuadro con TODO lo que los skills han dicho:

```
## Cuadro de Decision — {nombre del negocio}

### Lo que sabemos
| Dimension | Hallazgo |
|-----------|----------|
| Diagnostico | {ancla prioritaria del diagnostico inicial} |
| Vision | {cima a 3 años} |
| Poda | {que crecer, que transformar, que podar} |
| Finanzas | {margen real, CPA, LTV} |
| ... | ... |

### La decision que tenemos que tomar
{la pregunta concreta — ej: "¿Cual canal duplicar?"}

### Opciones sobre la mesa
1. {opcion A} — {pros} / {contras}
2. {opcion B} — {pros} / {contras}
3. {opcion C} — {pros} / {contras}
```

### Paso 2: Forzar la decision

Preguntar DIRECTO:

> "Basado en todo esto, ¿que vas a hacer?
> No 'voy a pensarle'. No 'la semana que viene decido'.
> HOY. Con la informacion que tienes.
>
> ¿Cual opcion eliges?"

El emprendedor NO puede salir de este skill sin responder.
Si duda, ayudarlo:
- "¿Que opcion te pesa menos en el estomago?"
- "¿Cual te acercaria mas a tu cima de 3 años?"
- "Si tuvieras que apostar $10,000 a una opcion, ¿cual eliges?"

### Paso 3: Formalizar

Escribir la decision en `.kokoro/decisiones.md` con:

```markdown
## Decision #{numero}
- **Fecha:** {fecha}
- **Skill:** kokoro-decide (post-{skills que llevaron a esta decision})
- **Contexto:** {1 linea del cuadro de decision}
- **Decision:** {la decision concreta}
- **Razon principal:** {por que}
- **Accion inmediata:** {que va a hacer MANANA para empezar}
- **Check en {N} dias:** {cuando va a revisar si la decision fue correcta}
```

Actualizar `memoria.md` con la decision.

### Paso 4: ADR (si aplica)

Si la decision es estrategica (cambio de canal, pivot del negocio, nueva linea), ofrecer:

> "Esta decision es importante. ¿Quieres capturarla como ADR inmutable en `.kokoro/agreements/` para que no se pierda en 6 meses?"

Si acepta, derivar al skill kokoro-adr con el contexto ya cargado.

## Contrato con otros skills

- **kokoro-adr** — si la decision es estrategica, este skill la alimenta
- **kokoro-prune** — las decisiones de poda necesitan este skill para cerrar
- **kokoro-finance** — las decisiones de inversion necesitan este skill
