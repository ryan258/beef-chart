# Hoja de ruta y estado de la evidencia

[English](roadmap.md) · **Español (Argentina)**

Estado reconciliado al 16 de octubre de 2026. **La v1 de referencia personal está completa dentro del alcance local acotado de abajo.** El proyecto es un atlas educativo bilingüe y una referencia personal de contexto minorista, con carga sencilla de precios locales. Los informes del 9, el 12 y el 14 de octubre en `reports/` son evaluaciones y propuestas con fecha. No convierten en requisito ni en función implementada cada extensión profesional de más abajo.

## Cierre de la v1 personal — 16 de octubre

- **Retomar:** enlaces estables de corte e idioma, copia del enlace y un botón explícito para retomar el último corte. Un ID desconocido permite seguir buscando; el almacenamiento bloqueado no impide consultar.
- **Llevar una nota:** las 24 fichas tienen una nota seleccionable y copiable con ambos nombres, las aclaraciones y el contexto de preparación existentes, y los precios manuales válidos seleccionados con monto, unidad y fecha originales. Si falla el portapapeles, el texto queda seleccionado.
- **Entender:** Compará lleva a los precios y Leé las proporciones de valor abre su tabla. El resumen separa los períodos de las fuentes de la fecha de compilación; Fuentes y métodos conserva el detalle.
- **Recorrido local verificado:** búsqueda bilingüe, ficha, nota/enlace, cierre y reanudación; foco y recorrido por teclado; escritorio y 320 px; carga, recarga y borrado de un precio sintético mediante el manejador real y un archivo temporal aislado. El [registro con fecha](docs/TRUTH-HARMONY.md) detalla las verificaciones y los límites de las herramientas del navegador.

Esto cierra la implementación de referencia personal. La cobertura completa, las unidades originales de achuras verificadas, las especificaciones y el costeo profesional, el historial completo, otras especies y los módulos de enseñanza quedan como opciones. La aceptación humana con tecnologías de asistencia o dispositivos, la revisión especializada y la publicación son alcances separados. Los cambios quedan sin commit.

## Seguimiento del 15 de octubre (implementado)

- **IPCVA** es la fuente mensual principal del AMBA para 22 filas de carne vacuna cubiertas. Los promedios de cotizaciones directas de USD del BCRA que les corresponden tienen su propia procedencia, y las observaciones originales de Carrefour conservan sus fechas y su tipo de cambio.
- **El ejemplo PDF/texto del USDA del 9 de octubre** se conserva, y su ventana explícita de finalización de ofertas del 3 al 15 de octubre se procesa sin la consulta a la página de publicación, que había agotado el tiempo de espera. Una corrida de una sola fuente aceptó 11 observaciones. Los formatos futuros desconocidos y la disponibilidad continua del proveedor siguen sin demostrarse.
- **Bola de lomo** se conecta con su propia observación del IPCVA. Las 24 fichas muestran cobertura, de modo que los valores conservados, faltantes, no publicados y manuales son visibles, y cada familia visual rotula qué es observación de una fuente y qué es ilustración. La equivalencia entre productos sigue con aclaraciones.
- **Precios manuales:** el archivo activo trae diez cortes ARS/kg precargados. Completá fecha y precio numérico de a poco; las filas sin terminar se ignoran. Los precios válidos del usuario reemplazan solo la selección que se muestra, y las observaciones de las fuentes y las advertencias originales sobre las achuras siguen disponibles.
- **Recarga:** alcanza con guardar un cambio en los precios manuales y recargar, gracias a la ruta loopback en vivo y sin caché. Solo un servidor que corre con el lanzador anterior necesita un reinicio para adoptarla; los cambios en otros archivos públicos siguen requiriendo reiniciar.
- **Validación y recuperación:** están implementadas la validación semántica automática compartida y la retención de entradas desactualizadas de la misma fuente. Una observación anterior más el archivo aparte de Carrefour originales dan una recuperación acotada, no un historial inmutable completo.

La [guía manual](docs/manual-prices.es.md), el [contrato del proceso de datos](docs/data-pipeline.es.md), la [arquitectura](docs/architecture.es.md) y el [registro de verificación](docs/TRUTH-HARMONY.md) con fechas describen el comportamiento actual. Las verificaciones de precios manuales y recarga pasaron 18 casos de integración en Node y siete del manejador HTTP en Python. Las verificaciones de visualización más amplias y la evidencia del navegador de antes siguen atadas a sus propias pasadas.

## Estado visual, 12 y 13 de octubre de 2026 (implementado)

Los 24 cortes del catálogo tienen ilustraciones de época en media tinta con fondo transparente, que usan seis tarjetas populares, cuatro tarjetas especiales y las fichas de cada corte. El ribeye y el sirloin son distintos. La vaca de la portada y el campo comparten el mismo arte en media tinta, y hay favicons de la vaca en SVG y PNG. Los diagramas interactivos de papel recortado mantienen 20 controles de cortes argentinos y nueve de regiones de EE. UU., con nombre completo al pasar el mouse o enfocar, activación por teclado y referencias de capas con rayado. Los mapas se apilan hasta los 800 px, y las fichas angostas dejan lugar para el control de cierre.

El [registro del arte](docs/artwork-prompts.md) reúne los prompts conservados, las asignaciones de imágenes, las fuentes y la evidencia del navegador en escritorio y celular. El trabajo de arte y diagramas mantuvo intactas las identidades de los cortes, las asignaciones de precios, los colores de los gráficos y las proporciones didácticas. Después, el seguimiento de correcciones de más abajo conectó las series de Pecho y Cuadrada que se habían omitido. Los derechos de las fuentes y la aceptación anatómica por especialistas siguen abiertos.

## Seguimiento de correcciones del 13 de octubre (implementado)

- **Límites de la actualización minorista:** se clasifica la recuperación ante respuestas HTTP incompletas; se validan las formas anidadas del catálogo; cada lote del catálogo y del USDA se valida antes de fusionarse; el estado del catálogo informa con honestidad sin coincidencias, parcial y error; las actualizaciones incompletas terminan con código distinto de cero.
- **Búsqueda y diseño:** la búsqueda indexa los dos idiomas sin importar el idioma que se muestre; los desplazamientos de los enlaces internos siguen la altura medida del encabezado fijo; el panel de búsqueda tiene foco con contraste (dorado sobre el panel azul, tinta dentro del cuadro blanco).
- **Estados de carga:** cargando, listo y no disponible son estados distintos, y la ficha activa se actualiza sin perder el foco ni el desplazamiento.
- **Precios y localización:** asignaciones de precios de Pecho y Cuadrada; ejes, leyenda, porcentajes, números de tablas y región de los registros nuevos localizados; el mismo comportamiento de lectura en tablas a 600 px; texto coherente para la molleja con glándula sin especificar.
- **Revisión final:** la precisión de los montos originales es la misma en todas las vistas de evidencia, la recuperación ante una carga fallida sigue distinta de la ausencia de observaciones, y el diálogo de Otros valores conserva su texto canónico al cambiar de idioma.

Ese seguimiento dejó intactos los datos guardados de entonces y el arte; las actualizaciones de fuentes del 15 de octubre son un trabajo aparte. La evidencia puntual y los límites que quedan están en [TRUTH-HARMONY.md](docs/TRUTH-HARMONY.md). No implementa las funciones posteriores de estado guardado, fichas para el carnicero, historial de fuentes ni mesa de trabajo profesional.

## Fase 1: Verdad y armonía (implementada)

Rechazo coherente de unidades, especies y presentaciones del catálogo que no coinciden. Un contrato explícito de semana de vigencia del USDA, con rechazo seguro ante formatos sin resolver. Validación de valores positivos y de fechas. Tipo de cambio histórico con aclaraciones. Estados de intento por fuente y por corte con referencias conservadas. Precios originales cuando falta la conversión. Contexto de datos guardados, de estado y de fuente. Diálogos nativos con alternativas de directorio y tablas completas. Aislamiento de D3 y de complementos. Fichas y vistas de tablas legibles en pantallas angostas. Un recorrido didáctico de 100 unidades, con semántica explícita de valor y radar. Nombres anatómicos con aclaraciones. Aclaración de escala de unidades para los precios de achuras (se retienen los precios de *mollejas*, *riñón* y *lengua* y se conserva la evidencia guardada). Un lanzador público seguro en loopback. Documentación reconciliada.

También están implementados: **C06**, intentos independientes de BLS, INDEC y tipo de cambio mensual con validación por fuente, observaciones conservadas, recuperación del INDEC solo en moneda original y una única escritura atómica; y **C14**, evidencia de muestreo del catálogo que pertenece a cada observación, con exposición coherente en fichas y tablas, que declara de forma explícita la cobertura histórica desconocida y la posible truncación de consultas.

La validación y los límites que quedan están en [TRUTH-HARMONY.md](docs/TRUTH-HARMONY.md). Las verificaciones deterministas y locales en el navegador no equivalen a aceptación profesional, de producción, con proveedores reales, en dispositivos o con tecnologías de asistencia, ni a WCAG. Están registrados un formato del USDA del 9 de octubre y una corrida de una sola fuente; los otros formatos y la compatibilidad continua con las fuentes en vivo siguen abiertos. Se conserva una observación anterior, y no hay un almacén de historial completo. La paginación del catálogo y la cobertura por región de entrega no están implementadas. Los derechos de fuentes e imágenes y la aceptación por especialistas de la correspondencia entre cortes siguen abiertos. Las pasadas de corrección originales no actualizaron precios, y las actualizaciones posteriores de IPCVA/BCRA y USDA conservan la fecha y la evidencia propias de cada observación.

## Fase 2: Una referencia excepcional para entusiastas

**Implementado:** funcionamiento bilingüe (inglés / castellano porteño) con `assets/i18n.js` y el botón del encabezado que cambia el idioma en el momento, con voseo rioplatense; un parámetro de URL (`?lang=es-AR` / `?lang=en`) que tiene prioridad sobre la preferencia opcional en `localStorage`; traducción dinámica de toda la página en las 24 fichas, los diagramas, las tablas y los mensajes de búsqueda; búsqueda bilingüe sin distinguir tildes y con alias argentinos; y se preservan la evidencia de precios, las unidades numéricas y las reglas sobre los precios de achuras que no se publican.

**Opciones después de v1:** una ampliación revisada y canónica del catálogo; sustitutos y comparaciones explicados; fichas diseñadas para imprimir; referencias de preparación y seguridad según el producto; cantidades editables; y tareas guardadas con varios cortes. Los enlaces, la reanudación de un corte y las notas de texto ya están implementados. *Prueba de la extensión:* alguien elige un corte que no conoce, hace un pedido entendible, llega a una guía de preparación con fuentes y retoma una tarea de varios cortes sin reconstruirla.

## Fase 3: Una mesa de trabajo profesional y práctica

Extensiones opcionales que se apoyan en el archivo de precios cargados por el usuario: especificaciones de producto revisadas, precios privados de proveedores con aclaraciones, rendimiento de desposte real o supuesto de forma explícita, costeo por porción utilizable, y escenarios reproducibles guardados o exportados. *Prueba de salida:* un profesional compara dos ofertas reales y calificadas y reproduce por su cuenta la decisión de costo utilizable.

## Fase 4: Contexto de mercado confiable

Adaptadores independientes aceptados, comprobantes originales, observaciones y revisiones inmutables, una fuente profesional elegida para cada mercado (EE. UU. y Argentina), y un transporte y una convención de tipo de cambio actual revisados. *Prueba de salida:* cada serie adoptada se concilia con la evidencia original conservada de la fuente y resiste los estados faltante, revisado y de error sin una falsa comparabilidad.

## Fase 5: Amplitud y uso revisados

Funciones elegidas de nutrición, entrenamiento, uso sin conexión e impresión, importaciones y cambios significativos, seguidas de las regiones, especies o necesidades de costo puesto en destino que se elijan. La ampliación sigue el valor real para las tareas y la aceptación del dominio. Una función planificada no es evidencia de algo entregado, y la programación futura, el acceso a proveedores, los commits, los push y la publicación siguen siendo acciones aparte, controladas por el dueño del proyecto.
