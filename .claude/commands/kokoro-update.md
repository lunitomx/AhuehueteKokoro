# /kokoro-update — Actualizar Kokoro en un Proyecto

> Sincroniza knowledge files y skills con la ultima version de AhuehueteKokoro.
> Ejecutar cuando haya actualizaciones disponibles.

> "El arbol que no se riega, deja de dar fruto."

## Contexto

Kokoro evoluciona constantemente — nuevos skills, nuevo conocimiento,
mejoras a los existentes. Este skill sincroniza un proyecto ya inicializado
con la ultima version de los knowledge files.

El modelo de actualizacion es: `git pull` dentro del directorio AhuehueteKokoro,
luego copiar los knowledge files actualizados al proyecto destino.

**Fuente:** `<ruta-a-tu-kokoro>/extension/.claude/knowledge/`
**Destino:** `.claude/knowledge/` del proyecto actual

### Cuando usar

- Cuando haya nuevos skills o knowledge files disponibles en AhuehueteKokoro
- Cuando un skill referencia un knowledge file que no tienes
- Periodicamente para mantenerse al dia

### Cuando NO usar

- Si el proyecto no tiene Kokoro instalado — usa `/kokoro-init` primero
- Si estas dentro del directorio AhuehueteKokoro (el update ahi es solo `git pull`)

## Instrucciones

### Paso 1: Verificar prerrequisitos

1. Verificar que `.claude/knowledge/` existe:
   - Si no existe: "Este proyecto no tiene Kokoro instalado. Usa `/kokoro-init` primero."

2. Preguntar al usuario donde tiene su clon de AhuehueteKokoro:
   > "Para actualizar Kokoro necesito la ruta de tu clon de AhuehueteKokoro.
   > ¿Puedes indicarme la ruta?"

3. Verificar que la fuente existe:
   - Si no existe: "No encuentro los knowledge files en esa ruta. Verifica que
     AhuehueteKokoro este disponible en la ubicacion indicada."

### Paso 2: Actualizar AhuehueteKokoro

Primero, traer los ultimos cambios del repo fuente:

```bash
git -C <ruta-indicada> pull
```

Informar al usuario el resultado del pull (nuevos commits, ya al dia, etc.)

### Paso 3: Comparar archivos

Ejecutar comparacion entre fuente y destino:

```bash
# Listar archivos en fuente
find <ruta-indicada>/extension/.claude/knowledge/ -name "*.md" -type f | sort > /tmp/kokoro-source-files.txt

# Listar archivos en destino
find .claude/knowledge/ -name "*.md" -type f | sort > /tmp/kokoro-dest-files.txt
```

Clasificar cada archivo en una de 3 categorias:

1. **Nuevo** — Existe en fuente pero no en destino (solo comparar nombre de archivo)
2. **Modificado** — Existe en ambos pero el contenido difiere (usar diff)
3. **Sin cambios** — Identico en ambos

### Paso 4: Presentar resumen ANTES de actuar

```
Kokoro Update — Resumen de cambios

Proyecto: {directorio actual}
Fuente: AhuehueteKokoro (ultimo commit: {fecha})

Nuevos ({N}):
  + meta-ads-placements-feeds.md
  + meta-ads-placements-stories-reels.md
  + ...

Modificados ({N}):
  ~ kokoro-ads-meta.md (fuente mas reciente)
  ~ kokoro-metodologia.md
  ~ ...

Sin cambios ({N}):
  = kokoro-phase1-diagnostico.md
  = ...

¿Proceder con la actualizacion? (se sobreescriben los modificados)
```

**HITL Gate:** Esperar confirmacion del usuario antes de copiar.

### Paso 5: Ejecutar actualizacion

Si el usuario confirma:

```bash
# Copiar nuevos y modificados
cp <ruta-indicada>/extension/.claude/knowledge/{archivo} .claude/knowledge/{archivo}

# Subdirectorios nuevos
cp -r <ruta-indicada>/extension/.claude/knowledge/{subdir}/ .claude/knowledge/{subdir}/
```

### Paso 6: Reportar resultado

```
Kokoro actualizado exitosamente.

  {N} archivos nuevos instalados
  {M} archivos actualizados
  {P} archivos sin cambios (no tocados)

Total: {T} knowledge files en .claude/knowledge/

Nuevos skills disponibles:
  /kokoro-placements — Analisis de ubicaciones de Meta Ads
  ... (listar skills nuevos si los hay)

Para ver que hay de nuevo: revisa el README en
github.com/lunitomx/AhuehueteKokoro
```

### Paso 7: Limpiar archivos huerfanos (opcional)

Si hay archivos en destino que NO existen en fuente:

```
Archivos locales sin equivalente en fuente ({N}):
  ? archivo-local-custom.md

Estos pueden ser archivos custom de este proyecto.
¿Quieres eliminarlos o conservarlos?
```

**Default: conservar.** Solo eliminar si el usuario lo pide explicitamente.

## Notas para Claude

- SIEMPRE mostrar resumen antes de copiar — nunca sobreescribir sin confirmacion
- No eliminar archivos locales que no esten en la fuente (pueden ser custom)
- No copiar datos personales ni archivos de cliente
- Si un archivo modificado tiene cambios locales del proyecto que el usuario
  hizo manualmente, advertir antes de sobreescribir
- Nunca asumir ni hardcodear una ruta de usuario — siempre preguntar
- Usar voz de Eduardo: "Tu Kokoro tiene {N} actualizaciones disponibles.
  Como un jardin, el conocimiento necesita riego constante."
