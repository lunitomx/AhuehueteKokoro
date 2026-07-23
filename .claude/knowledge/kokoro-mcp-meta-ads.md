<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# MCP Meta Ads — Conector público verificado

> Skill: /kokoro-mcp-reference
> Alcance: lectura y reportes; no muta campañas.

## Procedencia

Kokoro incluye un conector propio y auditable en connectors/meta-ads. Su
mantenedor es Ahuehuete Digital y su licencia es MIT. Usa el SDK oficial
facebook-business para consultar la Marketing API, pero no afirma ser un
servidor publicado ni mantenido por Meta.

El conector está limitado deliberadamente a ocho tools de lectura:

| Tool | Qué hace |
|---|---|
| list_ad_accounts | Lista cuentas publicitarias accesibles |
| get_campaigns | Lista campañas con filtros de lectura |
| get_campaign_performance | Consulta métricas por campaña y rango |
| get_campaign_status_and_budget | Lee estado y presupuesto |
| get_demographic_breakdown | Consulta desglose demográfico |
| get_ad_creative_details | Lee metadatos del creativo |
| get_account_insights_summary | Resume métricas de una cuenta |
| get_all_accounts_overview | Resume las cuentas accesibles |

Cada tool declara readOnlyHint=true y destructiveHint=false. Si el usuario
pide crear, editar, activar, pausar o eliminar algo, Kokoro prepara la
recomendación y remite a la interfaz oficial; no simula una mutación.

## Instalación

La instalación pública coloca el launcher en:

    $HOME/.claude/kokoro/connectors/meta-ads/run.sh

Y crea, sólo si no existe, un archivo vacío con permisos 0600:

    $HOME/.config/kokoro/meta-ads.env

Registra el launcher sin credenciales en línea:

    claude mcp add --scope user meta-ads -- "$HOME/.claude/kokoro/connectors/meta-ads/run.sh"
    codex mcp add meta-ads -- "$HOME/.claude/kokoro/connectors/meta-ads/run.sh"

La plantilla admite exactamente estos nombres:

    FACEBOOK_ACCESS_TOKEN
    FACEBOOK_APP_ID
    FACEBOOK_APP_SECRET

Completa los valores únicamente en el archivo local. No los copies al
repositorio, a un mensaje, al historial del shell ni al comando mcp add.

## Doctor

Ejecuta:

    "$HOME/.claude/kokoro/connectors/meta-ads/doctor.sh"

Estados esperados:

| Estado | Significado |
|---|---|
| unconfigured | El conector está instalado, pero faltan valores locales |
| configured | Están presentes los tres nombres requeridos |
| unsafe_configuration | El archivo es symlink, no es regular o no tiene modo 0600 |

El doctor sólo informa nombres faltantes y estado. Nunca imprime valores.

## Gate operativo

1. Ejecuta doctor.
2. Reinicia el cliente MCP si acabas de registrar el launcher.
3. Descubre las tools y confirma que aparecen las ocho de esta guía.
4. Empieza con list_ad_accounts.
5. Resuelve la cuenta correcta con el invitado.
6. Ejecuta una consulta pequeña y con rango explícito.

No describas configured como evidencia de acceso: la prueba real es una
consulta autorizada. No describas una consulta exitosa como permiso de
escritura: esta superficie es sólo lectura.

## Manejo de errores

- Sin configuración: explica qué nombres faltan, sin pedir los valores.
- Token expirado o sin permisos: indica que la persona debe renovar su acceso.
- Cuenta no visible: confirma que la cuenta pertenece al Business autorizado.
- Respuesta parcial: presenta lo obtenido y etiqueta lo faltante.
- Tool ausente: detente y vuelve a descubrir; no inventes aliases.
