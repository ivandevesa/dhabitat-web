# D&Habitat by Finance · web rediseñada

## Contenido del repositorio
- `docs/` — la web ya generada, lista para subir a cualquier hosting estático (Netlify, Cloudflare Pages, GitHub Pages...).
- `build.py` + `assets/` — el código fuente. Regenerar la web: `python3 build.py docs` (versión navegable sin servidor: `python3 build.py preview --preview`). Requiere solo Python 3.
- Los datos de los 38 inmuebles están en `build.py` (lista `PROPS`); las fotos en `assets/img/` (`p` portadas, `g` galerías, `s` sitio, `l` logos).

Sitio estático (HTML + CSS + 1 JS, sin dependencias) con el estilo Samara. Fotos reales de dhabitat.es incluidas en `img/` (galería completa en cada ficha) y logos de marca.

## Publicar
1. Sube la carpeta tal cual a Netlify, Cloudflare Pages, GitHub Pages o cualquier hosting estático.
2. Rellena `js/config.js`: `FORM_ENDPOINT` (a dónde enviar los formularios) y `GA4_ID` (analítica).
3. Importa `_redirects` (301 desde las URLs antiguas) o tradúcelo a tu servidor.
4. Envía `sitemap.xml` en Search Console.

## Qué problema de la auditoría resuelve cada cosa
| Auditoría | Solución |
|---|---|
| Fichas con title genérico, sin H1 y canonical roto | 38 fichas en `/inmueble/<tipo>-venta-<municipio>-<zona>-<ref>/` con title, H1, meta description y canonical propios |
| Sin sitemap de inmuebles | `sitemap.xml` con todas las fichas y páginas |
| Sin schema | `RealEstateAgent` (con `sameAs`), `WebSite`, `RealEstateListing`+`Offer` por ficha, `BreadcrumbList`, `FAQPage`, `Service`, `ItemList` |
| LCP de 16,3 s | Sin slider; una sola imagen hero con `fetchpriority`, resto `loading=lazy`, contenedores con proporción fija (sin CLS), 14 KB de CSS, JS diferido, sin plugins |
| Contenido orientado a Barcelona | Texto reescrito para Terrassa, Rubí y el Vallès Occidental |
| Páginas huérfanas (Rubí, Cerdanyola) | Terrassa y Rubí en el menú y el pie; Cerdanyola redirigida a Terrassa |
| Pie con 5 zonas | Pie con enlaces a ambas ciudades, filtros por tipo y servicios |
| Filtro con códigos numéricos | Filtro limpio (Terrassa, Rubí) con tipo y precio |
| Ficha duplicada | Las 3 parcelas de Castellnou-Vallès Park se unifican en una ficha |
| Tres nombres de marca | Un único nombre: «D&Habitat by Finance» (igual que la ficha de Google) |
| Sin equipo ni nombres | Sección de equipo con los nombres que citan las reseñas |
| Mismos 2-3 testimonios | Testimonios + enlace a las 321 opiniones de Google |
| Sin FAQ / AEO | 11 preguntas con respuesta directa y `FAQPage`; preguntas por ciudad |
| Sello AICAT sin explicar | Explicado en FAQ y en «Nosotros» |
| Medición | Eventos de llamada y formulario preparados para GA4, con consentimiento |
| Estética 2018 | Estilo Samara |

## Pendiente (no se puede resolver desde la web)
- **Ficha de Google**: cambiar la categoría principal a «Agencia inmobiliaria», dejar «Consultor inmobiliario» como secundaria, rellenar descripción y atributos, y usar el nombre exacto «D&HABITAT by FINANCE».
- Añadir el **número de registro AICAT** en el pie y en «Nosotros».
- Sustituir los avatares del equipo por **fotos y cargos reales**.
- Confirmar si sigue existiendo la **oficina de Cerdanyola** y, si hay oficina en Rubí, añadir su dirección y horario.
- Pegar los **textos legales** completos (las 3 páginas están en noindex hasta entonces).
- Las fotos son copias de las de dhabitat.es (JPEG optimizado). Si la cartera cambia, hay que volver a descargarlas; opcional: convertirlas a **WebP**.
- Los logos están recortados de una imagen PNG; sustituir `img/l/logo.png` por el **SVG** original si se dispone de él.
- Alimentar las fichas desde el CRM: las descripciones son un resumen de los datos publicados. Revisar datos: la casa 0110705 (197 m²) figura con 2 habitaciones.
- Alquiler: no hay sección porque solo había un inmueble en alquiler (parkings de Can Parellada). Se añade cuando haya cartera.
- Respuestas de FAQ y datos de cartera a **24/10/2026**: que D&Habitat los valide.
