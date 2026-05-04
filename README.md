# Kokoro

> El corazon estrategico de Eduardo Munoz Luna — donde la sabiduria ancestral se encuentra con la estrategia de marketing contemporanea.

Kokoro es un sistema de 51 skills para [Claude Code](https://claude.ai/claude-code) que guia emprendedores a traves de un proceso estrategico de 4 fases. No es un chatbot generico de marketing — es la voz, la filosofia y el metodo de un estratega que ha dedicado su vida a entender la riqueza desde la raiz.

---

## Instalacion

### Requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado y configurado
- Una cuenta activa de Claude (Pro, Team, o Enterprise)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/lunitomx/AhuehueteKokoro.git

# 2. Entrar a la carpeta del proyecto
cd AhuehueteKokoro

# 3. Abrir Claude Code
claude
```

Eso es todo. Claude Code carga automaticamente los skills desde `.claude/commands/` y el conocimiento desde `.claude/knowledge/`. No hay dependencias, no hay instalacion de paquetes, no hay configuracion.

### Configuracion opcional

Algunos skills usan APIs externas. Si quieres usarlos, crea un archivo `.env`:

```bash
# Para generar imagenes con /kokoro-creative y /kokoro-character
GEMINI_API_KEY=tu-api-key-de-google-ai-studio
```

---

## Como funciona

Kokoro funciona a traves de **slash commands** dentro de Claude Code. Escribes `/kokoro-` y el autocompletado te muestra todos los skills disponibles.

### Tu primera sesion

```
/kokoro-onboard
```

Escribe `/kokoro-onboard` la primera vez. Kokoro te hara preguntas profundas sobre ti, tu negocio, tus numeros, tu vision. Con eso:

1. Te registra en el grafo de invitados
2. Genera un documento de contexto completo
3. Diagnostica en que fase estas
4. Te recomienda por donde empezar

Las sesiones siguientes, usa `/kokoro-open` para retomar donde te quedaste.

---

## Las 4 Fases

Kokoro guia emprendedores a traves de un proceso organico. Cada fase tiene sus propias herramientas. No se saltan fases — un buen negocio camina DESDE la rentabilidad, no HACIA la rentabilidad.

### Fase 1 — Preparar el Suelo

Alineacion estrategica. Antes de sembrar, la tierra necesita estar lista.

| Skill | Que hace | Cuando usarlo |
|-------|----------|---------------|
| `/kokoro-diagnose` | Speed Boat + Vision 20/20 | Cuando sientes que algo esta trabado pero no sabes que |
| `/kokoro-mountain` | Montana del Manana + OKRs | Cuando no tienes vision clara a 3 anos |
| `/kokoro-prune` | Podar el Arbol de Productos | Cuando tienes demasiadas lineas de negocio |
| `/kokoro-finance` | Evaluacion financiera real | Cuando no conoces tus numeros reales |

### Fase 2 — Elegir la Semilla

Modelo de negocio. Validar antes de construir.

| Skill | Que hace | Cuando usarlo |
|-------|----------|---------------|
| `/kokoro-canvas` | Lean Canvas guiado | Cuando necesitas estructurar tu modelo de negocio |
| `/kokoro-forces` | Customer Forces Model | Cuando no sabes que mueve a tus clientes a elegirte |
| `/kokoro-interviews` | Guia de entrevistas | Cuando necesitas validar con personas reales |
| `/kokoro-validate` | Plan de Validacion | Cuando quieres probar hipotesis antes de invertir |

### Fase 3 — Germinar

Validacion y lanzamiento. Tu creacion se encuentra con las personas que la necesitan.

| Skill | Que hace | Cuando usarlo |
|-------|----------|---------------|
| `/kokoro-research` | Investigacion multi-fuente | Cuando necesitas entender tu mercado a profundidad |
| `/kokoro-pescar` | Metodologia PESCAR | Cuando necesitas estrategia de contenido y comunicacion |
| `/kokoro-experiment` | Experimento 3x3x3 | Cuando quieres probar algo en 3 semanas |
| `/kokoro-launch` | Lanzamiento al Mercado | Cuando estas listo para copies, landing y secuencia |
| `/kokoro-landing` | Auditoria de Landing Page | Cuando quieres evaluar tu landing contra la metodologia Lean |

### Fase 4 — Cosechar

Crecimiento y medicion. Sistematizar lo que funciona.

| Skill | Que hace | Cuando usarlo |
|-------|----------|---------------|
| `/kokoro-factory` | Customer Factory Blueprint | Cuando quieres sistematizar tu adquisicion |
| `/kokoro-funnel` | Funnel Consciente | Cuando necesitas optimizar tu embudo |
| `/kokoro-mafia` | Oferta Mafia | Cuando quieres crear una oferta irresistible |
| `/kokoro-rhythm` | Ritmo Semanal + Scorecard | Cuando necesitas cadencia y medicion semanal |

---

## Herramientas Transversales

Skills que aplican en cualquier fase del proceso.

### Gestion de sesiones

| Skill | Que hace |
|-------|----------|
| `/kokoro-onboard` | Primera consulta profunda — Kokoro te conoce antes de guiar |
| `/kokoro-open` | Abre sesion con un invitado (carga historial y propone foco) |
| `/kokoro-close` | Cierra sesion (guarda hallazgos y siguiente accion) |
| `/kokoro-client` | Gestionar invitados (crear, listar, buscar, ver perfil) |
| `/kokoro-session` | Mapa de progreso por fases |
| `/kokoro-init` | Inicializar Kokoro en un proyecto (instala knowledge files) |
| `/kokoro-update` | Actualizar knowledge files desde la fuente central |

### Marketing y publicidad

| Skill | Que hace |
|-------|----------|
| `/kokoro-ads` | Campanas de Meta Ads (copy + targeting + estructura) |
| `/kokoro-creative` | Generador de creativos con IA (imagenes via Gemini) |
| `/kokoro-creative-review` | Analisis de creativos bajo Meta AI (GEM, Andromeda, Lattice) |
| `/kokoro-placements` | Analisis de ubicaciones de Meta Ads (optimizar distribucion) |
| `/kokoro-publish` | Publicar creativos en Meta Ads |
| `/kokoro-character` | Generador de personajes hiper-realistas |
| `/kokoro-calendar` | Calendario de contenido semanal |

### Analitica

| Skill | Que hace |
|-------|----------|
| `/kokoro-analytics` | Consultar metricas (Meta Ads, GA4, Google Ads) |
| `/kokoro-scorecard` | Vista unificada cross-platform |
| `/kokoro-connect` | Conectar plataformas al invitado |
| `/kokoro-audit` | Auditoria de sitio web |
| `/kokoro-pulse` | Pulso de lo que funciona ahora |
| `/kokoro-intel` | Inteligencia competitiva en YouTube |

### Video pipeline

| Skill | Que hace |
|-------|----------|
| `/kokoro-listen` | Descargar y transcribir video/audio |
| `/kokoro-cuts` | Identificar mejores momentos para cortes |
| `/kokoro-shorts` | Extraer segmentos de video con ffmpeg |
| `/kokoro-overlay` | Agregar captions y reformatear a vertical |
| `/kokoro-render` | Ensamblar video final con normalizacion de audio |

### Modulo Lux by Kokoro (posicionamiento de lujo)

| Skill | Que hace |
|-------|----------|
| `/kokoro-luxury` | Router de modulos Lux by Kokoro |
| `/kokoro-luxury-assess` | Evaluacion de posicionamiento (triangulo FSE) |
| `/kokoro-luxury-scarcity` | Escasez estrategica |
| `/kokoro-luxury-quality` | Calidad extrema + poder simbolico |
| `/kokoro-luxury-experience` | Experiencias memorables |
| `/kokoro-luxury-communication` | Comunicacion que eleva |
| `/kokoro-luxury-pricing` | Estrategia de precios en lujo |
| `/kokoro-luxury-growth` | Crecer sin perder el brillo |

---

## Como interactuar

Kokoro no es un chatbot generico. Tiene una forma especifica de guiar:

### Espera la invitacion

Kokoro no empieza a dar consejos sin permiso. Primero pregunta, escucha, refleja. Cuando pidas ayuda — ahi si, derrama todo el conocimiento.

### Escucha mas de lo que habla

Haz preguntas, comparte contexto, cuenta tu historia. Kokoro escucha el 70% del tiempo y habla el 30%. Las preguntas poderosas abren mas puertas que las respuestas rapidas.

### Vocabulario

Kokoro usa un vocabulario especifico que posiciona:

| En lugar de... | Kokoro dice... |
|----------------|---------------|
| Cliente | **Invitado** |
| Producto | **Creacion** |
| Precio | **Inversion** |
| Vender | **Compartir / Invitar** |
| Problema | **Oportunidad / Reto** |
| Gratis | **Cortesia / De regalo** |

### Flujo recomendado

```
Primera vez:     /kokoro-onboard → diagnostica tu fase
Sesion normal:   /kokoro-open → [skill de fase] → /kokoro-close
Sin contexto:    /kokoro → router rapido de fases
```

---

## Estructura del proyecto

```
extension/
  .claude/
    CLAUDE.md              # Identidad y voz de Kokoro
    commands/              # 51 skills (slash commands)
      kokoro.md            # Router principal
      kokoro-onboard.md    # Onboarding profundo
      kokoro-diagnose.md   # Fase 1: Diagnostico
      kokoro-ads.md        # Meta Ads
      ...
    knowledge/             # 37 archivos de conocimiento
      kokoro-metodologia.md
      kokoro-ads-meta.md
      kokoro-onboard-methodology.md
      ...
```

Claude Code carga automaticamente `CLAUDE.md` como instrucciones del sistema, los archivos en `commands/` como slash commands, y los archivos en `knowledge/` son referenciados por los skills cuando los necesitan.

---

## Autor

**Eduardo Munoz Luna** — Guardian de la Riqueza, estratega de marketing con raiz ancestral.

- Proyector 1/3 en Diseno Humano
- Eneagrama 3w4 — El Profesional con Alma
- Fundador de Kokoro y la metodologia de las 4 Fases

---

## Licencia

Uso personal y educativo. Contacta a Eduardo para uso comercial.
