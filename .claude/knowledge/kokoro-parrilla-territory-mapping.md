# Territory Mapping — Sin Solapamiento

> Knowledge file para S46.4. Cada pieza de la parrilla debe ocupar un
> territorio distinto. Si dos piezas comparten mecanismo, una sobra.

## Principio

El error más común en parrillas es el refrito: mismo copy con palabras
cambiadas. Territory Mapping lo detecta antes de que ocurra.

Un territorio se define por el **mecanismo** que usa la pieza para
convencer, no por el tema que toca.

## Territorios (catálogo no exhaustivo)

| Territorio | Mecanismo | Ejemplo |
|-----------|-----------|---------|
| Producto | Mostrar lo que se ofrece con detalle concreto | "2 recamaras desde X. Interior real, no render." |
| Testimonial | Voz de alguien que ya tomó la decisión | "Lo que más nos gustó fue que no se siente como..." |
| Recorrido | Mostrar cómo se llega y qué se siente al estar ahí | Video desde la entrada hasta el interior |
| Contraste | Comparar el antes/después o esto vs aquello | "Cuando tu rutina ya no cabe entre tráfico y ruido..." |
| Educativo | Enseñar algo útil relacionado con la decisión | "3 cosas que debes saber antes de elegir X" |
| Objeción | Atacar directamente la razón #1 por la que no compran | "Si crees que es caro, compara con lo que pierdes..." |
| Urgencia legítima | Razón real por la que ahora es mejor que después | "Quedan X unidades. Después de eso, 18 meses de espera." |
| Comunidad | Mostrar quién más ya está aquí | "No eres el primero. Mira quién ya tomó la decisión." |

## Mapa de Territorios

```markdown
| Pieza | Territorio | Mecanismo específico |
|-------|-----------|---------------------|
| P1 | Producto | {qué muestra y cómo} |
| P2 | Testimonial | {qué historia cuenta} |
| P3 | Recorrido | {qué ruta muestra} |
```

**Regla:** Si dos piezas comparten territorio Y mecanismo específico,
una de las dos debe cambiar de mecanismo o eliminarse.

## Gate

Antes de aprobar la parrilla:
- [ ] Cada pieza tiene un territorio asignado
- [ ] Ningún territorio se repite con el mismo mecanismo
- [ ] Si hay N piezas, hay al menos N-1 territorios distintos
