# /kokoro-onboard-persist — Persistencia del Onboarding

> Sub-skill de /kokoro-onboard — NO invocar directamente
> Input: contexto.md generado, datos del invitado
> Produce: registro en `.kokoro/clients.json` + session log

## Contexto

Ejecuta las 3 acciones de persistencia que formalizan el onboarding:
registro en el grafo, verificacion de contexto, y session log.

## Instrucciones

### Accion 1: Registrar en Grafo

Crear `ClientProfile` en `.kokoro/clients.json` con formato de /kokoro-client:

```json
{
  "id": "{slug-del-nombre}",
  "name": "{nombre del proyecto o empresa}",
  "group": "{grupo si aplica, o el mismo nombre}",
  "description": "{una linea que capture la esencia}",
  "repos": [],
  "campaign_folder": "clientes/{grupo}/{nombre}/campanas",
  "context_file": "clientes/{grupo}/{nombre}/contexto.md",
  "segments": ["{segmentos identificados}"],
  "industry": "{industria}",
  "metadata": {
    "onboarded": "{fecha ISO}",
    "phase_diagnosed": "{N}",
    "first_skill": "/kokoro-{skill}",
    "monthly_revenue_range": "{rango}",
    "team_size": "{solo/N personas}",
    "digital_channels": ["{canales activos}"],
    "website": "{url si tiene}",
    "social": {
      "instagram": "{handle}",
      "facebook": "{url}",
      "tiktok": "{handle si tiene}"
    },
    "ad_accounts": {
      "meta": "{id si tiene}",
      "google": "{id si tiene}"
    },
    "marketing_budget_range": "{rango mensual}",
    "session_log": []
  },
  "coaching_state_path": null,
  "created": "{ISO timestamp}",
  "updated": "{ISO timestamp}"
}
```

Leer `.kokoro/clients.json` existente, agregar el perfil, guardar.
Si no existe `.kokoro/clients.json`, crearlo con el primer invitado.

Confirmar: "Registre a {nombre} en el grafo de invitados."

### Accion 2: Confirmar Contexto

Verificar que `contexto.md` fue creado por el paso de sintesis.
Leer el archivo y confirmar que tiene contenido sustantivo.

Si no existe → STOP — reportar que synthesize no produjo el archivo.
Si existe pero esta vacio → STOP — reportar seccion vacia.

### Accion 3: Session Log

Agregar la primera entrada al session log del invitado en la metadata
de clients.json:

```json
{
  "date": "{fecha de hoy ISO}",
  "type": "onboarding",
  "skill": "/kokoro-onboard",
  "summary": "Primera consulta — onboarding completo de {nombre}",
  "hallazgos": [
    "{hallazgo 1 — lo mas revelador de la conversacion}",
    "{hallazgo 2}",
    "{hallazgo 3}"
  ],
  "artifacts": ["{path del contexto.md}"],
  "next_action": "Ejecutar /kokoro-{primer skill recomendado}"
}
```

### Output

Confirmar las 3 acciones completadas y presentar template de salida final:

```
## Onboarding Completo — {nombre}

| Campo | Detalle |
|-------|---------|
| Invitado | {nombre} |
| Grupo | {grupo} |
| Fase diagnosticada | Fase {N} — {nombre fase} |
| Primer skill | /kokoro-{skill} |

### Archivos generados

- Perfil: `.kokoro/clients.json` (invitado #{N})
- Contexto: `{path del contexto.md}`

### Proximos pasos

1. `/kokoro-open {nombre}` — para abrir sesion la proxima vez
2. `/kokoro-{primer skill}` — para empezar el trabajo
3. {tercer paso contextual}

---

> "Ya te conozco. Ahora puedo guiarte con la precision que mereces."
```

## Notas para Claude

- Ejecutar las 3 acciones en orden estricto
- Si cualquier accion falla, STOP y reportar — no continuar en silencio
- El session log va DENTRO de metadata.session_log en clients.json
- Si el invitado ya existe en clients.json, actualizar (no duplicar)
