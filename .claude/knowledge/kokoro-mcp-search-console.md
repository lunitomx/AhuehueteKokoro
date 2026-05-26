<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Google Search Console — Referencia de Herramientas

> Skill: `/kokoro-mcp-reference`
> Herramienta transversal: aplica en cualquier fase

## Plataforma

Google Search Console (GSC). 19 tools disponibles. Gestion de indexacion,
rendimiento organico, y sitemaps.

## Instalacion

Disponible como integracion nativa en Claude. Se activa conectando la cuenta
de Google desde la interfaz de Claude.

Si necesitas instalacion local:

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

Para obtener credenciales:
1. Google Cloud Console → crear service account
2. Search Console → agregar service account como propietario
3. Descargar JSON de credenciales

## Tools por Caso de Uso

### Gestion de Propiedades

| Tool | Que hace |
|------|----------|
| `list_properties` | Lista todos los sitios verificados en Search Console |
| `get_site_details` | Detalles de un sitio (URL, nivel de verificacion) |
| `add_site` | Agrega sitio nuevo a Search Console |
| `delete_site` | Elimina sitio de Search Console |
| `get_creator_info` | Informacion del creador/propietario |

### Rendimiento Organico (SEO)

| Tool | Que hace |
|------|----------|
| `get_search_analytics` | Datos de busqueda (clicks, impresiones, CTR, posicion) |
| `get_advanced_search_analytics` | Busqueda avanzada con filtros y dimensiones multiples |
| `get_search_by_page_query` | Rendimiento por pagina y query especifica |
| `get_performance_overview` | Vista general de rendimiento del sitio |
| `compare_search_periods` | Compara rendimiento entre dos periodos |

### Indexacion y Salud

| Tool | Que hace |
|------|----------|
| `inspect_url_enhanced` | Inspeccion detallada de URL (indexacion, mobile, rich results) |
| `batch_url_inspection` | Inspeccion masiva de multiples URLs |
| `check_indexing_issues` | Detecta problemas de indexacion en el sitio |

### Sitemaps

| Tool | Que hace |
|------|----------|
| `get_sitemaps` | Lista sitemaps registrados |
| `get_sitemap_details` | Detalles de un sitemap (URLs, errores) |
| `submit_sitemap` | Registra sitemap nuevo |
| `delete_sitemap` | Elimina sitemap registrado |
| `list_sitemaps_enhanced` | Lista mejorada con estado y errores |
| `manage_sitemaps` | Gestion completa de sitemaps |

## Flujos Comunes

### Auditoria SEO basica
1. `list_properties` → identificar sitio
2. `get_performance_overview` → rendimiento general
3. `get_search_analytics` con dimensiones query → keywords que traen trafico
4. `get_search_by_page_query` → que paginas rankean y para que queries
5. `check_indexing_issues` → problemas de indexacion

### Verificar lanzamiento de landing
1. `inspect_url_enhanced` con URL de landing → esta indexada?
2. Si no indexada → `submit_sitemap` con sitemap actualizado
3. Esperar y re-inspeccionar

### Comparar rendimiento antes/despues de cambio
1. `compare_search_periods` → periodo A vs periodo B
2. Identificar queries que mejoraron o empeoraron
3. Cruzar con cambios hechos en el sitio

### Diagnostico de caida de trafico
1. `get_performance_overview` → confirmar caida
2. `get_advanced_search_analytics` filtrado por fecha → cuando empezo
3. `check_indexing_issues` → problemas tecnicos?
4. `batch_url_inspection` en paginas principales → estan indexadas?

## Metricas Clave para Kokoro

| Metrica | Uso en Kokoro |
|---------|---------------|
| `clicks` | Trafico organico real |
| `impressions` | Visibilidad en busqueda |
| `ctr` | Efectividad del snippet (titulo + descripcion) |
| `position` | Posicion promedio en resultados |
