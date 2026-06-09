<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Google Ads — Referencia de Herramientas

> Skill: `/kokoro-mcp-reference`
> Herramienta transversal: aplica en cualquier fase

## Plataforma

Google Ads (Search, Display, Performance Max, YouTube). Surfaces de lectura disponibles en el servidor oficial.

## Instalacion

Requiere configuracion en `settings.json` de Claude Code:

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "uvx",
      "args": ["google-ads-mcp-server"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "<tu-developer-token>",
        "GOOGLE_ADS_CLIENT_ID": "<tu-client-id>",
        "GOOGLE_ADS_CLIENT_SECRET": "<tu-client-secret>",
        "GOOGLE_ADS_REFRESH_TOKEN": "<tu-refresh-token>",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "<tu-manager-id>"
      }
    }
  }
}
```

Para obtener credenciales:
1. Google Ads API Center → solicitar developer token
2. Google Cloud Console → crear OAuth 2.0 credentials
3. Generar refresh token con el flujo OAuth

## Tools por Caso de Uso

### Lectura y Reportes

| Tool | Que hace |
|------|----------|
| `list_customers` | Lista cuentas de Google Ads bajo el manager |
| `get_campaigns` | Lista campanas con estado y tipo |
| `get_campaign_performance` | Metricas de rendimiento (clicks, impresiones, costo, conversiones) |
| `get_campaign_status_and_budget` | Estado actual y presupuesto de campanas |
| `get_customer_insights_summary` | Resumen general de la cuenta |
| `get_demographic_breakdown` | Rendimiento por edad, genero, dispositivo |
| `get_geographic_breakdown` | Rendimiento por ubicacion geografica |
| `get_keywords_performance` | Rendimiento de keywords (CTR, CPC, Quality Score) |
| `get_search_terms` | Terminos de busqueda reales que activaron los ads |
| `get_ad_details` | Detalles de un anuncio especifico |
| `execute_gaql` | Ejecuta consultas GAQL personalizadas (avanzado) |

### Creacion y Gestion

| Tool | Que hace |
|------|----------|
| `create_search_campaign` | Crea campana de busqueda nueva |
| `create_campaign_budget` | Crea presupuesto para campana |
| `create_ad_group` | Crea grupo de anuncios dentro de campana |
| `create_responsive_search_ad` | Crea anuncio de busqueda responsivo |
| `set_campaign_status` | Cambia estado (activo, pausado, eliminado) |

### Targeting y Optimizacion

| Tool | Que hace |
|------|----------|
| `add_keywords` | Agrega keywords a un grupo de anuncios |
| `add_negative_keywords` | Adapter local Kokoro para exclusiones; el servidor oficial solo expone lectura/discovery |
| `delete_negative_keywords` | Adapter local Kokoro; elimina negativas con idempotencia, auditoría y estados parciales |
| `set_language_targeting` | Configura idiomas objetivo |
| `set_location_targeting` | Configura ubicaciones objetivo (paises, ciudades, radios) |

## Flujos Comunes

### Auditar campana existente
1. `list_customers` → identificar cuenta
2. `get_campaigns` → ver campanas activas
3. `get_campaign_performance` → metricas generales
4. `get_keywords_performance` → rendimiento de keywords
5. `get_search_terms` → que busca la gente realmente
6. `get_geographic_breakdown` → donde estan los resultados

### Crear campana nueva
1. `create_campaign_budget` → definir presupuesto
2. `create_search_campaign` → crear campana
3. `create_ad_group` → crear grupo de anuncios
4. `add_keywords` → agregar keywords
5. `create_responsive_search_ad` → crear anuncio
6. `set_location_targeting` → definir ubicaciones
7. `set_language_targeting` → definir idiomas
