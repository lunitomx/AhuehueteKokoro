# /kokoro-update — Actualizar Kokoro en un Proyecto

> Sincroniza knowledge files y skills con la fuente central.
> Ejecutar cuando haya actualizaciones disponibles.

> "El arbol que no se riega, deja de dar fruto."

## Contexto

Kokoro evoluciona constantemente — nuevos skills, nuevo conocimiento,
mejoras a los existentes. Este skill sincroniza un proyecto ya inicializado
con la ultima version de los knowledge files.

**Fuente:** `/Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/`
**Destino:** `.claude/knowledge/` del proyecto actual

### Cuando usar

- Cuando Eduardo anuncia nuevos skills o knowledge files
- Cuando un skill referencia un knowledge file que no tienes
- Periodicamente para mantenerse al dia

### Cuando NO usar

- Si el proyecto no tiene Kokoro instalado — usa `/kokoro-init` primero
- Si estas en el repo fuente `RaizAncestral` (ya los tiene)

## Instrucciones

### Paso 1: Verificar prerrequisitos

1. Verificar que NO estamos en `RaizAncestral`:
   - Si es `RaizAncestral`: "Estas en el repo fuente. No necesitas update aqui."

2. Verificar que `.claude/knowledge/` existe:
   - Si no existe: "Este proyecto no tiene Kokoro instalado. Usa `/kokoro-init` primero."

3. Verificar que la fuente existe:
   - Si no existe: "No encuentro la fuente. Verifica que RaizAncestral este disponible."

### Paso 2: Comparar archivos

Ejecutar comparacion entre fuente y destino:

```bash
# Listar archivos en fuente
find /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/ -name "*.md" -type f | sort > /tmp/kokoro-source-files.txt

# Listar archivos en destino
find .claude/knowledge/ -name "*.md" -type f | sort > /tmp/kokoro-dest-files.txt
```

Clasificar cada archivo en una de 3 categorias:

1. **Nuevo** — Existe en fuente pero no en destino (solo comparar nombre de archivo)
2. **Modificado** — Existe en ambos pero el contenido difiere (usar diff)
3. **Sin cambios** — Identico en ambos

### Paso 3: Presentar resumen ANTES de actuar

```
Kokoro Update — Resumen de cambios

Proyecto: {directorio actual}
Fuente: RaizAncestral/extension (ultimo commit: {fecha})

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

### Paso 4: Ejecutar actualizacion

Si el usuario confirma:

```bash
# Copiar nuevos y modificados
cp /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/{archivo} .claude/knowledge/{archivo}

# Subdirectorios nuevos
cp -r /Users/soyahuehuetedigital/Documents/GitHub/RaizAncestral/extension/.claude/knowledge/{subdir}/ .claude/knowledge/{subdir}/
```

### Paso 5: Reportar resultado

```
Kokoro actualizado exitosamente.

  {N} archivos nuevos instalados
  {M} archivos actualizados
  {P} archivos sin cambios (no tocados)

Total: {T} knowledge files en .claude/knowledge/

Nuevos skills disponibles:
  /kokoro-placements — Analisis de ubicaciones de Meta Ads
  ... (listar skills nuevos si los hay)

Para ver que hay de nuevo: revisa el README del paquete publico AhuehueteKokoro
```

### Paso 6: Limpiar archivos huerfanos (opcional)

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
- Usar voz de Eduardo: "Tu Kokoro tiene {N} actualizaciones disponibles.
  Como un jardin, el conocimiento necesita riego constante."
