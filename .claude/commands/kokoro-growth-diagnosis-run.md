# /kokoro-growth-diagnosis-run — Diagnostico de Crecimiento Vivo

> Orquestador E48 basado en el corpus Tactiq 2025.
> Uso: cuando el usuario pide crecer, vender mas, mejorar campanas, ordenar
> leads o destrabar adquisicion, pero el cuello de botella real no esta claro.

## Contexto

Lee primero `.kokoro/memoria.md`. Este run nace de 56 sesiones de
campo donde el pedido tactico casi siempre escondia una pregunta mas profunda:
suelo, semilla, oferta, medicion, seguimiento o economia.

No reemplaza `/kokoro-diagnose`. Lo complementa cuando el reto ya esta en la
zona de crecimiento comercial y hay que decidir si conviene diagnosticar,
validar, mejorar oferta, ajustar campana, ordenar CRM o revisar finanzas.

## Entrada Minima

Antes de recomendar cualquier accion, captura:

- Creacion o linea de negocio.
- Objetivo que el crecimiento debe mover.
- Invitado principal y no-invitado.
- Canal actual: organic, Meta, Google, WhatsApp, CRM, referidos u otro.
- Evidencia disponible: ventas, leads, conversiones, costo, margen, LTV.
- Donde duele: trafico, oferta, landing, seguimiento, cierre o retencion.

## Gates

Detente si falta cualquiera de estos elementos y pide solo la siguiente pieza
critica:

| Gate | Si falta | Ruta |
|------|----------|------|
| Objetivo/OKR | No hay norte de negocio | `/kokoro-mountain` |
| Modelo o invitado | No queda claro que se ofrece ni a quien | `/kokoro-canvas` |
| Fuerzas de compra | No se sabe por que cambia el invitado | `/kokoro-forces` |
| Evidencia real | Todo es opinion interna | `/kokoro-interviews` o `/kokoro-validate` |
| Tracking | No hay fuente de verdad | `/kokoro-tracking-check` |
| Economia | No se conoce margen, CAC o LTV | `/kokoro-finance` |

## Flujo

1. **Mapa del sistema comercial**
   - Suelo: proposito, objetivo, foco, amenazas.
   - Semilla: oferta, modelo, invitado, promesa.
   - Germinacion: canales, contenido, campanas, landing.
   - Cosecha: CRM, WhatsApp, cierre, seguimiento, LTV.

2. **Identificar cuello de botella**
   - Trafico insuficiente.
   - Mensaje/gancho debil.
   - Oferta poco clara.
   - Landing o CTA incoherente.
   - Seguimiento roto.
   - Medicion incompleta.
   - Economia inviable.

3. **Decidir ruta**
   - Si el cuello es desconocido: `/kokoro-diagnose`.
   - Si el cuello es semilla: `/kokoro-canvas`, `/kokoro-forces`,
     `/kokoro-validate`.
   - Si el cuello es campana: `/kokoro-campaign-lab-run`.
   - Si el cuello es pauta: `/kokoro-ads` o `/kokoro-gads`.
   - Si el cuello es seguimiento: `/kokoro-factory`, `/kokoro-funnel`,
     `/kokoro-rhythm` o `/kokoro-tracking-check`.

4. **Plan de 7 dias**
   - Una decision.
   - Una metrica.
   - Un owner.
   - Una accion por canal o punto de contacto.
   - Un criterio para perseverar, pivotar o pausar.

## Salida

Entrega:

```markdown
## Diagnostico de Crecimiento

### Lectura del Sistema
| Capa | Estado | Evidencia |
|------|--------|-----------|
| Suelo | | |
| Semilla | | |
| Germinacion | | |
| Cosecha | | |

### Cuello de Botella Principal
[descripcion breve]

### Ruta Recomendada
[skill/run recomendado] porque [razon basada en evidencia].

### Plan de 7 Dias
| Dia | Accion | Metrica | Owner |
|-----|--------|---------|-------|

### Gate Abierto
[la pieza que debe resolverse antes de invertir mas energia o dinero]
```

## Reglas

- No recomiendes aumentar inversion si tracking, follow-up o margen son
  invisibles.
- No recomiendes anuncios si el problema es oferta, invitado o Customer Forces.
- No recomiendes cambiar todo. Elige el cuello de botella que mas limita el
  sistema.
- Usa "creacion", "invitado", "inversion" y "adquirir".

## Modo de grafo gobernado — E58

Cuando el runtime instalado y `.kokoro/.gitignore` existen en el proyecto,
declara literalmente `Modo: grafo gobernado` y ejecuta el flujo por paquetes,
sin llamadas directas a proveedores ni mutaciones externas:

```text
python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" graph start \
  --workflow growth-diagnosis-v1 --target <proyecto> \
  --input-file <proyecto>/growth-input.json --idempotency-key <clave>
```

Entrega cada paquete JSON en el `inbox/` del run y usa `next`, `submit`,
`resume`, `status` y `doctor` para conservar evidencia. El JSON de cada nodo es
la fuente canónica; el Markdown es una representación determinista.

Si faltan los prerrequisitos, declara `Modo: directo compatible` y explica la
razón exacta. El modo directo conserva este flujo existente, pero no puede
presentarse como persistencia gobernada ni como evidencia de la alfa E58.

E58 es `single-host-sequential`: los paquetes no son todavía colaboración
multi-agente independiente. La aprobación se registra como
`host_interaction`, no como identidad humana autenticada.
