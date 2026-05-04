<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Plataformas Digitales — Referencia para /kokoro-connect

> Skill: `/kokoro-connect`
> Herramienta transversal: onboarding de cuentas de plataformas

> "Cada plataforma es una ventana distinta al mismo paisaje. Conectarlas
> te da la vista panoramica desde la montana."

## Proposito

Referencia tecnica para el skill `/kokoro-connect`. Documenta los servidores
MCP disponibles, las herramientas de descubrimiento, los formatos de ID de
cada plataforma, y la estructura de persistencia en el modelo de invitado.

## Plataformas Soportadas

| Plataforma | Servidor MCP | Herramienta de Descubrimiento | Formato de ID | Ejemplo |
|------------|-------------|-------------------------------|---------------|---------|
| Meta Ads | `facebook-ads` | `mcp__facebook-ads__list_ad_accounts` | `act_XXXX` | `act_123456789` |
| Google Ads | `google-ads` | `mcp__google-ads__list_customers` | 10 digitos | `1234567890` |
| GA4 | `google-analytics` | `mcp__google-analytics__get_account_summaries` | `properties/XXXX` | `properties/123456` |
| GSC | `google-search-console` | `mcp__google-search-console__list_properties` | URL del sitio | `https://ejemplo.com` |

## Convenciones por Plataforma

### Meta Ads

- Los IDs de cuenta siempre comienzan con `act_` seguido de digitos
- Una cuenta de negocio puede tener multiples cuentas publicitarias
- La herramienta `list_ad_accounts` devuelve todas las cuentas accesibles
  con el token configurado
- Clave en metadata: `meta_ads`

### Google Ads

- Los IDs de cuenta son 10 digitos sin guiones (formato interno)
- En la interfaz de Google se muestran como `XXX-XXX-XXXX` pero se almacenan
  sin guiones
- La herramienta `list_customers` devuelve las cuentas accesibles
- Clave en metadata: `google_ads`

### GA4 (Google Analytics 4)

- Los IDs de propiedad usan el formato `properties/XXXXXX`
- Una cuenta de Google Analytics puede tener multiples propiedades
- La herramienta `get_account_summaries` devuelve cuentas con sus propiedades
- Clave en metadata: `ga4`

### GSC (Google Search Console)

- Los IDs son la URL del sitio verificado (con protocolo)
- Puede ser un dominio (`sc-domain:ejemplo.com`) o una URL prefix
  (`https://ejemplo.com`)
- La herramienta `list_properties` devuelve todos los sitios verificados
- Clave en metadata: `gsc`

## Estructura de Persistencia

Las cuentas se guardan en `ClientProfile.metadata["platform_accounts"]`:

```json
{
  "platform_accounts": {
    "meta_ads": "act_123456789",
    "google_ads": "1234567890",
    "ga4": "properties/123456",
    "gsc": "https://ejemplo.com"
  }
}
```

### Reglas de Persistencia

- Solo se guardan las plataformas que el invitado tiene activas
- Si una plataforma no se conecta, no se incluye la clave (no se guarda null)
- Re-ejecutar `/kokoro-connect` actualiza los valores existentes
- Es posible conectar una plataforma sin conectar las demas

## Degradacion Elegante

No todos los servidores MCP estaran disponibles en todo momento. El skill
debe manejar la indisponibilidad con gracia:

1. **Servidor no configurado** — Informar que el servidor no esta registrado
   y sugerir `/rai-mcp-add` para configurarlo
2. **Servidor no responde** — Reportar el error, continuar con los demas
3. **Sin cuentas accesibles** — Informar que el token no tiene acceso a
   cuentas en esa plataforma, sugerir verificar permisos
4. **Error de autenticacion** — Reportar que las credenciales necesitan
   actualizarse, continuar con las demas plataformas

En cualquier caso, nunca detener el proceso completo por una sola plataforma
que falle. Conectar lo que se pueda, reportar lo que no.
