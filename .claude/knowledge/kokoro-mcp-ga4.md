<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Google Analytics 4 — Servidor oficial experimental

> Skill: /kokoro-mcp-reference
> Alcance: lectura de propiedades y reportes GA4.

## Procedencia

La fuente verificada es:

    https://github.com/googleanalytics/google-analytics-mcp

El repositorio pertenece a la organización Google Analytics, usa licencia
Apache-2.0 y describe el servidor como experimental. Esta versión pública fija:

    analytics-mcp==0.6.0

No sustituyas ese paquete por otro con nombre parecido.

## Tools verificadas

| Tool | Qué hace |
|---|---|
| get_account_summaries | Lista cuentas y propiedades accesibles |
| get_property_details | Lee detalles de una propiedad |
| list_google_ads_links | Lista vínculos entre GA4 y Google Ads |
| list_property_annotations | Lee anotaciones de una propiedad |
| run_report | Ejecuta un reporte histórico |
| run_funnel_report | Ejecuta un reporte de embudo |
| run_conversions_report | Ejecuta un reporte enfocado en conversiones |
| get_custom_dimensions_and_metrics | Lee dimensiones y métricas personalizadas |
| run_realtime_report | Ejecuta un reporte en tiempo real |

La superficie verificada es de lectura. No promete cambiar la configuración de
GA4.

## Instalación

Instala pipx y registra el paquete fijado:

    claude mcp add --scope user google-analytics -- pipx run --spec analytics-mcp==0.6.0 analytics-mcp
    codex mcp add google-analytics -- pipx run --spec analytics-mcp==0.6.0 analytics-mcp

Después configura Application Default Credentials con el alcance:

    https://www.googleapis.com/auth/analytics.readonly

También deben estar habilitadas Google Analytics Admin API y Google Analytics
Data API. Sigue el README oficial para el proyecto de Google Cloud. No guardes
el JSON de OAuth, rutas privadas ni secretos en el repositorio.

## Flujos de lectura

### Descubrir propiedad

1. Usa get_account_summaries.
2. Presenta cuentas y propiedades sin elegir por el invitado.
3. Confirma el property ID.
4. Usa get_property_details para validar zona horaria y moneda.

### Reporte histórico

Usa run_report con `date_ranges`, métricas y dimensiones explícitas. Cada
rango es un objeto con `start_date` y `end_date`. Empieza con una consulta
pequeña. Si una métrica no existe, consulta
get_custom_dimensions_and_metrics antes de corregir el nombre.

### Tiempo real

Usa run_realtime_report sólo para actividad reciente. No lo mezcles con un
periodo histórico ni afirmes que una señal en vivo prueba una conversión.

### Embudos

Usa run_funnel_report cuando el usuario haya definido pasos observables. Si
faltan eventos o tracking, reporta la brecha; no inventes etapas.

Usa run_conversions_report sólo cuando exista una definición verificable de la
conversión. Una métrica con ese nombre no prueba por sí sola una venta.

## Gate de verdad

- Instalado no significa autenticado.
- Autenticado no significa acceso a todas las propiedades.
- Un evento no significa ingreso ni venta.
- Una atribución de GA4 no sustituye la fuente comercial o CRM.
- Al ser experimental, vuelve a descubrir las tools después de actualizar.
