# Propuesta de Diseño y Modificaciones - NakamaLog

## 1. Propuesta de Diseño Inicial

- **Jerarquía visual:**
  - `h1` (`1.8rem`) para el título principal de la aplicación (*NakamaLog*).
  - `h2` (`1.35rem`) para dividir las secciones de *Catálogo* y *Reviews*.
  - Texto en negritas para el nombre del anime y el puntaje de cada reseña.
- **Distribución de los elementos:**
  - Contenedor principal con `padding: 16px` y separación vertical (`gap: 12px`) entre cada tarjeta para evitar que la información se vea amontonada.
- **Contraste de colores accesible:**
  - Uso de los 4 colores definidos en `GEMINI.md`: fondo crema `#FAF7F2`, texto carbón `#191817` (contraste AAA mayor a 14:1), tarjetas en arena suave `#F2ECE4` y acentos en rojo terracota `#C83E2B`.
- **Separación de letras e interlineados accesible:**
  - `line-height: 1.6` en todo el cuerpo del documento y `letter-spacing: 0.02em` en encabezados y botones para mejorar la lectura.
- **Diseño responsivo (Móvil primero):**
  - El diseño base (sin media queries) está pensado para pantallas móviles en una sola columna vertical (`flex-direction: column`), con botones amplios fáciles de presionar.
  - Con `@media (min-width: 768px)` se acomoda en dos columnas para aprovechar pantallas de escritorio. Si se eliminan los media queries, el diseño conserva su estructura móvil primero.
- **Tipografía:**
  - `Georgia, serif` para los encabezados y `system-ui, sans-serif` para el contenido y controles.
- **Botones y tarjetas:**
  - Tarjetas con fondo `#F2ECE4`, `padding: 14px` y esquinas redondeadas de `6px`.
  - Botones en color `#C83E2B` con texto claro `#FAF7F2`.

---

## 2. Modificaciones Aplicadas a la Propuesta Inicial

### Modificación 1: Destacar visualmente la calificación en las tarjetas de reseñas
- **Cambio solicitado:** En la propuesta inicial el puntaje (`rating/10`) se veía igual que el resto del texto. Se modificó para que la calificación aparezca dentro de una etiqueta (`badge`) con el color de acento `#C83E2B` y texto claro `#FAF7F2`, separándola del comentario para identificar la nota de un vistazo.

### Modificación 2: Mejorar los botones y tarjetas en vista móvil
- **Cambio solicitado:** En móvil el botón *"Ver reviews"* quedaba pequeño al lado del título. Se modificó la tarjeta del anime para que en móvil el botón ocupe todo el ancho disponible (`width: 100%`) con un borde izquierdo de color `#C83E2B` en cada tarjeta, facilitando tocarlo con el pulgar en pantallas pequeñas.
