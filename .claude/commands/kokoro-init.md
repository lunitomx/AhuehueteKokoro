# /kokoro-init — Inicializar Kokoro en un Proyecto

> Instala la identidad, los comandos y el conocimiento de Kokoro en un proyecto.

## Contexto

Usa este skill cuando un proyecto todavía no tiene una superficie local de
Kokoro. La instalación debe conservar los archivos propios del proyecto y
crear únicamente los archivos que pertenecen a Kokoro.

## Prerrequisitos

1. Confirma que el directorio actual es el proyecto que la persona quiere
   preparar y que no es la raíz del paquete de Kokoro.
2. Comprueba que el paquete fuente o la instalación local de Kokoro contiene
   `IDENTITY_kokoro.md`, `commands/` y `knowledge/`.
3. Si falta alguna de esas piezas, detén el flujo y pide reinstalar o
   actualizar el paquete.

## Flujo

1. Revisa si ya existen `.claude/commands/`, `.claude/knowledge/`, `CLAUDE.md`
   o `AGENTS.md`. No sobreescribas contenido propio sin mostrar antes un
   resumen y pedir autorización.
2. Copia únicamente los comandos y archivos de conocimiento de Kokoro que no
   existan en el proyecto.
3. Integra la identidad de Kokoro en `CLAUDE.md` o `AGENTS.md` usando
   marcadores claros, sin borrar instrucciones existentes.
4. Mantén fuera del repositorio los datos del invitado, sesiones, credenciales,
   exports y otros artefactos privados.
5. Ejecuta el verificador del paquete y reporta el número de comandos y
   archivos de conocimiento disponibles.

## Gate de seguridad

Antes de terminar confirma:

- El paquete fuente está completo.
- Los archivos propios del proyecto se conservaron.
- No se copiaron secretos, datos de invitados ni archivos de sistema.
- El proyecto puede encontrar el router y el conocimiento sin depender del
  directorio donde se instaló el paquete.

Si el proyecto ya tiene Kokoro instalado, deriva a `kokoro-update`.
