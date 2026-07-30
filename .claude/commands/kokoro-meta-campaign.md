# /kokoro-meta-campaign — Campaña Meta desde cero

> Guía pública para llevar una creación desde la decisión comercial hasta un
> plan completo y una carga manual en Ads Manager.

## Verdad operativa

Kokoro puede ayudar a diseñar una campaña desde cero, revisar que esté lista y
dar los pasos exactos para configurarla en Ads Manager. No inicia sesión, no
solicita credenciales, no maneja datos de pago, no cambia cuentas ni publica
campañas. La persona que administra la cuenta revisa y hace el clic final de
publicación.

No prometas resultados. Una campaña publicada es una hipótesis que empieza a
aprender; no es evidencia de ventas ni de atribución correcta.

## Antes de guiar

Pide invitación para guiar y refleja el objetivo de la persona. Luego reúne
solamente los datos que falten. No inventes ni completes con valores genéricos:

| Decisión | Pregunta o evidencia |
|---|---|
| Creación y persona | ¿Qué creación se comparte y para quién es? |
| Resultado | ¿Qué acción importa: conversación, lead, compra, visita o llamada? |
| Destino | URL, WhatsApp, formulario instantáneo o llamada ya disponibles. |
| Medición | Pixel/dataset y evento de conversión, o la limitación explícita. |
| Inversión | Moneda, límite diario o total, fechas y tope aprobados. |
| Público | Geografía, edades, idioma, señales y exclusiones justificadas. |
| Activos | Cada imagen/video, texto principal, titular, CTA y URL aprobados. |
| Seguimiento | Quién responde, en qué canal y cómo se marca el resultado. |

Si faltan oferta, destino, tracking o seguimiento, no pases a Ads Manager.
Deriva a `/kokoro-launch`, `/kokoro-tracking-check`, `/kokoro-funnel` o
`/kokoro-ads` según corresponda.

## Paso 1 — Plan de campaña

Construye y muestra este plan. Todo campo desconocido queda como `Pendiente`,
nunca como una suposición.

```text
PLAN DE CAMPAÑA META

Estado: Preparación incompleta / Plan listo / Pendiente de publicación manual / Publicado observado
Negocio:
Creación:
Persona a quien sirve:
Resultado de negocio:
Objetivo de campaña en Ads Manager:
Ubicación de conversión:
Cuenta Meta:
Moneda e inversión máxima:
Fechas:
Pixel/dataset y evento de optimización:
Geografía, edad, idioma y señal de audiencia:
Placements:
Activo 1:
Texto principal:
Titular:
CTA:
Destino:
Responsable de seguimiento:
Riesgos o campos pendientes:
```

Pregunta: "¿Este plan representa exactamente la campaña que quieres cargar en
Ads Manager?" Si no hay un sí, corrige el plan; no entregues el playbook aún.

## Paso 2 — Preflight humano

Antes de abrir Ads Manager, la persona debe confirmar:

- Tiene acceso a la ad account correcta y una forma de pago activa.
- El pixel/dataset y evento existen cuando el objetivo los necesita.
- No hay borradores o cambios pendientes que puedan mezclarse.
- Los archivos creativos finales están disponibles y se revisaron para el
  placement elegido.
- El límite de inversión, fechas y responsable de seguimiento son correctos.

Si el objetivo pertenece a una categoría especial de Meta, la persona debe
elegirla correctamente en Ads Manager; Kokoro no debe inferirla.

## Paso 3 — Playbook manual en Ads Manager

Entrega sólo pasos que correspondan al plan confirmado:

1. Abrir Ads Manager y seleccionar la ad account confirmada.
2. Elegir **Crear** y el objetivo de campaña del plan.
3. Nombrar la campaña para que negocio, objetivo y fecha sean reconocibles.
4. Configurar presupuesto y calendario exactamente dentro del límite aprobado.
5. En el ad set, elegir ubicación de conversión, pixel/dataset, evento,
   geografía, edad, idioma, audiencia y placements del plan.
6. En el anuncio, cargar cada activo aprobado, copiar el texto, titular, CTA y
   destino; revisar la vista previa de los placements seleccionados.
7. Verificar que tracking, destino, inversión, fechas y responsable de
   seguimiento coinciden con el plan.
8. La persona revisa la pantalla final y publica manualmente. Kokoro no pulsa
   **Publish** ni afirma que la campaña quedó publicada sin evidencia.

Si la interfaz muestra una sugerencia automática que no está en el plan, la
persona debe decidirla explícitamente antes de seguir.

## Paso 4 — Cierre honesto

Después de publicar, pide sólo evidencia no sensible: campaign ID, ad set ID,
ad ID o una confirmación visible sin datos de pago ni credenciales. Registra uno
de estos estados:

| Estado | Evidencia |
|---|---|
| Preparación incompleta | Falta una decisión o activo indispensable. |
| Plan listo | Plan confirmado, aún fuera de Ads Manager. |
| Pendiente de publicación manual | Playbook entregado; no hay evidencia de publicación. |
| Publicado observado | La persona aportó IDs o una confirmación visible. |

El primer aprendizaje empieza después: deja correr el tiempo acordado, revisa
la medición y usa `/kokoro-analytics` antes de concluir que algo funciona o no.
