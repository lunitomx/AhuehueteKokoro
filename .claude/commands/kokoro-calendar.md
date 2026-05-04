# /kokoro-calendar — Calendario de Contenido Semanal

> Herramienta transversal: Planificacion de contenido basada en datos
> Aplica en Fase 3 (Germinar) y Fase 4 (Cosechar)

> "No publiques por publicar — cada pieza de contenido es una semilla
> plantada con intencion."

## Contexto

Este skill genera un plan semanal de contenido (videos horizontales +
shorts) basado en oportunidades detectadas por `/kokoro-intel` o en el
conocimiento directo del invitado. La salida es un calendario accionable
con titulos, ganchos, estructuras y sugerencias de thumbnails.

### Dependencias opcionales

- **Output de /kokoro-intel**: Oportunidades rankeadas por impacto
- **Datos de AnswerThePublic**: Si el invitado tiene cuenta, cruzar
  oportunidades con volumen de busqueda para priorizar
- **Transcripciones previas**: Si existen en clientes/{grupo}/transcripciones/

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio con `/kokoro-open`,
usar su contexto para personalizar el calendario:
- Segmentos del invitado → a quien va cada pieza
- Industria → lenguaje y temas relevantes
- Session log → que contenido ya se planeo o creo

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Un buen calendario de contenido no se llena — se cultiva. Cada
> pieza responde a una pregunta real del mercado, no a una ocurrencia
> del lunes por la manana. Disenemoslo con intencion."

### Proceso — 4 pasos

### Paso 1: Recopilar inputs

Preguntar al invitado:

1. **¿Tienes un reporte de /kokoro-intel?**
   - Si → leer las oportunidades rankeadas
   - No → preguntar: "¿Sobre que temas creas contenido? Dame 3-5 temas
     principales de tu nicho."

2. **¿Cuantos videos por semana puedes producir?**
   - Horizontales (8-15 min): default 2-3/semana
   - Shorts (30-60 seg): default 3-5/semana
   - Ajustar a la capacidad real del invitado

3. **¿Tienes datos de AnswerThePublic?**
   - Si → usar keywords con mayor volumen para priorizar
   - No → continuar sin datos de busqueda (funciona igual)

4. **¿Que dia publicas?**
   - Si tiene rutina → respetar horarios existentes
   - Si no → sugerir: L/Mi/V para horizontales, Ma/Ju/Sa para shorts

### Paso 2: Priorizar contenido

Si hay output de /kokoro-intel, usar el ranking de oportunidades.
Si no, priorizar con esta matriz:

| Criterio | Pregunta | Peso |
|----------|----------|:----:|
| Relevancia | ¿Tu audiencia pregunta por esto? | 35% |
| Autoridad | ¿Tienes experiencia real en esto? | 30% |
| Urgencia | ¿Es timely o evergreen? | 20% |
| Competencia | ¿Que tan saturado esta el tema? | 15% |

Si hay datos de AnswerThePublic, cruzar:
- Oportunidades de intel x Volumen de busqueda ATP = prioridad final
- Keywords con alto volumen + bajo coverage = oro

### Paso 3: Generar calendario semanal

Para cada pieza de contenido, generar:

**Video horizontal (8-15 min):**
- Titulo optimizado para YouTube (50-60 chars, keyword al inicio)
- Gancho (primeros 5-10 segundos — la frase que evita el scroll)
- Estructura: 3-5 secciones con bullet de contenido
- CTA de cierre
- Shorts derivados: 2-3 momentos del video que funcionan solos en 60s
- Sugerencia de thumbnail (descripcion para /kokoro-creative)

**Short (30-60 seg):**
- Titulo/caption
- Gancho (primeros 2-3 segundos)
- Contenido principal (una idea, no tres)
- Cierre con hook al horizontal completo (si aplica)

### Paso 4: Presentar y guardar

## Plantilla de Salida

```
## Calendario de Contenido — Semana del {fecha}

Invitado: {nombre} | Nicho: {nicho}
Capacidad: {N} horizontales + {M} shorts por semana
Fuente: {/kokoro-intel | manual | ATP}

### Lunes — Horizontal #1

**Titulo:** {titulo optimizado}
**Gancho:** "{primeros 5-10 segundos}"
**Estructura:**
1. Intro — {hook + contexto} (0:00-1:00)
2. {seccion} (1:00-4:00)
3. {seccion} (4:00-8:00)
4. {seccion} (8:00-11:00)
5. Cierre + CTA (11:00-12:00)
**Duracion:** ~12 min
**Keyword:** {keyword principal}
**Thumbnail:** {descripcion visual para /kokoro-creative}

**Shorts derivados:**
- Short 1: "{momento del min 3:00 — frase impactante}" (45s)
- Short 2: "{momento del min 7:00 — dato sorprendente}" (30s)

---

### Martes — Short #1

**Titulo:** {titulo/caption}
**Gancho:** "{primeros 2-3 segundos}"
**Contenido:** {la idea principal en 1 parrafo}
**CTA:** "Video completo en mi canal" (si aplica)
**Duracion:** 45s

---

{... repetir para cada dia de la semana ...}

### Resumen de la semana

| Dia | Tipo | Titulo | Keyword | Status |
|-----|------|--------|---------|:------:|
| Lun | Horizontal | {titulo} | {kw} | Pendiente |
| Mar | Short | {titulo} | {kw} | Pendiente |
| Mie | Horizontal | {titulo} | {kw} | Pendiente |
| Jue | Short | {titulo} | {kw} | Pendiente |
| Vie | Horizontal | {titulo} | {kw} | Pendiente |
| Sab | Short | {titulo} | {kw} | Pendiente |

### Siguiente paso

1. `/kokoro-creative` para disenar thumbnails
2. Graba los videos siguiendo la estructura
3. La proxima semana, corre `/kokoro-intel` de nuevo para actualizar
4. `/kokoro-rhythm` para integrar contenido en tu ritmo semanal
```

### Guardar calendario

**Si hay invitado resuelto:**
```
clientes/{grupo}/contenido/calendario-{YYYY-MM-DD}.txt
```

**Si no hay invitado:**
```
/tmp/kokoro-calendar/calendario-{YYYY-MM-DD}.txt
```

## Integracion con AnswerThePublic

Si el invitado tiene datos de ATP (CSV o screenshot):

1. Extraer las preguntas principales (what, how, why, can, etc.)
2. Cruzar con oportunidades de /kokoro-intel
3. Keywords con coincidencia = maxima prioridad
4. Keywords ATP sin cobertura en intel = oportunidades nuevas

Formato esperado de ATP:
- Preguntas (Questions): "how to...", "what is...", "why does..."
- Preposiciones: "for...", "with...", "without..."
- Comparaciones: "vs...", "like...", "or..."

Priorizar preguntas (intent de busqueda mas claro que preposiciones).

## Notas para Claude

- Usa la voz de Eduardo: "sembrar con intencion", "cada video es una semilla"
- Usa "creacion" no "producto", "invitado" no "cliente"
- Los titulos deben ser ESPECIFICOS — nada de "Todo lo que necesitas saber sobre X"
- Ganchos basados en curiosidad o dolor real, no clickbait vacio
- Cada short debe funcionar SOLO — no depender del horizontal
- Si no hay datos de intel o ATP, el calendario igual funciona con
  el conocimiento directo del invitado
- IMPORTANTE: No llenar la semana completa si el invitado no puede
  producir tanto — mejor 2 piezas excelentes que 7 mediocres
- IMPORTANTE: Los thumbnails son para /kokoro-creative — dar descripcion
  visual suficiente para generar con Gemini
- Complemento natural de `/kokoro-intel` (intel encuentra, calendar planea)
  y `/kokoro-rhythm` (rhythm ejecuta el ritmo semanal)

## Persistencia

### Session Log (si hay invitado resuelto)

```python
entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "calendar",
    "skill": "/kokoro-calendar",
    "client_id": client.id,
    "summary": "Calendario semana {fecha}: {N} horizontales + {M} shorts",
    "hallazgos": ["{insights sobre el contenido prioritario}"],
    "artifacts": ["{path del calendario}"],
    "next_action": "{siguiente paso: grabar, disenar thumbnails, etc.}"
}
```
