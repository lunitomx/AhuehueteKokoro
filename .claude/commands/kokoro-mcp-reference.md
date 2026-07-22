# /kokoro-mcp-reference — Catálogo verificable de MCP

> Herramienta transversal para /kokoro-connect y /kokoro-analytics.
>
> "Antes de conectar, saber qué conecta de verdad."

## Propósito

Este skill recomienda conectores sólo cuando su procedencia, instalación y
superficie de herramientas están verificadas. Nunca supone que un conector
existe por aparecer en una conversación, un registro de paquetes o una
integración de interfaz.

Lee el knowledge file de cada plataforma antes de guiar la instalación:

- kokoro-mcp-meta-ads.md
- kokoro-mcp-google-ads.md
- kokoro-mcp-ga4.md
- kokoro-mcp-search-console.md

## Gate Tactiq 2025

Lee `kokoro-tactiq-field-patterns.md` antes de recomendar una conexión.
Prioriza el MCP que responda una decisión real de pauta, atribución, landing,
seguimiento o reporting; una integración sin uso operativo no es avance.

## Estado de la versión pública

| Plataforma | Estado | Procedencia | Alcance verificado |
|---|---|---|---|
| Meta Ads | Incluido | connectors/meta-ads, mantenido por Ahuehuete Digital | 8 herramientas de lectura |
| Google Ads | Opcional | googleads/google-ads-mcp, mantenido por Google Ads | consulta y descubrimiento |
| Google Analytics 4 | Opcional y experimental | googleanalytics/google-analytics-mcp | 9 herramientas de lectura |
| Google Search Console | not_bundled | no_verified_official_mcp | sin catálogo de tools |

La instalación base de Kokoro no instala credenciales ni conecta cuentas. Cada
persona aporta su propia autorización en su equipo.

## Gate de decisión

Antes de recomendar un MCP, pregunta qué decisión necesita mejorar el
invitado:

| Necesidad | Recomendación |
|---|---|
| Leer inversión, campañas o creativos de Meta | Conector Meta Ads incluido |
| Consultar cuentas o rendimiento de Google Ads | Servidor oficial de Google Ads |
| Leer tráfico, eventos o propiedades GA4 | Servidor oficial experimental de Google Analytics |
| Analizar Search Console | Exportación manual o adaptador propio auditado; esta versión no incluye MCP |
| Crear, pausar o modificar campañas | No prometerlo: los conectores verificados de esta versión son de consulta |

Si no hay una decisión concreta, no acumules conectores. Define primero una
pregunta con rango de fechas, cuenta y resultado esperado.

## Reglas de seguridad

1. Nunca escribas tokens, secretos, archivos JSON de OAuth ni llaves privadas
   dentro del repositorio.
2. Nunca pegues credenciales en el comando claude mcp add o codex mcp add.
3. Registra un launcher o paquete; configura la autenticación por separado.
4. Ejecuta el doctor del conector y acepta un estado unconfigured como una
   instalación limpia todavía sin cuenta.
5. Descubre las tools en el cliente después de instalar. Si la tool no aparece,
   no la inventes ni la sustituyas por un nombre recordado.

## Instalación por plataforma

### Meta Ads

El instalador de Kokoro copia un conector local de sólo lectura. Su launcher es:

    $HOME/.claude/kokoro/connectors/meta-ads/run.sh

El archivo local de credenciales se crea vacío, con permisos 0600, en:

    $HOME/.config/kokoro/meta-ads.env

Registra el mismo launcher en el cliente que uses:

    claude mcp add --scope user meta-ads -- "$HOME/.claude/kokoro/connectors/meta-ads/run.sh"
    codex mcp add meta-ads -- "$HOME/.claude/kokoro/connectors/meta-ads/run.sh"

Después completa únicamente tu archivo local y ejecuta:

    "$HOME/.claude/kokoro/connectors/meta-ads/doctor.sh"

Tools verificadas: list_ad_accounts, get_campaigns,
get_campaign_performance, get_campaign_status_and_budget,
get_demographic_breakdown, get_ad_creative_details,
get_account_insights_summary y get_all_accounts_overview.

### Google Ads

Fuente oficial:

    git+https://github.com/googleads/google-ads-mcp.git

Esta versión fija la revisión
f48a6b85e1f43ebd44a72531c9611e2b7265ca28 para que el salón instale el mismo
código:

    claude mcp add --scope user google-ads -- pipx run --spec git+https://github.com/googleads/google-ads-mcp.git@f48a6b85e1f43ebd44a72531c9611e2b7265ca28 google-ads-mcp
    codex mcp add google-ads -- pipx run --spec git+https://github.com/googleads/google-ads-mcp.git@f48a6b85e1f43ebd44a72531c9611e2b7265ca28 google-ads-mcp

Estos comandos registran el servidor; no configuran la cuenta. Completa ADC,
el acceso de Google Ads API y el developer token siguiendo la guía oficial,
sin guardar secretos en el repositorio.

Tools expuestas con la configuración por defecto:
customers_list_accessible_customers, metadata_get_resource_metadata y
search_search. search_search recibe customer_id, fields, resource, conditions,
orderings y limit; el servidor construye GAQL. No hay una superficie de
mutación prometida por este catálogo.

### Google Analytics 4

El servidor oficial experimental de Google Analytics se instala desde el
paquete fijado analytics-mcp==0.6.0:

    claude mcp add --scope user google-analytics -- pipx run --spec analytics-mcp==0.6.0 analytics-mcp
    codex mcp add google-analytics -- pipx run --spec analytics-mcp==0.6.0 analytics-mcp

Configura Application Default Credentials con alcance
analytics.readonly siguiendo la documentación oficial. Los comandos no deben
contener rutas privadas ni valores de credenciales.

Tools verificadas en el paquete fijado: get_account_summaries,
get_property_details, list_google_ads_links, list_property_annotations,
run_report, run_funnel_report, run_conversions_report,
get_custom_dimensions_and_metrics y run_realtime_report.

### Google Search Console

Estado contractual:

    status: not_bundled
    reason: no_verified_official_mcp

No instales un paquete por semejanza de nombre y no anuncies tools que no
fueron verificadas. Para esta versión recomienda una exportación de Search
Console, la interfaz oficial o un adaptador propio que pase revisión de
seguridad antes de incorporarse al catálogo.

## Catálogo por flujo

| Flujo | Plataforma | Tool o ruta |
|---|---|---|
| Descubrir cuentas publicitarias | Meta Ads | list_ad_accounts |
| Leer campañas Meta | Meta Ads | get_campaigns |
| Comparar rendimiento Meta | Meta Ads | get_campaign_performance |
| Descubrir clientes Google Ads | Google Ads | customers_list_accessible_customers |
| Consultar métricas Google Ads | Google Ads | search_search con campos, recurso y condiciones |
| Descubrir propiedades GA4 | Google Analytics 4 | get_account_summaries |
| Reporte histórico GA4 | Google Analytics 4 | run_report |
| Reporte en vivo GA4 | Google Analytics 4 | run_realtime_report |
| SEO orgánico | Google Search Console | no disponible por MCP en esta versión |

## Comportamiento fail-closed

- Si falta autenticación, reporta unconfigured y explica el siguiente paso.
- Si el servidor no responde, identifica la plataforma y continúa con las que
  sí están disponibles.
- Si una tool no aparece en el descubrimiento actual, no la llames.
- Si el usuario pide una mutación, prepara la recomendación y solicita que la
  ejecute en la interfaz oficial; no simules que fue aplicada.
- Nunca presentes una instalación limpia como una cuenta conectada.

## Cierre

Presenta al invitado:

1. qué conector quedó registrado;
2. qué autenticación sigue pendiente;
3. qué tools descubrió realmente el cliente;
4. una consulta de lectura pequeña para validar el recorrido completo.
