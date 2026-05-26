# /kokoro-tracking-check — Metodologia de verificacion de tracking (Fase 0)

> Metodologia para auditar la salud de medicion digital antes de iniciar
> cualquier parrilla de contenido. Fase 0 del pipeline Parrilla.
>
> "Si el tracking miente, los datos no son datos — son ruido con formato."

## Principio fundacional

El tracking es la **rafz del sistema de decision**. Un pixel mal configurado,
un evento duplicado, o una UTM perdida hacen que cada decision posterior
se construya sobre informacion incorporea. Fase 0 verifica 5 dominios
criticos antes de que cualquier inversion en contenido ocurra.

## Los 5 dominios de verificacion

### D1 — Pixel: disparo en submit, no en page-view

El evento de conversion debe dispararse cuando el invitado completa el
formulario (submit), no cuando carga la pagina (page-view). Un pixel
disparado en page-view:
- Infla falsamente las conversiones
- Impide que Meta optimice para la accion real
- Distorsiona el CPA real

**Verificacion:**
1. Abrir la landing page en una pestana de incognito
2. Abrir las herramientas de desarrollador → Red (Network)
3. Buscar peticiones a `connect.facebook.net` o `fbevents.js`
4. Completar el formulario hasta submit (no enviar datos reales)
5. Confirmar que el pixel `fbq('track', 'SubmitApplication', ...)` o
   `fbq('track', 'Lead', ...)` aparece DESPUES del submit, no al cargar
6. Si el pixel dispara al cargar la pagina → **CRITICO**

### D2 — Deteccion de duplicados `generate_lead`

Meta Ads puede disparar el evento `generate_lead` multiples veces por
la misma accion si:
- La configuracion del pixel esta duplicada en el Tag Manager
- Hay una conversion personalizada compitiendo con el evento estandar
- El formulario tiene multiple event listeners

**Verificacion:**
1. Revisar en Events Manager de Meta la frecuencia del evento en modo test
2. Enviar un lead de prueba desde la landing
3. Verificar que aparece EXACTAMENTE 1 evento en Event Manager
4. Si aparece >1 evento por lead → **CRITICO** (CPA se duplica sin saberlo)

### D3 — Llegada de leads al CRM + visibilidad del closer

El lead debe llegar al CRM (Pipedrive, HubSpot, etc.) y ser visible para
el closer en tiempo real. Un lead que llega al CRM pero queda oculto en
una etapa incorrecta es funcionalmente un lead perdido.

**Verificacion:**
1. Enviar un lead de prueba con datos de tracking (nombre: "Test Fase 0",
   email: test@tracking-check.local)
2. Confirmar que aparece en el CRM en <5 minutos
3. Confirmar que la etapa asignada es la correcta (Nuevo / Recien Llegado)
4. Confirmar que el closer asignado puede verlo en su pipeline
5. Si el lead no llega → **CRITICO** | Si llega en etapa incorrecta → **WARNING**

### D4 — Persistencia de UTMs: ad → landing → form

Las UTMs de la campana (utm_source, utm_campaign, utm_content, utm_term)
deben pasar del clic en el ad → la landing page → el formulario submit →
el CRM. Un eslabon roto significa que no se puede atribuir el lead al
ad que lo genero.

**Verificacion:**
1. Crear un URL de prueba con UTMs visibles:
   `https://ejemplo.com/?utm_source=test_fase0&utm_campaign=tracking_check&utm_content=v1`
2. Hacer clic desde un ad de prueba o pegar el URL directamente
3. Inspeccionar que la landing recibe las UTMs (ver barra de URL)
4. Revisar que el formulario tiene campos ocultos que capturan UTMs
5. Enviar el lead de prueba y verificar que llegan al CRM
6. Si las UTMs se pierden en cualquier paso → **CRITICO**

### D5 — Compliance Google Ads (INE, dominio)

Para campanas de Google Ads que requieren verificacion de identidad
(INE/IFE del representante legal) y propiedad de dominio:

**Verificacion:**
1. Confirmar que la verificacion de anunciante (INE) esta completa en
   Google Ads → Facturacion → Verificacion de anunciante
2. Confirmar que el dominio del sitio esta verificado en Google Search
   Console o Google Ads → Configuracion → Dominio verificado
3. Si falta alguno → **CRITICO** (cuenta puede ser suspendida)

## Output: gap-list priorizada

Cada dominio produce un hallazgo con clasificacion:

| Clasificacion | Significado | Accion |
|--------------|-------------|--------|
| CRITICO | Tracking roto. Los datos actuales no son fiables. | Reparar antes de cualquier inversion |
| WARNING | Tracking funcional pero con riesgo. | Documentar y monitorear |
| OK | Domino verificado sin issues. | Continuar |

### Verdicto final

- **GO** — Cero criticos. Warnings documentados. Puede proceder a Fase A.
- **WAIT** — Uno o mas criticos presentes. No iniciar Fase A hasta
  reparacion confirmada.

## Referencias

- `kokoro-analytics-metrics.md` — glosario de metricas y herramientas MCP
- `kokoro-connect.md` — conexion de plataformas para verificacion automatizada
- `kokoro-quality-gates.md` — gates de calidad pre-delivery
