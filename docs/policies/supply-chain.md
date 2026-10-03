# Política de cadena de suministro — Kokoro

> Nada de afuera entra a Kokoro sin que una persona lo lea, lo revise y lo
> apruebe.

## Alcance

Aplica a todo lo que venga de fuera de este repositorio y pueda ejecutarse o
cargarse junto con Kokoro:

- skills, comandos y archivos de conocimiento de terceros
- servidores MCP y conectores
- paquetes de Python u otros lenguajes
- hooks, scripts de instalación y binarios
- plantillas o prompts copiados de otro proyecto

No aplica a texto que Kokoro lee como dato (páginas web, reseñas,
transcripciones). Ese texto nunca es instrucción. Ver
`.claude/knowledge/kokoro-evidence-model.md`.

## Regla base

**Nunca ejecutes algo directo desde una URL.** No se usa `curl … | bash`,
`pip install git+https://…` sin versión fija, ni un instalador que baje código
al momento de correr. Primero se descarga, se revisa y se aprueba. Después se
activa.

## Los 12 pasos

Antes de que una pieza externa entre a Kokoro:

1. **Fija la versión.** Usa el SHA completo del commit o una versión exacta
   del paquete. Nunca una rama ni `latest`. Ejemplo: el conector de Google Ads
   en `kokoro-package.yaml` lleva `revision:` con el SHA completo.
2. **Lee el diff.** Revisa todo lo que cambió desde la versión aprobada
   anterior. Si es la primera vez, revisa el contenido completo.
3. **Escanea el código.** Busca llamadas a `eval`, `exec`, subprocesos,
   descargas, ofuscación y secretos escritos en el código.
4. **Revisa los hooks.** Cualquier hook (de git, de la CLI, de instalación)
   se lee línea por línea. Un hook que corre en cada sesión necesita una razón
   escrita.
5. **Revisa binarios y scripts.** Un binario sin fuente no entra. Un script
   de instalación se lee completo antes de correrlo.
6. **Revisa las llamadas de red.** Lista cada dominio al que se conecta. Un
   dominio que no explica la función de la pieza es motivo de rechazo.
7. **Revisa las escrituras al disco.** Lista qué rutas escribe. Nada escribe
   fuera del proyecto o de `~/.claude/kokoro` sin aprobación explícita. Nada
   escribe en `.claude/commands/` ni en `.claude/knowledge/` al correr.
8. **Revisa los permisos.** Qué herramientas, tokens y cuentas pide. Un
   conector de lectura no pide permisos de escritura. Los tokens viven en el
   entorno de la persona, nunca en el repositorio.
9. **Revisa la licencia.** Aplica `docs/policies/licenses.md`. Sin licencia
   compatible, no entra código, prompts ni texto.
10. **Aprueba por escrito.** Una persona del equipo aprueba. La aprobación
    queda en el PR o en un ADR: qué versión, quién la revisó y qué se
    encontró.
11. **Cuarentena.** La pieza corre primero en un proyecto de prueba, sin datos
    reales de invitados y sin credenciales de cuentas reales.
12. **Activa después de verificar.** Solo después de la cuarentena se agrega
    al paquete o a `kokoro-package.yaml`, y `install/verify.sh` debe pasar.

## Actualizaciones

Una nueva versión de algo ya aprobado repite los pasos 1 a 12 sobre el diff.
No hay actualizaciones automáticas de dependencias externas.

## Lo que Kokoro no incorpora

- código, prompts, skills o texto sin licencia compatible
- dependencias que se instalan al momento de correr
- servidores MCP sin mantenedor identificado
- código, prompts, dependencias o MCP de Parker

## Si algo ya entró sin este proceso

1. Desactívalo: quítalo del paquete o de la configuración de MCP.
2. Revisa qué leyó y qué escribió mientras estuvo activo.
3. Rota cualquier credencial que haya podido ver.
4. Registra lo ocurrido en un ADR y decide si vuelve a entrar por los 12 pasos.
