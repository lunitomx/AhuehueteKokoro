# /kokoro-mcp-reference — Guía de Instalación y Catálogo de Tools MCP

> Herramienta transversal: aplica en cualquier fase
> Skills relacionados: `/kokoro-connect` (conectar plataformas), `/kokoro-analytics` (consultar métricas)

> "Antes de conectar, saber qué conectar. Antes de preguntar, saber qué preguntar."

## Contexto

Este skill guía al invitado en la instalación y uso de los MCP servers de
marketing digital. No es una API reference — es un mapa de herramientas por
caso de uso, para que Kokoro (y el invitado) sepan exactamente qué tool usar
en cada momento.

Lee `kokoro-tactiq-field-patterns.md` para priorizar MCPs por necesidad real:
lectura de pauta, atribucion, seguimiento, landing, CRM y reporting semanal.

### Plataformas cubiertas

| Plataforma | MCP Server | Tools |
|------------|------------|-------|
| Meta Ads | Claude AI MCP FB Ads (oficial) + Facebook Ads (third-party) | 28 + 8 |
| Google Ads | google-ads-mcp-server (uvx) | 20 |
| Google Analytics 4 | Claude integración nativa o @anthropic/google-analytics-mcp | 7 |
| Google Search Console | Claude integración nativa o @anthropic/google-search-console-mcp | 19 |

---

## Paso 1 — Identificar qué Necesita el Invitado

### Gate Tactiq 2025 — tool por decision

Antes de recomendar instalar un MCP, pide la decision que se quiere mejorar:

- Si el dolor es pauta, prioriza Meta Ads o Google Ads con lectura de campana.
- Si el dolor es landing o trafico, prioriza GA4 y Search Console.
- Si el dolor es seguimiento, aclara que falta CRM/WhatsApp/pipeline aunque
  los MCPs de marketing esten conectados.
- Si solo hay curiosidad tecnica, convierte la instalacion en un caso de uso
  verificable con input, output y responsable.

Pregunta al invitado qué quiere hacer antes de recomendar un MCP server.
Usa estas preguntas para guiar la conversación:

| Si el invitado quiere... | Plataforma recomendada | Tools clave |
|--------------------------|------------------------|-------------|
| Crear o modificar campañas de Meta/FB/IG | Meta Ads (oficial) | `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad` |
| Ver rendimiento de campañas Meta | Meta Ads (cualquier server) | `ads_insights_performance_trend`, `get_campaign_performance` |
| Comparar benchmarks de industria en Meta | Meta Ads (oficial) | `ads_insights_industry_benchmark`, `ads_insights_auction_ranking_benchmarks` |
| Gestionar catálogos de productos en Meta | Meta Ads (oficial) | `ads_catalog_create`, `ads_catalog_get_products` |
| Crear campañas de Google Search | Google Ads | `create_search_campaign`, `create_responsive_search_ad` |
| Auditar keywords y términos de búsqueda | Google Ads | `get_keywords_performance`, `get_search_terms` |
| Ver métricas de tráfico web | GA4 | `run_report`, `run_realtime_report` |
| Monitorear conversiones en vivo | GA4 | `run_realtime_report` |
| Auditar SEO orgánico | Search Console | `get_search_analytics`, `check_indexing_issues` |
| Verificar indexación de una landing | Search Console | `inspect_url_enhanced` |
| Comparar rendimiento SEO entre periodos | Search Console | `compare_search_periods` |

---

## Paso 2 — Guía de Instalación por Plataforma

Para cada plataforma, el skill referencia el knowledge file correspondiente
y guía al invitado paso a paso.

### Meta Ads

> Knowledge file: `kokoro-mcp-meta-ads.md`

**Opción A — Claude AI integración nativa:**
1. Abrir Claude Desktop
2. Ir a Settings → Integrations → Meta Ads
3. Conectar cuenta de Meta Business
4. Sin configuración adicional — funciona inmediatamente

**Opción B — Third-party (Claude Code):**
1. Agregar a `settings.json`:
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
2. Obtener token: Meta Business Suite → Configuración → Integraciones → Generar token
3. Obtener App ID y Secret: Meta for Developers → crear app → credenciales

**Cuándo usar cada opción:**
- Opción A para crear y gestionar campañas (oficial tiene más tools de escritura)
- Opción B para reportes rápidos y vista multi-cuenta

---

### Google Ads

> Knowledge file: `kokoro-mcp-google-ads.md`

1. Agregar a `settings.json`:
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
2. Solicitar developer token en Google Ads API Center
3. Crear OAuth 2.0 credentials en Google Cloud Console
4. Generar refresh token con flujo OAuth
5. Obtener Manager ID desde Google Ads → Configuración → Acceso y seguridad

---

### Google Analytics 4

> Knowledge file: `kokoro-mcp-ga4.md`

**Opción A — Claude integración nativa:**
1. Conectar cuenta de Google desde Claude Desktop
2. GA4 disponible inmediatamente

**Opción B — Claude Code:**
1. Agregar a `settings.json`:
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
2. Crear service account en Google Cloud Console
3. Agregar como viewer en GA4 Admin
4. Descargar JSON de credenciales

---

### Google Search Console

> Knowledge file: `kokoro-mcp-search-console.md`

**Opción A — Claude integración nativa:**
1. Conectar cuenta de Google desde Claude Desktop
2. Search Console disponible inmediatamente

**Opción B — Claude Code:**
1. Agregar a `settings.json`:
```json
{
  "mcpServers": {
    "google-search-console": {
      "command": "npx",
      "args": ["-y", "@anthropic/google-search-console-mcp"],
      "env": {
        "GSC_CREDENTIALS": "<path-a-service-account.json>"
      }
    }
  }
}
```
2. Crear service account en Google Cloud Console
3. Agregar como owner en Search Console
4. Descargar JSON de credenciales

---

## Paso 3 — Catálogo de Tools por Workflow Transversal

Cuando Kokoro necesita una herramienta MCP, este catálogo ayuda a encontrar
la correcta por contexto de trabajo, no por plataforma.

### Diagnóstico y Auditoría

| Qué necesitas | Plataforma | Tool |
|---------------|------------|------|
| Diagnóstico de tráfico web | GA4 | `run_report` (sessions, sources, bounce) |
| Diagnóstico de SEO orgánico | Search Console | `get_search_analytics` + `check_indexing_issues` |
| Auditoría de campañas Meta | Meta Ads | `ads_insights_performance_trend` + `ads_get_opportunity_score` |
| Auditoría de campañas Google | Google Ads | `get_campaign_performance` + `get_keywords_performance` |
| Calidad de tracking | Meta Ads | `ads_get_dataset_quality` |
| Comparativa con industria | Meta Ads | `ads_insights_industry_benchmark` |

### Creación y Optimización

| Qué necesitas | Plataforma | Tool |
|---------------|------------|------|
| Crear campaña Meta | Meta Ads | `ads_create_campaign` → `ads_create_ad_set` → `ads_create_ad` |
| Crear campaña Google | Google Ads | `create_campaign_budget` → `create_search_campaign` → `create_ad_group` → `create_responsive_search_ad` |
| Optimizar keywords Google | Google Ads | `add_keywords` + `add_negative_keywords` |
| Activar/pausar entidades Meta | Meta Ads | `ads_activate_entity` |
| Cambiar presupuesto Meta | Meta Ads | `ads_update_entity` |
| Gestionar catálogos Meta | Meta Ads | `ads_catalog_create` + `ads_catalog_get_products` |

### Monitoreo y Alertas

| Qué necesitas | Plataforma | Tool |
|---------------|------------|------|
| Tráfico en vivo del sitio | GA4 | `run_realtime_report` |
| Anomalías en métricas Meta | Meta Ads | `ads_insights_anomaly_signal` |
| Rendimiento en tiempo real Google | Google Ads | `get_campaign_performance` |
| Comparar periodos SEO | Search Console | `compare_search_periods` |

---

## Notas para Claude

- **Siempre preguntar qué necesita el invitado antes de recomendar un MCP.**
  No asumir plataforma.
- El knowledge file de cada plataforma tiene la referencia completa de tools.
  Este skill es la guía de instalación + el mapa de decisión.
- Si el invitado ya tiene MCPs instalados, usar `/kokoro-connect` para
  verificar el estado de conexión.
- Vocabulario Eduardo: invitado (no cliente), compartir (no vender),
  reto/oportunidad (no problema), inversión (no precio).
