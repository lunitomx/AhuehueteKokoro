# /kokoro-init — Inicializar Kokoro en un Proyecto

> Instalacion de Kokoro knowledge files en un proyecto nuevo.
> Ejecutar una sola vez por proyecto.

> "Antes de sembrar, prepara la tierra."

## Contexto

Kokoro necesita archivos de conocimiento (knowledge files) para funcionar a
profundidad. Este skill copia los archivos desde tu clon local de AhuehueteKokoro
al proyecto actual.

**Fuente:** `<ruta-a-tu-kokoro>/extension/.claude/knowledge/`
**Destino:** `.claude/knowledge/` del proyecto actual

### Cuando usar

- Primera vez que usas Kokoro en un proyecto nuevo
- Despues de clonar un repo que no tiene los knowledge files

### Cuando NO usar

- Si el proyecto ya tiene knowledge files instalados — usa `/kokoro-update`
- Si estas dentro del directorio AhuehueteKokoro (ya los tiene)

## Instrucciones

### Paso 1: Detectar contexto

1. Verificar el directorio actual (pwd)
2. Si el directorio actual contiene `.claude/commands/kokoro-init.md`:
   > "Estas dentro de AhuehueteKokoro — aqui ya estan los knowledge files
   > incluidos en el repo. Este skill es para instalar Kokoro en otros proyectos.
   > Abre AhuehueteKokoro en Claude Code y estaras listo para usar cualquier skill."
   → Terminar

3. Verificar si `.claude/knowledge/` ya existe y tiene archivos kokoro-*:
   - Si tiene archivos: avisar y preguntar
     > "Este proyecto ya tiene {N} knowledge files de Kokoro instalados.
     > ¿Quieres reinstalar desde cero (sobreescribe todo) o prefieres
     > usar `/kokoro-update` para sincronizar solo lo nuevo?"
   - Si no tiene archivos: continuar con instalacion

### Paso 2: Localizar la fuente

Preguntar al usuario donde tiene su clon de AhuehueteKokoro:

> "Para instalar Kokoro en este proyecto necesito saber donde tienes tu clon
> de AhuehueteKokoro. ¿Puedes indicarme la ruta?"

Ejemplo de respuesta esperada: `~/Documents/AhuehueteKokoro`

Verificar que la fuente existe:
```bash
ls <ruta-indicada>/extension/.claude/knowledge/
```

Si no existe, informar:
> "No encuentro los knowledge files en esa ruta. Verifica que tu clon de
> AhuehueteKokoro este en la ubicacion indicada y que contenga el directorio
> extension/.claude/knowledge/"

### Paso 3: Crear estructura

```bash
mkdir -p .claude/knowledge
```

### Paso 4: Copiar archivos

Copiar TODOS los archivos .md de la fuente al destino:

```bash
# Archivos en raiz de knowledge/
cp <ruta-indicada>/extension/.claude/knowledge/*.md .claude/knowledge/

# Subdirectorios (lux/, google-ads/, etc.)
cp -r <ruta-indicada>/extension/.claude/knowledge/*/ .claude/knowledge/ 2>/dev/null
```

### Paso 5: Verificar y reportar

Contar archivos copiados y presentar resumen:

```
Kokoro inicializado en: {directorio actual}

Archivos instalados:
- {N} knowledge files copiados
- Subdirectorios: {lista de subdirectorios si hay}

Fuente: <ruta-indicada>/extension/.claude/knowledge/
Destino: .claude/knowledge/

Para actualizar en el futuro: /kokoro-update
```

### Paso 6: Inicializar grafo de invitados (opcional)

Verificar si `.kokoro/clients.json` ya existe:

```bash
ls .kokoro/clients.json 2>/dev/null && echo "existe" || echo "no existe"
```

Si ya existe:
> "El grafo de invitados ya existe en este proyecto — tus invitados estan seguros."

Si NO existe, preguntar al usuario:

> "¿Quieres inicializar el grafo de invitados de Kokoro en este proyecto?
> Esto crea `.kokoro/clients.json` — el archivo donde Kokoro registra a los
> emprendedores que acompanas. Lo necesita `/kokoro-client` y `/kokoro-onboard`."
>
> (Si no lo inicializas ahora, puedes hacerlo despues con `/kokoro-client`.)

Si confirma:

```bash
mkdir -p .kokoro
cat > .kokoro/clients.json << 'EOF'
{
  "version": 1,
  "clients": [],
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

Informar:
> "Grafo de invitados inicializado en `.kokoro/clients.json`."
> "Agrega `.kokoro/` a tu `.gitignore` — contiene datos privados de tus
> invitados que no deben entrar al repositorio."

Si declina:
> "Puedes crearlo cuando quieras con `/kokoro-client`."

### Paso 7: Detectar contexto del proyecto (opcional)

Si el proyecto tiene archivos que sugieren un tipo de negocio, mencionarlo:
- `package.json` → proyecto web/Node
- `astro.config.*` → sitio Astro
- `wp-content/` → WordPress
- `.kokoro/clients.json` → ya tiene invitados registrados

> "Detecte que este es un proyecto {tipo}. Los knowledge files estan
> listos. Puedes empezar con `/kokoro-onboard` para tu primera sesion
> o `/kokoro` para un diagnostico rapido."

## Notas para Claude

- No copiar archivos que contengan datos personales de clientes
- No copiar `.kokoro/` (datos del grafo de invitados)
- Solo copiar archivos de knowledge (metodologia, frameworks, guias)
- Si el usuario tiene dudas, explicar que los knowledge files son las
  "instrucciones" que Kokoro necesita para guiar bien — como un libro
  de recetas que el chef necesita tener en la cocina
- Nunca asumir ni hardcodear una ruta de usuario — siempre preguntar
