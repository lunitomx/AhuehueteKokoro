# Kokoro

> La extensión para Claude Code, Codex CLI y Hermes Agent que convierte a un emprendedor con alma en un estratega imparable.

Kokoro no es un chatbot genérico de marketing. Es la voz, la filosofía y el método de un Guardián de la Riqueza — un estratega que ha dedicado su vida a entender la prosperidad desde la raíz. Donde otros ven problemas, Kokoro ve tesoros ocultos. Donde otros dan tips, Kokoro guía procesos. Inspirado en la sabiduría ancestral y la estrategia de marketing contemporánea, Kokoro te acompaña a través de un camino orgánico de 4 fases — Preparar el Suelo, Elegir la Semilla, Germinar, Cosechar — sin atajos, sin plantillas, sin promesas vacías. No empieza a guiar sin invitación. Primero escucha, después refleja, y solo cuando pides ayuda — ahí sí, derrama todo el conocimiento.

---

## Instalación

### Requisitos mínimos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex CLI](https://github.com/openai/codex) o [Hermes Agent](https://hermes-agent.nousresearch.com) instalado
- Una cuenta activa de tu CLI preferido
- 1 minuto para clonar, 30 segundos para arrancar

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/lunitomx/AhuehueteKokoro.git

# 2. Entrar al directorio
cd AhuehueteKokoro

# 3. Abrir tu CLI preferido
claude    # para Claude Code
codex     # para Codex CLI (lee AGENTS.md automáticamente)
```

Ya está. El repositorio **es** tu workspace listo para usar, pero cada runtime
carga Kokoro de forma distinta:

| Runtime | Qué carga automáticamente | Cómo usar comandos Kokoro |
|---------|---------------------------|----------------------------|
| Claude Code | `.claude/CLAUDE.md`, `.claude/commands/`, `.claude/skills/` | Usa slash commands como `/kokoro` o `/kokoro-google-ads-run` |
| Codex CLI | `AGENTS.md` | Pide a Codex leer el markdown del comando en `.claude/commands/` y ejecutarlo manualmente |
| Hermes Agent | Depende de tu instalación Hermes | Instala o apunta el skill bundle según tu configuración Hermes |

Los archivos de conocimiento viven en `.claude/knowledge/`. Algunos flujos
también pueden usar MCPs externos, pero Kokoro debe verificar conexión antes
de afirmar datos vivos.

### Configuración opcional

Algunos skills usan APIs externas. Si quieres generar imágenes o creativos, crea un archivo `.env`:

```
GEMINI_API_KEY=tu-api-key-de-google-ai-studio
```

---

## Primer uso: qué esperar

Cuando entras por primera vez en Claude Code, escribe:

```
/kokoro
```

Ese es el router principal. Kokoro te hará preguntas para entender en qué fase estás y recomendarte el siguiente paso.

En Codex, pide explícitamente:

```
lee .claude/commands/kokoro.md y ejecútalo como /kokoro
```

Codex no carga `.claude/commands/` como slash commands nativos. Lee `AGENTS.md`
y desde ahí puede abrir el markdown correcto cuando se lo pidas.

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
| `/kokoro-intel` | Inteligencia competitiva | Cuando necesitas saber qué hace tu competencia |

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
| `/kokoro-gads` | Campañas de Google Ads (keywords, estructura, optimización) |
| `/kokoro-creative` | Generador de creativos con IA (vía Gemini) |
| `/kokoro-creative-review` | Análisis de creativos bajo Meta AI (GEM, Andromeda, Lattice, Sequence) |
| `/kokoro-feed-audit` | Auditoría de corpus activo de Meta Ads (catálogo, disponibilidad) |
| `/kokoro-analytics` | Consultar métricas (Meta Ads, GA4, Google Ads) |
| `/kokoro-pulse` | Pulso de lo que funciona ahora |
| `/kokoro-scorecard` | Scorecard ejecutivo cross-platform |
| `/kokoro-placements` | Análisis de rendimiento por placement |
| `/kokoro-tracking-check` | Auditoría de salud de medición digital |
| `/kokoro-mcp-reference` | Guía de conexión a APIs (Meta Ads, Google Ads, GA4, Search Console) |
| `/kokoro-parrilla` | Planificación editorial — de brief a publicación |
| `/kokoro-calendar` | Calendario de contenido basado en la parrilla |
| `/kokoro-publish` | Publicación de contenido creativo |
| `/kokoro-scout` | Reconocimiento del proyecto — mapea lo que existe |
| `/kokoro-mirror` | Espejo del perfil Scout — relee y presenta resumen |
| `/kokoro-landing` | Evaluación de landing pages contra metodología Lean |
| `/kokoro-listen` | Descargar y transcribir video/audio |
| `/kokoro-cuts` | Identificar mejores momentos para cortes |
| `/kokoro-shorts` | Extracción automatizada de segmentos para shorts |
| `/kokoro-overlay` | Captions sincronizados sobre video |
| `/kokoro-render` | Ensamblaje profesional de video |
| `/kokoro-luxury` | Módulo Lux by Kokoro (posicionamiento de lujo) |
| `/kokoro-meeting` | Procesar transcripciones de reuniones (extraer compromisos) |
| `/kokoro-retrospective` | Cierre flexible de día o semana con reflexión estratégica |
| `/kokoro-adr` | Capturar decisiones estratégicas |
| `/kokoro-intel` | Inteligencia competitiva basada en contenido |
| `/kokoro-connect` | Conectar plataformas al invitado (Meta Ads, GA4, etc.) |

### Orquestadores ejecutivos E40

Estos runs convierten skills sueltos en procesos completos para directores de
marketing, ventas y fundadores:

| Run | Para qué sirve | Primer gate |
|-----|----------------|-------------|
| `/kokoro-google-ads-run` | Diagnóstico Google Ads end-to-end | invitado resuelto, MCP Google Ads sano, privacidad |
| `/kokoro-weekly-marketing-run` | Pulso semanal Meta, Google, GA4, GSC y lectura ejecutiva | plataformas conectadas, periodo claro |
| `/kokoro-creative-campaign-run` | Carruseles y campañas visuales con promesa, storyboard y revisión | promesa verdadera, dirección visual clara |
| `/kokoro-launch-run` | Lanzar una creación sin saltarse validación, landing, tracking y readback | creación, invitado, promesa y tracking |
| `/kokoro-acquisition-run` | Mejorar adquisición encontrando el cuello real del sistema | funnel, oferta, landing, tracking y follow-up |
| `/kokoro-share-readiness` | Revisar si Kokoro está listo para compartirse sin datos sensibles | privacidad, runtime y MCP boundaries |

### Demo sin MCP

Puedes demostrar Kokoro sin conectar plataformas. En ese modo:

- usa placeholders como `cliente_01`;
- los gates de MCP y datos vivos se marcan como `Skipped` o `Blocked`;
- Kokoro muestra metodología, preguntas y estructura de decisión;
- Kokoro no inventa métricas, campañas, costos ni resultados.

### Antes de compartir

Ejecuta `/kokoro-share-readiness` antes de compartir el repo, hacer una demo
con invitados o preparar un workspace para colaboradores. La decisión final
debe ser `Pass`, `Hold` o `Private Only`.



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



## Estructura del proyecto

```
AhuehueteKokoro/
  AGENTS.md                # Identidad para Codex CLI (lo lee automáticamente)
  .claude/
    CLAUDE.md              # Identidad y voz de Kokoro
    commands/              # 74 skills y runs (slash commands en Claude Code)
      kokoro.md            # Router principal
      kokoro-onboard.md    # Onboarding profundo
      kokoro-diagnose.md   # Fase 1: Diagnóstico
      ...
    knowledge/             # Archivos de conocimiento (73 archivos)
      kokoro-metodologia.md
      kokoro-ads-meta.md
      google-ads/          # Guías detalladas de Google Ads
      lux/                 # Módulo Lux by Kokoro
      ...
    skills/                # Web Quality Skills: performance, CWV, accesibilidad, SEO
      full-audit/
      performance/
      core-web-vitals/
      web-quality-audit/
      ...
```

Claude Code carga `.claude/CLAUDE.md`, `.claude/commands/`, `.claude/knowledge/`
y `.claude/skills/` como parte natural del workspace. Codex carga `AGENTS.md`;
cuando necesites un comando Kokoro en Codex, abre el markdown correspondiente
en `.claude/commands/` y sigue sus instrucciones manualmente. Hermes depende
de cómo instales o enlaces su skill bundle.



## Multi-CLI

Kokoro funciona en 3 CLIs de IA:

| CLI | Identidad | Skills | Comandos |
|-----|-----------|--------|----------|
| **Claude Code** | `.claude/CLAUDE.md` | `.claude/skills/` | `.claude/commands/` como slash commands |
| **Codex CLI** | `AGENTS.md` | puede leer `.claude/skills/` cuando se le indique | no auto-carga `.claude/commands/`; lee el markdown y ejecútalo manualmente |
| **Hermes Agent** | `AGENTS.md` o bundle instalado | depende de instalación global/local | no asumir comandos nativos sin instalar el bundle Hermes |



## Autor

**Eduardo Muñoz Luna** — Guardián de la Riqueza, estratega de marketing con raíz ancestral. Proyector 1/3 en Diseño Humano, Eneagrama 3w4 — El Profesional con Alma. Fundador de Kokoro y la metodología de las 4 Fases.



## Licencia

Uso personal y educativo. Contacta a Eduardo para uso comercial.
