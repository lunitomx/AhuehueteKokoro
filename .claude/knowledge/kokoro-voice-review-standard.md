# Estándar de Revisión de Voz v1

> La forma de nombrar define la categoría. Una palabra genérica regala el
> lugar que costó construir.

La regla canónica vive en `runtime/voice.py` (`VOCABULARY`,
`GENERIC_PHRASES`, `lint`). Si este archivo y el código no coinciden, el
código manda. La tabla de vocabulario espeja la de `CLAUDE.md`.

## Para qué sirve

Un copy puede ser verdadero y sonar a plantilla. La revisión de voz señala
palabras fuera del vocabulario Kokoro, frases de IA genérica y citas que
pueden ser testimonios inventados. Es consultiva: sugiere, no reescribe ni
bloquea. La persona decide.

## Contrato

Entrada: un archivo de texto plano con el copy (`voice check --input-file
copy.txt`). Salida: `status` (Pass o Partial), `findings` y `mutates: false`.
El código de salida siempre es 0.

### Vocabulario (`kind: vocabulary`)

| Se detecta | Se sugiere |
|---|---|
| precio, precios | inversión |
| producto, productos | creación |
| gratis | cortesía / de regalo |
| descuento, descuentos | condiciones especiales |
| cliente, clientes | invitado / persona |
| compra, comprar | adquirir / elegir |
| barato, barata, baratos, baratas | accesible |
| vender | compartir / invitar |
| problema, problemas | oportunidad / reto |
| gastar | invertir |
| price · free · discount · cheap | investment · complimentary · special conditions · accessible |

### Frases genéricas (`kind: generic_ai`)

Español: hacks, growth hacking, monetizar, escalar rápido, «N tips»,
duplica tus ventas, resultados garantizados, en el mundo actual, «no es solo
…, es…», desbloquea, potencia tu, lleva o llevar tu negocio al siguiente
nivel.

Inglés: in today's fast-paced o digital world, unlock, game-changer, take
your business to the next level.

Sugerencia del runtime: decir qué gana la persona, en concreto.

### Posible testimonio (`kind: possible_testimony`)

Se activa cuando el copy trae una cita (12 caracteres o más entre comillas) y
no lleva marca de ilustrativo. La sugerencia es correr el grounding check o
marcarla como ilustrativa.

## Reglas

1. **Consultiva, no gate.** Un Partial de voz no bloquea la publicación. Un
   Blocked de grounding sí. Por eso grounding va primero.
2. **La voz del invitado se respeta.** Las palabras dentro de comillas no se
   marcan: si una persona real dijo «el precio me asustó», es su voz.
3. **La cita no se valida aquí.** `possible_testimony` solo avisa. Si la cita
   es real lo dice `/kokoro-grounding-review`. Una frase de IA nunca es
   testimonio.
4. **Sustituir con sentido.** «Cliente» no siempre se vuelve «invitado»: a
   veces es «persona» o el nombre del rol («la contadora»).
5. **No reescribe.** El runtime solo señala. Kokoro propone la versión nueva;
   la persona la elige.
6. **Lo genérico se reemplaza con lo concreto.** «Lleva tu negocio al
   siguiente nivel» se vuelve lo que de verdad cambia: «cierra el mes sin
   abrir 10 portales».

## Ejemplo

Copy de `cliente_01`, datos ficticios:

> Desbloquea el mejor precio para tu cliente. Llevar tu negocio al siguiente
> nivel es gratis.

Resultado: Partial con 5 hallazgos.

| Tipo | Encontrado | Sugerencia |
|---|---|---|
| vocabulary | precio | inversión |
| vocabulary | gratis | cortesía / de regalo |
| vocabulary | cliente | invitado / persona |
| generic_ai | desbloquea | decir qué gana la persona |
| generic_ai | llevar tu negocio al siguiente nivel | decir qué gana la persona |

Versión propuesta para que la persona elija:

> Tu despacho cierra el mes sin abrir 10 portales. La primera revisión es de
> cortesía.

El número 10 vuelve a pasar por `/kokoro-grounding-review` antes de publicar.

## Anti-patrones

- **Lint como juez.** Pass de voz no significa copy verdadero.
- **Cambiar la cita real.** Ajustar la frase de una entrevista al vocabulario
  Kokoro la convierte en otra cosa.
- **Sustitución mecánica.** «Adquiere tu creación con condiciones especiales
  hoy» suena tan vacío como el original.
- **Saltar el grounding** porque la voz salió bien.

## Comandos y runtime

- `/kokoro-voice-review` corre el lint, explica cada hallazgo y propone
  versiones. Va al final: `/kokoro-grounding-review` →
  `/kokoro-creative-review` → `/kokoro-voice-review`.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K voice check --input-file copy.txt        # texto plano; siempre código 0; mutates: false
```

No escribe en el ledger. Todo vive en `.kokoro/` del workspace. No hay hooks
que reescriban copy.
