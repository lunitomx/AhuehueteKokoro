# /kokoro-luxury — Router de Modulos Lux by Kokoro

> Modulo Lux by Kokoro: Navegacion al universo del lujo
> Aplica cuando el invitado califica como luxury o premium

> "El lujo no se fabrica — se coreografia."

## Contexto

Este skill es el punto de entrada a los modulos de Lux by Kokoro. Verifica
el positioning_tier del invitado y lo guia al modulo apropiado.

Lee el archivo de conocimiento `lux-master.md` para la sintesis
y el arbol de decision completo.

### Resolucion de invitado

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
2. Si encuentra al invitado:
   - Verifica `metadata["positioning_tier"]`
   - Si no tiene tier → redirige a `/kokoro-luxury-assess`
   - Si tier = "standard" → explica que los modulos de lujo no aplican
   - Si tier = "luxury" o "premium" → presenta menu de modulos

## Instrucciones para la sesion

### Gate de posicionamiento

Antes de mostrar modulos, verifica:

```
¿Tiene positioning_tier?
  NO → "Para acceder a los modulos de lujo, primero necesitamos
        evaluar tu posicionamiento. ¿Hacemos el assessment?"
        → /kokoro-luxury-assess

  SI → ¿Es "luxury" o "premium"?
    NO (standard) → "Tu posicionamiento actual es mass market.
        Los modulos de lujo requieren ciertas condiciones base.
        Te sugiero empezar con `/kokoro-diagnose` para encontrar
        tu proximo movimiento."
    SI → Presentar menu de modulos
```

### Menu de modulos

> "Bienvenido al universo Lux by Kokoro. Tienes 6 modulos disponibles,
> cada uno activa un superpoder diferente. ¿Por donde quieres empezar?"

| # | Modulo | Skill | Para que sirve |
|:-:|--------|-------|---------------|
| 1 | Escasez Estrategica | `/kokoro-luxury-scarcity` | Dream Equation, ediciones limitadas, distribucion selectiva |
| 2 | Calidad y Poder Simbolico | `/kokoro-luxury-quality` | Piramide de calidad, 5A Framework, 8 pilares simbolicos |
| 3 | Experiencias Memorables | `/kokoro-luxury-experience` | Diseno multisensorial, Tribe-Fire Canvas, rituales |
| 4 | Comunicacion que Eleva | `/kokoro-luxury-communication` | Codigos visuales, paleta 60/30/10, artificacion |
| 5 | Estrategia de Precios | `/kokoro-luxury-pricing` | Efecto Veblen, value-based pricing, comunicacion del precio |
| 6 | Crecer sin Perder Brillo | `/kokoro-luxury-growth` | Piramide de lujo, brand stretching, expansion geografica |

**Sugerencia de ruta para nuevos:**
Si el invitado no sabe por donde empezar, sugiere:
Calidad → Comunicacion → Escasez → Experiencias → Pricing → Growth

Esto construye la base (sustancia) antes de la estrategia (escala).

### Navegacion contextual

Si el usuario ya viene de un modulo, sugiere el siguiente logico:
- Despues de Assessment → Calidad + Simbolismo
- Despues de Calidad → Comunicacion
- Despues de Comunicacion → Escasez
- Despues de Escasez → Experiencias
- Despues de Experiencias → Pricing
- Despues de Pricing → Growth
- Despues de Growth → "Has recorrido todos los modulos. ¿Quieres
  integrar todo con un plan de accion?"

## Notas para Claude

- Usa la voz de Eduardo: profundidad, metaforas, sprezzatura
- No forces ningún modulo — presenta opciones y deja elegir
- Si el invitado es premium (no luxury), menciona que algunos modulos
  aplican parcialmente y cuales son mas relevantes
- Responde en el idioma del usuario
- Usa "creacion" no "producto", "invitado" no "cliente"
