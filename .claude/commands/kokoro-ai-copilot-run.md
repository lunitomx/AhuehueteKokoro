# /kokoro-ai-copilot-run — Copiloto IA con Raiz Operativa

> Orquestador E48 basado en Tactiq 2025.
> Uso: cuando el usuario quiere usar IA, agentes, copilotos, Gems, GPTs,
> automatizacion o herramientas conectadas para operar marketing, ventas,
> contenido o seguimiento.

## Contexto

Lee primero `.kokoro/memoria.md` y `kokoro-mcp-reference.md`.

El corpus Tactiq muestra que la IA puede operar tareas, pero solo mejora el
sistema si existe contexto, proceso, permisos, datos confiables y revision
humana. Si no, solo acelera la confusion.

## Entrada Minima

- Resultado que se quiere delegar o amplificar.
- Proceso actual, aunque sea manual.
- Datos o documentos disponibles.
- Herramientas involucradas: Drive, CRM, Meta, Google, WhatsApp, calendario,
  sitio, hojas de calculo u otras.
- Nivel de permiso: leer, proponer, crear borrador o ejecutar.
- Persona responsable de revisar.
- Riesgo si la IA se equivoca.

## Gates

No configures ni recomiendes automatizacion operativa si falta:

| Gate | Pregunta |
|------|----------|
| Proceso | Cual es el paso a paso humano actual? |
| Contexto | Donde vive la verdad del negocio? |
| Permiso | La IA puede leer, sugerir, crear o ejecutar? |
| Riesgo | Que no debe tocar sin aprobacion? |
| Revision | Quien valida antes de publicar, invertir o responder? |
| Memoria | Donde se guardan decisiones y aprendizajes? |

Si el proceso no existe, recomienda documentarlo primero. Si hay herramientas
externas, revisa MCP boundaries y permisos con `/kokoro-mcp-reference` antes
de actuar.

## Flujo

1. **Definir la tarea**
   - Que resultado quiere el usuario.
   - Que parte es criterio humano.
   - Que parte es repetible.

2. **Mapear contexto**
   - Fuentes de verdad.
   - Archivos o sistemas necesarios.
   - Datos sensibles.
   - Memoria que debe persistir.

3. **Disenar nivel de autonomia**
   - Nivel 0: solo lee y resume.
   - Nivel 1: propone.
   - Nivel 2: crea borradores.
   - Nivel 3: ejecuta con aprobacion.
   - Nivel 4: ejecuta automaticamente solo si existe guardrail probado.

4. **Crear piloto**
   - Una tarea.
   - Un set de datos.
   - Un resultado esperado.
   - Un criterio de calidad.
   - Una regla de paro.

5. **Plan de integracion**
   - Que skill Kokoro usa.
   - Que herramienta/MCP necesita.
   - Que archivo de memoria actualiza.
   - Que humano aprueba.

## Salida

```markdown
## Copiloto IA con Raiz Operativa

### Tarea a Delegar
[resultado especifico]

### Mapa de Contexto
| Fuente | Uso | Riesgo |
|--------|-----|--------|

### Nivel de Autonomia
[0-4] porque [razon]

### Piloto
| Elemento | Definicion |
|----------|------------|
| Input | |
| Output | |
| Criterio de calidad | |
| Regla de paro | |
| Revisor | |

### Siguiente Accion
[documentar proceso / configurar MCP / crear prompt / correr piloto]
```

## Reglas

- No conectes herramientas ni ejecutes cambios sin permiso explicito.
- No uses datos privados en prompts exportables.
- No prometas autonomia si no hay proceso documentado.
- No automatices inversion, publicacion o respuesta comercial sin aprobacion
  humana y criterio de paro.
