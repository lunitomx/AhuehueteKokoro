# Grafo de Invitados

> Knowledge file para `/kokoro-client`.

## Estructura

```json
{
  "clients": [{
    "id": "unique-slug",
    "name": "Nombre del negocio",
    "group": "paraguas o holding",
    "segments": ["segmento A", "segmento B"],
    "metadata": {
      "session_log": [],
      "colores_marca": {},
      "sitio_web": ""
    }
  }]
}
```

## Operaciones

- `find_by_name` — búsqueda parcial, case-insensitive
- `find_by_id` — búsqueda exacta
- Registro, actualización, consulta de historial
