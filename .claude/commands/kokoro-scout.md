# /kokoro-scout — Auto-Discovery desde Repo

> Herramienta transversal: Reconocimiento de artefactos de marketing existentes
> Aplica antes del onboarding — o cuando el emprendedor ya tiene historia en su repo

> "Llegar sabiendo, no preguntando lo que puedes descubrir solo."

## Contexto

Este skill lee lo que ya existe. Antes de hacer preguntas, Scout explora el
repo del emprendedor en busca de artefactos de marketing — knowledge files,
landing pages, copies de ads, brand guidelines — y construye un perfil
estructurado del negocio desde lo que encuentra.

El resultado es un archivo `profile.md` que le dice a `/kokoro-onboard-explore`
exactamente qué ya sabe — para que la conversación empiece desde el hallazgo,
no desde cero.

Lee `kokoro-tactiq-field-patterns.md` antes de sintetizar el perfil para
marcar senales de campo: foco difuso, oferta sin validacion, landing sin
seguimiento, datos desconectados o necesidad de un copiloto operativo.

### Cuando usar este skill

- Un emprendedor llega por primera vez y su repo tiene historia (docs, landing, conocimiento instalado)
- Quieres un diagnóstico rápido del estado actual antes del onboarding
- El repo tiene knowledge files instalados por `/kokoro-init`

### Cuando NO usar este skill

- El repo está vacío o recién creado — ir directo a `/kokoro-onboard`
- Solo necesitas actualizar datos de un invitado ya registrado — usar `/kokoro-client`
- El emprendedor ya tiene `profile.md` reciente y no ha habido cambios relevantes

### Dependencias

- **Output**: `.kokoro/scout/{slug}/profile.md`
- **Alimenta**: `/kokoro-onboard-explore` en modo Scout-Aware (si profile.md existe)
- **ADR-004**: protocolo de discovery por niveles de confianza
- **ADR-005**: contrato de handoff Scout → Onboard via filesystem

---

## Paso 1 — Derivar el Slug del Invitado

### Gate Tactiq 2025 — discovery para diagnostico

Mientras exploras, etiqueta hallazgos por fase Kokoro:

- Fase 1: vision, lineas de negocio, finanzas o foco.
- Fase 2: canvas, fuerzas de compra, validacion o entrevistas.
- Fase 3: investigacion, mensajes, landing, campana o experimento.
- Fase 4: CRM, seguimiento, scorecard, analytics o ritmo semanal.
- Transversal: oportunidad de agente/copiloto solo si hay workflow repetible
  con entradas, salidas, responsable y regla de paro.

Antes de explorar el repo, necesitas saber a quién pertenece. El slug es el
identificador del negocio — kebab-case, nunca el nombre completo de una persona.

**Cadena de prioridad:**

1. **`.claude/knowledge/kokoro-cliente.md`** — Si existe, busca el campo `slug`
   o `nombre` en el frontmatter o en la primera sección. Este archivo es la
   fuente más confiable: fue creado específicamente para identificar al invitado
   en este repo y estará disponible incluso en la primera ejecución de Scout.

2. **Otros knowledge files** — Si `kokoro-cliente.md` no existe o no tiene slug,
   busca el campo `nombre` en cualquier otro `.claude/knowledge/kokoro-*.md`.
   Normaliza a kebab-case.

3. **Nombre del directorio del repo** — `basename $(pwd)` normalizado a
   kebab-case (minúsculas, espacios a guiones). Es un fallback confiable.

4. **Preguntar al usuario** — Solo si las opciones anteriores son ambiguas:
   > "¿Cómo identificamos este negocio? (ej: mi-tienda-online)"

**Guarda de privacidad:** El slug NUNCA debe contener el nombre completo de
una persona real. Usa el nombre del negocio o una referencia al proyecto.
Correcto: `raiz-ancestral`, `panaderia-don-jorge`. Incorrecto: `juan-garcia-lopez`.

---

## Paso 2 — Protocolo de Discovery (5 Niveles)

Scout no adivina, no inventa, no asume. Lee lo que existe y reporta lo que
no pudo encontrar. El protocolo avanza en orden de confianza, de más a menos.

### Reglas de parada y límites

- **Parada temprana:** Cuando el total acumulado de artefactos encontrados
  en todos los niveles ejecutados hasta ese momento alcanza ≥3, proceder
  con síntesis. No esperar a niveles inferiores.
- **Límite absoluto:** Máximo 10 archivos leídos en total en una ejecución.
  Si hay más candidatos, priorizar por tamaño (archivos más extensos = más contenido).
- **Tamaño máximo por archivo:** 50KB. Archivos más grandes probablemente no son
  copy de marketing.

### Exclusiones — Lo que Scout NUNCA lee

Scout ignora los siguientes tipos de archivo y directorios en todos los niveles:

- Código: `*.py`, `*.js`, `*.ts`, `*.css`, `*.jsx`, `*.tsx`
- Configuración: `*.json`, `*.yaml`, `*.yml`, `*.toml`, `*.env`, `*.ini`
- Directorios: `node_modules/`, `.git/`, `dist/`, `build/`, `__pycache__/`, `.venv/`
- Archivos de log, binarios, o archivos de más de 50KB

Excepción: un archivo `.json` o `.yaml` con "brand", "copy" o "ads" en el nombre
puede leerse si su contenido parece ser marketing copy, no configuración técnica.

---

### Nivel 1 — Knowledge Files de Kokoro (máxima confianza)

Busca en `.claude/knowledge/` archivos que sigan el patrón `kokoro-*.md`:

```
Archivos a explorar:
.claude/knowledge/kokoro-*.md
```

Estos archivos fueron creados específicamente para Kokoro con la voz del negocio
ya estructurada. Son la fuente más rica — ground truth. Si existen, son la base
principal del perfil. Los niveles siguientes solo complementan, no contradicen.

Si Nivel 1 produce ≥3 archivos → parada temprana, proceder a síntesis.
Si produce 1-2 archivos → continuar con Nivel 2 para complementar.
Si produce 0 archivos → continuar con Nivel 2.

---

### Nivel 2 — Landing Page y Documentación Raíz (alta confianza)

Busca los candidatos más comunes para landing pages y documentación principal:

```
Archivos a explorar (en orden de prioridad):
1. README.md (raíz del repo)
2. landing.md
3. landing/index.md
4. landing/index.html
5. index.html (raíz)
6. docs/index.md
```

Estos archivos generalmente contienen propuesta de valor, descripción del negocio,
y copy orientado al invitado. Son la segunda fuente más confiable.

Cuenta los archivos encontrados en este nivel. Si el total acumulado (Nivel 1 + Nivel 2)
alcanza ≥3 artefactos → parada temprana, proceder a síntesis.
Si el total sigue por debajo de 3 → continuar con Nivel 3.

---

### Nivel 3 — Copy y Contenido de Marketing (confianza media)

Si los niveles anteriores no produjeron suficientes artefactos, busca archivos
`.md` en rutas que típicamente contienen copy de marketing o contenido editorial:

```bash
find . -name "*.md" -path "*/copy/*" \
  -o -name "*.md" -path "*/ads/*" \
  -o -name "*.md" -path "*/content/*" \
  -o -name "*.md" -path "*/copies/*"
```

Excluir resultados que estén dentro de `node_modules/`, `.git/`, `dist/`, `build/`.

Si el total acumulado alcanza ≥3 artefactos → parada temprana, proceder a síntesis.
Si no → continuar con Nivel 4.

---

### Nivel 4 — Brand Guidelines y Voz de Marca (confianza media)

Busca archivos que por nombre sugieren ser guías de marca, tono o voz:

```bash
find . \( -iname "*brand*" -o -iname "*voz*" -o -iname "*guidelines*" -o -iname "*tono*" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*"
```

Incluir cualquier tipo de archivo de texto (`.md`, `.txt`) que coincida.
No incluir código aunque el nombre coincida.

Si el total acumulado alcanza ≥3 artefactos → parada temprana, proceder a síntesis.
Si no → continuar con Nivel 5.

---

### Nivel 5 — Fallback Conversacional (último recurso)

Si los Niveles 1 a 4 produjeron menos de 3 artefactos en total, Scout activa
el fallback conversacional. Esto no es un fracaso — es información: el repo no tiene
artefactos de marketing visibles, y eso en sí mismo es señal de Fase 1.

Presenta al usuario:

> "Exploré tu repo en los lugares donde generalmente encuentro artefactos
> de marketing, y no encontré suficiente información. ¿Puedes indicarme
> qué archivos o directorio revisar?"

Si el usuario indica una ruta → leer esos archivos (respetando el límite de
10 archivos total y las exclusiones del protocolo).

Si el usuario no puede indicar nada, o los archivos que indica tampoco tienen
contenido de marketing → proceder a síntesis con lo que hay. El perfil
resultante tendrá muchas secciones con "No detectado" y un Diagnóstico de Fase
de "Indeterminado" o "Fase 1" según las señales disponibles.

---

## Paso 3 — Síntesis del Perfil

Con los artefactos encontrados, sintetiza un perfil estructurado del negocio.
Este perfil es un documento de trabajo — un espejo de lo que el repo muestra,
no un juicio ni una recomendación. Scout describe antes de guiar.

### Reglas de síntesis

- **Las 8 secciones son obligatorias.** Siempre. Aunque no haya evidencia para
  alguna, la sección existe con el texto "No detectado".
- **Nunca inventar.** Si Scout no encontró evidencia, dice "No detectado" —
  nunca rellena con suposiciones razonables.
- **Solo fuentes reales.** La sección `## Fuentes Usadas` lista únicamente los
  archivos que Scout realmente leyó — no paths inferidos, no rutas inventadas.
- **Vocabulario Kokoro obligatorio.** Inversión (no precio), invitado (no cliente),
  creación (no producto), compartir (no vender), reto/oportunidad (no problema).
- Sin emojis. Sin lenguaje de "influencer". Sin promesas de resultados.

### Las 8 Secciones del Perfil (orden fijo, no modificar)

```markdown
## Negocio
{qué hace, qué vende, modelo de negocio detectado en los artefactos}

## Audiencia
{segmento principal detectado, dolores o motivaciones identificados en el copy}

## Propuesta de Valor
{diferenciador encontrado — qué hace único a este negocio según los artefactos}

## Voz de Marca
{tono, estilo, palabras y frases recurrentes, patrones de comunicación detectados}

## Actividad de Marketing
{canales activos detectados, plataformas identificadas, tipo de contenido presente}

## Diagnóstico de Fase
{ver reglas de inferencia abajo}
Señales encontradas:
- {evidencia 1 que apunta a esa fase}
- {evidencia 2 que apunta a esa fase}

## Fuentes Usadas
- {path relativo del archivo 1 realmente leído}
- {path relativo del archivo 2 realmente leído}

## Gaps Detectados
- {dimensión que Scout no pudo inferir}
- {otra dimensión sin evidencia}
```

### Reglas de inferencia de fase

El Diagnóstico de Fase debe ser exactamente uno de los cinco estados válidos,
seguido de una lista "Señales encontradas:" con las evidencias concretas.

**Fase 1 — Preparar el Suelo:**
Señales: No hay ads activos detectados. No hay copy de conversión orientado a
la acción. No hay knowledge files estructurados instalados. No hay menú de
creaciones o pricing documentado.

**Fase 2 — Elegir la Semilla:**
Señales: Hay una landing o descripción del negocio, pero sin evidencia de
tráfico de pago. El copy explora varios ángulos o propuestas. No hay métricas
de conversión visibles. Sin sistema de seguimiento de invitados.

**Fase 3 — Germinar:**
Señales: Ads activos o archivos de campañas presentes. Copy de campañas
documentado. Canales activos identificados (Meta, Google, etc.). Pero sin
sistema de seguimiento de invitados visible en el repo.

**Fase 4 — Cosechar:**
Señales: Knowledge files completos instalados por `/kokoro-init`. Múltiples
canales activos documentados. Copy maduro con distintos ángulos. Sistema de
CRM o grafo de invitados visible en `.kokoro/` o equivalente.

**Indeterminado:**
Señales contradictorias (ej: ads activos pero sin ningún copy documentado)
o insuficientes (ej: un solo archivo README con descripción mínima).

---

## Paso 4 — Escribir el Profile

Una vez sintetizado el perfil, Scout lo escribe al filesystem.

### Ruta de salida

```
.kokoro/scout/{slug}/profile.md
```

Si el directorio no existe:
```bash
mkdir -p .kokoro/scout/{slug}/
```

### Formato del encabezado (obligatorio, exactamente así)

```markdown
# Perfil Scout — {nombre del negocio}
> Generado por /kokoro-scout el {fecha}. Draft — confirmar con el invitado.
```

### Guarda de sobreescritura

Si `.kokoro/scout/{slug}/profile.md` ya existe:

1. Leer el archivo existente
2. Mostrar al usuario un resumen de qué cambiaría (secciones modificadas)
3. Preguntar confirmación explícita:
   > "Ya existe un perfil para este negocio. ¿Confirmas que quieres sobreescribirlo con la versión actual?"
4. **NO sobreescribir sin confirmación explícita.** Si el usuario no confirma,
   conservar el archivo existente y reportar que no se realizaron cambios.

---

## Paso 5 — Presentar Hallazgos

Después de escribir el perfil, Scout presenta sus hallazgos al usuario con voz
de Eduardo — desde la montaña, sin imposición, con densidad y sin superficialidad.

### Contrato de voz

La presentación DEBE abrirse con esta frase exacta:

> "Explorando tu repo, encontré que…"

Continúa con un resumen narrativo de los hallazgos más significativos — no
una lista mecánica de las 8 secciones, sino una lectura interpretativa de lo
que el repo revela sobre el negocio.

Ejemplo de apertura:
> "Explorando tu repo, encontré que tienes una base de conocimiento bien
> estructurada. Tu voz de marca está definida con claridad, y hay evidencia
> de campañas activas. Lo que no pude inferir habla tanto como lo que sí vi..."

Cierra siempre con la pregunta de los Gaps:

> "Estas son las dimensiones que no pude inferir. ¿Quieres que profundicemos
> en ellas ahora, o ejecuto /kokoro-onboard?"

---

## Notas para Claude

- Avanza en orden: Paso 1 (slug) → Paso 2 (discovery) → Paso 3 (síntesis) →
  Paso 4 (escribir) → Paso 5 (presentar). Nunca saltar pasos.
- No inventar rutas de archivos. Solo reportar lo que realmente se leyó.
- No modificar `kokoro-onboard-explore.md` ni ningún skill existente. Scout
  es un skill autónomo — su output es el archivo `profile.md`.
- El vocabulario de Eduardo aplica en todo: inversión, invitado, creación,
  compartir, reto/oportunidad. Nunca precio, cliente, producto, problema.
- Sin emojis. Sin tono de influencer. Sin listas de "10 tips".
- Responde en el idioma del usuario, manteniendo los nombres de secciones en español
  (son parte del contrato con /kokoro-onboard-explore — no se traducen).
- Si hay más de 10 archivos candidatos en Nivel 1, selecciona los 10 más extensos
  (más contenido = más riqueza para la síntesis).
- El perfil es un draft — siempre marcado así en el encabezado. El invitado
  confirma, Scout propone.
