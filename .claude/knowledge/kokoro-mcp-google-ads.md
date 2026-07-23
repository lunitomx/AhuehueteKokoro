<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Google Ads — Servidor oficial verificado

> Skill: /kokoro-mcp-reference
> Alcance verificado: consulta y descubrimiento.

## Procedencia

El servidor recomendado proviene de:

    https://github.com/googleads/google-ads-mcp

Está mantenido bajo la organización Google Ads y tiene licencia Apache-2.0.
Kokoro fija la revisión
f48a6b85e1f43ebd44a72531c9611e2b7265ca28 para evitar que un cambio remoto
altere el taller sin revisión.

Fuente de instalación:

    git+https://github.com/googleads/google-ads-mcp.git

## Superficie verificada

| Tool | Qué hace |
|---|---|
| customers_list_accessible_customers | Devuelve IDs de cuentas accesibles directamente |
| metadata_get_resource_metadata | Describe recursos y campos de Google Ads API |
| search_search | Ejecuta una consulta estructurada sobre una cuenta |

Los prefijos vienen del tools_config.yaml predeterminado del proveedor. Si la
persona personaliza los namespaces, debe volver a descubrir las tools y usar
los nombres realmente expuestos. El servidor también publica recursos para
métricas,
segmentos, notas de versión y el discovery document.

Esta referencia no promete herramientas de escritura. Para cambiar
presupuestos, estados, anuncios, keywords o segmentación, Kokoro prepara una
propuesta y pide realizarla en la interfaz oficial o mediante un adaptador
separado con aprobación explícita.

## Instalación reproducible

Instala pipx y registra la revisión fijada:

    claude mcp add --scope user google-ads -- pipx run --spec git+https://github.com/googleads/google-ads-mcp.git@f48a6b85e1f43ebd44a72531c9611e2b7265ca28 google-ads-mcp
    codex mcp add google-ads -- pipx run --spec git+https://github.com/googleads/google-ads-mcp.git@f48a6b85e1f43ebd44a72531c9611e2b7265ca28 google-ads-mcp

Registrar el proceso no autoriza una cuenta. La persona todavía debe:

1. habilitar Google Ads API en su proyecto;
2. obtener un developer token con acceso suficiente;
3. configurar Application Default Credentials con alcance adwords;
4. definir el proyecto y, si aplica, el login customer ID;
5. mantener todo secreto fuera del repositorio.

Sigue la guía del repositorio oficial para autenticación. No pegues developer
tokens, secretos OAuth ni contenido de google-ads.yaml dentro de comandos,
documentación o archivos versionados.

## Flujos de lectura

### Descubrir cuentas

1. Llama customers_list_accessible_customers.
2. Confirma con el invitado qué customer ID corresponde.
3. Si el acceso depende de una cuenta manager, confirma también el login
   customer ID en la configuración local.

### Consultar campañas

Usa search_search con parámetros estructurados. Para una lectura por rango explícito,
solicita campos concretos y filtra segments.date con fechas absolutas:

    customer_id: "1234567890"
    fields:
      - campaign.id
      - campaign.name
      - campaign.status
      - metrics.impressions
      - metrics.clicks
      - metrics.cost_micros
      - metrics.conversions
    resource: campaign
    conditions:
      - "segments.date BETWEEN '2026-07-01' AND '2026-07-07'"

No describas una etiqueta temporal como si fuera una fecha exacta. Si la
pregunta pide días concretos, usa días concretos.

### Descubrir campos

Usa metadata_get_resource_metadata antes de inventar un nombre de campo. Si
Google Ads rechaza la consulta:

1. reduce la selección;
2. valida recurso y campos;
3. conserva el rango exacto en conditions;
4. reporta el error sin exponer configuración.

## Gate de verdad

- Servidor instalado no significa cuenta autorizada.
- Cuenta listada no significa que todas las subcuentas sean accesibles.
- Una consulta vacía significa cero filas para ese filtro, no una falla.
- Conversiones y all_conversions no son equivalentes; explica cuál consultaste.
- Nunca afirmes que una mutación ocurrió sin evidencia de la interfaz o API que
  la ejecutó.
