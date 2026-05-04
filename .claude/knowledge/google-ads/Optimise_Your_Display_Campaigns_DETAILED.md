# Optimiza Tus Campañas Display: Guía Completa y Detallada

**Facilitador:** Eduardo Luna  
**Fecha:** 24/11/2025  
**Duración:** 8 minutos  
**Tema Principal:** Estrategias de optimización para campañas Display en Google Ads

---

## 📋 Tabla de Contenidos

1. [Introducción y Contexto](#introducción)
2. [Exclusión de Placements de Bajo Rendimiento](#exclusión-placements)
3. [Auditoría y Gestión de Audiencias](#auditoría-audiencias)
4. [Split Testing y Optimización de Anuncios Display](#split-testing)
5. [Resumen de Acciones Prioritarias](#resumen-acciones)

---

## 🎯 Introducción: El Diferenciador Clave de Display vs Search

### ¿Por Qué Display es Diferente?

| Aspecto | Search Campaigns | Display Campaigns |
|--------|-----------------|-------------------|
| **Tipo de Targeting** | Basado en **palabras clave** | Basado en **placements** (sitios web, apps, canales) |
| **Enfoque de Optimización** | Relevancia de keywords | Relevancia del sitio/contexto donde aparecen |
| **Control Principal** | Palabras clave que disparan anuncios | Sitios web y apps donde se muestran anuncios |
| **Métrica Crítica** | Click-Through Rate (CTR) | Cost per Conversion por placement |
| **Desafío Principal** | Gestionar palabras clave irrelevantes | Excluir placements que drenan presupuesto |

### 🔑 Concepto Core

> **En Display Campaigns, el éxito depende de encontrar los PLACEMENTS correctos, no las palabras clave correctas.**

Esto significa que necesitas un enfoque completamente diferente:
- ❌ **No controlas** qué sitios específicos Google elige para mostrar tus anuncios
- ✅ **Sí controlas** qué sitios excluyes después de ver dónde se gastan mal los fondos
- ✅ **Sí controlas** qué audiencias agregas después de identificar las que convierten

---

## 🚫 Exclusión de Placements de Bajo Rendimiento

### ¿Qué es un "Placement"?

Un placement es cualquier ubicación donde tu anuncio Display puede aparecer:
- 📱 **Aplicaciones móviles** (juegos, redes sociales, apps de noticias)
- 🌐 **Sitios web** (blogs, medios, portales)
- 🎬 **Canales de YouTube** (cualquier canal que monetiza con ads)
- 💻 **Otros contenido asociado** a tu red de Display

### Por Qué Excluir Placements

#### 📊 Problema Identificado

Los placements con **alto gasto pero cero conversiones** son drenadores de presupuesto que:
- Consumen fondos que podrían ir a placements de alto rendimiento
- Generan impresiones sin valor
- Aumentan artificialmente el Cost Per Conversion de toda la campaña
- A menudo son apps o sitios no relevantes a tu oferta

#### ⚠️ Caso Especial: Aplicaciones Móviles y Productos para Adultos

Un fenómeno específico ocurre cuando diriges a "adultos" pero el targeting alcanza a menores:

```
Escenario Real:
├─ Padre descarga app (juego, fitness, etc.)
├─ App tiene publicidad (monetizada)
├─ Niño juega la app usando el dispositivo del padre
└─ Anuncio se muestra al niño pero con perfil de targeting del padre

Resultado:
├─ Tu anuncio aparece ante audiencia equivocada (menores)
├─ Sin posibilidad de conversión (producto para adultos)
├─ Gasto desperdiciado en impresiones inútiles
└─ Es un problema especialmente común con apps de juegos
```

**Solución:** Excluir estas apps específicas completamente de tu campaña Display.

### 🔧 Proceso Paso a Paso: Cómo Excluir Placements

#### Paso 1: Acceder al Reporte de Placements

1. Abre tu **Display Campaign**
2. Ve a **Insights and Reports**
3. Busca la opción **"Where your ads have shown"** (no confundir con "When")
   - Si no la encuentras, usa la búsqueda del dashboard
   - El menú puede variar según la versión de Google Ads

**Visualización Correcta:**
```
Dashboard → Insights and Reports
                    ↓
        "Where ads have shown"  ✅ (CORRECTO)
        "When ads have shown"   ❌ (INCORRECTO - son timestamps)
```

#### Paso 2: Filtrar y Analizar por Placement Type

1. Cambia el rango de fechas a **últimos 30 días**
2. Agrupa por **Placement** (generalmente está disponible como columna)
3. Identifica el tipo de placement:
   - **Apps** - Donde usualmente están los problemas
   - **Websites** - Sitios específicos
   - **YouTube Channels** - Canales individuales

**Tabla de Análisis Recomendada:**

| Placement | Tipo | Costo | Conversiones | Acción |
|-----------|------|-------|--------------|--------|
| "Game App XYZ" | App | $450 | 0 | 🚫 EXCLUIR |
| "TikTok" | App | $320 | 2 | ⚠️ REVISAR |
| "Forbes.com" | Website | $280 | 12 | ✅ MANTENER |
| "Random Gaming App" | App | $85 | 0 | 🚫 EXCLUIR |
| "YouTube Gaming Channel" | YouTube | $150 | 3 | ✅ MANTENER |

#### Paso 3: Identificar Candidatos para Exclusión

**Criterios de Exclusión:**

| Señal | Descripción | Acción |
|-------|-----------|--------|
| 🔴 **Alto Costo + Cero Conversiones** | Gasto >$50 sin ninguna conversión | Excluir inmediatamente |
| 🟡 **Costo Moderado + Cero Conversiones** | Gasto $20-50 sin conversiones en 30 días | Monitorear, excluir si persiste |
| 🟢 **Costo Bajo + Cero Conversiones** | Gasto <$20 sin conversiones | Puede ser normal en pruebas, monitorear |

**Regla Práctica:**
> Si un placement gasta más de $100 sin generar NI UNA sola conversión en 30 días, excluye sin dudarlo.

#### Paso 4: Realizar la Exclusión

### ⚠️ IMPORTANTE: Dos Modelos de Targeting Diferentes

Tu método de exclusión depende del **targeting model** que usas:

---

### 📍 MODELO 1: Targeting Approach (Targeting Específico)

**Características:**
- Solo muestras anuncios en audiencias/placements ESPECÍFICOS que seleccionaste
- Control completo y restrictivo
- Menor alcance pero más enfocado

**Cómo Excluir (Fácil):**

```
Display Campaign → Audiences/Placements
                          ↓
              Click en placement problemático
                          ↓
                    Click "Remove"
                          ↓
                    ✅ Done - Excluido
```

**Pasos Detallados:**
1. Navega a tu Display Campaign
2. Ve a la pestaña **Audiences** o **Placements** (según tu configuración)
3. Localiza el placement que quieres excluir
4. Haz clic en los **3 puntos** o el ícono de opciones
5. Selecciona **"Remove"** o **"Exclude"**
6. Confirma

---

### 🔍 MODELO 2: Observation Approach (Observación + Exclusión)

**Características:**
- Muestras anuncios ampliamente (alcance máximo)
- Google elige dónde mostrar basado en audiencias
- Luego EXCLUYES manualmente lo que no funciona
- Control reactivo, no preventivo

**Cómo Excluir (Más Complejo - 2 pasos):**

```
PASO 1: Remover de Audiencia
────────────────────────────
Display Campaign → Audiences
                        ↓
        Click en audience problemática
                        ↓
                    Click "Remove"

PASO 2: Agregar como Exclusión
────────────────────────────
Display Campaign → Campaign Settings
                        ↓
           Exclusions (Audience Exclusions)
                        ↓
    Agregar la audiencia como EXCLUSIÓN
                        ↓
          ✅ Done - Completamente excluida
```

**Pasos Detallados - Modelo Observation:**

1. **Identifica** la audiencia o placement que no convierte (desde Insights)
2. Toma nota exacta del nombre
3. Ve a **Display Campaign → Audiences**
4. Busca y haz clic en la audiencia problemática
5. Selecciona **"Remove"** (la quita como targeting)
6. Ahora ve a **Campaign Settings**
7. Busca **"Audience Exclusions"** o **"Excluded Audiences"**
8. Agrega manualmente la audiencia que removiste
9. Guarda los cambios

**¿Por Qué 2 Pasos en Observation?**

Porque en modelo Observation:
- Removerla de "targeting" solo la deja de mostrar ALLÍ
- Pero Google puede seguir mostrándola en otros contextos
- Agregarla como **exclusión explícita** la bloquea completamente

---

### 📋 Checklist de Exclusión de Placements

```
□ Accedí a "Where your ads have shown"
□ Cambié a vista de últimos 30 días
□ Identifiqué placements con alto costo + cero conversiones
□ Tomé nota de qué modelo uso (Targeting vs Observation)
□ Si Targeting: Removí directamente
□ Si Observation: Removí + Agregué como exclusión
□ Documenté los placements excluidos
□ Programé revisión para próxima semana
```

---

## 👥 Auditoría y Gestión de Audiencias Display

### Contexto: Audiencias vs Placements

| Elemento | Display Search | Display Display |
|----------|---|---|
| **Audiencias** | Características de personas (edad, intereses, comportamiento) | Mismas características |
| **Placements** | NO aplicable en Search | Sitios/apps donde aparecen anuncios |
| **Enfoque en Display** | Opcional, se usa para refinamiento | CRÍTICO - es tu principal herramienta |

### 🎯 Objetivo de la Gestión de Audiencias

Hay **2 acciones opuestas** que hacer semanalmente:

| Acción | Objetivo | Impacto |
|--------|----------|---------|
| **AGREGAR** audiencias que convierten | Ampliar alcance de audiencias de alto rendimiento | Aumentar conversiones |
| **EXCLUIR** audiencias que gastan sin convertir | Detener desperdicio de presupuesto | Reducir CPC, aumentar ROI |

---

### ✅ ACCIÓN 1: Agregar Audiencias de Alto Rendimiento

#### Por Qué Funciona

Google **descubre automáticamente** audiencias que tienen alto engagement con tus anuncios Display. Aunque no las agregaste explícitamente, el sistema nota:
- Qué características demográficas hacen clic
- Qué intereses se alinean con conversiones
- Qué comportamientos generan compras

Si detectas una audiencia en Insights con muchas conversiones, debes **agregarlo como señal oficial** para que Google optimize mejor.

#### Paso 1: Acceder a Insights de Audiencias

```
Display Campaign
        ↓
  Insights Tab
        ↓
Busca sección "Audiences"
(Nota: Puede no estar disponible hasta que acumules datos)
```

**¿Cuándo Aparece?**
- Después de 2-4 semanas de datos
- Cuando hay suficientes conversiones asociadas a audiencias
- Si tu campaña está configurada con conversión tracking

#### Paso 2: Identificar Audiencias de Alto Rendimiento

**Filtros a Aplicar:**

| Métrica | Qué Buscar |
|--------|-----------|
| **Conversiones** | Ordena DESCENDENTE - busca top 3-5 |
| **Conversion Rate** | >5% es excelente en Display |
| **Cost Per Conversion** | Menor que el promedio de campaña |

**Ejemplo Real:**

```
Audiencia                    | Impresiones | Conversiones | CPC |
─────────────────────────────────────────────────────────────────
"Business Decision Makers"   | 1,200       | 18           | $45 | ← AGREGAR
"Tech Enthusiasts"           | 950         | 15           | $52 | ← CONSIDERAR
"General Interest"           | 2,100       | 12           | $78 | ❌ MANTENER
"Low Income"                 | 500         | 1            | $340| ❌ EXCLUIR
```

#### Paso 3: Copiar la Audiencia

1. Identifica la audiencia de alto rendimiento
2. Copia exactamente el **nombre/descripción** de la audiencia
3. Abre un **bloc de notas** o documento temporal
4. Pega ahí para tener lista durante el siguiente paso

**Ejemplo de copia:**
```
Business Decision Makers - Tech Sector
```

#### Paso 4: Agregar a tu Campaña Display

```
Display Campaign
        ↓
   Ad Groups
        ↓
Selecciona el Ad Group más relevante
        ↓
     Audiences Tab
        ↓
      Click "Edit"
        ↓
   Click "+ Audience"
        ↓
Pega el nombre de audiencia
        ↓
     Click "Save"
```

**Detalles Importantes:**

| Paso | Consideración |
|------|---------------|
| **Seleccionar Ad Group** | Elige el que más se alinee con la audiencia. Si tienes múltiples Ad Groups, crea relevancia |
| **Tipo de Agregación** | Aparecerá como "Observation" (Google observó conversiones) |
| **Impacto Inmediato** | No es inmediato; Google usa esto para futuros optimizations |

---

### ❌ ACCIÓN 2: Excluir Audiencias de Bajo Rendimiento

#### Cuándo Excluir

**Red Flag #1: High Spend + Zero Conversions**
```
Audiencia problemática:
├─ Costo acumulado: $200+
├─ Conversiones: 0
├─ Período: 30+ días
└─ ACCIÓN: Excluir inmediatamente
```

**Red Flag #2: High CPC vs Promedio**
```
Si el promedio de tu campaña es $50/conversión
Pero una audiencia cuesta $150/conversión
└─ ACCIÓN: Monitorear, considera excluir si no mejora
```

#### Paso 1: Acceder a Audiencias Actuales

```
Display Campaign (Remarketing usualmente)
        ↓
   Audiences Tab
        ↓
Mira la tabla de audiencias
        ↓
Ordena por Costo (descendente)
```

#### Paso 2: Analizar Rendimiento

Crea esta vista en tu campaña:

```
Display Campaign
        ↓
Audiences Tab
        ↓
Click "Conversions" column (visible en tabla)
        ↓
También agrega columna "Cost"
        ↓
Ordena por Costo > Conversiones
```

**Tabla de Análisis:**

| Audiencia | Costo | Conversiones | ROAS | Acción |
|-----------|-------|--------------|------|--------|
| "Visited Product Page" | $450 | 15 | 2.5x | ✅ Mantener |
| "Abandoned Cart" | $300 | 8 | 1.8x | ✅ Mantener |
| "Low Intent" | $200 | 0 | 0x | 🚫 Excluir |
| "Site Visitor 6mo" | $150 | 2 | 0.5x | ⚠️ Revisar |

#### Paso 3: Determinar Tu Targeting Model

Esto es CRÍTICO porque cambia cómo excluyes.

**¿Cómo saber qué modelo usas?**

```
Display Campaign → Audiences Tab
                        ↓
        Observa cómo están configuradas
                        ↓
```

| Señal | Modelo que Usas |
|-------|-----------------|
| Las audiencias dicen **"Targeting"** o están seleccionadas específicamente | TARGETING MODEL |
| Las audiencias dicen **"Observation"** o están listadas como "informational" | OBSERVATION MODEL |
| Mezcla de ambas | HYBRID (menos común) |

---

### 🎯 Modelo Targeting (Exclusión Fácil)

Si usas **Targeting Model**, la exclusión es simple:

```
Step 1: Ve a Audiences Tab
            ↓
Step 2: Encuentra la audiencia problema
            ↓
Step 3: Haz clic en ella
            ↓
Step 4: Click "Remove" o "Delete"
            ↓
Step 5: ✅ Confirmado - No se mostrará más a esa audiencia
```

**Visualización:**
```
Audiences Targeting:
├─ ✅ Business Decision Makers (performing well)
├─ ✅ Tech Professionals (performing well)
├─ ❌ Low Income (cost $200, 0 conversions) → REMOVE
└─ ✅ C-Level Executives (performing well)
```

---

### 🔍 Modelo Observation (Exclusión con 2 Pasos)

Si usas **Observation Model**, necesitas hacer dos cosas:

#### Paso A: Remover de Audiencias

```
Display Campaign
        ↓
   Audiences Tab
        ↓
Encuentra audiencia problemática
        ↓
   Click el nombre o selecciona
        ↓
    Click "Remove"
```

#### Paso B: Agregar como Exclusión Explícita

Aquí es donde es diferente a Targeting. Simplemente remover NO es suficiente en Observation. Debes bloquearla completamente:

```
Display Campaign
        ↓
  Campaign Settings
        ↓
  Scroll a "Audience Exclusions"
        ↓
   Click "Edit Exclusions"
        ↓
   Add the problematic audience
        ↓
      Save Changes
```

**¿Por Qué 2 Pasos?**

```
Observation Model Flujo:
├─ Sin remover: Google sigue mostrando anuncios a esa audiencia
├─ Remover solo: Se quita de "targeting" pero puede mostrarse en otros contextos
└─ Remover + Excluir: Completamente bloqueada, sin excepciones
```

---

### 📋 Guía Rápida: ¿Targeting o Observation?

```
┌─────────────────────────────────────────────────────┐
│ Veo una audiencia que no convierte                   │
├─────────────────────────────────────────────────────┤
│                                                       │
│ ¿Uso Targeting Model?                               │
│    │                                                  │
│    └─→ YES: Simplemente REMOVE (1 paso) ✅           │
│                                                       │
│ ¿Uso Observation Model?                             │
│    │                                                  │
│    └─→ YES: REMOVE + ADD EXCLUSION (2 pasos) ✅      │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

### 📊 Resumen: Auditoría de Audiencias Display

**Checklist Semanal:**

```
AGREGAR Audiencias de Alto Rendimiento:
□ Accedí a Insights → Audiences
□ Identifiqué audiencias con 10+ conversiones
□ Copié el nombre exacto
□ Agregué a Ad Group relevante
□ Guardé cambios

EXCLUIR Audiencias de Bajo Rendimiento:
□ Accedí a Audiences Tab
□ Ordené por costo y conversiones
□ Identifiqué audiencias con costo >$100 y 0 conversiones
□ Determiné mi modelo (Targeting vs Observation)
□ Removí (Targeting) o Removí + Excluí (Observation)
□ Documenté cambios para referencia futura
```

---

## 📺 Split Testing y Optimización de Anuncios Display

### Contexto: Diferencias Display vs Search Ads

| Aspecto | Search Ads | Display Ads |
|--------|-----------|-----------|
| **Elementos a Testear** | Títulos, descripciones, CTA | Imágenes, títulos, copy, promociones |
| **Duración de Test** | 30 días estándar | 30-60 días (más variable) |
| **Parada Común** | No aplica | **Campanias promocionales** (períodos específicos) |
| **Métrica Principal** | CTR y Conversion Rate | Conversion Rate primario, CTR secundario |
| **Complejidad de Ad** | Texto principalmente | Imágenes, video, texto |

### 🎬 Escenario Especial: Display para Promociones

Aquí está la clave: **Display campaigns a menudo se usan SOLO durante períodos promocionales específicos.**

```
Ejemplo Timeline:
├─ Enero: Campaña "New Year" (ad copy único)
├─ Febrero: Sin campaña Display
├─ Marzo: Campaña "Spring Sale" (ad copy diferente)
├─ Abril: Sin campaña
└─ Diciembre: Campaña "Holiday Promo" (ad copy único)

Problema: 
No puedes hacer split test tradicional si cambias 
todo el copy con cada promoción
```

**Solución: Review Retrospectivo**

Aunque no hagas split tests formales durante campanias promocionales, puedes:
- Comparar el mejor performing ad de Enero vs Marzo
- Analizar qué elementos funcionaron mejor
- Identificar patrones en imágenes ganadoras
- Aplicar aprendizajes a próximas campanias

---

### ✅ Proceso 1: Split Testing Tradicional

#### Configuración del Test

**Requisitos:**
- ✅ Dos versiones de anuncios Display diferentes
- ✅ Misma audiencia/placement
- ✅ Período mínimo 30 días
- ✅ Mínimo 100+ impresiones por ad

**Elementos para Testear en Display:**

```
Opción 1: IMÁGENES
├─ Ad A: Imagen tipo landscape
└─ Ad B: Imagen tipo portrait (variable única)

Opción 2: HEADLINES
├─ Ad A: "Limited Time Offer"
└─ Ad B: "Exclusive Deal This Week" (variable única)

Opción 3: CALL TO ACTION
├─ Ad A: "Learn More"
└─ Ad B: "Start Free Trial" (variable única)

❌ NO HAGAS ESTO:
├─ Ad A: Imagen diferente + Headline diferente + CTA diferente
└─ Ad B: Otra imagen + Otro headline + Otro CTA
   (No puedes saber cuál elemento hizo la diferencia)
```

#### Paso 1: Crear Variantes de Anuncios

```
Display Campaign
        ↓
    Ads & Extensions
        ↓
      Click "+ Ad"
        ↓
Selecciona "Display Ad Format"
        ↓
Crea primera variante (Ad A)
        ↓
Guarda y crea Ad B con UNA sola diferencia
```

**Checklist de Variante:**

| Elemento | Ad A | Ad B | Nota |
|----------|------|------|------|
| Imagen | Version 1 | Version 2 | ÚNICA DIFERENCIA |
| Headline | Mismo | Mismo | ✅ IGUAL |
| Description | Mismo | Mismo | ✅ IGUAL |
| CTA | Mismo | Mismo | ✅ IGUAL |

#### Paso 2: Reunir Datos por 30+ Días

Metrics a monitorear durante el test:

```
Display Campaign → Ads Tab
        ↓
Columns: Clicks, Impressions, CTR, Conversions, Cost
        ↓
Weekly Review (mejor que daily)
```

**Tabla de Seguimiento:**

| Semana | Ad A Clicks | Ad B Clicks | Ad A Conv | Ad B Conv | Leading |
|--------|------------|------------|-----------|-----------|---------|
| Week 1 | 125 | 118 | 8 | 7 | A (Incierto) |
| Week 2 | 132 | 129 | 9 | 9 | Tied (Incierto) |
| Week 3 | 128 | 145 | 8 | 11 | B (Tendencia) |
| Week 4 | 120 | 152 | 7 | 13 | **B (Claro)** |

#### Paso 3: Evaluar Ganador (Conversiones > CTR)

**Regla de Decisión:**

```
Métrica #1: Click-Through Rate
├─ Ad A CTR: 2.8%
└─ Ad B CTR: 3.2%
    → Ad B tiene mejor CTR ✓

Métrica #2: Conversion Rate (CRÍTICA)
├─ Ad A Conv Rate: 3.2%
└─ Ad B Conv Rate: 4.8%
    → Ad B tiene mejor Conv Rate ✓✓

Métrica #3: Cost Per Conversion
├─ Ad A CPC: $65
└─ Ad B CPC: $48
    → Ad B es más eficiente ✓✓✓

DECISIÓN FINAL: Ganador = Ad B
```

**Caso Donde CTR Engaña:**

```
Ad A (El Llamativo):
├─ CTR: 4.5% (muy alto)
├─ Conversions: 6
└─ CPC: $85 (caro)

Ad B (El Relevante):
├─ CTR: 2.1% (más bajo)
├─ Conversions: 12 (doble)
└─ CPC: $42 (mitad de precio)

DECISIÓN: Mantener Ad B a pesar del CTR más bajo
RAZÓN: Las conversiones importan más que los clics
```

#### Paso 4: Pausar Perdedor y Crear Nuevo Test

```
Display Campaign
        ↓
    Ads & Extensions
        ↓
Encontrar Ad A (perdedor)
        ↓
    Click "Pause"
        ↓
Ahora crea Ad C como nueva variante
        ↓
Testea Ad B (ganador) vs Ad C (nuevo)
```

---

### 📊 Proceso 2: Review Retrospectivo (Para Campañas Promocionales)

Cuando **no puedes hacer split tests formales** (porque cambias todo cada temporada), usa esta estrategia:

#### Escenario

```
Campaña "Holiday 2024" (Nov-Dec):
├─ Ad 1: Santa Theme, "Gift Your Loved Ones", Red CTA
├─ Ad 2: Elegant Snow Theme, "Premium Selection", Silver CTA  
├─ Ad 3: Family Theme, "Create Memories", Warm CTA
└─ Resultado: Ad 2 ganador con 5.2% Conv Rate

Campaña "Spring 2025" (Feb-Mar):
├─ Ad A: Flower Theme, "New Arrivals", Green CTA
├─ Ad B: Minimal Design, "Refresh Your Style", Blue CTA
└─ Ad C: Nature Theme, "Feel Alive", Brown CTA
└─ Resultado: Ad A ganador con 4.8% Conv Rate
```

#### Análisis Retrospectivo

**Pregunta:** ¿Qué aprendizajes puedo sacar comparando Holiday vs Spring?

```
Holiday Winner (Ad 2):
├─ Image Style: Elegant / Sophisticated
├─ Tone: Premium / Exclusive
├─ Color Scheme: Cool tones (Silver/White)
└─ CTA Sentiment: Refinement-focused

Spring Winner (Ad A):
├─ Image Style: Vibrant / Fresh
├─ Tone: Contemporary / Modern
├─ Color Scheme: Warm/Natural (Greens/Browns)
└─ CTA Sentiment: Action-focused

PATTERN FOUND:
├─ Both winners = Simple, uncluttered imagery
├─ Both winners = Clear, benefit-driven messaging
├─ Both winners = Single color palette (not multi-colored)
└─ APRENDIZAJE: Minimalist design > Cluttered design
```

#### Elementos a Comparar

| Elemento | Holiday Winner | Spring Winner | Pattern |
|----------|---|---|---|
| **Image Complexity** | Simple | Simple | Simplicity wins |
| **Text Readability** | Large font | Large font | Size matters |
| **Color Count** | 2-3 dominant | 2-3 dominant | Less is more |
| **Product Visibility** | 70% of image | 70% of image | Clear focus |
| **Promotion Clarity** | "Premium Offer" | "Fresh Offer" | Clarity essential |

#### Documentar Aprendizajes

Crea un documento tipo:

```
DISPLAY CAMPAIGN AD INSIGHTS
═══════════════════════════

Período: 2024-2025

WINNING PATTERNS:
✓ Images: Simple, uncluttered (max 2-3 dominant colors)
✓ Headlines: Action-oriented or benefit-driven
✓ Copy Length: 2-3 lines maximum
✓ Product Ratio: 60-70% of image space
✓ CTA Buttons: Contrasting colors, large

LOSING PATTERNS:
✗ Multi-layered images (too much visual info)
✗ Vague headlines ("Learn More")
✗ Small fonts on images
✗ Product placement in corner (insufficient focus)

PRÓXIMAS CAMPAÑAS:
Apply minimalist design principles
Use benefit-driven headlines
Ensure product takes center stage
```

---

### 🔄 Frequency of Ad Review and Updates

#### Timing by Campaign Type

| Campaign Type | Review Frequency | Test Duration | Notes |
|--------------|-----------------|----------------|-------|
| **Ongoing Campaign** | Weekly | 30+ days | Standard timing |
| **Promotional Campaign** | 2x per week | Duration of promo | Time-sensitive |
| **Holiday Campaign** | Daily (last week) | 30+ days | Peak period tracking |
| **Test Phase** | 3x per week | 60+ days | More data = better decisions |

#### Key Metrics Dashboard

**Create this view in your Display Campaign:**

```
Display Campaign → Ads Tab
        ↓
Add Columns:
├─ Clicks
├─ Impressions
├─ CTR
├─ Conversions
├─ Conv. Rate
├─ Cost
├─ Cost Per Conversion
└─ (Optional) Conversion Value if tracking
        ↓
Segment By: Ad Type or Image
        ↓
Date Range: Last 30/60 days
        ↓
Sort By: Conversions (Descending)
```

---

### 📋 Checklist de Testing Display

```
SETUP DEL TEST:
□ Creé 2 versiones de ad (UNA variable diferente)
□ Ambos ads tienen mínimo 100+ impresiones
□ Período de test configurado para 30+ días
□ Métricas a monitorear identificadas

DURANTE EL TEST:
□ Reviso semanalmente (no diariamente)
□ Registro datos en spreadsheet
□ Observo tendencias (no variaciones semanales)
□ Recopilo mínimo 4 semanas de datos

EVALUACIÓN (Semana 4+):
□ Comparo CTR (secundario)
□ Comparo Conversion Rate (primario)
□ Comparo Cost Per Conversion (crítico)
□ Determino ganador claro vs incierto
□ Si incierto: continúo test 2 semanas más

ACCIÓN FINAL:
□ Pauso ad perdedor
□ Creo nuevo ad para nuevo test
□ Documento aprendizajes
□ Aplico insights a próximas campañas
```

---

## 📈 Resumen de Acciones Prioritarias

### Frecuencia y Impacto

| Acción | Frecuencia | Impacto | Prioridad |
|--------|-----------|---------|-----------|
| **Excluir placements con alto costo/cero conversiones** | Semanal | 🔴 Muy Alto | 1️⃣ |
| **Revisar y agregar audiencias de alto rendimiento** | Semanal | 🔴 Muy Alto | 1️⃣ |
| **Excluir audiencias de bajo rendimiento** | Semanal | 🔴 Muy Alto | 1️⃣ |
| **Monitorear split tests de anuncios** | Semanal | 🟠 Alto | 2️⃣ |
| **Pausar ads perdedores y crear nuevos tests** | Cada 30 días | 🟠 Alto | 2️⃣ |
| **Revisión retrospectiva de campañas pasadas** | Post-campaña | 🟡 Medio | 3️⃣ |

### Rutina Semanal Recomendada (30 minutos)

```
LUNES:
├─ 10 min: Acceder a "Where your ads shown"
├─ Excluir placements con costo >$50 y 0 conversiones
└─ Documentar en lista de exclusiones

MIÉRCOLES:
├─ 8 min: Ir a Audiences → Insights
├─ Agregar 1-2 audiencias de alto rendimiento
└─ Revisar high-spend/low-conversion audiences

VIERNES:
├─ 7 min: Revisar ads en split test
├─ Analizar tendencias de performance
├─ Tomar notas para decisiones futuras
└─ Crear nuevo test si alguno concluyó
```

---

## 🎓 Notas Importantes y Takeaways

### 1. **Display ≠ Search**
Display campaigns se optimizan por **placements y audiencias**, no por keywords. Tu enfoque debe ser completamente diferente: encuentras malos placements y los excluyes, encuentras buenas audiencias y las agregas.

### 2. **Placements Primero, Audiencias Segundo**
```
Prioridad de optimización:
1. Excluir bad placements (afecta directamente dónde apareces)
2. Gestionar audiencias (refina quién ve tu ad)
3. Testear anuncios (mejora el mensaje)
```

### 3. **Modelo Matters: Targeting vs Observation**
No es lo mismo en ambos modelos. Saber cuál usas es esencial para hacer exclusiones correctamente. Targeting = simple, Observation = requiere 2 pasos.

### 4. **Display para Promociones: Especial**
Si usas Display solo para períodos promocionales, no esperes split tests tradicionales. En su lugar, guarda datos históricos y compara patrones entre campañas diferentes.

### 5. **Conversions > Clicks > Impressions**
En Display:
```
❌ NO optimices por: Impresiones
⚠️  CONSIDERA: Click-Through Rate (relevancia)
✅ OPTIMIZA por: Conversion Rate y Cost Per Conversion
```

### 6. **Weekly Review Needed**
Display campaigns requieren revisión semanal porque:
- Los placements pueden cambiar dinámicamente
- Las audiencias varían en performance rápidamente
- Los datos se recopilan más lentamente que en Search

### 7. **Documentation is Power**
Mantén un registro de:
- Placements excluidos (para no re-agregar accidentalmente)
- Audiencias que funcionan (para reutilizar)
- Winning ad patterns (para future campaigns)

---

## 🚀 Próximos Pasos

### Inmediato (Esta Semana)

```
1. Accede a tu Display Campaign
2. Ve a "Where your ads shown"
3. Identifica 2-3 placements con alto costo/cero conversiones
4. Excluye esos placements (usando tu modelo: Targeting o Observation)
5. Documenta la acción en una hoja de cálculo
```

### Próximas 2 Semanas

```
1. Revisa Insights → Audiences
2. Agrega 2-3 audiencias de alto rendimiento a tu campaña
3. Identifica audiencias con costo alto pero cero conversiones
4. Excluye esas audiencias
5. Inicia 1 split test si aún no tienes datos
```

### Este Mes

```
1. Establece rutina semanal de 30 minutos de revisión
2. Revisa resultados de split test (si está en semana 4+)
3. Crea documento de "Winning Ad Patterns" basado en resultados
4. Escala presupuesto en placements/audiencias de alto rendimiento
```

---

## 📞 Recursos Rápidos

### Dónde Encontrar Cada Cosa

| Tarea | Ubicación | Ruta |
|-------|-----------|------|
| Ver placements | Dashboard | Campaign → Insights → Where ads shown |
| Revisar audiencias | Dashboard | Campaign → Audiences Tab |
| Gestionar exclusiones | Campaign | Campaign Settings → Audience Exclusions |
| Ver ads performance | Dashboard | Campaign → Ads & Extensions |
| Crear ad groups | Campaign | Campaign → Ad Groups → + Ad Group |

### Terminología Clave

```
PLACEMENT: Ubicación donde aparece tu anuncio (app, website, canal)
AUDIENCE: Características de la persona que ve tu anuncio
TARGETING MODEL: Solo muestras en lo que específicamente seleccionaste
OBSERVATION MODEL: Muestras ampliamente, luego excluyes lo malo
IMPRESSION: Vez que tu anuncio se mostró
CONVERSION: Acción valiosa completada (compra, signup, etc.)
COST PER CONVERSION: Gasto promedio por acción valiosa lograda
```

---

**Versión Final: Markdown Ultradetallado de Máximo Valor**  
*Creado a partir de transcripción de Eduardo Luna*  
*Optimizado para implementación inmediata*
