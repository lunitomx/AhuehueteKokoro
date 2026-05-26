# Checklist de Optimización — Cuentas Basadas en Servicios

**Fuente:** Service Based Checklist (Google Ads)
**Aplicación:** Cuentas de servicios con campañas Search, Performance Max y Display

---

## Ritmo de optimización

Este checklist define QUÉ revisar y CON QUÉ FRECUENCIA. El ritmo es el contrato — no se adelanta, no se omite.

| Frecuencia | Qué abarca |
|------------|------------|
| Cada 72 horas | Negativos urgentes (Search Terms) |
| Semanal | Audiencias, términos positivos, recomendaciones, presupuesto |
| Mensual | Anuncios, Quality Score, conversiones, ubicaciones |
| Cada 90 días | Bidding strategy, segmentación de campañas, landing pages |

---

## 1. Pestaña Insights

### Cada 72 horas
- **Search Term Insights** → agregar palabras negativas para detener búsquedas no relacionadas *(Search)*

### Semanal
- **Search Term Insights** → agregar términos que convierten como [exact match] *(Search)*
- **Search Term Insights** → agregar términos que convierten al audience signal del asset group correspondiente *(P.Max)*
- **Audience Insights** → agregar audiencias con conversiones a la campaña/ad group *(Search & Display)*
- **Audience Insights** → revisar audiencias con alto gasto y sin conversiones *(Display)*
- **Audience Insights** → agregar audiencias con conversiones al asset group correspondiente *(P.Max)*
- **"Where ads showed"** → excluir apps o sitios web con alto gasto y sin conversiones *(Display)*

---

## 2. Activos de anuncios

### Mensual

**Search:**
- Revisar split test en cada ad group (2 anuncios activos). Con datos suficientes: pausar el de menor CTR y conversiones. Si datos inconcluyentes, dejar correr 30 días más.
- Al tener anuncio ganador: copiarlo y hacer 1 sola variación para iniciar nuevo split test.

**Performance Max:**
- Revisar headlines, descriptions y long descriptions → actualizar los de bajo performance score
- Revisar imágenes → actualizar las de bajo performance score
- Revisar videos → actualizar los de bajo performance score

**Display:**
- Mismo criterio de split test que Search (2 anuncios, pausar el perdedor, iniciar nueva variación)

---

## 3. Quality Score (keywords y anuncios)

### Mensual *(Search)*
- Identificar keywords y anuncios con Quality Score bajo
- Ajustar copy de anuncios para mejorar relevancia de keywords
- Actualizar landing page para mejorar relevancia de keywords

> Referencia: Quality Score White Paper de Google

---

## 4. Estrategia de bidding

### Cada 90 días *(Search & P.Max)*

**Regla base:** No usar Max Conversions ni Max Conversion Value hasta tener 30 conversiones en 30 días.

**Con Target CPA (Max Conversions):**
- Revisar Cost/Conv de los últimos 90, 60 y 30 días
- Si mejora y la varianza semanal de los últimos 4 weeks es <20% → actualizar el Target CPA

**Con Target ROAS (Max Conversion Value):**
- Revisar ROAS real de los últimos 90, 60 y 30 días
- Si mejora y la varianza semanal de los últimos 4 weeks es <20% → actualizar el Target ROAS

**Principio:** Quieres datos de conversión semanales estables antes de tocar los targets. Cambiar estrategia cada semana es como arrancar la planta para ver si creció.

---

## 5. Segmentación y distribución de presupuesto

### Mensual
- ¿Alguna campaña de alto rendimiento está limitada por presupuesto? *(Search, P.Max & Display)*

### Cada 90 días *(Search, P.Max & Display)*
- ¿Se necesitan campañas adicionales para segmentar mejor por categoría de servicio, volumen de tráfico o ubicación?
- El criterio: separar en campaña propia cuando quieres darle más presupuesto a un servicio/tema/ubicación específica que produce mejores resultados de forma independiente.

---

## 6. Acciones de conversión

### Mensual *(Search, P.Max & Display)*
- Verificar que todas las acciones de conversión están activas y funcionando
- Si se rastrean llamadas telefónicas: revisar el reporte de call extensions *(Search & P.Max)*

---

## 7. Segmentación geográfica

### Mensual
- Identificar búsquedas desde ubicaciones no objetivo → excluirlas *(Search & P.Max)*
- Revisar rendimiento por ubicación y agregar bid optimizations si aplica *(Search & Display)*

---

## 8. Landing page

### Mensual
- ¿Hay landing pages irrelevantes que Google está usando? → excluirlas *(P.Max)*

### Cada 90 días *(Search, P.Max & Display)*
- ¿La página tiene una oferta clara y un call to action?
- ¿La landing es relevante para los search terms? (revisar "Ad Relevance" score) *(Search)*
- ¿La página incluye marcadores de credibilidad: testimonios, reseñas?

---

## 9. Pestaña Recommendations

### Semanal *(Search, P.Max & Display)*
- Revisar recomendaciones generadas por el sistema → implementar o rechazar (nunca ignorar)

---

## 10. Control de calidad

### Semanal
- Verificar pacing del presupuesto (budget pacing checks)

### Mensual
- Revisar pagos y presupuestos de cuenta (payment & account budgets)

---

## Resumen de ritmo por tipo de campaña

| Tarea | Search | P.Max | Display | Frecuencia |
|-------|--------|-------|---------|------------|
| Negativos urgentes | ✅ | — | — | 72h |
| Keywords positivas exactas | ✅ | — | — | Semanal |
| Audience signal PMax | — | ✅ | — | Semanal |
| Audiencias con conversiones | ✅ | — | ✅ | Semanal |
| Exclusión apps/sitios (Display) | — | — | ✅ | Semanal |
| Recommendations tab | ✅ | ✅ | ✅ | Semanal |
| Budget pacing | ✅ | ✅ | ✅ | Semanal |
| Split test anuncios | ✅ | — | ✅ | Mensual |
| Assets PMax | — | ✅ | — | Mensual |
| Quality Score | ✅ | — | — | Mensual |
| Conversiones activas | ✅ | ✅ | ✅ | Mensual |
| Segmentación geográfica | ✅ | ✅ | ✅ | Mensual |
| Landing pages irrelevantes | — | ✅ | — | Mensual |
| Presupuesto de cuenta | ✅ | ✅ | ✅ | Mensual |
| Bidding strategy review | ✅ | ✅ | — | 90 días |
| Segmentación de campañas | ✅ | ✅ | ✅ | 90 días |
| Landing page calidad | ✅ | ✅ | ✅ | 90 días |
