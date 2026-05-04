<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Reporte de Experimento 3x3x3 — Guia Completa

> Skill: `/kokoro-experiment`
> Fase 3: Germinar

> "La velocidad de aprendizaje es la ventaja injusta."

> **See also:** Para documentar el cierre de un sprint 3x3x3 con el formato
> canonico LeanStack (6 bloques: BACKGROUND / FALSIFIABLE HYPOTHESES /
> DETAILS / RESULTS / VALIDATED LEARNING / NEXT ACTION), usa la guia en
> `kokoro-experiment-report.md` y copia el template listo en
> `kokoro-experiment-report-template.md`. La seccion VALIDATED LEARNING es
> el corazon del artefacto — una sola frase accionable. NEXT ACTION es
> triadico: Perseverar / Pivotar / Pausar, exactamente como se describe
> abajo en este mismo documento.

## Proposito

Guiar al emprendedor a ejecutar, documentar y aprender de sprints de
experimentacion sistematicos. No es prueba y error — es el metodo cientifico
aplicado al negocio: hipotesis → experimento → datos → aprendizaje → decision.

## Filosofia Central

Eduardo dice: "No fracasaste — aprendiste algo que no funciona. Y lo aprendiste
en 3 semanas, no en 6 meses." El framework 3x3x3 comprime el ciclo de
aprendizaje para que el emprendedor valide (o invalide) rapidamente.

### Framework 3x3x3

- **3 anos** — la vision (de /kokoro-mountain). El norte que no cambia.
- **3 meses** — la meta especifica. Una metrica que mueve la aguja.
- **3 semanas** — el sprint. Un ciclo de build → measure → learn.

Cada ciclo de 3 semanas es un experimento completo:
1. **Build** (Semana 1) — construir lo minimo necesario para probar
2. **Measure** (Semana 2) — lanzar y recolectar datos
3. **Learn** (Semana 3) — analizar, decidir, planificar siguiente sprint

### El Ciclo No Es Lineal

Despues de "Learn", tienes 3 opciones:
- **Perseverar** — la hipotesis se valido, escalar
- **Pivotar** — la hipotesis fallo, cambiar enfoque
- **Pausar** — datos insuficientes, necesitas mas tiempo/datos

Eduardo: "Pivotar no es fracasar. Pivotar es tener la honestidad de decir
'esto no funciona' y el coraje de intentar diferente."

## Estructura del Reporte de Experimento

### 1. Hipotesis

**Formato:**
"Creemos que [accion] para [segmento] resultara en [metrica esperada]
porque [razon basada en evidencia]."

**Ejemplo:**
"Creemos que publicar 3 carruseles educativos semanales en Instagram para
disenadoras freelance resultara en 50 seguidores nuevos/semana porque
nuestras entrevistas mostraron que buscan contenido practico de negocio."

**Regla:** La hipotesis debe ser falsifiable. Si no puedes probar que es
falsa, no es una hipotesis — es una opinion.

### 2. Diseno del Experimento

| Elemento | Detalle |
|----------|---------|
| **Hipotesis** | [de arriba] |
| **Metrica principal** | [numero especifico a medir] |
| **Umbral de exito** | [criterio definido ANTES de empezar] |
| **Umbral de fracaso** | [criterio para invalidar] |
| **Duracion** | 3 semanas |
| **Inversion** | [tiempo + dinero] |
| **Riesgo principal** | [que puede salir mal] |

**Clave de Eduardo:** "El umbral de exito se define ANTES de ejecutar.
Si lo defines despues, caes en el sesgo de confirmacion — siempre
encontraras una forma de declarar victoria."

### 3. Ejecucion (Semana por Semana)

**Semana 1 — Build:**
- ¿Que construiste? (MVP, landing, contenido, oferta)
- ¿Cuanto tiempo tomo?
- ¿Que cortaste para mantenerte en el sprint?

**Semana 2 — Measure:**
- ¿Que datos recolectaste?
- ¿La metrica se movio?
- ¿Algo inesperado sucedio?

**Semana 3 — Learn:**
- ¿La hipotesis se valido o invalido?
- ¿Que aprendiste que no esperabas?
- ¿Que harias diferente?

### 4. Resultados

| Metrica | Esperado | Real | Delta |
|---------|----------|------|-------|
| [metrica 1] | [umbral] | [dato real] | [+/- %] |

**Veredicto:**
- [ ] Hipotesis validada — perseverar y escalar
- [ ] Hipotesis invalidada — pivotar (especificar hacia donde)
- [ ] Datos insuficientes — extender sprint o cambiar metrica

### 5. Aprendizajes

- **Confirmado:** [que ahora sabes con certeza]
- **Sorpresa:** [que no esperabas]
- **Para investigar:** [preguntas nuevas que surgieron]
- **Siguiente sprint:** [hipotesis para el proximo ciclo]

## Tipos de Experimento por Riesgo

Eduardo prioriza por tipo de riesgo (de /kokoro-validate):

1. **Riesgo de Creacion** — ¿La creacion resuelve el reto?
   - Test: MVP, prototipo, version beta
   - Metrica: adopcion, uso, satisfaction

2. **Riesgo de Invitado** — ¿El segmento existe y tiene el reto?
   - Test: landing page, ads, encuesta
   - Metrica: registros, clics, respuestas

3. **Riesgo de Mercado** — ¿Puedes llegar al segmento de forma rentable?
   - Test: campana pequena, cold outreach, contenido
   - Metrica: CPA, conversion, ROI

**Ataca primero el riesgo mas alto.** Si no validas al invitado, no importa
que tu creacion sea perfecta.

## Anti-patrones de Experimentacion

- **Experimentar sin hipotesis** — "A ver que pasa." Eduardo: "Eso no es
  un experimento, es una loteria."
- **Mover el umbral despues de medir** — "Bueno, 30 no es 50, pero esta
  cerca..." No. El umbral se definio antes. Respetalo.
- **Sprint de 3 meses** — Eso no es un sprint. Es una maraton mal disfrazada.
  3 semanas. Si necesitas mas, divide en sprints.
- **Medir todo** — Mide UNA metrica principal. Las demas son contexto.
  Si tienes 10 metricas, no tienes ninguna.
- **Nunca pivotar** — Enamorarte de tu hipotesis. Eduardo: "El mercado no
  le importa lo que tu crees. Le importa lo que el necesita."
