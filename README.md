# Kokoro

> La extensión de Claude Code que convierte a un emprendedor con alma en un estratega imparable.

Kokoro no es un chatbot genérico de marketing. Es la voz, la filosofía y el método de un Guardián de la Riqueza — un estratega que ha dedicado su vida a entender la prosperidad desde la raíz. Donde otros ven problemas, Kokoro ve tesoros ocultos. Donde otros dan tips, Kokoro guía procesos. Inspirado en la sabiduría ancestral y la estrategia de marketing contemporánea, Kokoro te acompaña a través de un camino orgánico de 4 fases — Preparar el Suelo, Elegir la Semilla, Germinar, Cosechar — sin atajos, sin plantillas, sin promesas vacías. No empieza a guiar sin invitación. Primero escucha, después refleja, y solo cuando pides ayuda — ahí sí, derrama todo el conocimiento.

---

## Instalación

### Requisitos mínimos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado y configurado
- Una cuenta activa de Claude (Pro, Team o Enterprise)
- 1 minuto para clonar, 30 segundos para abrir Claude Code

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/lunitomx/AhuehueteKokoro.git

# 2. Entrar al directorio
cd AhuehueteKokoro

# 3. Abrir Claude Code
claude
```

Ya está. Claude Code carga automáticamente los skills desde `.claude/commands/`, el conocimiento desde `.claude/knowledge/`, y la personalidad de Kokoro desde `CLAUDE.md`. No hay dependencias, no hay paquetes que instalar, no hay configuración — el repositorio **es** tu workspace listo para usar.

### Configuración opcional

Algunos skills usan APIs externas. Si quieres generar imágenes o creativos, crea un archivo `.env`:

```
GEMINI_API_KEY=tu-api-key-de-google-ai-studio
```

---

## Primer uso: qué esperar

Cuando entras a Claude Code por primera vez, escribe:

```
/kokoro
```

Ese es el router principal. Kokoro te hará preguntas para entender en qué fase estás y recomendarte el siguiente paso.

Si prefieres una sesión más profunda desde el inicio, usa:

```
/kokoro-onboard
```

Kokoro te hará preguntas sobre ti, tu negocio, tus números, tu visión. Escucha más de lo que habla. Refleja antes de aconsejar. Y cuando diagnostica la fase correcta, te guía desde ahí.

**El flujo natural:**

1. Primera vez: `/kokoro` o `/kokoro-onboard`
2. Sesión normal: `/kokoro-open` → [skill de fase] → `/kokoro-close`
3. Entre sesiones: Kokoro recuerda el contexto de tu proyecto

---

## Las 4 Fases

Un buen negocio camina **desde** la rentabilidad, no **hacia** la rentabilidad. No se saltan fases. Cada una tiene sus propias herramientas.

### Fase 1 — Preparar el Suelo

*Alineación estratégica. Antes de sembrar, la tierra necesita estar lista.*

| Skill | Qué hace | Cuándo usarlo |
|-------|----------|---------------|
| `/kokoro-diagnose` | Speed Boat + Visión 20/20 — encuentra las causas raíz | Cuando sientes que algo está trabado pero no sabes qué |
| `/kokoro-mountain` | Montaña del Mañana + OKRs | Cuando no tienes visión clara a 3 años |
| `/kokoro-prune` | Podar el Árbol de Productos | Cuando tienes demasiadas líneas de negocio |
| `/kokoro-finance` | Evaluación financiera real | Cuando no conoces tus números reales |

### Fase 2 — Elegir la Semilla

*Modelo de negocio. Validar antes de construir.*

| Skill | Qué hace | Cuándo usarlo |
|-------|----------|---------------|
| `/kokoro-canvas` | Lean Canvas guiado | Cuando necesitas estructurar tu modelo de negocio |
| `/kokoro-forces` | Customer Forces Model | Cuando no sabes qué mueve a tus invitados a elegirte |
| `/kokoro-interviews` | Guía de entrevistas + procesamiento | Cuando necesitas validar con personas reales |
| `/kokoro-validate` | Plan de Validación | Cuando quieres probar hipótesis antes de invertir |

### Fase 3 — Germinar

*Validación y lanzamiento. Tu creación se encuentra con las personas que la necesitan.*

| Skill | Qué hace | Cuándo usarlo |
|-------|----------|---------------|
| `/kokoro-research` | Investigación multi-fuente | Cuando necesitas entender tu mercado a profundidad |
| `/kokoro-pescar` | Metodología PESCAR completa | Cuando necesitas estrategia de contenido y comunicación |
| `/kokoro-experiment` | Experimento 3x3x3 | Cuando quieres probar algo en 3 semanas |
| `/kokoro-launch` | Copies + scripts + landing | Cuando estás listo para lanzar |
| `/kokoro-landing` | Auditoría de landing page | Cuando quieres evaluar contra la metodología Lean |

### Fase 4 — Cosechar

*Crecimiento y medición. Sistematizar lo que funciona.*

| Skill | Qué hace | Cuándo usarlo |
|-------|----------|---------------|
| `/kokoro-factory` | Customer Factory Blueprint | Cuando quieres sistematizar tu adquisición |
| `/kokoro-funnel` | Funnel Consciente | Cuando necesitas optimizar tu embudo |
| `/kokoro-mafia` | Crear Oferta Mafia | Cuando quieres una oferta irresistible |
| `/kokoro-rhythm` | Ritmo Semanal + Scorecard | Cuando necesitas cadencia y medición semanal |

### Herramientas transversales

Skills que aplican en cualquier fase:

| Skill | Qué hace |
|-------|----------|
| `/kokoro-onboard` | Primera consulta profunda — Kokoro te conoce antes de guiar |
| `/kokoro-open` | Abre sesión con un invitado (carga historial y propone foco) |
| `/kokoro-close` | Cierra sesión (guarda hallazgos y siguiente acción) |
| `/kokoro-client` | Gestionar invitados (crear, listar, buscar, ver perfil) |
| `/kokoro-session` | Mapa de progreso por fases |
| `/kokoro-init` | Inicializar Kokoro en un proyecto |
| `/kokoro-update` | Actualizar skills desde el repositorio (git pull) |
| `/kokoro-ads` | Campañas de Meta Ads (copy + targeting + estructura) |
| `/kokoro-creative` | Generador de creativos con IA (vía Gemini) |
| `/kokoro-analytics` | Consultar métricas (Meta Ads, GA4, Google Ads) |
| `/kokoro-pulse` | Pulso de lo que funciona ahora |
| `/kokoro-listen` | Descargar y transcribir video/audio |
| `/kokoro-cuts` | Identificar mejores momentos para cortes |
| `/kokoro-luxury` | Módulo Lux by Kokoro (posicionamiento de lujo) |

---

## Cómo interactúa Kokoro

Kokoro no es un asistente genérico. Tiene una forma específica de guiar:

**Espera la invitación.** Kokoro no empieza a dar consejos sin permiso. Primero pregunta, escucha, refleja. Cuando pidas ayuda — ahí sí, derrama todo el conocimiento. Es la estrategia del Proyector: reconocimiento antes de compartir sabiduría.

**Escucha más de lo que habla.** Haz preguntas, comparte contexto, cuenta tu historia. Kokoro escucha el 70% del tiempo y habla el 30%. Las preguntas poderosas abren más puertas que las respuestas rápidas.

**Vocabulario que posiciona.** Kokoro usa un lenguaje que define tu categoría:

| En lugar de... | Kokoro dice... |
|----------------|---------------|
| Cliente | **Invitado** |
| Producto | **Creación** |
| Precio | **Inversión** |
| Vender | **Compartir / Invitar** |
| Problema | **Oportunidad / Reto** |
| Gratis | **Cortesía / De regalo** |

---

## Estructura del proyecto

```
AhuehueteKokoro/
  .claude/
    CLAUDE.md              # Identidad y voz de Kokoro
    commands/              # 55+ skills (slash commands)
      kokoro.md            # Router principal
      kokoro-onboard.md    # Onboarding profundo
      kokoro-diagnose.md   # Fase 1: Diagnóstico
      ...
    knowledge/             # Archivos de conocimiento
      kokoro-metodologia.md
      kokoro-ads-meta.md
      ...
```

Claude Code carga automáticamente `CLAUDE.md` como instrucciones del sistema, los archivos en `commands/` como slash commands, y los archivos en `knowledge/` son referenciados por los skills cuando los necesitan.

---

## Autor

**Eduardo Muñoz Luna** — Guardián de la Riqueza, estratega de marketing con raíz ancestral. Proyector 1/3 en Diseño Humano, Eneagrama 3w4 — El Profesional con Alma. Fundador de Kokoro y la metodología de las 4 Fases.

---

## Licencia

Uso personal y educativo. Contacta a Eduardo para uso comercial.
