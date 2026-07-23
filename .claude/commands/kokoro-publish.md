# /kokoro-publish — Preparar Publicación en Meta Ads

> Herramienta transversal: handoff seguro de creativos.
>
> "La creación está lista cuando puede compartirse sin perder su intención."

## Verdad operativa

El conector público `meta-ads` es de sólo lectura. Este skill no sube
imágenes, no crea anuncios y no modifica Meta Ads. Prepara un paquete de
publicación, valida el destino con datos de lectura y acompaña al usuario para
que publique en Ads Manager.

Nunca afirmes "publicado" por haber generado un archivo. La publicación sólo
queda confirmada cuando el usuario aporta evidencia de Ads Manager o un ID
creado por una integración externa autorizada.

## Dependencias

- Output de /kokoro-ads o /kokoro-creative.
- Cuenta Meta mapeada o elegida por el usuario.
- Conector `meta-ads` opcional para listar campañas existentes.
- Acceso humano a Meta Ads Manager para ejecutar la publicación.

No solicita ni almacena tokens. No requiere permisos de escritura para el
conector de Kokoro.

## Alcance

Este skill puede:

- reunir copy, imagen, URL, CTA y nombre sugerido;
- leer campañas con `get_campaigns`;
- mostrar un preview completo;
- producir una lista de pasos para Ads Manager;
- registrar evidencia aportada después de publicar.

Este skill no puede:

- subir archivos a Meta;
- crear o editar creativos;
- tocar presupuesto, targeting, audiencias o estados;
- eliminar anuncios;
- validar una publicación sin evidencia.

## Proceso

### Paso 1 — Resolver invitado y artefactos

Busca el invitado en `.kokoro/clients.json` y lee
`metadata.platform_accounts.meta_ads`. Localiza los outputs de
/kokoro-ads o /kokoro-creative. Si no existe una creación lista, regresa al
skill que la produce.

Presenta todos los archivos encontrados y pide elegir uno. No mezcles versiones
sin aprobación.

### Paso 2 — Confirmar destino

Si `meta-ads` está configurado, usa:

    get_campaigns(account_id="{act_XXXX}")

Presenta nombre, ID y estado de las campañas. El conector no lista ad sets, así
que pide al usuario elegir el ad set directamente en Ads Manager. Si el MCP no
está disponible, solicita cuenta, campaña y ad set sin fingir descubrimiento.

### Paso 3 — Preview obligatorio

Muestra:

- cuenta y campaña;
- ad set indicado por el usuario;
- nombre propuesto;
- archivo y dimensiones;
- título, texto principal, CTA y URL;
- cualquier campo todavía pendiente.

Pregunta: "¿Este es exactamente el paquete que quieres llevar a Ads Manager?"
Sin un sí explícito, vuelve a editar el paquete.

### Paso 4 — Handoff a Ads Manager

Entrega una secuencia manual:

1. abrir la cuenta y campaña confirmadas;
2. elegir el ad set;
3. crear o editar el anuncio en la interfaz oficial;
4. subir el archivo elegido;
5. copiar título, texto, CTA y URL del preview;
6. revisar tracking y vista previa;
7. publicar desde Ads Manager;
8. devolver el ad ID o una captura sin datos sensibles.

No pidas screenshots que muestren tokens, facturación, datos personales o
credenciales.

### Paso 5 — Aceptación y registro

Estados válidos:

| Estado | Evidencia |
|---|---|
| Preparado | Preview y paquete completos |
| Pendiente de publicación | Handoff entregado, sin evidencia de Ads Manager |
| Publicado confirmado | El usuario aporta ad ID o captura válida |
| Bloqueado | Falta destino, artefacto o acceso humano |

Registra `Publicado confirmado` sólo con evidencia. Si el usuario no regresa
con ella, conserva `Pendiente de publicación`.

## Plantilla de salida

```
## Paquete de Publicación Meta Ads — {invitado}

| Campo | Valor |
|---|---|
| Estado | Preparado / Pendiente / Publicado confirmado / Bloqueado |
| Cuenta | {account_id} |
| Campaña | {campaign_name} |
| Ad set | {valor confirmado o pendiente} |
| Archivo | {ruta} |
| Título | {headline} |
| CTA | {cta} |
| URL | {destination_url} |

### Texto principal

{copy completo}

### Evidencia

{ad ID, captura válida o "pendiente"}

### Siguiente paso

{acción humana exacta en Ads Manager o verificación posterior}
```

## Anti-patrones

- No declarar que una acción de plataforma ocurrió por intención.
- No pedir secretos para "desbloquear" publicación.
- No llamar tools que no aparecen en el descubrimiento actual.
- No cambiar inversión ni segmentación dentro de este skill.
- No adjuntar evidencia con datos sensibles.

## Cierre

La creación puede quedar lista aunque la publicación siga pendiente. Nombra
ambos estados por separado: eso protege al invitado y conserva la verdad del
proceso.
