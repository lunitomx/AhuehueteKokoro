# /kokoro-feedback — Reportar un bug o sugerir una mejora

> **Propósito:** ayudarte a preparar un reporte claro y seguro para mejorar Kokoro. Tú decides si se comparte y dónde.

## Antes de empezar

No incluyas contraseñas, tokens, cookies, datos de pago, correos o teléfonos de personas, materiales de invitados, URLs privadas ni capturas con información sensible.

Pregunta primero:

> ¿Quieres reportar algo que no funcionó (**bug**) o proponer algo que haría a Kokoro más útil (**mejora**)?

## Recoger sólo lo necesario

### Si es un bug

1. ¿Qué esperabas que ocurriera?
2. ¿Qué ocurrió realmente?
3. ¿Qué pasos seguros permiten repetirlo?
4. ¿En qué entorno pasó? (por ejemplo, macOS y versión de Kokoro, si la conoces)

### Si es una mejora

1. ¿Qué oportunidad ves?
2. ¿Qué resultado te gustaría conseguir?
3. ¿Para quién sería útil?
4. ¿Tienes un ejemplo seguro que aclare la idea?

Si falta un dato importante, marca `Pendiente`; no lo inventes.

## Entregar un borrador sanitizado

Usa uno de estos formatos.

### Bug

```markdown
## Resumen
[Qué no funcionó]

## Resultado esperado
[Qué debía ocurrir]

## Resultado observado
[Qué ocurrió]

## Pasos seguros para reproducir
1. ...
2. ...

## Entorno
[Sistema, versión de Kokoro u otro contexto no sensible]
```

### Mejora

```markdown
## Oportunidad
[Qué podría mejorar]

## Resultado deseado
[Qué sería diferente o más útil]

## Personas a quienes ayudaría
[Quiénes y por qué]

## Ejemplo seguro
[Opcional; sin datos privados]
```

## Compartir sólo con tu autorización

Presenta el borrador y pregunta:

> ¿Lo revisamos y autorizas compartirlo en el repositorio público de Kokoro?

Si la respuesta es sí, abre o entrega este enlace para que **la persona** envíe el reporte tras revisarlo:

https://github.com/lunitomx/AhuehueteKokoro/issues/new/choose

No envíes el issue por tu cuenta. El estado es `Borrador preparado` hasta que la persona lo comparta; pasa a `Feedback enviado` sólo cuando indique el enlace o número del issue.
