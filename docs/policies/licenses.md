# Política de licencias — Kokoro

> Las ideas se estudian. El código, los prompts y el texto se respetan.

## Principio

Kokoro puede aprender de cualquier proyecto público: leerlo, analizarlo y
escribir lo que observa. Lo que no hace es copiar sin permiso. Estudiar una
idea es libre. Incorporar la expresión de otra persona depende de su licencia.

## Qué se puede hacer sin licencia

- leer código, documentación y prompts de otros proyectos
- describir con palabras propias qué patrón usan y por qué funciona
- comparar ese patrón con el método de Kokoro
- diseñar una solución propia que resuelva el mismo reto

Ejemplo: un proyecto externo guarda aprendizajes con un estado de revisión.
Kokoro puede anotar "separar captura de promoción ayuda" y diseñar su propio
contrato de learning traces, con sus propios nombres, campos y reglas.

## Qué necesita licencia compatible

Solo entra a Kokoro si la licencia lo permite y se cumplen sus condiciones:

- código fuente, completo o en fragmentos
- prompts, instrucciones de sistema o skills
- texto de documentación, ejemplos o plantillas
- esquemas de datos copiados tal cual

Si la licencia exige atribución, la atribución va en el archivo que usa la
pieza y en el README. Si la licencia no es clara o no
existe, la respuesta es no.

## Diseño en sala limpia

Cuando Kokoro implementa algo inspirado en otro proyecto:

1. **Estudio.** Se escribe un análisis con palabras propias (por ejemplo,
   en `docs/research/`). El análisis describe patrones, no copia texto.
2. **Especificación.** Se escribe la especificación de Kokoro a partir del
   análisis: nombres, campos, estados y reglas propios.
3. **Implementación.** Se programa desde la especificación, sin tener abierto
   el código ni los prompts del otro proyecto.
4. **Revisión.** Antes de fusionar, alguien compara el resultado contra la
   fuente para confirmar que no hay texto ni código copiado.

## Lo que este repositorio no contiene

- código, prompts, dependencias ni MCP de Parker
- texto de terceros dentro de `.claude/commands/` o `.claude/knowledge/`
- material de cursos o metodologías sin el permiso de su autor

Las metodologías que Kokoro usa (por ejemplo, Lean Canvas o Customer Forces)
se citan por nombre y con atribución a su autor. Kokoro escribe sus propias
guías sobre ellas.

## Licencia de Kokoro

El código de Kokoro está bajo MIT (`LICENSE`). La metodología, la
documentación y los prompts originales están bajo CC BY 4.0
(`LICENSE-CONTENT.md`). Esta política no cambia esas licencias: solo define
qué puede entrar al paquete.
