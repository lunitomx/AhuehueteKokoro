# Meta Ads Placements — Feeds

> Referencia visual y contextual de cada ubicación (placement) dentro de la
> categoría **Feeds** de Meta Ads Manager. Documentado desde los controles de
> ubicación reales de Meta, con descripciones detalladas de cómo se renderiza
> el anuncio en cada superficie.
>
> **Uso:** Cuando se analiza el rendimiento de una campaña por placement, esta
> referencia permite entender QUÉ experiencia visual tuvo la persona en cada
> ubicación — no solo el nombre técnico, sino el contexto, el formato y la
> psicología de atención.

---

## 1. `facebook_feed`

**Nombre en Ads Manager:** Feed de Facebook
**Categoría:** Feeds
**Formato recomendado:** Imagen o video vertical (4:5)

**Descripción visual del preview:**

El anuncio aparece dentro del scroll principal del Feed de Facebook en móvil.
La estructura de arriba hacia abajo es:

1. **Encabezado del anuncio** — Foto de perfil circular del anunciante + nombre
   de la página + etiqueta "Sponsored" en gris debajo del nombre
2. **Creativo principal** — Imagen que ocupa todo el ancho de la pantalla del
   dispositivo. Aspecto ratio cercano a 4:5 (vertical). Este es el elemento de
   mayor peso visual — domina el 60% del espacio del anuncio
3. **Barra de enlace** — Franja gris debajo de la imagen con: dominio en
   mayúsculas + headline del anuncio
4. **Prueba social** — Línea de reacciones: ícono de like + "[nombre] and X
   others" a la izquierda, "X Comments" a la derecha
5. **Barra de acciones** — Tres botones: Like | Comment | Share

**Contexto de experiencia:** El anuncio compite directamente con publicaciones
orgánicas de amigos y páginas. El usuario lo encuentra mientras hace scroll
vertical. La atención es fugaz — el creativo tiene que detener el pulgar en
menos de 1 segundo.

---

## 2. `facebook_profile_feed`

**Nombre en Ads Manager:** Feed del perfil de Facebook
**Categoría:** Feeds
**Formato recomendado:** Imagen cuadrada (1:1) o video vertical (4:5)

**Descripción visual del preview:**

El anuncio aparece cuando un usuario visita el perfil de otra persona y hace
scroll por su feed. El contexto es distinto al Feed principal — el usuario
está explorando el contenido de alguien específico.

Estructura de arriba hacia abajo:

1. **Contexto del perfil anfitrión** — En la parte superior se ve el perfil del
   dueño con sus tabs de navegación: Posts | Photos | Reels. El anuncio vive
   *dentro* del contenido de ese perfil
2. **Encabezado del anuncio** — Foto de perfil circular del anunciante + nombre
   + badge de verificación + etiqueta "Sponsored" + disclaimer "Not affiliated
   with [nombre]" (Meta aclara que el anuncio no tiene relación con el dueño
   del perfil) + botón X para cerrar el anuncio
3. **Copy del anuncio** — Texto sobre el creativo
4. **Creativo principal** — Imagen de ancho completo, aspecto cercano a 1:1
   (cuadrado)
5. **Barra de enlace** — Dominio + headline + botón CTA "Shop Now" a la derecha
6. **Prueba social** — Reacciones + contadores de likes y comentarios
7. **Barra de acciones** — Like | Comment | Share

**Contexto de experiencia:** El usuario NO está en modo scroll pasivo — está
visitando intencionalmente el perfil de alguien. El anuncio interrumpe esa
exploración dirigida. Meta agrega el disclaimer "Not affiliated with [nombre]"
para evitar confusión. El creativo compite contra el contenido de la persona
cuyo perfil se visita, lo cual eleva el estándar de relevancia.

**Diferencia clave vs Facebook Feed:** El disclaimer de no-afiliación, el formato
cuadrado (1:1) como recomendación primaria en lugar de vertical (4:5), y el
contexto de atención dirigida vs scroll pasivo.

---

## 3. `instagram_feed`

**Nombre en Ads Manager:** Feed de Instagram
**Categoría:** Feeds
**Formato recomendado:** Imagen cuadrada (1:1) o video vertical (4:5)

**Descripción visual del preview:**

El anuncio aparece en el scroll principal del Feed de Instagram en móvil. La
interfaz es visualmente más limpia que Facebook — menos texto, más peso en la
imagen.

Estructura de arriba hacia abajo:

1. **Header de navegación** — Logo "Instagram" en la esquina superior izquierda,
   íconos de corazón (notificaciones) y messenger a la derecha
2. **Encabezado del anuncio** — Foto de perfil circular del anunciante + nombre
   de usuario (handle) + etiqueta "Ad" en gris + botón "Follow" en azul. Más
   compacto que Facebook — no hay línea de "Sponsored" separada, solo "Ad"
3. **Creativo principal** — Imagen que ocupa todo el ancho de pantalla. Aspecto
   ratio cercano a 4:5 (vertical). Botón CTA "Shop now" como overlay en la
   parte inferior del creativo
4. **Barra de engagement** — Íconos de corazón, comentario, compartir (paper
   plane) a la izquierda + ícono de guardar (bookmark) a la derecha. Contadores
   de likes y comentarios debajo
5. **Prueba social contextual** — "Followed by @[handle] and X others" —
   Instagram muestra si personas que tú sigues también siguen a ese anunciante.
   Esto es exclusivo de Instagram
6. **Copy del anuncio** — Texto debajo de la imagen (no arriba como en Facebook)
7. **Siguiente post orgánico** — Se asoma el inicio del siguiente post,
   indicando que el anuncio vive en un flujo continuo de contenido

**Contexto de experiencia:** Instagram es visual-first. El copy queda subordinado
al creativo — aparece *debajo* de la imagen, no arriba como en Facebook. El
botón "Follow" compite con el CTA "Shop now", creando dos posibles acciones. La
prueba social de "Followed by [gente que conoces]" es un mecanismo de confianza
poderoso que Facebook Feed no tiene.

**Diferencias clave vs Facebook Feed:** No hay barra de enlace separada (el CTA
está sobre la imagen), el copy va debajo del creativo en vez de arriba, la
prueba social es de seguidores mutuos en lugar de reacciones, y el botón
"Follow" agrega un segundo objetivo de conversión.

---

## 4. `instagram_profile_feed`

**Nombre en Ads Manager:** Feed del perfil de Instagram
**Categoría:** Feeds
**Formato recomendado:** Imagen cuadrada (1:1) o video vertical (4:5)

**Descripción visual del preview:**

El anuncio aparece cuando un usuario visita el perfil de otra persona en
Instagram y hace scroll por sus publicaciones en vista expandida (no en la
grilla, sino ya dentro del post).

Estructura de arriba hacia abajo:

1. **Contexto del perfil anfitrión** — Header con "Posts" + nombre de usuario
   del dueño del perfil. El usuario estaba navegando las publicaciones de esa
   persona específica
2. **Encabezado del anuncio** — Foto de perfil circular + handle del anunciante
   + etiqueta "Ad" en gris
3. **Creativo principal** — Imagen de ancho completo, ratio cercano a 4:5.
   Botón CTA "Shop now" como overlay en la zona inferior del creativo
4. **Barra de engagement** — Corazón, comentario, compartir a la izquierda +
   bookmark a la derecha. Contadores de likes y comentarios
5. **Prueba social** — "Followed by @[handle] and X others" — misma mecánica de
   seguidores mutuos del Feed de Instagram
6. **Copy del anuncio** — Texto debajo de la imagen
7. **Siguiente post orgánico** — Se asoma el post del dueño del perfil debajo,
   con su grilla de íconos (grid, reels, tagged)

**Contexto de experiencia:** El usuario está en modo exploración dirigida —
visitó un perfil específico y está recorriendo su contenido. El anuncio se
intercala entre los posts de esa persona. Es una interrupción más notoria que
en el Feed general porque el usuario tiene expectativa de ver solo contenido
de ese perfil.

**Diferencias clave vs Instagram Feed:** Contexto de navegación intencional
(perfil específico vs scroll general). El post siguiente es del dueño del
perfil. No se muestra disclaimer de "Not affiliated" como en Facebook Profile
Feed — Instagram lo maneja con la etiqueta "Ad" solamente. Visualmente casi
idéntico, pero la psicología de atención es distinta.

---

## 5. `facebook_marketplace`

**Nombre en Ads Manager:** Facebook Marketplace
**Categoría:** Feeds
**Formato recomendado:** Imagen cuadrada (1:1) o video vertical (4:5)

**Descripción visual del preview:**

El anuncio aparece dentro de Facebook Marketplace — el contexto donde la
persona ya está en mentalidad de compra/búsqueda de productos.

Estructura de arriba hacia abajo:

1. **Header de Marketplace** — Barra de búsqueda en la parte superior
   ("Search"), confirmando que el usuario está dentro de la sección Marketplace
2. **Encabezado del anuncio** — Foto de perfil circular del anunciante + nombre
   de la página + etiqueta "Sponsored". Mismo formato que Facebook Feed
3. **Creativo principal** — Imagen de ancho completo, ratio cercano a 4:5
4. **Barra de enlace (diferente al Feed)** — Fondo oscuro/gris. Contiene:
   headline + subtexto con propuesta de valor + botón CTA "Shop Now" a la
   derecha. Esta barra es más prominente que la del Feed — tiene más texto y
   el CTA es un botón visible
5. **Sección "More Items"** — Debajo del anuncio aparece "More Items" seguida de
   thumbnails de productos reales de Marketplace. El anuncio se intercala entre
   listings orgánicos de productos

**Contexto de experiencia:** El usuario está en modo compra activa — navegando
productos, comparando. La intención comercial es alta de entrada. El anuncio
compite contra listings orgánicos de productos reales con precio visible. La
barra de enlace es más agresiva (headline + beneficio + CTA) porque el
contexto lo permite.

**Diferencias clave vs Facebook Feed:** La barra de búsqueda arriba (contexto
Marketplace), la barra de enlace más robusta con subtexto de beneficio + botón
CTA explícito, y los thumbnails de "More Items" debajo. No hay barra de
acciones (Like/Comment/Share) ni prueba social — prioriza conversión directa
sobre engagement social.

---

## 6. `facebook_right_column`

**Nombre en Ads Manager:** Columna derecha de Facebook
**Categoría:** Feeds
**Formato recomendado:** Imagen o video horizontal (1.91:1)
**Dispositivo:** Solo desktop

**Descripción visual del preview:**

Este es el único placement de Feeds que es exclusivo de desktop. El anuncio
aparece en la columna derecha de Facebook mientras el usuario navega el Feed
principal en su computadora.

Estructura visible:

1. **Contexto desktop** — Interfaz completa de Facebook en computadora: barra
   superior con nombre del usuario, íconos de navegación. En la columna central
   se ve contenido orgánico. El anuncio vive a la DERECHA de todo esto
2. **Etiqueta "Sponsored"** — Texto pequeño sobre el anuncio, sin foto de
   perfil del anunciante. Mucho más discreto que los placements de Feed
3. **Creativo principal** — Imagen compacta en formato horizontal (1.91:1). El
   tamaño es significativamente más pequeño que en cualquier placement de Feed
   — ocupa solo la columna derecha, no el ancho completo
4. **Texto del anuncio** — Debajo de la imagen: headline + URL + copy
   descriptivo. Todo en tipografía pequeña
5. **Elementos circundantes** — Debajo del anuncio aparecen links de Facebook:
   selector de idioma, links de Privacy, Terms, Advertising. El anuncio comparte
   espacio con el footer informativo de Facebook

**Contexto de experiencia:** Es el placement más periférico y de menor impacto
visual de todos los Feeds. El usuario tiene su atención en la columna central
(el Feed) y la columna derecha es territorio de visión lateral. Es esencialmente
un banner lateral clásico.

**Diferencias clave vs otros Feeds:** Solo desktop (no mobile), formato
horizontal obligatorio (1.91:1), sin foto de perfil del anunciante, sin barra
de engagement, sin prueba social, tamaño significativamente menor. Es el
placement con menor inmersión visual de toda la familia Feeds.

---

## 7. `instagram_explore`

**Nombre en Ads Manager:** Sección "Explorar" de Instagram
**Categoría:** Feeds
**Formato recomendado:** Imagen cuadrada (1:1) o video vertical (4:5)

**Descripción visual del preview:**

El anuncio aparece cuando el usuario ya hizo tap en una publicación desde la
grilla de Explore y está haciendo scroll vertical por el feed de contenido
expandido. No aparece en la grilla de thumbnails, sino dentro del flujo de
posts una vez que se entra a ver uno.

Estructura de arriba hacia abajo:

1. **Header de navegación** — Flecha de regreso (←) + título "Explore" centrado,
   confirmando que el usuario está dentro de la sección Explore
2. **Encabezado del anuncio** — Foto de perfil circular + handle del anunciante
   + badge de verificación + etiqueta "Ad" en gris
3. **Creativo principal** — Imagen de ancho completo, ratio cercano a 4:5. Botón
   CTA "Shop now" como overlay en la zona inferior del creativo
4. **Barra de engagement** — Corazón, comentario, compartir a la izquierda +
   bookmark a la derecha. Contadores de likes y comentarios
5. **Copy del anuncio** — Texto debajo de la imagen
6. **Barra inferior de navegación** — Íconos de Home, Search, Reels, Shopping,
   Profile. El ícono de Search (lupa) resaltado

**Contexto de experiencia:** El usuario está en modo descubrimiento — entró a
Explore buscando contenido nuevo, fuera de las cuentas que sigue. La mentalidad
es curiosidad y apertura. Mayor receptividad a marcas nuevas y contenido
inesperado. Es uno de los mejores placements para awareness y adquisición de
nuevas audiencias.

**Diferencias clave vs Instagram Feed:** El header dice "Explore" con flecha de
regreso. La psicología es distinta: en Feed el usuario ve contenido de gente
que eligió seguir; en Explore está abierto a descubrir lo desconocido.
Visualmente idéntico, pero la receptividad a marcas nuevas es mayor.

---

## 8. `instagram_explore_home`

**Nombre en Ads Manager:** Inicio de la sección "Explorar" de Instagram
**Categoría:** Feeds
**Formato recomendado:** Imagen o video vertical (4:5)

**Descripción visual del preview:**

Este es el placement que aparece directamente en la **grilla de thumbnails** de
Explore — antes de que el usuario haga tap en cualquier post. Es la primera
pantalla que ve al entrar a la lupa.

Estructura visible:

1. **Grilla de Explore** — Mosaico de thumbnails en formato variable: algunas
   celdas pequeñas cuadradas, algunas rectangulares que ocupan más espacio (2
   filas de alto). La grilla tiene aproximadamente 3 columnas
2. **El anuncio como celda** — Una de las celdas de la grilla ES el anuncio. No
   tiene encabezado, no tiene copy, no tiene barra de engagement. Es solo la
   imagen/thumbnail compitiendo visualmente con todas las demás celdas orgánicas.
   No se distingue "Sponsored" o "Ad" a nivel de grilla
3. **Barra inferior de navegación** — Íconos de Home, Search (lupa), Reels,
   Shopping, Profile. La lupa activa

**Contexto de experiencia:** Es el momento de máxima distracción visual. El
usuario ve 9-12 thumbnails simultáneamente en pantalla. El anuncio tiene que
ganar un tap solo con la fuerza de la imagen — no hay texto, no hay nombre de
marca, no hay CTA visible. Es pura competencia visual.

**Diferencias clave vs Sección "Explorar":** Ese otro placement aparece DESPUÉS
del tap (en el feed vertical expandido). Este aparece ANTES — en la grilla
misma. No hay copy, no hay engagement, no hay branding visible. Solo el
creativo como thumbnail. Es el placement más exigente visualmente de toda la
familia Feeds.

---

## 9. `facebook_explore_businesses`

**Nombre en Ads Manager:** Sección "Explorar negocios" de Facebook
**Categoría:** Feeds
**Disponibilidad:** Limitada por país — Meta indica "Esta ubicación no está
disponible para al menos uno de los países que seleccionaste"
**Formato recomendado:** No especificado (estructura similar a Facebook Feed)

**Descripción visual del preview:**

El anuncio aparece dentro de la sección "Explore Businesses" de Facebook — un
espacio dedicado exclusivamente a descubrir negocios y páginas comerciales.

Estructura de arriba hacia abajo:

1. **Header de sección** — Flecha de regreso (←) + título "Explore Businesses"
   centrado. Sección separada del Feed principal
2. **Encabezado del anuncio** — Logo/foto de perfil del anunciante + badge de
   verificación + nombre de la página + etiqueta "Sponsored" + menú (⋯). Copy
   del anuncio debajo del nombre
3. **Creativo principal** — Imagen de ancho completo, ratio cercano a 4:5
4. **Barra de enlace** — Dominio + headline + botón CTA "Shop Now" a la derecha
5. **Prueba social** — Reacciones (like, love, care) + contadores
6. **Barra de acciones** — Like | Comment | Share

**Contexto de experiencia:** El usuario entró voluntariamente a una sección de
descubrimiento de negocios. La intención comercial es explícita — no es un
anuncio interrumpiendo contenido social, es contenido comercial dentro de un
espacio comercial. La resistencia al anuncio es mínima.

**Diferencias clave vs Facebook Feed:** El header "Explore Businesses" cambia
todo — el usuario eligió ver negocios. Disponibilidad geográfica limitada.
Estructura del anuncio prácticamente idéntica al Feed.

---

## 10. `threads_feed`

**Nombre en Ads Manager:** Feed de Threads
**Categoría:** Feeds
**Formato recomendado:** Imagen o video horizontal (1.91:1) o cuadrado (1:1)

**Descripción visual del preview:**

El anuncio aparece dentro del feed principal de Threads — la plataforma de
conversación de Meta. Threads es text-first.

Estructura de arriba hacia abajo:

1. **Header de Threads** — Logo de Threads (ícono @) en la parte superior
2. **Encabezado del anuncio** — Foto de perfil circular + handle del anunciante
   + etiqueta "Ad" + menú (⋯). Formato compacto, estilo conversacional
3. **Copy del anuncio (arriba)** — Texto del post ARRIBA del creativo. En
   Threads el texto es protagonista
4. **Creativo principal** — Imagen con bordes redondeados, NO ocupa el ancho
   completo. Tiene márgenes laterales visibles. Aspecto de tarjeta incrustada
   dentro del post
5. **Copy del anuncio (abajo)** — Texto adicional debajo de la imagen
6. **Barra de engagement** — Corazón, comentario (burbuja), repost (flechas
   circulares), compartir (paper plane). Sin contadores visibles

**Contexto de experiencia:** Threads es conversación pública al estilo Twitter/X.
El usuario está leyendo texto, opiniones, noticias. Un anuncio visual resalta
en un feed text-heavy. El copy tiene más peso relativo que en Instagram porque
la plataforma entrena al usuario a leer primero.

**Diferencias clave vs otros Feeds:** Formato horizontal (1.91:1) como opción
primaria — único entre plataformas móviles de Meta. Imagen con bordes
redondeados y márgenes (no full-width). Copy arriba Y debajo del creativo. Sin
contadores de engagement visibles. Sin botón CTA explícito. Sin prueba social.
Es el placement más "orgánico" visualmente — se disfraza de post de Threads.

---

## 11. `facebook_notifications`

**Nombre en Ads Manager:** Notificaciones de Facebook
**Categoría:** Feeds
**Formato recomendado:** No se requieren imágenes ni videos

**Descripción visual del preview:**

Este es el placement más atípico de toda la familia Feeds — no usa creativos
visuales. El anuncio aparece como una línea de texto dentro de la bandeja de
notificaciones de Facebook.

Estructura visible:

1. **Lista de notificaciones** — Notificaciones orgánicas con formato estándar:
   foto de perfil circular + texto + menú (⋯)
2. **El anuncio como notificación** — Una línea entre las notificaciones
   orgánicas. Contiene: foto de perfil del anunciante (logo pequeño circular) +
   texto tipo "You might be interested in [marca]: '[copy truncado]...'" +
   etiqueta "Sponsored" debajo en texto gris pequeño. El texto se trunca con
   "..." indicando que hay más copy si se hace tap
3. **Sin creativo visual** — No hay imagen, no hay video, no hay CTA visible.
   Solo texto + ícono de la página. Es puro copy

**Contexto de experiencia:** El usuario está revisando SUS notificaciones —
respuestas a sus posts, menciones, cumpleaños. Es un espacio personal e íntimo.
El anuncio se disfraza de notificación. No hay competencia visual — es pura
competencia de copywriting. El headline tiene que ser irresistible en una sola
línea truncada.

**Diferencias clave vs todos los demás Feeds:** Cero componente visual — es el
único placement donde no se necesita imagen ni video. Contexto de bandeja de
notificaciones (espacio más personal de Facebook). Formato de una sola línea
con truncado. Sin engagement, sin prueba social, sin CTA visible. Es puro
copywriting.

---

## Tabla resumen — Feeds

| # | Placement | Formato | Dispositivo | Prueba social | CTA | Visual weight |
|---|-----------|---------|-------------|---------------|-----|---------------|
| 1 | Facebook Feed | 4:5 | Mobile | Reacciones + comentarios | Barra de enlace | Alto |
| 2 | Facebook Profile Feed | 1:1 / 4:5 | Mobile | Reacciones + comentarios | Shop Now + enlace | Alto |
| 3 | Instagram Feed | 1:1 / 4:5 | Mobile | Seguidores mutuos | Overlay en imagen | Alto |
| 4 | Instagram Profile Feed | 1:1 / 4:5 | Mobile | Seguidores mutuos | Overlay en imagen | Alto |
| 5 | Facebook Marketplace | 1:1 / 4:5 | Mobile | Ninguna | Shop Now prominente | Alto |
| 6 | Facebook Right Column | 1.91:1 | Desktop | Ninguna | Ninguno visible | Bajo |
| 7 | Instagram Explore | 1:1 / 4:5 | Mobile | Ninguna visible | Overlay en imagen | Alto |
| 8 | Instagram Explore Home | 4:5 | Mobile | Ninguna | Ninguno | Thumbnail |
| 9 | Facebook Explore Businesses | ~4:5 | Mobile | Reacciones + comentarios | Shop Now + enlace | Alto |
| 10 | Threads Feed | 1.91:1 / 1:1 | Mobile | Ninguna | Ninguno visible | Medio |
| 11 | Facebook Notifications | Sin imagen | Mobile | Ninguna | Ninguno | Cero (solo texto) |
