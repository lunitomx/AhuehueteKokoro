<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Plan de Validacion — Experimentos y Ciclo de Aprendizaje

> Skill: `/kokoro-validation`
> Fase 2: Elegir la Semilla

> "La velocidad de aprendizaje es la ventaja injusta."

> **See also:** Para llenar un Plan de Validacion canonico con los 6
> bloques de LeanStack (BACKGROUND / CURRENT CONDITION / FUTURE
> CONDITION / ANALYSIS / PROPOSAL / FOLLOW-ON PLANS), usa la guia en
> `kokoro-validation-plan.md` y copia el template listo en
> `kokoro-validation-plan-template.md`.

## Proposito

Disenar experimentos sistematicos para validar las hipotesis mas riesgosas
del modelo de negocio. Atacar primero lo que mas puede matar al negocio.
Convertir suposiciones en evidencia usando el ciclo construir-medir-aprender.
Cada decision debe estar respaldada por datos, no por intuicion.

## Los 10 Principios del Mindset Emprendedor

Estos principios guian todo el proceso de validacion:

1. **Amar el Problema, No la Solucion** — Olvidarse del producto actual,
   enfocarse en el problema del invitado
2. **El Modelo de Negocio ES el Producto** — Incluye como creas valor,
   como entregas valor, como capturas valor
3. **La Meta es la Traccion** — Un buen producto genera traccion natural.
   Si no hay traccion, hay un problema de producto
4. **Acciones Correctas en el Tiempo Correcto** — No todas las acciones son
   igualmente importantes
5. **Pensar 10X** — Facturacion actual x 10 = Meta
6. **Atacar la Asuncion Mas Riesgosa Primero** — Lo que asumes como razon de
   compra podria ser la razon de no venta
7. **Decisiones Basadas en Evidencia** — Actuar como cientifico, solo tomar
   decisiones con evidencia real
8. **Validar Cualitativo, Verificar Cuantitativo** — Primero entender el
   "por que", despues medir el "cuanto"
9. **Eliminar "Fracaso" del Vocabulario** — Cambiar por "aprendizaje". Los
   aprendizajes deben suceder rapido
10. **Convertirse en Lean** — Aplicar Lean Canvas, usar modelos de traccion,
    mejorar metricas constantemente

## Modelo de Planificacion 3x3x3

### Estructura

- **3 anos:** Vision a largo plazo (definida en la Montana del Manana, Fase 1).
  Es el ancla que da direccion a todo lo demas.
- **3 meses:** Estrategia a mediano plazo con metrica especifica. Ejemplo:
  "10% de mejora en facturacion." Si al mes 2-3 vas en 6%, revisar que esta
  en riesgo en el modelo.
- **3 semanas:** Sprints de ejecucion y medicion. Cada sprint es un ciclo
  completo de construir-medir-aprender.

### Metodologia de Sprints

Cada sprint de 3 semanas sigue el ciclo:

1. **Construir** — Crear el minimo necesario para probar la hipotesis.
   No un producto completo, sino lo minimo para obtener datos.
2. **Medir** — Recoger datos reales. No opiniones, no intenciones —
   comportamientos observables y medibles.
3. **Aprender** — Analizar resultados y tomar decision: pivotar, perseverar
   o parar. Decisiones cada 3 semanas sobre continuidad.

La duracion minima es 3 semanas por sprint. Menos tiempo no genera datos
suficientes para decidir.

## Identificacion de Riesgos desde el Lean Canvas

El Lean Canvas revela tres categorias de riesgo que el plan de validacion
debe abordar:

### Riesgo de Producto
- El problema no vale la pena resolver
- La solucion es demasiado compleja o costosa
- La propuesta de valor no es clara
- Se piensa a escala demasiado pequena

### Riesgo de Consumidor (Invitado)
- El segmento no quiere realmente la creacion
- Los canales no alcanzan al segmento correcto
- Falta de especializacion en el nicho

### Riesgo de Mercado
- La competencia es objetivamente mejor y mas accesible
- Los consumidores dicen que comprarian pero no compran
- Los costos crecen proporcionalmente con las ventas
- La nomina fija puede eliminar ganancias de todo un ano

**Regla:** Siempre atacar la asuncion mas riesgosa primero. Si la hipotesis
mas critica falla, el resto no importa.

## Diseno de Experimentos

### Plantilla de Hipotesis

Cada experimento debe documentar:

1. **Hipotesis:** "Creemos que [segmento] tiene [problema] porque [evidencia
   inicial]"
2. **Metrica:** Que numero especifico mediremos
3. **Umbral:** Que resultado consideramos exitoso (definir ANTES del
   experimento)
4. **Duracion:** Cuanto tiempo durara el experimento (minimo 3 semanas)
5. **Decision:** Si el umbral se cumple → perseverar. Si no → pivotar.

### Tipos de Experimento

**Cualitativos (primero — validar):**
- Entrevistas de problema (10 invitados minimo)
- Entrevistas de solucion (con hallazgos de las de problema)
- Observacion de comportamiento real
- Tests de la "Oferta Mafia" en persona

**Cuantitativos (despues — verificar):**
- Landing pages con metricas de conversion
- Campanas pagadas a pequena escala
- Pre-ventas con compromiso real (inversion, no "me interesa")
- Metricas de traccion: velocidad a la que el modelo captura valor
  monetizable

### Principio 8 en Accion

Validar cualitativo, verificar cuantitativo:
- Cualitativo responde: "Es este el problema correcto? Existe demanda?"
- Cuantitativo responde: "Cuanta demanda hay? A que inversion? Por que canal?"

Nunca saltar a cuantitativo sin haber validado cualitativamente. Es como
medir la velocidad de un tren que va en la direccion equivocada.

## Concepto de Traccion

**Definicion (Ash Maurya):** Traccion = Velocidad en la cual un modelo de
negocio captura valor monetizable de sus invitados.

**Indicadores positivos:**
- Google My Business trae invitados constantemente
- Ventas diarias incluso con campanas deficientes
- La creacion se comparte incluso con mala comunicacion

**Indicadores negativos:**
- No compartes nada por ningun canal
- Requieres convencer constantemente sobre inversion y calidad
- No hay resultados ni con esfuerzos directos del fundador

**Principio:** Si tu creacion es buena, no tienes que convencer a la gente
de que te elija. Si tienes que convencer, hay un problema en el modelo.

## Validacion Plan Canvas (Leanstack)

El Validation Plan de Leanstack estructura el proceso:

1. **Background** — Contexto y situacion actual del negocio
2. **Current Condition** — Donde estas ahora (metricas reales)
3. **Future Condition (The Goal)** — A donde quieres llegar
4. **Analysis** — Que obstaculos existen entre aqui y alla
5. **Proposal** — Que experimento propones para avanzar
6. **Follow-on Plans** — Que sigue si el experimento tiene exito o falla

## Errores Comunes en Validacion

1. **Enamorarse de la solucion** — La "pildora azul": permanecer enamorado
   del producto, ignorar que no genera ingresos
2. **Proyecciones en Excel** — Crear curvas de palo de hockey que nunca se
   materializan. La curva de palo de hockey muchas veces esta en los gastos,
   no en las ventas
3. **Medir intenciones, no acciones** — "Me interesa" no es lo mismo que
   "aqui esta mi inversion"
4. **Sprints sin decision** — Ejecutar pero no decidir al final del sprint
5. **No pivotar cuando los datos lo exigen** — Cuando decides construir un
   martillo, a todo le ves cara de clavo

## Conexion con Otros Skills

- La Montana del Manana (`/kokoro-mountain`, Fase 1) define la vision a 3 anos
  que ancla el modelo 3x3x3
- El Lean Canvas (`/kokoro-canvas`) identifica los riesgos que el plan de
  validacion debe atacar
- Las entrevistas (`/kokoro-interviews`) son el primer tipo de experimento
  cualitativo en el plan
- Las Customer Forces (`/kokoro-forces`) revelan que fuerzas estan debiles
  y necesitan validacion
- Los experimentos 3x3x3 (`/kokoro-experiment`, Fase 3) ejecutan los
  sprints disenados en este plan
