<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Google Analytics 4 — Referencia de Herramientas

> Skill: `/kokoro-mcp-reference`
> Herramienta transversal: aplica en cualquier fase

## Plataforma

Google Analytics 4 (GA4). 7 tools disponibles. Lectura y reportes — no hay
tools de creacion/configuracion.

## Instalacion

Disponible como integracion nativa en Claude. Se activa conectando la cuenta
de Google desde la interfaz de Claude.

Si necesitas instalacion local:

```json
{
  "mcpServers": {
    "google-analytics": {
      "command": "npx",
      "args": ["-y", "@anthropic/google-analytics-mcp"],
      "env": {
        "GA4_CREDENTIALS": "<path-a-service-account.json>",
        "GA4_PROPERTY_ID": "<tu-property-id>"
      }
    }
  }
}
```

Para obtener credenciales:
1. Google Cloud Console → crear service account
2. GA4 Admin → agregar service account como viewer
3. Descargar JSON de credenciales

## Tools por Caso de Uso

### Estructura de Cuenta

| Tool | Que hace |
|------|----------|
| `get_account_summaries` | Lista todas las propiedades y cuentas GA4 accesibles |
| `get_property_details` | Detalles de una propiedad (nombre, timezone, moneda, tipo) |
| `get_custom_dimensions_and_metrics` | Dimensiones y metricas personalizadas configuradas |

### Reportes

| Tool | Que hace |
|------|----------|
| `run_report` | Ejecuta reporte con dimensiones, metricas, filtros y rango de fechas |
| `run_realtime_report` | Reporte en tiempo real (usuarios activos, eventos recientes) |

### Integraciones

| Tool | Que hace |
|------|----------|
| `list_google_ads_links` | Links entre GA4 y Google Ads (verificar integracion) |
| `list_property_annotations` | Anotaciones en la propiedad (marcadores de eventos) |

## Flujos Comunes

### Diagnostico de sitio web
1. `get_account_summaries` → identificar propiedad
2. `get_property_details` → verificar configuracion
3. `run_report` con dimensiones `pagePath`, metricas `sessions`, `bounceRate` → paginas principales
4. `run_report` con dimensiones `sessionSource`, `sessionMedium` → fuentes de trafico
5. `get_custom_dimensions_and_metrics` → verificar tracking personalizado

### Monitoreo en vivo
1. `run_realtime_report` → usuarios activos ahora
2. Verificar si campana recien lanzada esta generando trafico

### Verificar integracion Google Ads
1. `list_google_ads_links` → confirmar que GA4 esta conectado con Google Ads
2. Si no hay link → recomendar conectar para ver conversiones en Google Ads

## Metricas Clave para Kokoro

| Metrica | Uso en Kokoro |
|---------|---------------|
| `sessions` | Volumen de visitas |
| `totalUsers` | Personas unicas |
| `bounceRate` | Calidad de landing page |
| `averageSessionDuration` | Engagement |
| `conversions` | Resultados de negocio |
| `screenPageViews` | Paginas vistas |
| `eventCount` | Interacciones trackeadas |
