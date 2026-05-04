# Sistema de Delivery de Meta Ads — Referencia para /kokoro-ads

> "El algoritmo no es tu enemigo — es un aprendiz que necesita tiempo.
> Apagar un ad en exploracion es como arrancar una semilla el segundo dia
> porque todavia no da frutos."
> — Eduardo Munoz Luna

## Filosofia del Sistema

El emprendedor que entiende como Meta entrega sus ads tiene una ventaja
competitiva invisible: paciencia estrategica. Mientras otros apagan campanas
al tercer dia porque "no funcionan", el emprendedor informado sabe que el
sistema todavia esta aprendiendo — y que apagar en ese momento es lo peor
que puede hacer.

Meta no muestra tu ad a personas aleatorias. Cuatro sistemas de inteligencia
artificial trabajan simultaneamente para encontrar a las personas correctas
(ver `kokoro-meta-ai-ecosystem.md` para descripcion completa de cada sistema).
Pero esos sistemas necesitan datos para aprender. Y los datos requieren
tiempo e inversion.

La metafora agricola aplica con precision: sembrar no es lo mismo que
cosechar. El emprendedor que invierte $500 MXN y espera conversiones en
48 horas esta confundiendo exploracion con optimizacion. Son fases
fundamentalmente diferentes — y cada una tiene sus propias reglas.

**Principio central:** Nunca tomes decisiones de on/off basandote en datos
de exploracion. Es como juzgar la cosecha mirando la tierra recien sembrada.

---

## Las 3 Fases del Ad Delivery

Cada ad set que lanzas atraviesa tres fases secuenciales. La fase en la que
te encuentras determina que acciones son validas y cuales son destructivas.

---

### Fase 1 — Exploracion (Dias 1-3)

**Que esta pasando dentro de Meta:**

El sistema esta mapeando tu creativo a clusters de audiencia. Andromeda
escanea 10+ millones de ads por subasta para encontrar donde encaja el tuyo
dentro de su indice jerarquico de 4 niveles. GEM tiene cero signal de
conversion — literalmente no sabe quien va a responder a tu ad. Lattice
esta probando superficies (Feed, Reels, Stories) sin datos historicos.

Los dias 1-2 son "ruido caro" — el sistema esta invirtiendo inference
computacional para mapear tu creativo a los clusters correctos. Los CPAs
de estos dias NO son indicativos de rendimiento futuro.

**Lo que ves en el dashboard:**

- CPAs erraticos (pueden ser 5x o 10x tu target)
- Impresiones bajas (<500)
- CTR inestable
- Posiblemente cero conversiones

**Lo que debes hacer:** NADA. Absolutamente nada. No toques presupuesto,
no cambies copy, no pauses. Cada cambio reinicia el proceso.

**Lo que nunca debes hacer:** Tomar decisiones basadas en estos numeros.
Son ruido estadistico, no signal.

---

### Fase 2 — Learning (Dias 3-14)

**Que esta pasando dentro de Meta:**

GEM esta construyendo modelos de probabilidad de conversion basados en las
primeras interacciones. Andromeda tiene clusters iniciales pero necesita
volumen para refinar. Lattice esta identificando que superficies funcionan
mejor para tu creativo especifico. Sequence Learning esta comenzando a
mapear el journey temporal de tus visitantes.

El target de Meta es claro: **50 eventos de optimizacion en 7 dias** para
salir de learning phase. Para campanas de Purchase o Mobile App Install,
el threshold reducido es **10 conversiones en 3 dias**.

**Lo que ves en el dashboard:**

- CPAs comenzando a estabilizarse (pero aun con variacion)
- Impresiones creciendo (500-2000+)
- Patrones emergentes en horarios y placements
- Posiblemente algunas conversiones

**Lo que debes hacer:** Monitorear sin intervenir. La unica excepcion es
el hard kill threshold (ver Matriz de Decision). Si despues de invertir
3x tu CPA target no tienes una sola conversion, hay un reto fundamental
que el algoritmo no va a resolver.

**Lo que nunca debes hacer:** Cambios de presupuesto >20%, cambios de
targeting, cambios de evento de optimizacion. Cualquiera de estos reinicia
el learning completo.

---

### Fase 3 — Optimizacion (Dia 14+)

**Que esta pasando dentro de Meta:**

GEM tiene predicciones calibradas. Andromeda tiene asignaciones estables de
clusters. Lattice sabe exactamente que superficie funciona para cada
segmento de tu audiencia. Sequence Learning tiene suficiente historia
temporal para predecir el siguiente paso logico del journey.

Para campanas de alto volumen (>50 conversiones/semana), la optimizacion
es efectiva desde el dia 14. Para volumen medio (10-50 conversiones/semana),
el sistema necesita hasta el dia 21 para calibrarse completamente.

**Lo que ves en el dashboard:**

- CPAs estables y predecibles
- Patrones claros de rendimiento por placement
- Conversion rate consistente
- Datos suficientes para decisiones informadas

**Lo que debes hacer:** AHORA si puedes evaluar con justicia. Compara
contra tu CPA target. Optimiza lo que funciona, pausa lo que no. Pero
hazlo con datos de optimizacion, no con datos de exploracion.

**Lo que nunca debes hacer:** Relajarte. Creative fatigue llega cuando
la frecuencia supera 3.0. Monitorea el diversity score — el target es
60%+ de diversidad dentro de las primeras 4 semanas.

---

## Thresholds Oficiales de Meta

Estos son los numeros que Meta publica y que el sistema usa internamente
para determinar cuando un ad set sale de learning phase.

**Salida de Learning Phase:**
- **Estandar:** 50 eventos de optimizacion por ad set en 7 dias
- **Reducido (Purchase / Mobile App Install):** 10 conversiones en 3 dias
- **Tiempo minimo sin cambios:** 7 dias desde el ultimo cambio significativo

**Reglas de cambio de presupuesto:**
- **<20% de cambio:** Seguro. El sistema absorbe sin reiniciar learning.
- **20-50% de cambio:** Zona gris. Puede o no reiniciar dependiendo de la
  estabilidad del ad set. Proceder con cautela.
- **>50% de cambio:** Reinicio completo de learning. Equivale a lanzar
  un ad set nuevo.

**Volumen y tiempos de calibracion:**
- **Alto volumen (>50 conv/semana):** Learning inicial 7-14 dias.
  Optimizacion efectiva desde dia 14.
- **Volumen medio (10-50 conv/semana):** Learning inicial 14-21 dias.
  Optimizacion efectiva desde dia 21.
- **Dato critico:** Contenido organico (3+ Reels organicos) alimenta las
  predicciones de GEM — emprendedores con presencia organica activa ven
  hasta 2.5x en conversion rate sobre ads pagados.

*Fuente: documentacion oficial de Meta Ads + Meta AI blog posts (2024-2025).*

---

## Thresholds Practicos (Consenso de Media Buyers)

Estos thresholds no vienen de Meta — vienen de la experiencia colectiva de
media buyers que manejan millones en inversion mensual. Son las reglas de
campo que complementan los numeros oficiales.

| Situacion | Threshold | Accion |
|-----------|-----------|--------|
| **Hard kill** | 3x CPA target invertido, 0 conversiones | Apagar inmediatamente |
| **Soft pause** | CPA 30%+ arriba del target despues de 72h | Pausar para revision |
| **Evaluacion minima** | 5 dias sin cambios antes de decidir | Esperar |
| **Presupuesto minimo** | 5x CPA target por dia por ad set | Requerido para que el sistema aprenda |
| **Piso de conversiones** | 50 eventos/semana (10 para Purchase) | Debajo = atascado en learning |

**Lectura estrategica:** El hard kill es la unica razon para apagar antes
del dia 7. Todo lo demas requiere paciencia. El emprendedor que apaga ads
"porque el CPA esta alto" en el dia 3 esta tomando decisiones con datos
de exploracion — es como decidir que una planta no va a dar frutos porque
a los 3 dias no ves flores.

*Fuente: consenso de media buyers experimentados, no documentacion oficial de Meta.*

---

## Los 4 Sistemas y el Delivery

Cada fase del delivery activa los 4 sistemas de IA de Meta de manera
diferente. Entender que sistema esta trabajando en cada momento te da
claridad sobre por que los numeros se ven como se ven.

(Para descripcion completa de cada sistema, ver `kokoro-meta-ai-ecosystem.md`.)

| Sistema | Exploracion (Dias 1-3) | Learning (Dias 3-14) | Optimizacion (Dia 14+) |
|---------|----------------------|---------------------|----------------------|
| **GEM** | Cero signal. Sin datos de conversion para modelar. | Construyendo modelos de probabilidad con datos iniciales. | Predicciones calibradas. Scoring de intencion confiable. |
| **Andromeda** | Mapeando creativo a clusters. Probando posiciones en el indice jerarquico. | Clusters iniciales asignados. Refinando con datos de interaccion. | Asignaciones estables. Sabe exactamente donde compite tu ad. |
| **Lattice** | Probando todas las superficies sin preferencia. Todos los placements activos = mas datos. | Identificando que superficies funcionan mejor. Cross-surface intelligence emergiendo. | Inteligencia cross-surface completa. Sabe que formato funciona para cada usuario. |
| **Sequence Learning** | Sin historia temporal. No puede predecir journeys. | Comenzando a mapear secuencias (vista → visita → conversion). | Historia temporal suficiente. Predice el siguiente paso del journey. |

**Implicacion practica:** Si restringes placements en Fase 1, le quitas
datos a Lattice. Si cambias el creativo en Fase 2, reinicias el mapeo de
Andromeda. Si ignoras la frecuencia en Fase 3, Sequence Learning muestra
el mismo ad a la misma persona hasta que lo ignora.

---

## Resets que Reinician Learning

Estas acciones reinician el learning phase completo — el sistema vuelve a
Exploracion como si fuera un ad set nuevo. Cada reset representa dias de
inversion y datos perdidos.

1. **Cambio de evento de optimizacion** — Pasar de "Lead" a "Purchase" o
   viceversa. GEM tiene que reconstruir todos sus modelos de probabilidad
   desde cero.

2. **Cambio de presupuesto >50%** — Un salto dramatico en presupuesto
   cambia fundamentalmente el espacio de subasta donde compites. Andromeda
   tiene que remapear tus clusters.

3. **Agregar o quitar targeting** — Cualquier cambio en la definicion de
   audiencia invalida los clusters que Andromeda ya habia construido.

4. **Cambio de estrategia de bidding** — Pasar de "Lowest Cost" a "Cost Cap"
   o viceversa cambia las reglas del juego para todos los sistemas.

**Lo que NO reinicia learning:**
- Cambios de presupuesto <20%
- Agregar nuevos creativos al ad set (sin quitar los existentes)
- Cambios en el schedule de entrega
- Ediciones menores de copy que no alteran el mensaje central

---

## Matriz de Decision — Referencia Central para /kokoro-ads

Esta es la tabla que `/kokoro-ads` debe consultar antes de recomendar
apagar, pausar, o continuar cualquier ad. Cada fila representa un
escenario real con la accion correcta basada en la fase del delivery.

| Impresiones | Inversion vs CPA | Tiempo activo | Conversiones | Fase | Accion |
|-------------|-------------------|---------------|--------------|------|--------|
| <500 | <1x CPA target | <3 dias | 0 | Exploracion | **ESPERAR** — datos insuficientes para cualquier decision |
| <500 | <1x CPA target | 3-5 dias | 0 | Learning temprano | **ESPERAR** — el sistema aun no tiene signal |
| 500-2000 | 1-2x CPA target | 5-7 dias | 0 | Learning | **REVISAR** copy/targeting conceptualmente, no apagar |
| 500-2000 | 2-3x CPA target | 5-7 dias | 0 | Learning | **SOFT PAUSE** — revisar antes de reactivar |
| >2000 | >3x CPA target | >5 dias | 0 | Learning/Optimizacion | **HARD KILL** — signal suficiente, el ad no convierte |
| cualquiera | cualquiera | <5 dias | >0 | Learning | **ESPERAR** — hay signal positiva, dejar que el sistema aprenda |
| cualquiera | >1.3x CPA target | >7 dias | >0 | Optimizacion | **OPTIMIZAR** — ajustar creativos o audiencia, no apagar |

**Como leer la matriz:**

1. Ubica las impresiones del ad
2. Calcula cuanto has invertido vs tu CPA target
3. Cuenta los dias activos sin cambios significativos
4. Revisa si hay conversiones (aunque sean pocas)
5. La interseccion te da la fase y la accion correcta

**Principio rector:** La accion default es ESPERAR. Apagar es la excepcion,
no la regla. Solo el hard kill (3x CPA, 0 conversiones, >5 dias) justifica
apagar antes de que el sistema complete su learning.

---

## Caso de Referencia — lunitomx/kokoro#1

**Contexto:** Un ad fue evaluado con 283 impresiones, $79 MXN de inversion,
0 conversiones, 8 dias activo. Kokoro recomendo apagar.

**Analisis con la Matriz de Decision:**

- **Impresiones:** 283 → <500 → Fase de Exploracion
- **Inversion vs CPA target (~$225 MXN):** $79 → ~0.35x CPA → muy por
  debajo del threshold minimo de evaluacion
- **Tiempo activo:** 8 dias → suficiente en teoria, pero las impresiones
  indican que el ad nunca salio de exploracion
- **Conversiones:** 0 → esperado con <500 impresiones

**Decision correcta:** ESPERAR. El ad no ha salido de exploracion — con
283 impresiones, Andromeda apenas ha comenzado a mapear clusters. La
inversion total ($79 MXN) es 0.35x del CPA target, lo cual significa que
el sistema no ha tenido suficiente presupuesto para aprender.

**Decision incorrecta:** APAGAR. Que es lo que Kokoro recomendo. Este
error ocurrio porque el analisis se baso en el tiempo activo (8 dias)
sin considerar que las impresiones (<500) indican que el ad nunca salio
de la fase de exploracion.

**Leccion:** El tiempo activo es necesario pero no suficiente. Un ad
puede estar "activo" 8 dias pero seguir en exploracion si el presupuesto
es insuficiente para generar las impresiones necesarias. La fase se
determina por la combinacion de impresiones + inversion + tiempo, no
por tiempo solamente.
