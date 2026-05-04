# Optimiza Tus Campañas Performance Max

**Facilitador:** Eduardo Luna  
**Fecha:** 24/11/2025  
**Duración:** 19 minutos

---

## 1. Revisión del Tab Insights (Señales de Audiencia)

### Objetivo
Identificar términos de búsqueda y audiencias que convierten para optimizar la campaña

### Por Qué Es Importante
- Google usa estos datos para mejorar el algoritmo
- Proporciona señales de audiencia más precisas
- **Frecuencia:** Revisar SEMANALMENTE

### Diferencia Entre Etiquetas Blue y Green

#### 🔵 Blue Tags (Etiquetas Azules)
- Audience signals que **YA HAS AGREGADO**
- Son sugerencias que proporcionaste
- Google ya las usa para optimizar

#### 🟢 Green Tags (Etiquetas Verdes)
- Audience signals que **NO HAS AGREGADO AÚN**
- Google los descubrió y encontró conversiones
- **ESTOS son los que debes agregar**

### Proceso: Agregar Audiencias que Convierten

#### Paso 1: Identificar Green Tags
`Insights Tab` → Buscar audiencias/términos con conversiones
- Prioridad: Enfocarte en CONVERSIONES, no en impresiones
- Ejemplo: "Mother's Day Flowers" = #2 en conversiones

#### Paso 2: Copiar Señal de Audiencia
1. Copiar el término o audiencia que convierte
2. Tener un bloc de notas abierto para pegar

#### Paso 3: Agregar a Asset Group
1. Ir a `Asset Groups`
2. Seleccionar el asset group más relevante
3. Ir a `Audience Signal` → `Edit`
4. Navegar a `Interest and Detailed Demographics`
5. Pegar la audiencia

#### Paso 4: Guardar
- **"Save"** → Actualiza en ambas campañas si está en multiple
- **"Save as Copy"** → Crea una copia solo en este asset group
- Hacer clic en `Save` nuevamente para confirmar

### Regla Clave
❌ No agregues audiencias por impresiones  
✅ Agrega SOLO las que generan conversiones

---

## 2. Estrategias de Puja (Bidding Strategies)

### Regla Crítica

⏰ **Revisar SOLO cada 90 días**

⚠️ **Razón importante:** Los cambios de bidding strategy toman tiempo para surtir efecto. Cambios muy frecuentes generan volatilidad y datos poco confiables.

### Cuándo Introducir Target CPA/ROAS

#### ⏸️ Requisito Previo: Esperar Suficientes Datos

**Mínimo recomendado:**
- 3 meses de campaña activa ANTES de agregar Target CPA/ROAS
- Tener conversiones consistentes
- Al menos 4 semanas de buen volumen de conversiones

❌ **NO Hagas Esto:**
- Agregar Target CPA con datos erráticos (1 conversión, 0, 6, 1, 11 en semanas alternadas)
- Introducir estrategia antes de 3 meses

✅ **Hazlo Así:**
- Espera 3 meses de datos estables
- Asegúrate de tener conversiones consistentes
- Luego agrega Target CPA/ROAS

### Cómo Revisar Target CPA

#### Paso 1: Recopilar Datos
`Campaigns` → Ver Target CPA actual establecido

Comparar:
- Target CPA vs. Actual Cost Per Conversion
- Rango de fecha: Últimas 4-6 semanas

#### Paso 2: Cambiar a Vista Semanal/Mensual
- Cambiar vista a "Weekly" (lunes a domingo)
- Más fácil ver tendencias en bidding strategies
- Revisar período de 3 meses completo

#### Paso 3: Analizar 4 Métricas Clave

| Métrica | Qué Buscar | Señal |
|---------|-----------|--------|
| **Cost Per Conversion** | Estabilidad consistente | $27, $25, $27, $26 = ✅ |
| **Impressions** | Sin caídas dramáticas | Variación pequeña = ✅ |
| **Conversions** | Volumen consistente | Estable = ✅ |
| **Tendencia General** | CPA bajando sin volatilidad | Mejora sostenida = ✅ |

### Ejemplo Real: Cuándo Sí y Cuándo No Cambiar

#### ✅ CAMBIO RECOMENDADO
```
CPA por semana: $27, $25, $27, $26
Impresiones: Estables
Conversiones: Consistentes
Acción: Ajustar Target CPA está justificado
```

#### ❌ NO CAMBIES
```
CPA por semana: $30, $56, $31, $99
Impresiones: Up/down/up/down
Conversiones: Erráticas
Acción: Espera más estabilidad
```

### Caso de Estudio: Implementación de Target CPA

**Timeline:**
- **Mes 1-3:** Campaña sin Target CPA, CPA baja de $132 → $56 naturalmente
- **Mes 4:** Se introduce Target CPA de $81
  - CPA baja inmediatamente a $45-$28
  - Impresiones: Consistentes
  - Conversiones: Sólidas 4 semanas previas
- **Mes 5-6:** Se ajusta a $28
  - Se espera 4 semanas más antes de cambiar
  - CPA permanece estable en $27-$28 por 6 semanas

**Lección:** La paciencia con datos estables > cambios constantes

### Señales de Alerta

🚨 **NO cambies Target CPA si ves:**
- Fluctuaciones semana a semana (up/down inconsistente)
- Impresiones saltando dramáticamente
- Conversiones erráticas
- Menos de 2 semanas de datos nuevos

✅ **SÍ puedes cambiar si ves:**
- 4+ semanas de CPA consistente por encima/debajo del target
- Impresiones estables
- Conversiones consistentes
- Tendencia clara (bajando o subiendo sostenidamente)

---

## 3. Segmentación de Presupuesto y Escalado

### Objetivo
Identificar asset groups/product lines que deberían tener campañas propias para mejorar ROI

### Cuándo Separar un Asset Group en Su Propia Campaña

#### 🚨 Señal #1: Asset Group "Devorador de Presupuesto"
- Consume >50% del presupuesto de la campaña
- Tiene conversiones bajas o CERO
- Limita el presupuesto de otros asset groups de alto rendimiento

#### 📊 Señal #2: Diferencia de Conversión Value Cost
Asset groups en la misma campaña con ROAS muy diferentes:
- Asset A: 0.5-1 ROAS (bajo rendimiento)
- Asset B: 2.5-3 ROAS (alto rendimiento)
- Asset A consume todos los fondos limitando B

### Beneficios de Separar

#### 1️⃣ Control de Presupuesto Mejorado
- Asset group con bajo ROAS → presupuesto inicial pequeño
- Asset group con alto ROAS → presupuesto para escalar
- Antes no podías hacer esto (estaban mezclados)

#### 2️⃣ Bidding Strategy Independiente
- Cada campaña = Target CPA/ROAS propio
- Optimizar según el rendimiento específico del product line

#### 3️⃣ Escalado Efectivo
- Los asset groups ganadores pueden crecer sin límites
- Los que no convierten = gastos contenidos

### Caso de Estudio: Campañas para Mujeres

#### 🔴 ANTES (Mezcladas)
```
Campaign: Women's Products
├─ Asset Group A: Clothing (0.5 ROAS)
│  └─ Spend: $8,000 | Conversions: Pocas
└─ Asset Group B: Accessories (2.5 ROAS)
   └─ Spend: $2,000 | Conversions: Muchas

Problema: A come el presupuesto de B
```

#### 🟢 DESPUÉS (Separadas)
```
Campaign 1: Women's Clothing
└─ Asset Group: Clothing (ahora 3.0 ROAS)
   └─ Spend: Controlado, pequeño presupuesto inicial

Campaign 2: Women's Accessories  
└─ Asset Group: Accessories (ahora 3.0 ROAS)
   └─ Spend: Escalado, presupuesto mayor
```

#### 📈 Resultados
| Métrica | Antes | Después |
|---------|-------|---------|
| Clothing ROAS | 0.5 | 3.0 |
| Accessories ROAS | 2.5 | 3.0 |
| Overall ROAS | 1.5 | 3.0 |
| Control | Bajo | Alto |

### Proceso: Separar Asset Groups

#### Paso 1: Identificar Candidatos
`Campaigns` → `Asset Groups`
1. Agregar columnas: Clicks, Cost, Impressions, CTR, Conversions, Cost Per Conversion, Conversion Rate
2. Usar **Table View** para mejor análisis
3. Buscar asset groups con:
   - Alto gasto + bajos conversiones
   - Diferencia grande en ROAS vs otros

#### Paso 2: Crear Nueva Campaña
- Copiar configuración de la campaña original
- Asignar presupuesto inicial PEQUEÑO (restricción temporal)
- Mantener mismo bidding strategy al principio

#### Paso 3: Mover el Asset Group
- Crear nuevo asset group en la nueva campaña
- Copiar los assets (headlines, descriptions, images)
- Comenzar con presupuesto limitado

#### Paso 4: Monitorear y Escalar
- Esperar 2-4 semanas de datos
- Si ROAS es positivo → aumentar presupuesto gradualmente
- Si ROAS es bajo → ajustar o pausar

### Requisitos para Separación

✅ **Criterios que Deben Cumplirse:**
- Asset group debe tener diferencia notable en ROAS vs otros
- Debe estar consumiendo >40% del presupuesto
- Debe haber suficientes datos (4+ semanas)

❌ **Evita Separar Si:**
- El asset group es nuevo (menos de 2 semanas)
- Los ROAS son similares entre grupos
- Tienes pocos asset groups (2 o menos)

---

## Resumen de Acciones Prioritarias

| Acción | Frecuencia | Impacto |
|--------|-----------|--------|
| Revisar Insights y agregar audience signals | Semanal | Muy Alto |
| Revisar bidding strategy | Cada 90 días | Muy Alto |
| Monitorear estabilidad de CPA/ROAS | Semanal | Alto |
| Evaluar oportunidades de segmentación | Mensual | Muy Alto |
| Escalar presupuesto en asset groups ganadores | Según datos | Muy Alto |

---

## Notas Importantes

1. **Insights > Impresiones:** Enfócate en CONVERSIONES cuando agregas audience signals, no en impresiones
2. **Paciencia con Bidding:** Espera 3 meses ANTES de introducir Target CPA/ROAS
3. **Estabilidad Primero:** Solo cambia bidding strategy cuando ves datos consistentes por 4+ semanas
4. **No Cambies Cada Semana:** Los cambios toman tiempo, revisar cada 90 días evita volatilidad
5. **Separación Estratégica:** Solo separa si un asset group consume presupuesto sin conversiones
6. **ROAS es Rey:** En Performance Max, ROAS es la métrica más importante para decisiones
7. **Data Over Instinct:** Tus números dicen la verdad sobre cuándo actuar
