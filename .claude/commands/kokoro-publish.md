# /kokoro-publish — Publicar Creativos en Meta Ads

> Herramienta transversal: Publicacion de contenido creativo
> Aplica despues de /kokoro-ads o /kokoro-creative

> "El arte no existe hasta que se comparte. La creacion no vive hasta
> que encuentra a su invitado."

## Contexto

Este skill toma el output de `/kokoro-ads` o `/kokoro-creative` y lo
publica directamente en una campana de Meta Ads. SOLO sube contenido
creativo — NUNCA toca presupuesto, targeting, ni estado de campanas.

### Dependencias

- **MCP facebook-ads**: Server con write tools habilitados
  - `create_ad_creative` — crear creativo nuevo
  - `update_ad_creative_text` — actualizar titulo/texto
  - `upload_ad_image` — subir imagen
- **Token con scope `ads_management`**: Verificar con S17.1

### Scope HARDCODEADO — No negociable

**PUEDE hacer:**
- Subir imagenes a Meta Ads
- Crear/actualizar titulos y textos de anuncios
- Preview antes de publicar

**NUNCA puede hacer (HARDCODED):**
- Tocar presupuesto (daily_budget, lifetime_budget)
- Pausar/activar campanas o ad sets
- Modificar targeting o audiencias
- Crear campanas nuevas (solo creativos dentro de existentes)
- Eliminar anuncios

Si el usuario pide cualquier operacion prohibida:
> "Esa operacion esta fuera del alcance de Kokoro por diseno. Los
> presupuestos y el estado de campanas se gestionan directamente en
> Meta Ads Manager. Kokoro solo toca creativos — asi protegemos tu
> inversion."

### Resolucion de invitado

1. Busca en `.kokoro/clients.json`
2. Si encuentra al invitado:
   - Lee `metadata["platform_accounts"]` para Meta Ads account ID
   - Si no tiene account → sugiere `/kokoro-connect` primero
   - Presenta: "Invitado: {name} | Cuenta: {account_name} ({account_id})"
3. Si NO encuentra:
   - Sugiere registrar con `/kokoro-client` primero

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Tienes creativos listos. Vamos a subirlos a tu campana de Meta Ads.
> Antes de publicar cualquier cosa, te muestro EXACTAMENTE que se va
> a subir y tu me das la luz verde. ¿Procedemos?"

### Proceso — 5 pasos EN ORDEN

### Paso 1: Identificar el contenido a publicar

Buscar el ultimo output de /kokoro-ads o /kokoro-creative:
- Archivos en `clientes/{grupo}/{nombre}/campanas/meta-ads/creativo-*.txt`
- Imagenes generadas en la misma carpeta

Si no hay output reciente, preguntar:
> "No encuentro creativos recientes. ¿Quieres generar contenido primero
> con `/kokoro-ads` (copy) o `/kokoro-creative` (imagenes)?"

Presentar lo que se encontro:
```
Creativos disponibles para publicar:
1. creativo-01-mamas.txt (copy: 5 titulos, 5 textos, WhatsApp, Advantage+)
2. creativo-02-profesionales.txt (copy: 5 titulos, 5 textos)
3. generated-01-mamas-cuadrado.png (1080x1080)
4. generated-01-mamas-vertical.png (1080x1920)
...

¿Cual quieres publicar?
```

### Paso 2: Seleccionar destino

Listar campanas activas del invitado:
```
Usa el MCP tool `get_campaigns` con el account_id del invitado
```

Presentar:
```
Campanas activas en {account_name}:

| # | Campana | Status | Ad Sets |
|---|---------|--------|---------|
| 1 | {nombre} | Active | {N} |
| 2 | {nombre} | Active | {N} |

¿A cual campana va este creativo?
```

Despues de elegir campana, listar ad sets:
> "¿A cual ad set dentro de '{campana}' publico el creativo?"

### Paso 3: Preview — GATE OBLIGATORIO

Mostrar EXACTAMENTE lo que se va a publicar:

```
## Preview — Confirmacion requerida

### Destino
| Campo | Valor |
|-------|-------|
| Cuenta | {account_name} ({account_id}) |
| Campana | {campaign_name} |
| Ad Set | {adset_name} |

### Contenido a publicar
| Campo | Valor |
|-------|-------|
| Imagen | {filename} ({dimensions}) |
| Titulo | {headline seleccionado} |
| Texto | {primary text seleccionado} |
| CTA | {call to action} |
| Link | {destination URL} |

### Vista previa del texto
---
{titulo}

{texto principal completo}

{CTA}
---

⚠ CONFIRMA: ¿Publico esto exactamente como se ve arriba? (si/no)
```

**SOLO ejecutar con "si" explicito del usuario.**
Si el usuario dice "no", preguntar que quiere ajustar.

### Paso 4: Publicar

Con confirmacion explicita, ejecutar en orden:

1. **Subir imagen** (si aplica):
```
MCP: upload_ad_image(account_id, image_path)
→ Retorna image_hash
```

2. **Crear creativo**:
```
MCP: create_ad_creative(
  account_id="{account_id}",
  name="{nombre descriptivo}",
  image_hash="{hash de paso 1}",
  title="{titulo seleccionado}",
  body="{texto principal seleccionado}",
  link_url="{URL destino}"
)
→ Retorna creative_id
```

3. **Confirmar publicacion**:
> "Creativo publicado exitosamente.
> - Creative ID: {creative_id}
> - Imagen: subida ({image_hash})
> - Titulo: {titulo}
> - En campana: {campaign_name} → {adset_name}"

### Paso 5: Verificar y documentar

Despues de publicar, verificar que el creativo aparece:
```
MCP: get_ad_creative_details(creative_id)
```

Guardar registro en el archivo de campaña:
```
Apendice al archivo creativo-{NN}-{slug}.txt:

PUBLICACION META ADS
--------------------
Fecha: {YYYY-MM-DD HH:MM}
Creative ID: {creative_id}
Campana: {campaign_name}
Ad Set: {adset_name}
Cuenta: {account_id}
Status: Publicado
```

## Modo batch — Multiples creativos

Si el usuario quiere publicar multiples creativos:

1. Mostrar preview de TODOS antes de publicar
2. Confirmar el batch completo
3. Publicar secuencialmente
4. Presentar resumen final:

```
## Publicacion batch completada

| # | Titulo | Campana | Ad Set | Status |
|---|--------|---------|--------|:------:|
| 1 | {titulo} | {campana} | {adset} | OK |
| 2 | {titulo} | {campana} | {adset} | OK |

Todos los creativos publicados exitosamente.
```

## Manejo de Errores

### Token sin permisos de escritura
"El token de Facebook no tiene permisos de escritura (ads_management).
Necesitas re-autorizar la app con el scope correcto. Contacta al admin
de cliente_07 para actualizar el token."

### MCP write tools no disponibles
"Los tools de escritura no estan habilitados en el MCP de facebook-ads.
Esto requiere actualizar el server en cliente_07 (S17.2). Por ahora,
copia el contenido manualmente a Meta Ads Manager."

### Error al subir imagen
"No pude subir la imagen a Meta Ads. Verifica que:
1. El formato es PNG o JPG
2. El tamano es menor a 30MB
3. La cuenta tiene permisos activos"

### Error al crear creativo
"No pude crear el creativo en Meta Ads. Error: {error}
El contenido esta listo — puedes copiarlo manualmente a Meta Ads Manager."

## Notas para Claude

- Usa la voz de Eduardo: profundidad, sprezzatura
- "Creacion" no "producto", "invitado" no "cliente"
- GATE DE CONFIRMACION ES OBLIGATORIO — nunca publicar sin "si" explicito
- NUNCA tocar presupuesto — es la regla mas importante de este skill
- Si los MCP write tools no existen aun, ofrecer flujo manual (copiar/pegar)
- Mostrar siempre el preview completo antes de publicar
- Si hay error, el contenido ya esta generado — el valor no se pierde
- IMPORTANTE: Meta Ads es dinero real. Doble confirmacion es el minimo.

## Persistencia

### Session Log

```python
entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "publish",
    "skill": "/kokoro-publish",
    "client_id": client.id,
    "summary": "{N} creativos publicados en campana {nombre}",
    "hallazgos": ["{observaciones sobre la publicacion}"],
    "artifacts": ["{creative_ids publicados}"],
    "next_action": "{monitorear rendimiento en 24-48h}"
}
```
