# Optimizaciones Generales de Cuentas Google Ads

**Facilitador:** Eduardo Luna  
**Fecha:** 24/11/2025  
**Duración:** 20 minutos

---

## 1. Segmentación Mejorada y Asignación de Presupuesto

### Problema Identificado
- Servicios/temas clave con alta tasa de conversión están limitados por presupuesto
- Agrupados con otros temas en la misma campaña pero diferentes grupos de anuncios
- Los grupos de anuncios con mayor gasto consumen todo el presupuesto disponible

### Estrategias de Solución

#### A) Consolidar Grupos de Anuncios Duplicados
Combinar grupos de anuncios que disparan las mismas palabras clave para:
- Evitar "keyword bleeding" (solapamiento de palabras clave)
- Mejorar control sobre pruebas A/B de copias de anuncios
- **Ejemplo:** Combinar "physician licensing" y "Dr licensing" en un solo grupo

#### B) Separar en Campaña Independiente
Crear una campaña separada para un tema/servicio si cumple estas condiciones:

✅ **Requisitos para separar:**
- Tasa de conversión superior a otros grupos
- Share de impresiones de búsqueda BAJO (menos del 10%)
- Rendimiento comparable o mejor con menor gasto
- Budget limitado que no refleja el potencial

📊 **Ejemplo de caso:**
| Métrica | Tema A | Tema B |
|---------|--------|--------|
| Target CPA | $40 | $69 |
| Gasto | $9,800 | $4,200 |
| Conversiones | 141 | 120 |
| Search Impression Share | 65%+ | <10% |

→ **Decisión:** Separar Tema B a su propia campaña para aumentar presupuesto

### Métricas Clave a Revisar
- **Search Impression Share:** Buscar valores bajos para candidatos a separación
- **CPA:** Comparar rendimiento de costos
- **Tasa de Conversión:** Validar que el tema separado convierte mejor

---

## 2. Revisión de Recomendaciones y Optimization Score

### Importancia del Optimization Score

⚠️ **Score ALTO es importante solo al inicio:**
- Cuenta nueva: algo de importancia (datos limitados de Google)
- Cuenta con datos: MENOS importante
- Una vez con datos de conversión y CTR → priorizar estos sobre el score

### Cómo Gestionar Recomendaciones

#### En Dashboard Antiguo
`Recommendations` → Filtrar por relevancia

#### En Dashboard Nuevo
`Campaigns` → `Recommendations`

### Proceso de Revisión Recomendado

1. **Revisar cada recomendación** (actualizadas semanalmente)
2. **Desactivar automáticamente:**
   - Target CPA automático
   - Target ROAS automático
   - Aumento de pujas

   *Razón: Necesitas revisar antes de aplicar para validar CPA/ROAS*

3. **Aceptar selectivamente:**
   - Extensiones (Sitelinks, etc.)
   - Nuevas palabras clave (después de validar)

4. **Descartar automático:**
   - Usar "Dismiss All" para recomendaciones no relevantes
   - Google subirá el score aunque no las apliques

### Gestión Automática de Recomendaciones

⚠️ **AUTO-APPLY FEATURE:** 
- Ubicación: `All Campaigns` → `Recommendations` → Auto-apply settings
- **Desactivar por defecto** porque Google puede cambiar:
  - Target CPA
  - Target ROAS
  - Otros ajustes que necesitas revisar manualmente

### Rutina de Mantenimiento
- **Frecuencia:** Semanal
- **Proceso:** Revisar, aceptar selectivamente o descartar

---

## 3. Revisión de Landing Pages

### Objetivo General
Asegurar que las landing pages generan conversiones satisfactorias y son relevantes

### Estándar de Conversión
- **Campañas de búsqueda (servicios):** >5% tasa de conversión
- **Meta:** Mejora continua, pero 5%+ es aceptable

### Elementos Clave de Landing Page Efectiva

#### 1️⃣ Call to Action (CTA)
- Claro y visible
- Máximo 2 oraciones
- Generar urgencia o motivación

#### 2️⃣ Oferta
- Descuento, bonificación o valor claro
- Elemento de tiempo (ej: countdown timer)
- Debe justificar la conversión

#### 3️⃣ Credibilidad
- Testimonios
- Garantía de devolución de dinero
- Demostración de ser negocio establecido

#### ⚠️ Recomendación
No necesitas landing pages complicadas. Lo simple y directo funciona si tiene los elementos esenciales.

### Auditoría de Landing Pages

#### Paso 1: Revisar Rendimiento
`Campaigns` → `Landing Pages`

**Filtrar por:**
- Costo mayor
- Costo por conversión

**Buscar:**
- ❌ Landing pages con alto costo pero CERO conversiones

#### Paso 2: Excluir Underperformers
Si encuentras páginas que no convierten:

1. Copiar la URL
2. `Campaign Settings` → `Campaign Exclusions` → `Excluded URLs`
3. Pegar URL problemática

**Esto es crítico en Performance Max** porque Google elige automáticamente las landing pages

#### Checklist de Auditoría
- ✅ Landing page tiene oferta clara
- ✅ Relevante al término de búsqueda
- ✅ Markers de credibilidad visibles
- ✅ Sin páginas de alto costo y cero conversiones

---

## Resumen de Acciones Prioritarias

| Acción | Frecuencia | Impacto |
|--------|-----------|--------|
| Revisar recomendaciones | Semanal | Alto |
| Auditar landing pages | Mensual | Alto |
| Validar CPA/ROAS | Semanal | Alto |
| Evaluar segmentación | Trimestral | Muy Alto |
| Aumentar presupuesto a temas ganadores | Según datos | Muy Alto |

---

## Notas Importantes

1. **Data > Optimization Score:** Una vez tengas conversión y CTR, estos son más importantes que el score
2. **Revisión Manual:** No confíes 100% en auto-apply de recomendaciones
3. **Separación de Campañas:** Solo si el tema tiene bajo impression share (<10%) y alto rendimiento
4. **Simplicidad:** Las landing pages efectivas no son necesariamente complicadas
