<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
---
meeting_date: "YYYY-MM-DD"
topic: "{slug-unaccented-spanish}"
session_type: "coaching"
invitado: "{Nombre del invitado}"
attendees:
  - "{Nombre completo} ({role})"
---

# Meeting Minutes — YYYY-MM-DD — {Topic}

## Attendees

[Nombre completo de cada persona en la sesion, con el rol asignado
entre parentesis. Roles posibles: strategist, invitado, stakeholder,
observer, facilitator. El transcript crudo probablemente trae etiquetas
como "Eduardo:" o "Speaker 1:" — la extraccion debe convertir esas
etiquetas en roles, no dejarlas literales. Si una persona aparece en
el transcript pero no se identifica claramente por rol, anotala como
"(rol no determinado)" — extraccion, no invencion.]

## Decisions

[Una decision por linea. Si durante la sesion aparecio una alternativa
real considerada antes de elegir, nombrala en una sub-bullet. Si la
decision cumple el perfil ADR (al menos 2 de 3: opciones multiples
explicitas, consecuencias nombradas, scope estrategico), agrega el
sufijo `→ candidata a /kokoro-adr` al final de la linea. Si no hubo
decisiones explicitas en la sesion, deja literal:
`_(ninguna decision explicita en esta sesion)_`. Extraccion, no
invencion — no llenes el bloque con decisiones inferidas que nadie
nombro.]

## Hypotheses

[Ideas nuevas que surgieron durante la sesion y que son candidatas
para el backlog de validacion — no son decisiones tomadas, son
posibilidades por explorar. Cada hipotesis en una linea, con su test
observable si el invitado lo nombro, o con `(sin test aun)` si no lo
nombro. El bloque Hypotheses es la materia prima para
`/kokoro-experiment` y `/kokoro-validate` en una sesion posterior; no
es automatico — alguien tiene que extender la invitacion despues.]

## Commitments

[Cada compromiso en una linea con formato `{owner}: {accion} — due
{fecha}`. Si el transcript no especifica owner, escribe `(sin owner)`;
si no especifica fecha, escribe `(sin fecha)`. No inventes fechas o
owners que no aparecen en la sesion — la ambiguedad del transcript se
refleja en las minutes, no se repara con suposiciones. El bloque
Commitments es el unico que tiene owner explicito; todo lo demas
es narrativa.]

## Quotes & Blockers

**Quotes:**

[Lineas verbatim del transcript que vale la pena recordar —
positioning, insights, momentos de claridad, resistencias elegantes,
frases que son copy crudo. Atribuye a quien la dijo. Si tienes el
timestamp en el transcript original, preservalo entre parentesis.
Minimo cero, maximo los que realmente brillen — este no es un bloque
para rellenar, es un bloque para honrar.]

**Blockers:**

[Cosas que estan trabando el avance del invitado. No compromisos, no
decisiones — bloqueos reales, cosas que el invitado no puede
destrabar solo o cosas esperando a alguien externo. Cada bloqueador
en una linea, con una frase corta de contexto si ayuda a entender por
que esta trabado. Los bloqueadores del dia son las invitaciones de
manana.]
