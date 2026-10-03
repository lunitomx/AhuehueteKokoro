# Session Log — Esquema y Guia para /kokoro-open y /kokoro-close

> Referencia tecnica para el historial de sesiones por invitado.
> Usado por: `/kokoro-open`, `/kokoro-close`, `/kokoro-ads`, `/kokoro-creative`

> "Cada sesion deja una huella. Kokoro recuerda para que no repitas."

## Proposito

Define el esquema de datos para el historial de sesiones que Kokoro mantiene
por cada invitado. Vive en `metadata["session_log"]` del perfil del invitado — una
lista plana de entradas ordenadas por fecha descendente.

## Ubicacion

```
.kokoro/clients.json → clients[N].metadata.session_log
```

Lo valida y lo escribe `runtime/clients.py` (`client log`). `session_log` es una
clave reservada: `client set-meta` no puede reemplazarla.

## Schema

```json
{
  "session_log": [
    {
      "date": "2026-03-27",
      "type": "creative",
      "skill": "/kokoro-creative",
      "client_id": "cliente_01",
      "summary": "6 creativos de la coleccion 01 — 2 publicos x 3 tamanos",
      "hallazgos": [
        "Publico mamas responde a dolor 'no se si mi bebe va bien'",
        "Fotos lifestyle > clinicas para segmento mamas"
      ],
      "artifacts": [
        "campanas/meta-ads/creativo-01-mamas.txt",
        "campanas/meta-ads/creativo-02-profesionales.txt"
      ],
      "next_action": "Lanzar campana en Meta Ads con los creativos generados"
    }
  ]
}
```

## Campos

| Campo | Tipo | Requerido | Descripcion |
|-------|------|:---------:|-------------|
| date | string (YYYY-MM-DD) | si | Fecha de la sesion |
| type | string | si | Tipo de trabajo realizado |
| skill | string | no | Skill que genero la entrada |
| client_id | string | si | ID del invitado en el grafo |
| summary | string | si | Que se hizo (1-2 lineas, concreto) |
| hallazgos | list[string] | no | Que se aprendio del invitado, su publico, su mercado |
| artifacts | list[string] | no | Paths relativos a clientes/{grupo}/ |
| next_action | string | no | Que hacer la proxima vez con este invitado |
| platform | string | no | Plataforma asociada (`google_ads`, `meta_ads`, etc.) |
| campaign_type | string | no | Tipo de canal de Google Ads (`search` `display` `pmax` `shopping` `other`) |
| learning_state | string | no | Estado de avance: `learning`, `stable` o `needs_attention` |
| task_group | string | no | Agrupador operativo (`insight`, `optimization`, `launch`) |
| task | string | no | Tarea concreta para esa sesión (`audiencias`, `creativos`, `presupuesto`) |
| cadence | string | no | Ritmo sugerido para seguimiento (`72h`, `weekly`, `monthly`, `90d`) |
| landing_page | string | no | Landing sugerida o confirmada en la sesión |
| asset_group | string | no | Nombre de asset group o conjunto de activos |
| change_made | string | no | Cambio ejecutado o recomendado |
| reason | string | no | Razon de la accion o recomendación |

### Extensión Google Ads (recomendado para S47.1)

- Mantener siempre `summary`, `hallazgos` y `next_action` como campos base.
- `platform` debe registrar `google_ads` cuando aplique.
- `learning_state`:
  - `learning`: hipótesis o prueba abierta.
  - `stable`: enfoque validado y mantenido.
  - `needs_attention`: requiere corrección antes de escalar.
- `task_group` y `task` deben ir juntos para reducir ambigüedad en el siguiente paso.
- Limitar campos opcionales a lo que realmente se trabajó en la sesión (no inventar).

### Valores validos para `type`

| type | Cuando usarlo |
|------|---------------|
| creative | Generacion de imagenes con /kokoro-creative |
| ads | Copy y campanas con /kokoro-ads |
| strategy | Diagnostico, canvas, fuerzas, poda, finanzas |
| research | Investigacion de mercado con /kokoro-research |
| launch | Lanzamiento con /kokoro-launch |
| experiment | Experimentos 3x3x3 con /kokoro-experiment |
| onboarding | Registro inicial o conexion de plataformas |
| general | Trabajo que no encaja en las categorias anteriores |

### Valores validos para `skill`

Cualquier skill de Kokoro: `/kokoro-creative`, `/kokoro-ads`,
`/kokoro-diagnose`, `/kokoro-canvas`, `/kokoro-pescar`, etc.
Si el trabajo fue manual (sin skill), omitir el campo.

## Reglas de Escritura

### Quien escribe

- `/kokoro-close` — siempre (es su funcion principal)
- `/kokoro-ads` — al final de generar entregables
- `/kokoro-creative` — al final de generar imagenes
- Otros skills — cuando se integren (S15.4)

### Como escribir una entrada

Escribe la entrada en `.kokoro/local/session-entry.json` (carpeta privada,
ignorada por git). El runtime agrega `client_id`, la pone primero y conserva
las 20 mas recientes.

```json
{
    "date": "{YYYY-MM-DD}",
    "type": "creative",
    "skill": "/kokoro-creative",
    "summary": "6 creativos de la coleccion 01 — 2 publicos x 3 tamanos",
    "hallazgos": [
        "Publico mamas responde a dolor 'no se si mi bebe va bien'"
    ],
    "artifacts": [
        "campanas/meta-ads/creativo-01-mamas.txt"
    ],
    "next_action": "Lanzar campana en Meta Ads"
}
```

```bash
python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" client log --id "{client_id}" \
  --input-file .kokoro/local/session-entry.json
```

### Limite de entradas

Maximo 20 entradas por invitado. Al agregar la entrada 21, la mas antigua
se descarta automaticamente. 20 sesiones es contexto suficiente.

### Paths de artifacts

Siempre relativos a `clientes/{grupo}/`. No paths absolutos.

Ejemplo: si el archivo esta en
`clientes/cliente_01/campanas/meta-ads/creativo-01.txt`,
el artifact se registra como `campanas/meta-ads/creativo-01.txt`.

## Reglas de Lectura

### /kokoro-open lee asi

1. Resolver invitado con `python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" client find --name "<nombre>"`
2. Si ya conoces el id, usa `client show --id <id>`
3. Leer `metadata.session_log` del resultado (lista vacia si no existe)
4. Mostrar las ultimas 3-5 entradas como contexto
5. Extraer `next_action` de la entrada mas reciente como propuesta de foco

### Formato de presentacion

```
## Sesion con {name}

Ultima sesion: {date} — {summary}
Hallazgos: {hallazgos como bullets}
Pendiente: {next_action}

¿Continuamos con esto o tienes otra prioridad hoy?
```

## Anti-patrones

- **No crear archivos separados por sesion** — todo vive en metadata
- **No guardar conversaciones completas** — solo resumen y hallazgos
- **No guardar datos que ya estan en el perfil** — el session_log es
  historial de interacciones, no duplicacion del perfil
- **No guardar entradas vacias** — si no hubo hallazgos ni artifacts,
  al menos el summary debe ser sustancial
- **No omitir next_action** — /kokoro-close SIEMPRE debe proponer
  siguiente paso. Es el valor principal del cierre
