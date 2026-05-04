# Keyword Targeting, Search Term Audits y Campaign Bidding Review
## Guía Completa para Search & Shopping Campaigns

**Facilitador:** Eduardo Luna  
**Fecha:** 24/11/2025  
**Duración:** 25 minutos  
**Tema Principal:** Estrategias avanzadas de optimización de pujas, auditoría de términos de búsqueda e insights de subastas

---

## 📋 Tabla de Contenidos

1. [Introducción: La Importancia de la Puja Correcta](#introducción)
2. [Audit de Términos de Búsqueda y Palabras Clave](#search-term-audit)
3. [Reporte de Auction Insights](#auction-insights)
4. [Review de Split Tests en Search Campaigns](#split-tests)
5. [Campaign Bidding Review: La Guía Definitiva](#bidding-review)
6. [Resumen de Acciones Prioritarias](#resumen-acciones)

---

## 🎯 Introducción: La Importancia de la Puja Correcta

### El Mayor Desafío en Google Ads

> **Eduardo Luna:** "Getting your bidding strategies right for Google is one of the hardest things to get right but it's also when you get it right it can make one of the biggest differences in your account."

La puja correcta es lo que separa a los profesionales de Google Ads de los aficionados. Sin embargo, es también donde más daño se puede hacer a una campaña.

### El Problema con Google's Recommendations

Google constantemente recomienda:
- ❌ Cambiar a "Maximize Conversions" o "Maximize Conversion Value"
- ❌ Agregar Target ROAS (Return on Ad Spend)
- ❌ Agregar Target CPA (Cost Per Acquisition)

**El problema:** Google **empuja estas características demasiado temprano**, y cuando se implementan sin datos suficientes, pueden causar **resultados devastadores** para tu cuenta.

### 🔴 La Verdad Incómoda Sobre Smart Bidding

Smart bidding es poderoso, pero es como un arma:
- 🎯 **En manos correctas:** Puede multiplicar ROI
- ⚡ **En manos incorrectas:** Puede destruir una campaña

Este documento te enseña cuándo, cómo y por qué aplicar (o NO aplicar) smart bidding.

---

## 🔍 Audit de Términos de Búsqueda y Palabras Clave

### ¿Por Qué es Crítico?

En Search Campaigns, tus campañas se rigen por **palabras clave**, pero los usuarios buscan usando **términos específicos**. Estos pueden no coincidir perfectamente.

**Ejemplo:**
```
Tu palabra clave: "lawyer services"
Término que busca usuario #1: "best lawyer in my area"
Término que busca usuario #2: "free legal consultation"
Término que busca usuario #3: "what qualifications do lawyers need"

Resultado: Tu anuncio aparece en búsquedas que no generan conversiones
```

### El Objetivo del Search Term Audit

**Dos acciones principales:**

| Acción | Objetivo | Resultado |
|--------|----------|-----------|
| **AGREGAR** términos que convierten a palabras clave | Ampliar relevancia y capturar más tráfico de calidad | Más conversiones con mismo presupuesto |
| **EXCLUIR** términos que gastan sin convertir | Detener desperdicio de presupuesto | Mejor ROI, CPA más bajo |

### 📋 Proceso: Auditar Términos de Búsqueda

#### Paso 1: Acceder al Search Terms Report

```
Search Campaign
        ↓
Keywords Tab
        ↓
Search Terms (opción en el menú lateral)
        ↓
Cambiar rango de fechas a últimos 30 días
```

#### Paso 2: Identificar Términos de Alto Rendimiento

**Filtros Recomendados:**

| Métrica | Qué Buscar | Acción |
|---------|-----------|--------|
| **Conversions** | Términos con 3+ conversiones | ✅ AGREGAR como palabra clave |
| **Conversion Rate** | >10% conversion rate | ✅ AGREGAR como palabra clave |
| **Cost per Conversion** | Menor que CPA de campaña | ✅ AGREGAR como palabra clave |

**Tabla de Ejemplo:**

| Search Term | Clicks | Conversions | CPC | Conv Rate | Acción |
|------------|--------|-------------|-----|-----------|--------|
| "best lawyer for divorce" | 45 | 8 | $32 | 17.8% | ✅ AGREGAR |
| "free legal advice" | 28 | 6 | $28 | 21.4% | ✅ AGREGAR |
| "lawyer near me" | 52 | 4 | $41 | 7.7% | ⚠️ CONSIDERAR |
| "how to become a lawyer" | 120 | 0 | $15 | 0% | 🚫 EXCLUIR |
| "legal dictionary" | 89 | 0 | $18 | 0% | 🚫 EXCLUIR |

#### Paso 3: Agregar Términos Como Palabras Clave

**Opción A: Agregar Directamente**

```
Search Terms Report
        ↓
Seleccionar término de alto rendimiento
        ↓
Click "Add as keyword"
        ↓
Elegir tipo de match (Broad, Phrase, Exact)
        ↓
Elegir Ad Group destino
        ↓
Save
```

**¿Qué tipo de Match elegir?**

| Match Type | Cuándo Usarlo | Ejemplo |
|-----------|--------------|---------|
| **Exact [término]** | Cuando quieres máxima relevancia | [best divorce lawyer] - Solo esa búsqueda |
| **Phrase "término"** | Balance entre relevancia y volumen | "best divorce lawyer" - Con palabras alrededor permitidas |
| **Broad +término +específico** | Cuando quieres flexibilidad | +best +divorce +lawyer - Todas las palabras pero en cualquier orden |

**Recomendación de Eduardo:** Usa **Exact match** para términos de alto valor (conversión clara) y **Phrase match** para términos de volumen moderado.

#### Paso 4: Excluir Términos de Bajo Rendimiento

**Criterios para Exclusión:**

| Señal | Descripción | Acción |
|-------|-----------|--------|
| 🔴 **Alto costo + Cero conversiones** | Término ha gastado $100+ sin conversión | Excluir inmediatamente |
| 🟡 **Relevancia cuestionable** | Término claramente no relacionado | Excluir |
| 🟢 **Bajo volumen, bajo costo** | <$20 gastado, 0 conversiones | Monitorear antes de excluir |

**Cómo Excluir:**

```
Search Terms Report
        ↓
Seleccionar término a excluir
        ↓
Click "Add as negative keyword"
        ↓
Elegir nivel (Campaign o Ad Group)
        ↓
Elegir tipo de match (Broad, Phrase, Exact)
        ↓
Save
```

**¿Campaign o Ad Group Level?**

```
Campaign Level Negative:
├─ Se aplica a TODA la campaña
├─ Usa para términos universalmente irrelevantes
└─ Ejemplo: "free" si tu servicio no es gratuito

Ad Group Level Negative:
├─ Se aplica SOLO a ese grupo
├─ Usa para términos específicos a ese grupo
└─ Ejemplo: Excluir "residential" si ad group es "commercial"
```

### 📊 Frecuencia y Timing

| Tarea | Frecuencia | Tiempo Requerido |
|-------|-----------|-----------------|
| Revisar Search Terms | Semanal | 15 minutos |
| Agregar nuevas keywords | Según datos | 10 minutos |
| Excluir términos pobres | Semanal | 10 minutos |
| Análisis detallado | Mensual | 30 minutos |

---

## 📈 Reporte de Auction Insights

### ¿Qué es y Por Qué Importa?

El Auction Insights Report te muestra **quién más está pujando** en tus subastas de Google Ads. Es una herramienta diagnóstica para entender por qué tu CPC está subiendo.

**Recuerda:** Google Ads es una subasta. Más competidores = CPC más alto

### Escenario Principal de Uso

```
Situación:
├─ Tu CPC ha subido de $25 a $45
├─ No sabes la razón
└─ ¿Es porque Google subió precios? ¿Hay nuevos competidores?

Solución:
└─ Revisa Auction Insights para diagnosticar
```

### 📋 Cómo Acceder a Auction Insights

```
Search Campaign
        ↓
Keywords (o Ad Groups)
        ↓
Columns → Auction Insights
        ↓
(Aparecerán nuevas columnas en tu tabla)
```

**Alternativa:**
```
Campaign
        ↓
Insights and Reports
        ↓
Buscar "Auction Insights"
```

### 🔍 Métricas Principales del Reporte

| Métrica | Qué Significa | Qué Buscar |
|---------|--------------|-----------|
| **Impression Share** | % de impresiones que ganaste de todas las disponibles | Mayor es mejor (60%+) |
| **Overlap Rate** | % de subastas donde compites contra competidor específico | Baja es mejor (<30%) |
| **Position Above Rate** | % de subastas donde competidor aparece por encima de ti | Baja es mejor (<30%) |
| **Top of Page Rate** | % de subastas donde tu ad aparece en posición #1-3 | Mayor es mejor (>60%) |

### 📊 Caso de Estudio Real: Análisis de Competencia

**Escenario:** Tu CPC subió de 14% impression share a 10% en un mes

```
AGOSTO (Dato Anterior):
├─ Tu Impression Share: 14%
├─ Competidor A: Ranking #1 (31% impression share)
├─ Competidor B: Ranking #2 (15% impression share)
├─ Competidor C: Ranking #3 (12% impression share)
└─ Tu Ranking: #4

SEPTIEMBRE (Dato Actual):
├─ Tu Impression Share: 10% (BAJÓ de 14%)
├─ Competidor A: Ranking #1 (31% impression share) - IGUAL
├─ Competidor B: Ranking #2 (18% impression share) - SUBIÓ
├─ Competidor C: Ranking #3 (15% impression share) - SUBIÓ
├─ Nuevo Competidor D: Ranking #4 (12% impression share) - NUEVO
└─ Tu Ranking: #5

DIAGNÓSTICO:
└─ Tu CPC subió porque nuevos competidores entraron + competidores existentes aumentaron gasto
```

### 🎯 Cómo Interpretar los Datos

#### Escenario 1: Aumento de CPC + Nuevos Competidores

```
Datos:
├─ CPC aumentó de $25 a $40 (+60%)
├─ Auction Insights: 2 competidores nuevos
├─ Tu Impression Share: Bajó de 60% a 45%
└─ Top of Page Rate: Bajó de 70% a 50%

Conclusión:
└─ El aumento de CPC se debe a AUMENTO DE COMPETENCIA
└─ Es un problema del mercado, no de tu estrategia

Acciones Posibles:
├─ 1. Mejorar Quality Score para compensar
├─ 2. Revisar y mejorar CTR
├─ 3. Revisar y mejorar Conversion Rate
├─ 4. Aceptar CPC más alto como costo de hacer negocios
└─ 5. Reducir presupuesto si ROI no justifica CPC
```

#### Escenario 2: Aumento de CPC + Sin Nuevos Competidores

```
Datos:
├─ CPC aumentó de $25 a $40 (+60%)
├─ Auction Insights: Mismos competidores
├─ Top of Page Rate: Bajó de 70% a 50%
├─ Position Above Rate: Aumentó (competidores por encima)
└─ Tu Impression Share: Bajó de 60% a 40%

Conclusión:
└─ El aumento NO es por competencia externa
└─ Es porque tu ad rank bajó

Acciones Prioritarias:
├─ 1. REVISAR QUALITY SCORE - Probablemente bajó
├─ 2. REVISAR CTR - Probablemente bajó
├─ 3. REVISAR LANDING PAGE - Menos relevante
├─ 4. Revisar Max CPC si está establecido
└─ 5. Revisar estrategia de puja actual
```

### 📊 Overlap Rate y Position Above Rate

**¿Por Qué Son Importantes?**

```
Overlap Rate (Frecuencia de Compra):
├─ Alto (>50%): Compites frecuentemente contra este competidor
│  └─ Acción: Mejora tu ad rank para ganar posiciones
└─ Bajo (<20%): Rara vez compites contra él
   └─ Información: No es una amenaza inmediata

Position Above Rate (Quién Gana):
├─ Alto (>50%): Competidor te supera frecuentemente
│  └─ Acción: Tu ad rank es más bajo, mejora Quality Score
└─ Bajo (<30%): Frecuentemente los superas
   └─ Posición: Tienes ventaja en este mercado
```

### 📋 Checklist de Auction Insights

```
□ Accedí a Auction Insights Report
□ Cambié a vista mensual (mejor para tendencias)
□ Comparé mes actual vs mes anterior
□ Identifiqué nuevos competidores
□ Revisé si competidores aumentaron gasto
□ Revisé mi Impression Share (bajó o subió)
□ Revisé Position Above Rate (gano o pierdo)
□ Determiné si aumento CPC es por competencia o por ad rank
□ Documenté hallazgos para acción
```

---

## 🧪 Review de Split Tests en Search Campaigns

### Principios Fundamentales

✅ **Lo Correcto:**
- Testear UN SOLO elemento a la vez
- Reunir datos por mínimo 30 días
- Usar mínimo 100-200 conversiones antes de decidir
- Pausar perdedor y crear nuevo test

❌ **Lo Incorrecto:**
- Cambiar múltiples elementos simultáneamente
- Decidir ganador demasiado rápido (antes de 30 días)
- Basarse solo en CTR (conversion rate es más importante)
- Mantener ambos anuncios activos sin pausar al perdedor

### 📊 Interpretación de Resultados: CTR vs Conversion Rate

**Caso Real: Ad A vs Ad B**

```
Métrica              | Ad A    | Ad B    | Ganador
─────────────────────────────────────────────────
Click-Through Rate   | 4.6%    | 3.7%    | Ad A ✓
Conversion Rate      | 8.27%   | 5.25%   | Ad B ✓✓✓
Total Conversions    | 142     | 98      | Ad B ✓✓
Cost Per Conversion  | $68     | $85     | Ad A ✓

GANADOR FINAL: Ad B
RAZÓN: Conversion rate es MÁS importante que CTR
```

**¿Por Qué Ad B es Ganador Pese a CTR Más Bajo?**

```
Ad A (CTR Alto, Conv Rate Baja):
├─ Muchísimas personas hacen clic
├─ Pero pocos se convierten
└─ El anuncio "engaña" al usuario → Baja calidad

Ad B (CTR Bajo, Conv Rate Alta):
├─ Menos clics pero más selectivos
├─ Más personas que hacen clic se convierten
└─ El anuncio "promete y entrega" → Alta calidad
```

### 🔄 Proceso Completo de Split Testing

#### Paso 1: Revisar Ads Actuales

```
Search Campaign
        ↓
Ad Groups
        ↓
Seleccionar Ad Group
        ↓
Ads & Extensions
        ↓
Revisar tabla con métricas
```

**Columnas a Agregar:**
```
□ Clicks
□ Impressions
□ CTR
□ Conversions
□ Conversion Rate
□ Cost
□ Cost Per Conversion
```

#### Paso 2: Identificar Ganador

Usar esta jerarquía:

```
1. MIRA: Conversion Rate (La métrica más importante)
        ↓
2. LUEGO: Cost Per Conversion (Eficiencia)
        ↓
3. LUEGO: Total Conversions (Volumen)
        ↓
4. SOLO COMO REFERENCIA: CTR (Relevancia, no rentabilidad)

GANADOR = El con mejor Conversion Rate + Mejor CPC
```

#### Paso 3: Pausar Anuncio Perdedor

```
Ad Group
        ↓
Ads & Extensions
        ↓
Seleccionar ad perdedor
        ↓
Click "Pause"
        ↓
Confirmar
```

#### Paso 4: Duplicar Anuncio Ganador

```
Ad Group
        ↓
Ads & Extensions
        ↓
Seleccionar ad ganador
        ↓
Click 3 dots menú
        ↓
Click "Copy"
```

#### Paso 5: Crear Variante con UN Cambio

**Lo que NO cambies:**
```
✅ Mantén el resto del copy igual
✅ Mantén la estructura igual
✅ Mantén el landing page link igual
```

**Lo que SÍ cambies (UNA SOLA COSA):**

| Elemento | Ejemplo Antes | Ejemplo Después |
|----------|--------------|-----------------|
| **CTA principal** | "Learn More" | "Get Started Free" |
| **Headline pinned** | #1 posición | #2 posición |
| **Unique selling point** | "Trusted by 10,000+" | "Free Demo Available" |
| **Tone** | Formal | Casual |
| **Beneficio enfatizado** | Price | Speed |

**Caso Real de Eduardo:**
```
Paso 1: Ad A tenía CTA "Learn More" pinned en posición #1
        └─ Resultado: Buen conversion rate

Paso 2: Pausa Ad A (el perdedor de primer test)

Paso 3: Duplica Ad A y crea Ad B

Paso 4: En Ad B, cambia:
        └─ CTA a "Get Free Demo" (Unique Selling Point)
        └─ Pin position a #2

Paso 5: Run nuevo split test (Ad B ganador vs Ad C nuevo)
```

#### Paso 6: Pegar Duplicado

```
Copy realizado
        ↓
Volver a Ad Group
        ↓
Click "+ Ad"
        ↓
Click "Paste"
        ↓
Seleccionar: "If ad already exists, create the duplicate"
        ↓
Paste
```

#### Paso 7: Hacer Cambio Único

```
Nuevo ad abierto
        ↓
Editar UNA sola cosa
        ↓
Save Ad
        ↓
Ahora tienes: Ad ganador original vs Ad nuevo con 1 cambio
```

### 📊 Monitoreo Durante el Test

**Frecuencia de Revisión:**
```
Semana 1-2: Revisar 1x por semana (reunir datos)
Semana 3-4: Revisar 2x por semana (confirmar tendencia)
Semana 4+: Revisar 1x por semana (consolidar datos)

NO REVISES DIARIAMENTE - Los datos son muy variables
```

**Tabla de Seguimiento (Ejemplo):**

| Semana | Ad A Clicks | Ad B Clicks | Ad A Conv | Ad B Conv | Trending |
|--------|------------|------------|-----------|-----------|----------|
| 1 | 156 | 148 | 12 | 11 | Tied |
| 2 | 162 | 175 | 13 | 15 | B Slight Lead |
| 3 | 148 | 189 | 12 | 18 | B Clear Lead |
| 4 | 144 | 202 | 11 | 22 | **B Winner** |

**Decisión en Semana 4:**
```
Ad A: 4.6% conversion rate (43 conversiones / 936 clicks)
Ad B: 5.4% conversion rate (66 conversiones / 1,214 clicks)

DECISIÓN: Pausar Ad A, mantener Ad B activo, crear Ad C
```

### ❌ Errores Comunes en Split Testing

| Error | Por Qué es Malo | Solución |
|-------|-----------------|----------|
| Cambiar múltiples elementos | No sabes cuál causó el cambio | Cambiar UNA sola cosa |
| Decidir ganador en semana 1-2 | Datos insuficientes | Esperar 30 días mínimo |
| Basarse solo en CTR | CTR alto ≠ conversiones | Priorizar conversion rate |
| No pausar al perdedor | Sigues gastando en ads malos | Pausar inmediatamente |
| Crear tests sin conversiones | No puedes medir éxito | Asegurar al menos 1-2 conv/día |

---

## 💰 Campaign Bidding Review: La Guía Definitiva

### 🚨 La Advertencia de Eduardo

> **"Adding a target ROAS or target CPA too early can actually be a brake or limiting part for your campaign."**

La puja inteligente es poderosa pero peligrosa sin datos suficientes. Esta es la sección más crítica del documento.

### ❌ El Error #1: Smart Bidding Demasiado Temprano

```
Escenario Incorrecto (NUNCA HAGAS ESTO):

├─ Día 1: Lanzas campaña
├─ Día 5: Google recomienda "Maximize Conversions"
├─ Día 6: ACEPTAS la recomendación ← ❌ ERROR CRÍTICO
├─ Día 7-14: Campaign desmorona
│          - Google no tiene datos para optimizar
│          - Pujas aleatorias sin patrón
│          - CPC sube dramáticamente
│          - Conversiones bajan
└─ Resultado: Presupuesto desperdiciado

COSTO: Potencialmente $1,000+ en gasto inútil
```

### ✅ Requisito #1: 30 Conversiones en 30 Días

**Conversiones REALES, no cualquier evento:**

```
❌ NO CONTAR COMO CONVERSIÓN:
├─ Add to cart
├─ Lead form incompleto
├─ Click en "Learn More"
├─ Descarga de guía gratuita
└─ Cualquier acción que no genere revenue/leads

✅ CONTAR COMO CONVERSIÓN:
├─ Compra completada
├─ Lead completo que se puede vender
├─ Booking/reserva confirmada
├─ Call completado
└─ Acción que genera ingresos o clientes viables
```

**Regla de Oro:**
```
Necesitas: 30 conversiones primarias en los últimos 30 días
Matemática: ~1 conversión por día mínimo
Período: Últimos 30 días consecutivos
```

### ✅ Requisito #2: Conversiones Estables y Crecientes

**Patrón Bueno:**

```
Semana 1: 6 conversiones ✓
Semana 2: 7 conversiones ✓
Semana 3: 8 conversiones ✓
Semana 4: 9 conversiones ✓

TOTAL: 30 conversiones
PATRÓN: Creciente y consistente
CONCLUSIÓN: Listo para smart bidding
```

**Patrón Malo:**

```
Semana 1: 5 conversiones
Semana 2: 15 conversiones (pico)
Semana 3: 2 conversiones (caída)
Semana 4: 8 conversiones
Semana 5: 0 conversiones

TOTAL: 30 conversiones pero INCONSISTENT
PATRÓN: Errático
CONCLUSIÓN: NO LISTO para smart bidding

¿POR QUÉ? Google no puede aprender de un patrón inconsistente
```

### ✅ Requisito #3: Esperar 90+ Días (Preferiblemente 6 Meses)

**La Línea de Tiempo Recomendada:**

```
Día 1-30: Campaña en Maximize Clicks
└─ Reunir datos iniciales
└─ Entender audience
└─ Validar conversión tracking

Día 30-60: Revisar datos, optimizar manualmente
└─ Mejorar Quality Score
└─ Mejorar CTR
└─ Refinar keywords

Día 60-90: Esperar a requisito de 30 conversiones
└─ Hacer 30+ conversiones consistentes
└─ Preparar data para smart bidding

Día 90+: AHORA puedes considerar Target CPA/ROAS
└─ PERO solo si se cumplen los requisitos

RECOMENDACIÓN IDEAL: 6 meses antes de Target ROAS/CPA
```

### 📊 Análisis de Datos: Cuándo NO Cambiar Bidding

**Escenario 1: Aumento en Conversion Value Cada Semana**

```
DATOS:
Semana 1: Conversion Value = $4,200
Semana 2: Conversion Value = $4,800 (↑ +14%)
Semana 3: Conversion Value = $5,100 (↑ +6%)
Semana 4: Conversion Value = $5,600 (↑ +10%)

CONCLUSIÓN: 🚫 NO CAMBIES BIDDING

RAZÓN: La campaña está en fase de SCALING
- Conversion value sigue subiendo
- ROAS está mejorando naturalmente
- Agregar Target ROAS LIMITARÍA el crecimiento
```

**Escenario 2: Estás Aumentando Presupuesto**

```
DATOS:
├─ Budget Mes Anterior: $5,000/día
├─ Budget Este Mes: $6,500/día (↑ +30%)
├─ Conversiones: Aumentando semana a semana
├─ ROAS: Fluctuando (normal durante scaling)
└─ Cost Per Conversion: Fluctuando

CONCLUSIÓN: 🚫 NO CAMBIES BIDDING

RAZÓN: Cuando aumentas presupuesto:
- Impactas el equilibrio del algoritmo
- Agregación de Target CPA/ROAS creará conflicto
- Espera 4-6 semanas después de cambio de presupuesto
```

### 📊 Análisis de Datos: Cuándo SÍ PUEDES Cambiar Bidding

**Requisitos Cumplidos:**

```
✅ 30+ conversiones en últimos 30 días
✅ Conversiones estables (no fluctúan wildly)
✅ Sin cambios recientes de presupuesto
✅ Sin cambios recientes de landing pages
✅ Quality Score estable o mejorando
✅ CTR estable o mejorando
✅ Conversion Rate estable o mejorando
```

**Indicador Visual de "Listo":**

```
Semana 1: 8 conversiones | 2.1% conv rate | $58 CPA
Semana 2: 7 conversiones | 2.0% conv rate | $60 CPA
Semana 3: 8 conversiones | 2.2% conv rate | $57 CPA
Semana 4: 9 conversiones | 2.1% conv rate | $58 CPA

PATRÓN: Flatline nice and stable (±5% variación)
CONCLUSIÓN: ✅ LISTO para Target CPA/ROAS
```

### 📊 Caso de Estudio 1: Performance Max con Scaling Budget

**Situación:**
- Campaign Type: Performance Max
- Current Bidding: Maximize Conversion Value (automático)
- Google Recommendation: Add Target ROAS

**Datos Semanales:**

| Semana | Conversions | Conversion Value | ROAS | Impressions | Cost |
|--------|-------------|------------------|------|-------------|------|
| 1 | 21 | $4,200 | 2.1x | 12,400 | $2,000 |
| 2 | 24 | $4,800 | 2.4x | 13,200 | $2,000 |
| 3 | 28 | $5,100 | 2.55x | 14,800 | $2,000 |
| 4 | 31 | $5,600 | 2.8x | 16,200 | $2,000 |

**Análisis:**

```
POSITIVO:
✅ Conversions creciendo semana a semana
✅ Conversion value aumentando constantemente
✅ ROAS mejorando (2.1x → 2.8x)
✅ Impresiones aumentando (algoritmo encontró good spots)

PROBLEMAS:
❌ Aún estamos en fase SCALING (v value sube cada semana)
❌ ROAS no es "flatline", está mejorando
❌ Si añades Target ROAS ahora, LIMITARÍAS el crecimiento

DECISIÓN: 🚫 NO AGREGAR TARGET ROAS TODAVÍA
ESPERAR: Hasta que Conversion Value se estabilice
RAZÓN: Queremos que siga creciendo sin límites
```

### 📊 Caso de Estudio 2: Tracking Issue Corregido

**Situación:**
- Account: Performance Max, tenía Target ROAS
- Problem: Tracking issue (over-reporting de 2x)
- Action: Se removió Target ROAS, se corrigió tracking

**Datos Antes y Después:**

```
ANTES (Con sobre-tracking):
Semana 1: Conversions = 45 (pero realmente 22.5)
Semana 2: Conversions = 52 (pero realmente 26)
Semana 3: Conversions = 48 (pero realmente 24)

DESPUÉS (Tracking corregido):
Semana 1: Conversions = 22 ✓
Semana 2: Conversiones = 26 ✓
Semana 3: Conversions = 0 (anomalía)
Semana 4: Conversions = 24 ✓

¿POR QUÉ SEMANA 3 = 0?
└─ Posible cambio en landing page o form
└─ Posible problema técnico
└─ Necesita investigación
```

**Action Taken:**

```
1. Removieron Target ROAS (que estaba limitando)
2. Bajaron Target ROAS de $800 a $500 como test
3. Resultado: Impresiones aumentaron inmediatamente

Gráfico de Impressiones:
Semana 1: 8,200 impresiones
Semana 2: 8,400 impresiones
Semana 3 (Target bajado de 800→500): 12,300 impresiones ⬆️
Semana 4: 12,100 impresiones
```

**Conclusión:**
```
❌ Target ROAS alto ESTABA actuando como freno
✅ Cuando bajaron el target, algoritmo pudo escalar
⚠️ PERO: No recomendable tener Target ROAS sin datos estables
```

### 🎯 Search & Shopping Campaigns: Target CPA por Ad Group

**Contexto Especial:**
- En Search/Shopping, Target CPA se configura a nivel **Ad Group**, no campaign
- Cada Ad Group puede tener diferente Target CPA
- Permite optimización granular

**Proceso:**

```
Search Campaign
        ↓
Ad Groups
        ↓
Seleccionar cada Ad Group
        ↓
Campaign Settings → Bidding
        ↓
Configurar Target CPA individual
```

**Ejemplo de Tabla de Revisión (Últimos 30 días):**

| Ad Group | Target CPA | Actual CPA | Conversions | Status |
|----------|-----------|-----------|-------------|--------|
| "Divorce Services" | $60 | $58 | 14 | ✅ GOOD |
| "Family Law" | $55 | $54 | 9 | ✅ GOOD |
| "Bankruptcy" | $75 | $76 | 6 | ⚠️ SLIGHTLY HIGH |
| "General Consultation" | $50 | $61 | 3 | ❌ NEEDS ADJUST |

**Criterios de Ajuste:**

```
✅ MANTENER TARGET si:
├─ Actual CPA es ±5% del Target CPA
├─ Actual CPA es más BAJO que Target
└─ Conversiones son consistentes

⚠️ REVISAR DESPUÉS SI:
├─ Actual CPA es +5% a +15% del Target
├─ Pero conversiones están bajando
└─ Esperar 2 semanas más de datos

❌ REDUCIR TARGET CPA si:
├─ Actual CPA es consistentemente 20%+ más que Target
├─ Conversiones están bajando
├─ Has tenido 4+ semanas de este patrón
└─ Ejemplo: Target $60, pero gastando $75+
```

### 📋 La Regla de Eduardo: Never Rush Smart Bidding

```
🚫 NUNCA:
├─ Agregues Target CPA en primeros 30 días
├─ Agregues Target ROAS sin 30+ conversiones
├─ Cambies bids mientras aumentas presupuesto
├─ Ignores Google's recomendaciones pero tampoco ciegamente las sigas
└─ Agregues múltiples estrategias a la vez

✅ SIEMPRE:
├─ Espera 90+ días (idealmente 6 meses)
├─ Valida que tengas 30 conversiones consistentes
├─ Revisa cada 4-6 semanas, no diariamente
├─ Documenta cambios para poder revertir si algo sale mal
├─ Tiene un plan B si bidding strategy falla
└─ Mantén vigilancia semanal de métricas clave
```

### 🔍 Monitoreo Semanal de Bidding (15 minutos)

**Qué Revisar:**

```
PASO 1 (5 min): Métricas Generales
├─ Conversions: ¿Aumentando o disminuyendo?
├─ CPA/ROAS: ¿Mejorando o empeorando?
└─ Impressions: ¿Estable o hay caídas dramáticas?

PASO 2 (5 min): Comparación Semanal
├─ Esta semana vs semana anterior
├─ Busca caídas repentinas (>20% caída es roja flag)
└─ Busca crecimiento consistente

PASO 3 (5 min): Documentación
├─ Nota cualquier anomalía
├─ Mantén spreadsheet con datos históricos
└─ Prepara acciones para próxima revisión
```

**Tabla de Monitoreo Semanal:**

| Métrica | Semana 1 | Semana 2 | Semana 3 | Trend | Alert |
|---------|----------|----------|----------|-------|-------|
| Conversions | 28 | 29 | 31 | ↑ Positive | ✅ |
| Avg CPA | $62 | $61 | $58 | ↓ Improving | ✅ |
| Impressions | 9,200 | 9,400 | 9,600 | ↑ Growing | ✅ |
| CTR | 3.2% | 3.3% | 3.4% | ↑ Improving | ✅ |

### 🚨 Red Flags: Cuándo Actuar Inmediatamente

| Red Flag | Significa | Acción |
|----------|-----------|--------|
| **Caída >30% conversiones en 1 semana** | Problema grave | Revisar campaign, landing page, tracking |
| **CPA aumentó 40%+ sin cambios** | Posible tracking issue | Validar conversion tracking |
| **Impressions caída 50%+ repentina** | Posible cambio algoritmo o budget | Revisar budget settings, bids |
| **Quality Score bajó múltiples puntos** | Ads menos relevantes | Revisar CTR, landing page, ad copy |

---

## 📈 Resumen de Acciones Prioritarias

### Matriz de Urgencia

| Acción | Frecuencia | Urgencia | Impacto |
|--------|-----------|----------|---------|
| **Revisar Search Terms** | Semanal | 🔴 Alta | Muy Alto |
| **Revisar Auction Insights** | Mensual | 🟠 Media | Medio |
| **Review de Split Tests** | Semanal | 🔴 Alta | Muy Alto |
| **Validar Bidding Stability** | Semanal | 🔴 Alta | Muy Alto |
| **Monitoreo Target CPA/ROAS** | Semanal | 🔴 Alta | Alto |

### Rutina Semanal Recomendada (60 minutos)

```
LUNES (15 min):
├─ Revisar Search Terms Report
├─ Agregar 2-3 términos de alto rendimiento como keywords
└─ Excluir 2-3 términos de bajo rendimiento

MIÉRCOLES (15 min):
├─ Revisar split test ads
├─ Analizar conversion rate vs CTR
└─ Documentar tendencias

VIERNES (15 min):
├─ Revisar métricas de bidding
├─ Validar conversiones estables
├─ Revisar cualquier cambio en CPC/CPA
└─ Documentar en spreadsheet

MENSUAL (15 min extra):
└─ Revisar Auction Insights para detectar cambios competitivos
```

### Rutina Mensual (30 minutos)

```
1. Audit Completo de Search Terms (últimos 30 días)
2. Revisar Auction Insights para cambios competitivos
3. Análisis de Split Tests finalizados
4. Revisión de Target CPA por Ad Group
5. Documentación de todas las acciones
6. Planificación para próximo mes
```

### Rutina Trimestral (60 minutos)

```
1. Análisis profundo de todas las métricas
2. Revisión de cambios de bidding strategy
3. Evaluación de cumplimiento de requisitos para smart bidding
4. Planificación de cambios estratégicos
5. Revisión de decisiones de puja previas
6. Optimización de estructura de campañas
```

---

## 🎓 Notas Importantes y Takeaways

### 1. **Data Over Google's Recommendations**
Google constantemente recomienda smart bidding, pero tú necesitas validar que tienes suficientes datos. No sigas ciegamente sus recomendaciones.

### 2. **Smart Bidding es Poderoso pero Peligroso**
```
Con datos correctos: +30-50% de ROI
Sin datos suficientes: -40-60% de ROI

El riesgo es MUCHO mayor que la recompensa sin datos
```

### 3. **Search Terms son Tu Mina de Oro**
Los términos que encuentres en tu Search Terms Report son conversiones futuras esperando ser agregadas. Revisalos SEMANALMENTE.

### 4. **Auction Insights es Diagnóstico, No Prescripción**
```
NO es para cambiar bids inmediatamente
SÍ es para ENTENDER por qué tus costos cambian
```

### 5. **Split Testing es Un Proceso Continuo**
```
Semana 1-30: Test 1
Semana 30-60: Test 2 (basado en aprendizajes)
Semana 60-90: Test 3 (basado en aprendizajes)
...
Mejora continua sin fin
```

### 6. **Target CPA/ROAS = Límite de Performance**
Una vez estableces Target CPA de $50, Google NUNCA gastará menos para alcanzar esa meta. Es un piso, no un objetivo.

```
❌ INCORRECTO: "Quiero Target CPA de $50"
✅ CORRECTO: "Estoy listo para Target CPA cuando tenga datos consistentes"
```

### 7. **Conversiones Errátil = Espera Más Tiempo**
```
Si conversiones saltan de 2 → 18 → 5 → 12
├─ NO agregues Target CPA
├─ NO cambies bidding
└─ ESPERA hasta que sea más consistente
```

### 8. **Budget Scaling = Pausa Smart Bidding**
Cuando aumentas presupuesto 25%+, espera 4-6 semanas antes de tocar estrategia de puja.

---

## 🚀 Próximos Pasos

### Esta Semana

```
1. Accede a tu Search Campaign
2. Abre Search Terms Report
3. Identifica 3-5 términos de alto rendimiento
4. Agrega esos términos como nuevas keywords (Exact match)
5. Identifica 2-3 términos con alto costo/cero conversiones
6. Agrega esos como negative keywords

TIEMPO: 20 minutos
```

### Próximas 2 Semanas

```
1. Revisa tus split tests actuales
2. Reúne datos de 2+ semanas
3. Determina ganador basado en conversion rate
4. Pausa al perdedor
5. Duplica al ganador
6. Crea nuevo test con UN cambio único

TIEMPO: 30 minutos
```

### Este Mes

```
1. Revisa Auction Insights mensual
2. Compara vs mes anterior
3. Identifica nuevos competidores o cambios
4. Revisa tu Impression Share
5. Documenta hallazgos

TIEMPO: 20 minutos
```

### Próximos 90 Días (Si aplica)

```
Si tienes 30+ conversiones consistentes:
├─ Valida que cumples todos los requisitos
├─ Prepara datos para smart bidding
├─ Documenta baseline actual
├─ Planifica implementación cuidadosa
└─ Establece monitoreo muy frecuente

Si todavía NO tienes:
├─ Sigue optimizando manualmente
├─ Mejora Quality Score
├─ Mejora CTR
├─ Continúa con split testing
└─ Reconsidera en 30 días más
```

---

## 📊 Plantillas para Descargar

### Plantilla 1: Search Terms Audit Log

```
Fecha: _______________
Campaña: _______________

TÉRMINOS AGREGADOS COMO KEYWORDS:
├─ Término 1: ____________ (Match Type: ____)
├─ Término 2: ____________ (Match Type: ____)
└─ Término 3: ____________ (Match Type: ____)

TÉRMINOS AGREGADOS COMO NEGATIVES:
├─ Término 1: ____________ (Level: ____ )
├─ Término 2: ____________ (Level: ____ )
└─ Término 3: ____________ (Level: ____ )

OBSERVACIONES:
_____________________________________
_____________________________________
```

### Plantilla 2: Split Test Tracking

```
TEST #: ___
Campaña: _______________
Ad Group: _______________

AD A (Ganador Anterior):
├─ Cambio previo: _______________
├─ CTR: ____%
├─ Conv Rate: ____%
└─ Conversions: ____

AD B (Nuevo):
├─ Cambio único: _______________
├─ CTR: ____%
├─ Conv Rate: ____%
└─ Conversions: ____

GANADOR: ___ | RAZÓN: ___________
PRÓXIMO TEST: _______________
```

### Plantilla 3: Bidding Stability Check

```
SEMANA: ____________
Campaña: _______________

CONVERSIONES:
├─ Semana 1: ____ | Semana 2: ____ | Semana 3: ____ | Semana 4: ____
└─ Trend: ________

CPA/ROAS:
├─ Semana 1: ____ | Semana 2: ____ | Semana 3: ____ | Semana 4: ____
└─ Trend: ________

IMPRESSIONS:
├─ Semana 1: ____ | Semana 2: ____ | Semana 3: ____ | Semana 4: ____
└─ Trend: ________

¿LISTO PARA SMART BIDDING?
├─ 30+ conversiones: [ ] SÍ [ ] NO
├─ Conversiones estables: [ ] SÍ [ ] NO
├─ 90+ días de campaña: [ ] SÍ [ ] NO
└─ Decisión: _________________
```

---

**Versión Final: Markdown Ultradetallado de Máximo Valor**  
*Creado a partir de transcripción de Eduardo Luna (25 minutos)*  
*Optimizado para implementación inmediata*  
*Última actualización: 24/11/2025*
