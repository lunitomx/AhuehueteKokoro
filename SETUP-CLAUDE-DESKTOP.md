# Kokoro para Claude Desktop — Guia de Instalacion

> 3 pasos para conectar Kokoro con Claude Desktop.

## Paso 1: Instalar uv

Abre la terminal y ejecuta:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Cierra y reabre la terminal.

## Paso 2: Configurar Claude Desktop

Abre Claude Desktop → Settings → Developer → Edit Config.

Agrega esto al archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kokoro": {
      "command": "uvx",
      "args": ["--from", "kokoro[mcp]", "kokoro-mcp"],
      "env": {
        "KOKORO_PROJECT_DIR": "~/Documents/mi-negocio"
      }
    }
  }
}
```

Cambia `mi-negocio` por el nombre de tu carpeta de proyecto.

## Paso 3: Reiniciar Claude Desktop

Cierra y abre Claude Desktop. Kokoro aparecera como herramienta disponible.

## Como usar

En Claude Desktop, escribe:

- **"Usa kokoro_init para iniciar mi negocio 'Mi Tienda'"** — crea tu estado
- **"Usa kokoro_diagnose"** — inicia el diagnostico estrategico
- **"Usa kokoro_progress"** — ve tu avance en las 4 fases

## Las 12 herramientas disponibles

### Fase 1 — Preparar el Suelo
| Herramienta | Que hace |
|-------------|---------|
| `kokoro_diagnose` | Diagnostico: Speed Boat + Vision 20/20 |
| `kokoro_mountain` | Vision a 3 anos + OKRs |
| `kokoro_prune` | Podar lineas de negocio |
| `kokoro_finance` | Evaluacion financiera real |

### Fase 2 — Elegir la Semilla
| Herramienta | Que hace |
|-------------|---------|
| `kokoro_canvas` | Lean Canvas guiado |
| `kokoro_forces` | Customer Forces Model |
| `kokoro_interviews` | Guia de entrevistas |
| `kokoro_validate` | Plan de validacion |

### Fase 3 — Germinar
| Herramienta | Que hace |
|-------------|---------|
| `kokoro_research` | Investigacion multi-fuente |
| `kokoro_pescar` | Estrategia PESCAR |
| `kokoro_experiment` | Sprint 3x3x3 |
| `kokoro_launch` | Lanzamiento al mercado |

### Utilidades
| Herramienta | Que hace |
|-------------|---------|
| `kokoro_init` | Crear estado para nuevo emprendedor |
| `kokoro_progress` | Ver progreso en las 4 fases |

## Soporte

Si tienes problemas, contacta a tu instructor o abre un issue en el
repositorio del proyecto.
