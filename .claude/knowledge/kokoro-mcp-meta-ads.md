<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Meta Ads — Referencia de Herramientas

> Skill: `/kokoro-mcp-reference`
> Herramienta transversal: aplica en cualquier fase

## Plataforma

Meta Ads (Facebook Ads + Instagram Ads). Dos MCP servers disponibles:
- **Claude AI MCP FB Ads** (oficial) — 28 tools, gestion completa
- **Facebook Ads** (third-party) — 8 tools, lectura y reportes

## Instalacion

### Claude AI MCP FB Ads (oficial)

Disponible como integracion nativa en Claude. No requiere instalacion local.
Se activa desde la interfaz de Claude conectando la cuenta de Meta Business.

### Facebook Ads (third-party)

Requiere configuracion en `settings.json` de Claude Code:

```json
{
  "mcpServers": {
    "facebook-ads": {
      "command": "npx",
      "args": ["-y", "@anthropic/facebook-ads-mcp"],
      "env": {
        "FB_ACCESS_TOKEN": "<tu-token>",
        "FB_APP_ID": "<tu-app-id>",
        "FB_APP_SECRET": "<tu-app-secret>"
      }
    }
  }
}
```

Para obtener el token: Meta Business Suite → Configuracion → Integraciones → Generar token.

## Tools por Caso de Uso

### Lectura y Reportes

| Tool | Server | Que hace |
|------|--------|----------|
| `ads_get_ad_accounts` | Oficial | Lista cuentas publicitarias del Business Manager |
| `ads_get_ad_entities` | Oficial | Lista campanas, ad sets o ads de una cuenta |
| `ads_insights_performance_trend` | Oficial | Tendencia de rendimiento en periodo |
| `ads_insights_industry_benchmark` | Oficial | Comparacion con benchmarks de industria |
| `ads_insights_auction_ranking_benchmarks` | Oficial | Ranking en subastas vs competidores |
| `ads_insights_anomaly_signal` | Oficial | Detecta anomalias en metricas |
| `ads_insights_advertiser_context` | Oficial | Contexto del anunciante para analisis |
| `get_account_insights_summary` | Third-party | Resumen de metricas de cuenta |
| `get_campaign_performance` | Third-party | Rendimiento por campana |
| `get_campaign_status_and_budget` | Third-party | Estado y presupuesto de campanas |
| `get_campaigns` | Third-party | Lista campanas con filtros |
| `get_demographic_breakdown` | Third-party | Desglose demografico de audiencia |
| `get_ad_creative_details` | Third-party | Detalles del creativo (imagen, copy, CTA) |
| `get_all_accounts_overview` | Third-party | Vista general de todas las cuentas |
| `list_ad_accounts` | Third-party | Lista cuentas publicitarias |

### Creacion y Gestion

| Tool | Server | Que hace |
|------|--------|----------|
| `ads_create_campaign` | Oficial | Crea campana nueva (objetivo, presupuesto, fechas) |
| `ads_create_ad_set` | Oficial | Crea ad set (audiencia, ubicaciones, puja) |
| `ads_create_ad` | Oficial | Crea anuncio (creativo, destino, CTA) |
| `ads_activate_entity` | Oficial | Activa campana, ad set o ad pausado |
| `ads_update_entity` | Oficial | Modifica cualquier entidad (presupuesto, audiencia, etc.) |

### Catalogos y Productos

| Tool | Server | Que hace |
|------|--------|----------|
| `ads_catalog_create` | Oficial | Crea catalogo de productos |
| `ads_catalog_get_catalogs` | Oficial | Lista catalogos existentes |
| `ads_catalog_get_details` | Oficial | Detalles de un catalogo |
| `ads_catalog_get_products` | Oficial | Lista productos del catalogo |
| `ads_catalog_get_product_details` | Oficial | Detalles de un producto |
| `ads_catalog_get_product_sets` | Oficial | Conjuntos de productos |
| `ads_catalog_get_product_set_products` | Oficial | Productos en un conjunto |
| `ads_catalog_get_product_feed_details` | Oficial | Detalles del feed de productos |
| `ads_catalog_get_feed_rules` | Oficial | Reglas del feed |
| `ads_catalog_get_diagnostics` | Oficial | Diagnostico del catalogo |

### Diagnostico y Datasets

| Tool | Server | Que hace |
|------|--------|----------|
| `ads_get_errors` | Oficial | Errores recientes en la cuenta |
| `ads_get_opportunity_score` | Oficial | Score de oportunidad (que mejorar) |
| `ads_get_dataset_details` | Oficial | Detalles de dataset (Conversions API) |
| `ads_get_dataset_quality` | Oficial | Calidad del dataset |
| `ads_get_dataset_stats` | Oficial | Estadisticas del dataset |
| `ads_get_help_article` | Oficial | Busca articulos de ayuda de Meta |
| `ads_get_pages_for_business` | Oficial | Paginas asociadas al Business Manager |

## Cuando Usar Cada Server

- **Oficial (Claude AI)**: Para crear, modificar o activar campanas. Para catalogos.
  Para benchmarks e insights avanzados. Conexion nativa, sin token manual.
- **Third-party**: Para reportes rapidos de rendimiento. Para vista general de
  multiples cuentas. Requiere token manual pero mas ligero.
