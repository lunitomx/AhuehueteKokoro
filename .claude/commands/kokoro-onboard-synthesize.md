# /kokoro-onboard-synthesize — Sintesis y Diagnostico

> Sub-skill de /kokoro-onboard — NO invocar directamente
> Input: `.kokoro/onboarding/{slug}/notes.md`
> Produce: `clientes/{grupo}/{nombre}/contexto.md`

## Contexto

Lee las notas de exploracion y produce una sintesis narrativa, un diagnostico
de fase, y el documento de contexto del invitado. Consulta
`kokoro-onboard-methodology.md` para criterios de diagnostico y template
de contexto.

## Instrucciones

### Paso 1 — Sintesis Narrativa

Presenta al invitado un resumen desde la montana que integre:
- Quien es como persona y que lo mueve
- Que tiene (creacion, invitados, numeros)
- Donde esta su mayor oportunidad
- Cual es el reto que necesita resolver primero

Apertura:
> "Dejame compartirte lo que veo desde la montana — un panorama de todo
> lo que me compartiste."

Presenta 3-4 parrafos narrativos (NO bullet points). La sintesis debe
sentirse como un retrato hablado, no como un reporte.

Cierre:
> "¿Te resuena? ¿Falta algo importante?"

Si el usuario corrige o agrega, integrar antes de continuar.

### Paso 2 — Diagnostico de Fase

Usar criterios de `kokoro-onboard-methodology.md` seccion "Criterios de
Diagnostico de Fase":

- **Fase 1** si: no tiene claridad estrategica, muchas lineas de negocio,
  sin numeros claros, necesita alineacion
- **Fase 2** si: tiene idea pero no validacion, sin modelo de negocio claro,
  necesita estructura
- **Fase 3** si: tiene modelo pero no ha lanzado, necesita validar mercado,
  crear presencia
- **Fase 4** si: ya opera con invitados reales, necesita crecimiento y
  medicion sistematica

Presentar:
> "Basandome en todo lo que me compartiste, creo que tu punto de partida
> es la **Fase {N} — {nombre de la fase}**.
>
> {Razon especifica basada en lo que el emprendedor dijo — no generica}
>
> Tu primer paso seria `/kokoro-{skill}` porque {razon concreta}.
>
> Despues de eso, los siguientes pasos serian:
> 1. {paso 2}
> 2. {paso 3}"

### Paso 3 — Documento de Contexto

Generar `contexto.md` usando el template de `kokoro-onboard-methodology.md`.
Llenar TODAS las secciones con la informacion recopilada.

**Ubicacion del archivo:**
- Si tiene grupo: `clientes/{grupo}/{nombre}/contexto.md`
- Si no tiene grupo: `clientes/{nombre}/contexto.md`

Crear los directorios necesarios si no existen.

Confirmar: "Genere el documento de contexto en {path}."

## Notas para Claude

- La sintesis es NARRATIVA — NO bullet points, NO tabla, NO lista
- El diagnostico debe ser especifico (basado en lo que dijo), no generico
- Si notes.md tiene dimensiones marcadas `[PENDIENTE]`, mencionarlo en la
  sintesis: "Hay dimensiones que no exploramos aun..."
- Si el invitado corrige la sintesis, actualizar notes.md tambien
- Nunca diagnostiques sin haber leido todas las dimensiones disponibles
