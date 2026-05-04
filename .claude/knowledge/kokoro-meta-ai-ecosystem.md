# Ecosistema de IA de Meta Ads — Referencia para /kokoro-creative-review

> "No compites contra otros anunciantes — compites contra la capacidad del
> algoritmo de ENTENDER tu creacion."

## Los 4 Sistemas que Evaluan Cada Creativo

Cuando un emprendedor sube un creativo a Meta, 4 sistemas de IA lo procesan
simultaneamente. Entender como opera cada uno es la diferencia entre invertir
con intencion y quemar presupuesto.

---

### 1. GEM — El Super Cerebro (Generative Ads Model)

**Que hace:** Modelo fundacional que unifica billones de puntos de datos para
predecir la intencion del usuario. Opera con Sequence Learning — analiza
interacciones como una narrativa continua, no como eventos aislados.

**3 capas de profundidad:**
- **Capa 1 (Fundacion):** Entiende la "Intencion Humana Central" — distingue
  entre interes persistente en lujo vs. busqueda puntual de vuelos.
- **Capa 2 (Dominio):** Especializada para Ads, Messaging o Discovery.
  Hereda patrones de comportamiento de Capa 1.
- **Capa 3 (Vertical):** Especializada para E-commerce, Lead Gen o B2B.
  Scoring final de relevancia segun patrones de conversion del negocio.

**Lo que esto significa para el creativo:**
- GEM busca DIVERSIDAD de senales de intencion — si todos tus creativos dicen
  lo mismo con diferente imagen, GEM los agrupa como uno solo
- La diversidad creativa ES el nuevo targeting — broad targeting (18-65+) es
  superior porque GEM ya sabe a quien mostrarle que
- Contenido organico de calidad (Reels, Threads) entrena a GEM — lo paid y lo
  organico ya no son mundos separados

**Metricas de rendimiento vs legacy:**
- +5% precision de conversion (IG), +3% (FB)
- +22% ROAS en usuarios Advantage+
- 4x mayor capacidad de modelo

---

### 2. Andromeda — El Consejero Personal (Ads Retrieval System)

**Que hace:** Motor de recuperacion acelerado por GPU. Reemplazo del filtrado
heuristico legacy. Escanea 10+ millones de anuncios por subasta usando un
indice jerarquico de 4 niveles.

**Indice jerarquico de 4 niveles:**
1. **Super-categorias** (ej: E-commerce vs. Servicios)
2. **Categorias** (ej: Real Estate de Lujo)
3. **Sub-categorias** (ej: Condos pre-construccion)
4. **Clusters de anuncios** (ads visual/conceptualmente similares)

**Lo que esto significa para el creativo:**
- Si tus creativos son repetitivos, Andromeda NO PUEDE encontrar nuevos clusters
  que explorar — los resultados caen exponencialmente
- Necesitas 8-15+ conceptos unicos (hooks/visuales diferentes) para darle al
  motor un "Campo de Accion" amplio
- Video vertical (9:16) de alta resolucion tiene mayor densidad de features
  para las redes neuronales
- Segmentos de alto valor reciben MAS esfuerzo de inferencia — marcas premium
  deben usar assets de alta calidad para aprovechar esta asignacion

**Metricas de rendimiento vs legacy:**
- +6% precision de recall
- +8% Ad Quality Score
- 100x mas rapido en extraccion de features
- +22% ROAS (Advantage+)

---

### 3. Lattice — La Biblioteca Gigante (Cross-Surface Intelligence)

**Que hace:** Capa de unificacion arquitectonica. Reemplaza modelos fragmentados
(uno para Reels, otro para Feed) con un modelo masivo que aprende de TODAS las
superficies, formatos y objetivos simultaneamente.

**Arquitectura Multi-Task Learning:**
- **90% parametros compartidos** — "Transferencia de Conocimiento Cross-Objetivo"
- **10% cabezas especializadas** — prediccion especifica (Purchase vs. Like)

**Lo que esto significa para el creativo:**
- Habilitar TODOS los placements es obligatorio — restringir desactiva la
  capacidad de Lattice de tomar inteligencia de otras superficies
- Fluidez de formato: el mismo asset en multiples formatos permite a Lattice
  identificar cual funciona mejor para cada usuario
- Lattice sabe que un usuario que hace click frecuentemente puede eventualmente
  comprar — usa senales de "baja intencion" para encontrar compradores de
  "alta intencion"

**Metricas de rendimiento vs legacy:**
- 2x mas rapido en actualizacion del modelo
- +12% ROAS en placement multi-superficie
- +15% rendimiento cold-start (campanas nuevas aprenden de las anteriores)

---

### 4. Sequence Learning — El Juego de Memoria (Temporal Intelligence)

**Que hace:** Capa de memoria temporal. Analiza el ORDEN cronologico de las
interacciones del usuario para predecir el siguiente paso logico en su journey.

**Cadena temporal de 3 estados:**
1. **Estado 1:** Impresion + Vista (interes establecido)
2. **Estado 2:** Visita a sitio web (intencion confirmada)
3. **Estado 3:** Compra/Conversion (necesidad cumplida)

**Lo que esto significa para el creativo:**
- Secuenciacion vertical: tus creativos deben seguir un flujo logico
  (Hook → Educacion → Manejo de objeciones → Oferta)
- No muestres el mismo producto visto — muestra el COMPLEMENTARIO que
  Sequence Learning predice como siguiente necesidad
- Crea contenido para el estado "Post-Compra" — el sistema prioriza estos
  usuarios para hooks de valor agregado

**Metricas de rendimiento vs legacy:**
- +30% relevancia de anuncio (percepcion del usuario)
- -18% impresiones redundantes
- +10% precision en prediccion de LTV

---

## Como Interactuan los 4 Sistemas

```
GEM (intencion) → proporciona "Intent Score" a Andromeda
Andromeda (recuperacion) → filtra millones a top 1,000 candidatos
Lattice (unificacion) → organiza datos cross-surface para GEM
Sequence Learning (memoria) → refina cronologicamente las predicciones de GEM
```

El creativo del emprendedor es evaluado por los 4 simultaneamente.
Un creativo fuerte satisface a todos. Un creativo debil falla en al menos uno.
