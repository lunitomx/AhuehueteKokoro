<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Google Search Console — Estado del conector

> Skill: /kokoro-mcp-reference

## Estado contractual

    status: not_bundled
    reason: no_verified_official_mcp
    trust: unavailable

Al 22 de julio de 2026 no se verificó un MCP oficial de Google para Search
Console que forme parte de esta distribución. Kokoro no incluye un servidor,
no instala un paquete y no garantiza nombres ni cantidad de tools.

Esto es una decisión fail-closed: un nombre plausible no es evidencia de
procedencia, mantenimiento ni seguridad.

## Rutas disponibles

Cuando el invitado necesite datos de Search Console, ofrece una de estas rutas:

1. exportación manual desde la interfaz oficial;
2. archivo CSV aportado por el invitado para análisis local;
3. consulta directa a la Search Console API mediante un adaptador propio;
4. revisión en la interfaz oficial para indexación o sitemaps.

Un adaptador futuro debe pasar antes:

- revisión de repositorio, mantenedor y licencia;
- inventario real de tools;
- política de sólo lectura o confirmación de mutaciones;
- configuración sin secretos versionados;
- doctor sin filtración de valores;
- instalación limpia en Claude y Codex;
- pruebas de humo y desinstalación.

## Comportamiento de los skills

- /kokoro-connect debe mostrar Search Console como no disponible por MCP y
  permitir registrar una propiedad sólo si el usuario aporta y confirma la URL.
- /kokoro-analytics debe pedir una exportación o explicar la ausencia del
  conector; nunca simular una consulta.
- /kokoro-scorecard debe marcar el bloque SEO como no consultado cuando no haya
  evidencia aportada.
- /kokoro-mcp-reference no debe recomendar paquetes no verificados.

## Métricas que puede contener una exportación

Una exportación válida puede incluir clicks, impressions, ctr y position por
fecha, consulta, página, país o dispositivo. Antes de interpretar:

1. confirma propiedad y rango;
2. conserva el archivo fuente;
3. distingue cero filas de error de exportación;
4. no infieras indexación a partir de impresiones solamente;
5. etiqueta cualquier dato faltante como no probado.
