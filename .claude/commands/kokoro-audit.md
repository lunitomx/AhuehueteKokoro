# /kokoro-audit — Auditoria de Sitio Web

> Herramienta transversal: Diagnostico de salud web para emprendedores
> Powered by web-quality-skills de Addy Osmani
> (https://github.com/nicholasgriffintn/web-quality-skills)

> "Tu sitio web es tu escaparate digital. Vamos a asegurarnos de que
> refleja la calidad de lo que ofreces."

## Contexto

Este skill guia una auditoria completa de sitio web: rendimiento, SEO,
accesibilidad y buenas practicas. Usa las herramientas de web-quality-skills
(credito a Addy Osmani) y traduce los hallazgos tecnicos a recomendaciones
accionables en lenguaje de emprendedor.

No es necesario entender terminos tecnicos — Kokoro traduce todo:
- "LCP alto" → "Tu pagina tarda mucho en mostrar el contenido principal"
- "Falta alt text" → "Las imagenes no tienen descripcion para buscadores"
- "Sin HTTPS" → "Tu sitio no tiene candado de seguridad"

### Contexto previo

Si existe `.kokoro/clients.json`, busca el sitio web del invitado
registrado. Si el invitado tiene un repo web, usalo para contexto.

### Resolucion de invitado

Antes de iniciar, intenta resolver el invitado desde el grafo:

1. Si el usuario menciona un nombre de invitado, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra el invitado:
   - Lee su `context_file` si existe
   - Lee sus `repos` para obtener datos del sitio
   - Presenta un resumen: "Invitado: {name} | Grupo: {group}"
3. Si NO encuentra el invitado:
   - Pregunta: "No encontre ese invitado en el grafo. Quieres que lo creemos
     ahora con `/kokoro-client`? O prefieres continuar sin contexto guardado?"
4. Si no hay `.kokoro/clients.json`:
   - Continua sin contexto de invitado (backward compatible)

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Voy a revisar la salud de tu sitio web — como un chequeo medico para tu
> presencia digital. Al final tendras un diagnostico claro con las acciones
> mas importantes para mejorar. Me das tu invitacion para guiarte?"

Si el usuario acepta, continua. Si no, escucha y ajusta.

### Ejercicio 1: Identificar el sitio

Pregunta: "Cual es la URL de tu sitio web?"

Si el invitado esta registrado en el grafo y tiene repo, ofrece:
"Veo que tienes registrado {site_url}. Es ese el sitio a auditar?"

### Ejercicio 2: Ejecutar auditoria

Usa las herramientas de web-quality-skills disponibles. Ejecuta en este orden:

1. **SEO tecnico** — usa el skill `seo-technical` o `seo-page`
2. **Rendimiento** — usa el skill `performance` o `core-web-vitals`
3. **Accesibilidad** — usa el skill `accessibility`
4. **Buenas practicas** — usa el skill `best-practices`

Si los skills estan disponibles como herramientas, invocalos.
Si no, guia al usuario a ejecutarlos manualmente.

### Ejercicio 3: Traducir hallazgos

Para CADA hallazgo tecnico, traduce a lenguaje de emprendedor:

| Hallazgo tecnico | Traduccion para emprendedor |
|-----------------|---------------------------|
| LCP > 2.5s | Tu pagina tarda en mostrar contenido. Los visitantes se van |
| CLS > 0.1 | Tu pagina "salta" mientras carga. Se ve poco profesional |
| Sin meta description | Google no sabe que mostrar de tu pagina en los resultados |
| Imagenes sin alt | Los buscadores no pueden "ver" tus imagenes |
| Sin HTTPS | Tu sitio no tiene candado. Los visitantes no confian |
| Sin responsive | Tu sitio no se ve bien en celular. 70% del trafico es movil |
| JavaScript bloqueante | Tu sitio carga lento por codigo innecesario al inicio |
| Sin structured data | Google no puede mostrar tu negocio con estrellitas y datos enriquecidos |

### Ejercicio 4: Priorizar acciones

Clasifica los hallazgos en 3 niveles:

1. **Urgente** — afecta ventas o confianza AHORA (seguridad, velocidad critica)
2. **Importante** — mejora posicionamiento y experiencia (SEO, accesibilidad)
3. **Deseable** — refinamientos profesionales (structured data, optimizacion fina)

### Persistencia

Si existe `.kokoro/state.json` en el directorio del proyecto del invitado,
registra los hallazgos como nodos en el grafo de coaching.

## Notas para Claude

- SIEMPRE dar credito a Addy Osmani y web-quality-skills
- Usa vocabulario Kokoro: "invitado" no "cliente", "creacion" no "producto"
- NO uses jerga tecnica sin traducir — el emprendedor no es developer
- Prioriza por impacto en NEGOCIO, no por severidad tecnica
- Si el sitio esta bien, celebra: "Tu sitio tiene buena salud digital"

## Template de salida

```
## Auditoria Web — {nombre del sitio}

> Powered by web-quality-skills de Addy Osmani

| Area | Estado | Impacto |
|------|--------|---------|
| Rendimiento | {estado} | {impacto en negocio} |
| SEO | {estado} | {impacto en negocio} |
| Accesibilidad | {estado} | {impacto en negocio} |
| Seguridad | {estado} | {impacto en negocio} |

### Acciones urgentes
{lista priorizada}

### Acciones importantes
{lista priorizada}

### Acciones deseables
{lista priorizada}

### Siguiente paso

Elige 1-2 acciones urgentes para resolver esta semana.
Usa `/kokoro-pescar` para comunicar las mejoras a tus invitados.
Usa `/kokoro-experiment` para medir el impacto de los cambios.
```
