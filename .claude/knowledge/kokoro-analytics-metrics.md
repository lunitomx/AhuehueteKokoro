<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Metricas Digitales — Referencia para /kokoro-analytics

> Skill: `/kokoro-analytics`
> Herramienta transversal: consulta conversacional de metricas

> "Un numero sin contexto es ruido. Un numero con contexto es una brujula."

## Proposito

Referencia tecnica para el skill `/kokoro-analytics`. Documenta las
herramientas MCP disponibles por plataforma, el glosario de traduccion
de metricas, los patrones de interpretacion de fechas, y la matriz de
ruteo de consultas.

## Inventario de Herramientas MCP

### Meta Ads (servidor: facebook-ads)

| Herramienta | Proposito | Parametros Requeridos |
|-------------|-----------|----------------------|
| `mcp__facebook-ads__get_account_insights_summary` | Metricas generales de cuenta | `account_id` (act_XXXX), `date_range` |
| `mcp__facebook-ads__get_campaign_performance` | Rendimiento por campana | `account_id`, `date_range` |
| `mcp__facebook-ads__get_campaigns` | Lista de campanas | `account_id` |
| `mcp__facebook-ads__get_campaign_status_and_budget` | Estado y presupuesto | `account_id` |
| `mcp__facebook-ads__get_demographic_breakdown` | Desglose demografico | `account_id`, `date_range` |
| `mcp__facebook-ads__get_ad_creative_details` | Detalles de creativos | `account_id` |

**Formato de account_id:** `act_` seguido de digitos (ej. `act_123456789`)
**Clave en metadata:** `platform_accounts.meta_ads`

### Google Ads (servidor: google-ads)

| Herramienta | Proposito | Parametros Requeridos |
|-------------|-----------|----------------------|
| `mcp__google-ads__get_customer_insights_summary` | Metricas generales de cuenta | `customer_id` |
| `mcp__google-ads__get_campaign_performance` | Rendimiento por campana | `customer_id`, `date_range` |
| `mcp__google-ads__get_campaigns` | Lista de campanas | `customer_id` |
| `mcp__google-ads__get_keywords_performance` | Rendimiento de keywords | `customer_id`, `date_range` |
| `mcp__google-ads__get_search_terms` | Terminos de busqueda | `customer_id`, `date_range` |
| `mcp__google-ads__get_demographic_breakdown` | Desglose demografico | `customer_id`, `date_range` |
| `mcp__google-ads__get_geographic_breakdown` | Desglose geografico | `customer_id`, `date_range` |

**Formato de customer_id:** 10 digitos sin guiones (ej. `1234567890`)
**Clave en metadata:** `platform_accounts.google_ads`

### GA4 — Google Analytics (servidor: google-analytics)

| Herramienta | Proposito | Parametros Requeridos |
|-------------|-----------|----------------------|
| `mcp__google-analytics__run_report` | Reporte personalizado | `property_id`, `date_range`, `metrics`, `dimensions` |
| `mcp__google-analytics__run_realtime_report` | Datos en tiempo real | `property_id` |
| `mcp__google-analytics__get_property_details` | Info de propiedad | `property_id` |

**Formato de property_id:** `properties/XXXXXX` (ej. `properties/123456`)
**Clave en metadata:** `platform_accounts.ga4`

**Metricas comunes para run_report:**
- `sessions` — sesiones totales
- `totalUsers` — usuarios unicos
- `newUsers` — usuarios nuevos
- `bounceRate` — tasa de rebote
- `averageSessionDuration` — duracion promedio
- `screenPageViews` — paginas vistas
- `conversions` — conversiones (si hay eventos configurados)

**Dimensiones comunes:**
- `sessionDefaultChannelGroup` — canal de adquisicion (organico, pagado, directo)
- `country` — pais
- `city` — ciudad
- `deviceCategory` — dispositivo (desktop, mobile, tablet)
- `landingPage` — pagina de entrada

### Search Console (servidor: google-search-console)

| Herramienta | Proposito | Parametros Requeridos |
|-------------|-----------|----------------------|
| `mcp__google-search-console__get_performance_overview` | Panorama de busqueda | `site_url`, `days` |
| `mcp__google-search-console__get_search_analytics` | Datos de busqueda detallados | `site_url`, `date_range` |
| `mcp__google-search-console__inspect_url_enhanced` | Inspeccion de URL | `site_url`, `url` |

**Formato de site_url:** URL del sitio (ej. `https://ejemplo.com`) o dominio (`sc-domain:ejemplo.com`)
**Clave en metadata:** `platform_accounts.gsc`

## Glosario de Metricas

Traducciones del lenguaje tecnico al lenguaje del emprendedor (voz Kokoro).

| Metrica Tecnica | Significado | Traduccion Kokoro |
|-----------------|-------------|-------------------|
| **CTR** (Click-Through Rate) | Porcentaje de personas que hicieron clic despues de ver el anuncio | "De cada 100 personas que vieron la creacion, {X} hicieron clic" |
| **CPC** (Cost Per Click) | Costo promedio de cada clic | "Cada clic costo en promedio ${X}" |
| **CPM** (Cost Per Mille) | Costo por cada 1,000 impresiones | "La inversion por cada mil impresiones fue ${X}" |
| **ROAS** (Return on Ad Spend) | Retorno por cada peso invertido en publicidad | "Por cada peso invertido, regresaron ${X}" |
| **Impressions** | Veces que la creacion fue mostrada | "Las creaciones de {invitado} se mostraron {N} veces" |
| **Clicks** | Numero de clics en la creacion | "{N} visitas generadas a traves de {plataforma}" |
| **Bounce Rate** | Porcentaje que se fue sin interactuar | "De cada 100 visitantes, {X} se fueron sin explorar" |
| **Sessions** | Visitas al sitio (puede incluir multiples paginas) | "{N} sesiones en el sitio" |
| **Avg. Session Duration** | Tiempo promedio que dura cada visita | "Cada visita duro en promedio {X} minutos" |
| **Conversions** | Acciones valiosas completadas (compras, formularios, etc.) | "{N} acciones de valor completadas" |
| **Search Impressions** | Veces que el sitio aparecio en resultados de busqueda | "{N} veces aparecio en los resultados de Google" |
| **Average Position** | Posicion promedio en resultados de busqueda | "Posicion promedio en busqueda: {X}" |

### Meta Ads — Metricas Completas

| Metrica | Significado | Traduccion Kokoro | Bueno | Malo |
|---------|-------------|-------------------|:-----:|:----:|
| **Reach** | Personas unicas que vieron el anuncio | "{N} personas unicas alcanzadas" | >1000/dia | <100/dia |
| **Frequency** | Veces promedio que cada persona vio el anuncio | "Cada persona vio la creacion {X} veces en promedio" | 1.5-3 | >5 (fatiga) |
| **Spend** | Monto total invertido | "Inversion total: ${X}" | Dentro del presupuesto | >120% presupuesto |
| **Cost per Result** | Costo por cada accion objetivo | "Cada resultado costo ${X}" | <CPC promedio industria | >3x promedio |
| **Result Rate** | Porcentaje de impresiones que generan resultado | "{X}% de las impresiones generaron resultado" | >2% | <0.5% |
| **Video Views** | Reproducciones de video (3+ segundos) | "{N} personas vieron el video" | >50% de reach | <10% |
| **ThruPlay** | Reproducciones completas o 15+ segundos | "{N} personas vieron el video completo" | >30% de views | <10% |
| **Link Clicks** | Clics al enlace destino | "{N} personas visitaron el destino" | CTR >1% | CTR <0.5% |
| **Landing Page Views** | Personas que cargaron la pagina destino | "{N} personas llegaron a la pagina" | >80% de link clicks | <50% |
| **Messaging Conversations** | Conversaciones iniciadas por WhatsApp/Messenger | "{N} conversaciones iniciadas" | Depende campana | 0 en 48h |

### Google Ads — Metricas Completas

| Metrica | Significado | Traduccion Kokoro | Bueno | Malo |
|---------|-------------|-------------------|:-----:|:----:|
| **Quality Score** | Calidad del anuncio segun Google (1-10) | "Google califica la relevancia de tu anuncio en {X}/10" | >7 | <5 |
| **Search Impression Share** | % del mercado que capturas | "De todas las busquedas posibles, apareces en {X}%" | >60% | <20% |
| **Conversion Rate** | % de clics que convierten | "De cada 100 visitas, {X} tomaron accion" | >3% | <1% |
| **Cost per Conversion** | Costo por cada conversion | "Cada conversion costo ${X}" | <valor del lead | >3x valor |
| **Search Terms** | Terminos reales que activaron anuncios | "Terminos que la gente busco para encontrarte" | Relevantes | Irrelevantes >30% |
| **Avg CPC** | Costo promedio por clic | "Cada clic costo ${X} en promedio" | <$15 MXN | >$50 MXN |
| **Conv. Value/Cost** | Valor generado por peso invertido | "Por cada peso invertido, generaste ${X} en valor" | >3 | <1 |

### GA4 — Metricas Completas

| Metrica | Significado | Traduccion Kokoro | Bueno | Malo |
|---------|-------------|-------------------|:-----:|:----:|
| **Active Users** | Usuarios activos en el periodo | "{N} personas visitaron el sitio" | Crecimiento mes a mes | Caida >20% |
| **New Users** | Visitantes nuevos | "{N} personas visitaron por primera vez" | >50% de total | <20% (no atrae nuevos) |
| **Engagement Rate** | % de sesiones con interaccion significativa | "{X}% de los visitantes interactuaron activamente" | >60% | <40% |
| **Events** | Acciones rastreadas en el sitio | "{N} acciones registradas" | Depende config | 0 (mal configurado) |
| **Pages per Session** | Paginas vistas por visita | "Cada visitante vio {X} paginas en promedio" | >2 | <1.5 |
| **Channel Grouping** | De donde vienen los visitantes | "{X}% llegan por {canal}" | Diversificado | >80% un solo canal |
| **Conversions** | Objetivos completados | "{N} objetivos completados en el sitio" | Crecimiento | Caida >30% |

### Search Console — Metricas Completas

| Metrica | Significado | Traduccion Kokoro | Bueno | Malo |
|---------|-------------|-------------------|:-----:|:----:|
| **Total Impressions** | Apariciones en resultados de busqueda | "Apareciste {N} veces en Google" | Crecimiento | Caida >20% |
| **Total Clicks** | Clics desde resultados de busqueda | "{N} personas eligieron tu sitio en Google" | CTR >3% | CTR <1% |
| **Average CTR** | % de impresiones con clic | "De cada 100 apariciones, {X} personas hicieron clic" | >3% | <1% |
| **Average Position** | Posicion promedio en resultados | "Posicion promedio: {X}" | <10 (pagina 1) | >20 (pagina 3+) |
| **Top Queries** | Busquedas que muestran tu sitio | "Las personas te encuentran buscando: {queries}" | Relevantes al negocio | Irrelevantes |
| **Top Pages** | Paginas con mas trafico organico | "Tus paginas mas visitadas: {pages}" | Paginas clave del negocio | Solo home |
| **Mobile Usability** | Problemas de uso en movil | "{N} paginas con problemas en movil" | 0 | >5 |
| **Index Coverage** | Paginas indexadas vs errores | "{N} paginas indexadas, {M} con errores" | 0 errores | >10% errores |

## Metricas Desconocidas — Guia

Si una metrica NO aparece en este glosario:

1. **Nombra la metrica** tal cual aparece en la respuesta del MCP
2. **Describe su valor** en terminos simples: "El sistema reporta {metrica} = {valor}"
3. **No inventes traducciones** — es mejor ser preciso que creativo
4. **Sugiere investigar**: "Esta metrica ({nombre}) merece atencion. ¿Quieres que la investiguemos?"
5. **Registra** para expansion futura del glosario

## Patrones de Fecha

Interpretacion de lenguaje natural a parametros MCP.

| El usuario dice | Interpretacion | Parametro date_range |
|-----------------|---------------|---------------------|
| "este mes" / "this month" | Inicio del mes actual a hoy | `this_month` |
| "la semana pasada" / "last week" | Lunes a domingo de la semana anterior | `last_week` |
| "esta semana" / "this week" | Lunes actual a hoy | `this_week` |
| "ayer" / "yesterday" | Solo el dia anterior | `yesterday` |
| "hoy" / "today" | Solo hoy (datos parciales) | `today` |
| "los ultimos 7 dias" / "last 7 days" | Ultimos 7 dias naturales | `last_7_days` |
| "los ultimos 30 dias" / "last 30 days" | Ultimos 30 dias naturales | `last_30_days` |
| "los ultimos 90 dias" / "last 90 days" | Ultimos 90 dias | `last_90_days` |
| "marzo" / "March" | Mes completo (1-31 o hasta hoy si es el mes actual) | `2026-03-01,2026-03-31` |
| "enero a marzo" / "Jan to March" | Rango de meses | `2026-01-01,2026-03-31` |
| (sin fecha mencionada) | **Default: ultimos 7 dias** | `last_7_days` |

**Nota:** Para Search Console, usar el parametro `days` en lugar de `date_range`
para `get_performance_overview` (ej. `days=7` para ultimos 7 dias).

## Matriz de Ruteo de Consultas

Guia para determinar que herramientas llamar segun la intencion del usuario.

### Por tipo de consulta

| Intencion del usuario | Plataformas a consultar | Herramientas |
|----------------------|------------------------|--------------|
| "Como va {invitado}?" | Todas las conectadas | Overview de cada plataforma |
| "Meta Ads de {invitado}" | Solo Meta Ads | `get_account_insights_summary` + `get_campaign_performance` |
| "Google Ads de {invitado}" | Solo Google Ads | `get_customer_insights_summary` + `get_campaign_performance` |
| "Trafico de {invitado}" | GA4 | `run_report` (sessions, users, sources) |
| "SEO de {invitado}" | Search Console | `get_performance_overview` + `get_search_analytics` |
| "Campanas de {invitado}" | Meta Ads + Google Ads | `get_campaigns` de ambas |
| "Demograficos de {invitado}" | Meta Ads + Google Ads | `get_demographic_breakdown` de ambas |
| "Keywords de {invitado}" | Google Ads | `get_keywords_performance` |
| "Que buscan sobre {invitado}?" | Search Console + Google Ads | `get_search_analytics` + `get_search_terms` |

### Por nivel de profundidad

| Profundidad | Herramientas por plataforma |
|-------------|---------------------------|
| **Overview** | `get_account_insights_summary` (Meta), `get_customer_insights_summary` (GAds), `run_report` basico (GA4), `get_performance_overview` (GSC) |
| **Detallado** | Overview + `get_campaign_performance` + `get_campaigns` |
| **Profundo** | Detallado + `get_demographic_breakdown` + `get_keywords_performance` + `get_search_analytics` |

## Analisis de Placements (Meta Ads)

Cuando el usuario pide "que placements apagar", "donde se va el presupuesto",
o "analisis de ubicaciones", este es el flujo:

### Paso 1: Intentar via MCP

```
get_demographic_breakdown(
  account_id="{act_XXXX}",
  breakdowns="publisher_platform,platform_position",
  level="campaign",
  date_preset="last_90d"
)
```

Esto devuelve spend, impressions, clicks, **actions** y **cost_per_action_type**
por placement. Busca en `actions` los tipos: `lead`, `offsite_conversion.fb_pixel_purchase`,
`onsite_conversion.messaging_conversation_started_7d`.

### Paso 2: Si el MCP no devuelve conversiones

Guia al usuario a exportar CSV del Ads Manager:
1. Ads Manager → Columnas: "Rendimiento" o personalizado con leads/compras
2. Desglose → Por ubicacion
3. Rango: ultimos 90 dias (o el periodo que necesite)
4. Exportar CSV

Lee el CSV localmente y haz el analisis sobre el archivo.

### Paso 3: Presentar decision accionable

| Placement | Spend | Leads | CPL | Decision |
|-----------|-------|-------|-----|----------|
| Feed | $X | N | $Y | Mantener |
| Reels | $X | N | $Y | Evaluar |
| Audience Network | $X | 0 | - | Apagar |

**Anti-patron:** No hagas 20+ llamadas al MCP intentando reconstruir lo que
un CSV da en un archivo. Si la primera llamada no da conversiones, pide CSV.

## Limitaciones Conocidas del MCP

| Herramienta | Limitacion | Workaround |
|-------------|-----------|------------|
| `get_campaign_performance` | No acepta breakdowns | Usar `get_demographic_breakdown` con actions |
| `get_demographic_breakdown` | Antes no devolvia actions (fix aplicado 2026-04-09) | Si aun falla: pedir CSV |
| `get_ad_creative_details` | Ads de Advantage+ pueden tener body/title vacios | Fallback a object_story_spec aplicado |
| `get_campaigns` | `status_filter` usaba campo incorrecto (fix aplicado 2026-04-09) | — |
| `get_campaign_performance` nivel `ad` | Devuelve ~98K chars, puede exceder limites | Empezar a nivel `campaign`, bajar solo si necesario |
| `list_ad_accounts` | Devuelve TODAS las cuentas sin filtro | Si buscas una cuenta especifica, pide el act_id al usuario |

## Degradacion Elegante

| Escenario | Respuesta |
|-----------|-----------|
| Servidor MCP no responde | "El servidor de {plataforma} no esta respondiendo. Puedo consultar las otras plataformas conectadas." |
| Cuenta no encontrada | "La cuenta {id} no se encontro. Puede que haya cambiado. Usa `/kokoro-connect` para actualizar." |
| Sin datos para el rango | "No hay datos de {plataforma} para {rango}. ¿Quieres intentar con un periodo mas amplio?" |
| Invitado sin plataformas | "Encontre a {nombre} pero no tiene plataformas conectadas. Usa `/kokoro-connect {nombre}` para empezar." |
| Invitado no encontrado | "No encontre a ese invitado. Usa `/kokoro-client` para registrarlo primero." |
