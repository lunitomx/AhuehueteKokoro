# Optimiza Tus Campañas de Búsqueda

**Facilitador:** Eduardo Luna  
**Fecha:** 24/11/2025  
**Duración:** 22 minutos

---

## 1. Segmentación de Audiencias y Bid Adjustments

### Objetivo
Identificar y aprovechar audiencias de alto rendimiento mientras se excluyen las que generan alto gasto sin conversiones

### Cómo Configurar Audiencias

#### Paso 1: Agregar Audiencias
`Ad Groups` → `Audiences` → `Click Edit` → Agregar audiencias

#### Paso 2: Configurar Bid Adjustments
Ajustar pujas por audiencia según su rendimiento

### Cuándo Usar Bid Adjustments

⚠️ **Importante:** Los bid adjustments funcionan en estrategias como:
- ✅ Maximize Clicks
- ✅ Maximize Impression Share
- ❌ NO funcionan en estrategias de puja por conversión (pero igual mantenerlos)

### Casos de Uso

#### Audiencias de Alto Rendimiento
- Aumentar bid adjustment
- Registrar datos para futuros campaigns de Performance Max o Display

#### Audiencias de Bajo Rendimiento
- Buscar: Alto gasto + CERO conversiones (durante período largo)
- Solución: Excluir como audiencia específica

---

## 2. Split Testing de Anuncios

### Principios Clave

📋 **Regla de Oro:** Probar UNA SOLA COSA a la vez

No cambies múltiples elementos simultáneamente. Modifica:
- Un titular
- Un call to action
- Una descripción

### Período de Revisión

- **Revisión:** Cada 30 días
- **Impresiones mínimas:** Mínimo 500 impresiones por anuncio
- **Flexibilidad:** Si no hay resultados conclusivos, continúa el test

### Métricas a Comparar

| Métrica | Importancia | Nota |
|---------|-------------|------|
| Click-Through Rate (CTR) | Alta | Indicador de relevancia |
| Conversion Rate | Muy Alta | La métrica definitiva |
| Cost Per Conversion (CPC) | Muy Alta | Supera al CTR en decisiones finales |

### Proceso de Decisión

⚠️ **Caso Real:** Un anuncio puede tener CTR superior pero CPC peor
- **Decisión:** Mantener el anuncio con mejor CPC aunque CTR sea más bajo
- **Razón:** Conversiones > Clics

### Ejemplo de Split Test Exitoso

📊 **Escenario:** 4 meses de testing

| Fecha | Ad A (CTR) | Ad B (CTR) | Ad A (CPC) | Ad B (CPC) | Ganador |
|-------|-----------|-----------|-----------|-----------|---------|
| Mes 1 | 18% | 15% | $65 | $58 | Incierto |
| Mes 2 | 19% | 16% | $62 | $55 | Incierto |
| Mes 3 | 21% | 18% | $59 | $52 | B empieza a ganar |
| Mes 4 | 22% | 20% | $58 | $48 | **B definitivamente** |

→ **Resultado:** Pausar Ad A, mantener Ad B

### Elementos a Testear

#### Call to Action (CTA)
- ❌ "Request Free Demo" → $54/conversión
- ✅ "Get Free Demo" → $48/conversión (ganador)

#### Encabezados Dinámicos
- Probar: Dynamic Keyword Insertion
- Luego: Encabezados fijos alternativos

---

## 3. Quality Score: Palabras Clave y Anuncios

### Importancia del Quality Score

📊 **Jerarquía de prioridades:**

| Fase de Campaña | Prioridad 1 | Prioridad 2 | Prioridad 3 |
|-----------------|-------------|-------------|-------------|
| Nueva | Quality Score | Ad Strength | CTR |
| Establecida | CTR | Conversion Rate | Quality Score |

### Estándares de Quality Score

✅ **Objetivo mínimo:** Quality Score de 5
- Una vez alcanzado, enfocarse en **CTR > 10%**
- Ideal: Quality Score 7-10

❌ **Riesgo:** Quality Score 1-3
- Acción inmediata requerida

### Auditoría de Quality Score

#### Paso 1: Configurar Columnas
`Campaigns` → `Ad Groups` → `Search Keywords`
1. Agregar columna "Quality Score"
2. Ordenar por Impresiones
3. Revisar top 10 con bajo score

#### Paso 2: Diagnóstico
Si encuentras keywords con QS bajo:

**Revisar:**
- 📝 Ad Copy (titular y descripción relevante)
- 🌐 Landing Page (contiene palabras clave)
- 🔗 Relevancia general

#### Paso 3: Plan de Mejora

**Opción A (Rápida):** Mejorar Ad Copy
1. Agregar keyword al titular
2. Agregar keyword a descripción
3. Revisar cambios en 30 días

**Opción B (Si A no funciona):** Actualizar Landing Page
1. Asegurar que landing contiene keyword
2. Revisar relevancia del contenido

**Opción C (Si B no funciona):** Crear Ad Group Separado
1. Crear grupo específico para esa keyword
2. Ads y landing page 100% relevantes

### Ejemplo de Mejora

❌ **Antes:**
- Keyword: "Club Membership Management Software"
- Titular: Genérico
- Descripción: Vacía
- Landing Page: Sin mención de "club membership"
- Result: Quality Score = 1

✅ **Después:**
1. Agregar "Club Membership Management" al titular
2. Descripción: "Contact us today for a free demo of our club management system"
3. Actualizar landing page si es necesario
4. Result esperado: Quality Score ≥ 5

### Ad Strength (Fortaleza del Anuncio)

⚠️ **Nota:** Similar al Quality Score, Ad Strength importa más en campañas nuevas

- **Nueva campaña:** Mejorar Ad Strength es importante
- **Campaña establecida:** CTR y Conversion Rate > Ad Strength Score

---

## 4. Estrategias de Puja (Bidding Strategies)

### Regla Crítica

⏰ **Revisar solo cada 90 días**

⚠️ **Problema común:** Ajustar estrategias de puja demasiado frecuentemente
- Esto genera volatilidad
- Impide ver resultados reales

### Cómo Revisar Target CPA

#### Paso 1: Verificar Target CPA Actual
`Campaigns` → Ver Target CPA establecido

Comparar:
- Target CPA vs. Actual CPC (Cost Per Conversion)
- Si CPC > Target CPA → ajuste necesario

#### Paso 2: Análisis de Período Largo
**Vista recomendada:** 3 meses
- Cambiar a vista semanal (lunes a domingo)
- Revisar últimas 4-6 semanas

#### Paso 3: Evaluar Estabilidad

| CPC por Semana | Interpretación | Acción |
|---|---|---|
| $25, $27, $26, $28 | Estable | Mantener Target CPA |
| $30, $56, $31, $99 | Inestable | No cambiar, esperar datos |
| $45, $38, $42 (trending down) | Mejorando | Esperar 30 días más |

#### Paso 4: Ajuste de CPA

Si hace ajustes:
1. **Registrar:** Fecha de revisión
2. **Próxima revisión:** 90 días después
3. **No cambiar antes**

### Por Ad Group (Si Aplica)

💡 Si tienes 3-4 Ad Groups en una campaña:
- Cada grupo puede tener diferente Target CPA
- Permitido: Editar CPA por grupo individual
- Común tener variaciones entre grupos

### Señales de Alerta para Cambios

🚨 **Cambia de Target CPA si observas:**
- Descenso consistente de conversiones
- Aumento consistente de CPC (por varias semanas)
- Cambio dramático en impresiones

✅ **NO cambies si observas:**
- Fluctuaciones normales semana a semana
- Datos limitados (menos de 2-3 semanas)
- Estabilidad general (pequeñas variaciones)

---

## Resumen de Acciones Prioritarias

| Acción | Frecuencia | Impacto |
|--------|-----------|--------|
| Revisar Quality Score por palabras clave | Mensual | Alto |
| Split testing de anuncios | Cada 30 días | Muy Alto |
| Configurar audiencias y bid adjustments | Una vez + ajustes | Medio-Alto |
| Revisar estrategia de puja (CPA/ROAS) | Cada 90 días | Muy Alto |
| Monitorear CTR y Conversion Rate | Semanal | Alto |

---

## Notas Importantes

1. **Quality Score ≠ Final:** Un score bajo no significa que dejes el keyword, es una señal para optimizar
2. **CTR vs. Conversion Rate:** CTR es importante para relevancia, pero conversión es lo que importa al final
3. **Split Testing Requiere Paciencia:** 30 días mínimo, pero 4 meses de datos es más confiable
4. **Una Variable a la Vez:** No cambies múltiples elementos en un test simultáneamente
5. **Bidding: Menos es Más:** Deja tiempo (90 días) entre cambios de estrategia de puja
6. **Data over Gut:** Tus números dicen la verdad, no tu intuición
