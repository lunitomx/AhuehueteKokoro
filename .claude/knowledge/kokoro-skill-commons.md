# Kokoro Skill Commons

> Instrucciones compartidas entre skills. Los skills referencian este archivo
> en vez de duplicar estos bloques.

## Resolucion de Invitado

Antes de iniciar cualquier sesion, resuelve al invitado desde el grafo:

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Lee su `context_file` si existe (datos reales del proyecto)
   - Lee sus `repos` para datos actualizados (inventario, tarifas)
   - Lee sus `segments` para entender los publicos
   - Lee su `metadata` para datos clave
   - Presenta: "Invitado: {name} | Grupo: {group} | Segmentos: {segments}"
3. Si NO encuentra al invitado:
   - Pregunta: "No encontre ese invitado en el grafo. Quieres que lo registremos
     ahora con `/kokoro-client`? O prefieres continuar sin contexto guardado?"
4. Si no hay `.kokoro/clients.json`:
   - Continua sin contexto de invitado (backward compatible)
   - Al final, sugiere: "Considera registrar este invitado con
     `/kokoro-client` para que la proxima vez tenga todo el contexto listo."

## Persistencia Comun

Al terminar cualquier sesion con invitado resuelto:

1. Actualiza `.kokoro/state.json` del proyecto con el estado actual
2. Si hay invitado resuelto, registra en su `session_log`:

```python
entry = {
    "date": "YYYY-MM-DD",
    "type": "{skill_type}",
    "skill": "/{skill_name}",
    "client_id": client.id,
    "summary": "{resumen de una linea}",
    "hallazgos": ["{insights clave}"],
    "artifacts": ["{paths de archivos generados}"],
    "next_action": "{siguiente paso logico}"
}
```

Consulta `kokoro-session-log.md` para el schema completo de session_log.
Limitar a 20 entradas (las mas recientes).

Si no hay invitado resuelto, omitir session_log (backward compatible).

## Verificacion de Tier Luxelling

Para skills del modulo Luxelling (`/kokoro-luxury-*`):

1. Busca en `.kokoro/clients.json` y verifica `positioning_tier`
2. Si `positioning_tier` = luxury o premium: continua normalmente
3. Si no tiene tier: sugiere ejecutar `/kokoro-luxury-assess` primero
4. Sin invitado resuelto: la evaluacion no puede persistir — informar al usuario

## Contexto de Fase

| Fase | Tema | Skills | Knowledge prefix |
|------|------|--------|-----------------|
| 1 | Preparar el Suelo | diagnose, mountain, prune, finance | `kokoro-phase1-*` |
| 2 | Elegir la Semilla | canvas, forces, interviews, validate | `kokoro-phase2-*` |
| 3 | Germinar | research, pescar, experiment, launch | `kokoro-phase3-*` |
| 4 | Cosechar | factory, funnel, mafia, rhythm | `kokoro-phase4-*` |

Si existe `.kokoro/state.json`, lee el progreso de fases anteriores como contexto.
