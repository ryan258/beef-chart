# La vaca, de dos maneras (Beef Chart)

[English](README.md) · **Español (Argentina)**

Un atlas interactivo que pone lado a lado los cortes de carne vacuna de Argentina y de EE. UU., con una foto guardada y fechada de precios minoristas y lugar para cargar tus propios precios locales. Sirve para explorar y comparar con contexto. No muestra precios en vivo ni te dice qué está ofreciendo hoy un proveedor.

El asado argentino y la parrilla de steakhouse norteamericana reparten el mismo animal de distinta manera. Los nombres, el desposte, el hueso y la preparación cambian de un lado y del otro, así que los mapas y las ilustraciones de acá sirven para *entender* un corte, no para especificar una compra. La página combina un diseño Bauhaus con arte de época en media tinta, mapas de papel recortado en SVG y gráficos D3.

---

## Qué podés hacer

La **v1 de referencia personal está completa al 16 de octubre de 2026** para el recorrido local de consulta, nota/enlace, reanudación y precios manuales que describe la hoja de ruta. Las extensiones profesionales y la aceptación más amplia tienen un alcance separado.

- **Recorrer dos mapas de una misma vaca.** Veinte controles de cortes argentinos y nueve de regiones de EE. UU. comparten el resaltado al pasar el mouse o enfocar, muestran el nombre completo y funcionan con teclado. Si el mapa no te sirve, hay un directorio completo. El rayado marca al lomo, la entraña y el peceto como referencias superpuestas.
- **Abrir la ficha de cualquiera de los 24 cortes.** Cada una trae su ilustración en media tinta, el contexto de cocción y los precios guardados con su evidencia. Hay tarjetas para seis cortes populares y cuatro especiales (*bife de costilla*, *mollejas*, *riñón*, *lengua*).
- **Retomar un corte y llevarte una nota.** Cada ficha tiene **Copiá el enlace del corte** y una **Nota para la carnicería** con ambos nombres de referencia, la aclaración sobre su relación y el contexto de preparación. Los precios manuales seleccionados conservan monto, unidad y fecha originales. **Retomá el último corte** ofrece el último corte abierto y su idioma cuando el navegador permite guardarlos; nunca abre una ficha anterior por su cuenta.
- **Leerlo en inglés o en castellano porteño.** El botón del encabezado traduce toda la página: fichas, gráficos, tablas, mensajes de búsqueda y aclaraciones sobre los precios. El español usa voseo rioplatense y algo de lunfardo, y los nombres estadounidenses quedan a la vista como referencia cruzada. La búsqueda entiende los dos vocabularios, con o sin tildes, y también alias como *ojo de bife* y *tira de asado*.
- **Leer cada precio con su contexto.** Cada observación indica fuente, región, período, presentación del producto, disponibilidad y criterio de tipo de cambio. Los valores convertidos a USD/libra aparecen en el gráfico de comparación; los que solo existen en pesos se muestran en ARS/kg, en el texto y en las tablas. Un resumen de cobertura te dice, para cada uno de los 24 cortes, si hay una observación, una referencia conservada, un precio no publicado, un precio manual o nada.
- **Cargar tus propios precios locales.** Hay diez cortes argentinos precargados en [`data/manual-prices.json`](data/manual-prices.json). Completá fecha y precio, guardá y recargá. Las filas sin terminar se ignoran, y las observaciones automáticas siguen disponibles por debajo. Mirá [Precios manuales](docs/manual-prices.es.md).
- **Seguir la historia completa con cuatro gráficos D3:**
  - **Sankey de recorrido:** nueve regiones primarias que fluyen hacia sus usos culinarios (100 unidades ilustrativas, no un rendimiento medido).
  - **Comparación de precios EE. UU. vs. Argentina:** ofertas anunciadas del USDA y promedios mensuales del BLS frente a los precios del relevamiento del IPCVA, los promedios del INDEC, las referencias conservadas de Carrefour y los precios manuales opcionales. El color identifica al país. Los puntos vacíos y los asteriscos marcan referencias conservadas; las dagas, precios manuales en USD.
  - **Treemap de valor:** un reparto fijo e ilustrativo del valor minorista, no un cálculo con precios.
  - **Radar editorial:** seis puntajes orientativos, no mediciones sensoriales ni categorías oficiales.

Tres precios guardados de achuras (*mollejas*, *riñón*, *lengua*) quedan fuera de la comparación porque sus unidades no están verificadas. Los valores originales siguen visibles como evidencia rotulada.

### Un animal, dos vocabularios

| Argentina | Estados Unidos | Ojo con |
|---|---|---|
| Bife ancho | Ribeye | Con o sin hueso, tapa, desposte |
| Bife de chorizo | Strip loin / NY strip | No es lo mismo que una *costeleta* con hueso |
| Asado de tira | Cross-cut short ribs | Importan el grosor y la sección de costillar |
| Vacío | Flank (coincidencia parcial) | No es automáticamente un flank steak estadounidense |
| Entraña | Skirt | La entraña fina y la gruesa son distintas |
| Colita de cuadril | Tri-tip | Confirmá el desposte |

La tabla completa está en la [guía de cortes](docs/cuts-guide.es.md).

---

## Diseño

La página es un **diseño Bauhaus con ilustración de imprenta de época**. Los estilos base están en `index.html` y se completan en `assets/bauhaus.css`.

- **Grilla:** bordes de tinta de 1 px, portadas asimétricas y tarjetas de datos modulares.
- **Paleta:** lienzo `#f1f0e8`, tinta `#20211e`, rojo `#c73524`, dorado `#edc445` y azul `#234dba`. Los mapas usan sus propias tintas (terracota/ocre y azul apagado/ocre) y nunca modifican los colores de los gráficos.
- **Tipografía:** `Space Grotesk` e `Inter` para la página, `Oswald` para las etiquetas de los diagramas y `Playfair Display` para los títulos de las fichas.
- **Arte:** ilustraciones de cortes en WebP transparente de 1024 × 1024, imágenes opacas en media tinta para la portada y el campo, y diagramas SVG nativos. Los prompts, las asignaciones, las referencias y las verificaciones de visualización están en el [registro del arte](docs/artwork-prompts.md).
- **Adaptable:** puntos de corte con CSS grid y flexbox, desde más de 1600 px hasta 320 px.
- **Accesibilidad:** hay foco visible, enlaces de salto, estilos para reducir el movimiento, directorio completo y tablas de los gráficos, diálogos nativos con nombre, aislamiento de fallas y diseños de lectura para pantallas angostas. No se verificó la conformidad completa con WCAG ni el comportamiento en dispositivos y tecnologías de asistencia.

---

## Fuentes de datos

| Mercado | Fuente | Frecuencia | Qué mide |
|---|---|---|---|
| EE. UU. | **Bureau of Labor Statistics (BLS)** | Mensual | Precios promedio nacionales al consumidor, USD/libra |
| EE. UU. | **USDA AMS Grocery Feature Survey** | Semanal | Ofertas minoristas anunciadas, ponderadas por locales, extraídas de un PDF |
| AR | **Exportación de precios al consumidor del IPCVA** | Mensual | Promedios del relevamiento en el AMBA para 22 filas de carne vacuna, ARS/kg; fuente automática principal para los cortes que cubre |
| AR | **INDEC IPC-GBA** vía `datos.gob.ar` | Mensual | Promedios minoristas del Gran Buenos Aires, ARS/kg |
| AR | **Catálogo online de Carrefour Argentina** | A demanda; no hay tarea programada | Mediana de ofertas de producto crudo por kilo, de carnicería, convertida con la última cotización del BCRA devuelta |
| FX | **Historial de cotizaciones directas de USD del BCRA** | Meses completos coincidentes para el IPCVA | Promedio aritmético de las cotizaciones publicadas devueltas; distinto de la serie de tipo de cambio de valuación |
| FX | **BCRA** vía `datos.gob.ar` | Promedio mensual para el INDEC; último valor diario devuelto para el catálogo | ARS por USD, con criterio, fecha y procedencia (registrada, inferida o desconocida) en cada registro |

La salida automática se consolida en [`data/prices.json`](data/prices.json), junto con los registros separados por fuente argentina y el archivo original de Carrefour, que se conserva. Los [precios manuales](data/manual-prices.json) son una capa de visualización independiente que los scripts de actualización nunca escriben, y requieren primero una foto automática válida. El [contrato de datos](docs/data-pipeline.es.md) cubre la selección, las fechas, el tipo de cambio y el comportamiento ante fallas.

---

## Estructura del proyecto

```
beef-chart/
├── index.html                      # Catálogo de cortes, búsqueda, validación, gráficos y fichas
├── assets/
│   ├── bauhaus.css                 # Diseño y reglas de lectura adaptable
│   ├── i18n.js                     # Catálogo inglés / español argentino y formatos
│   ├── manual-prices.js            # Borradores, validación y selección de precios manuales
│   ├── reference-tools.js          # Enlaces de cortes, guardado opcional y notas de texto
│   ├── snapshot-summary.js         # Resumen de períodos de fuentes, separado de la compilación
│   └── *.webp / favicon*           # Ilustraciones de cortes, vaca y campo; íconos del navegador
├── data/
│   ├── prices.json                 # Foto automática, registros por fuente, FX y archivo original
│   ├── manual-prices.json          # Planilla activa de diez cortes: editá fecha y precio y recargá
│   └── manual-prices.template.json # Planilla en blanco opcional; la app no la carga
├── docs/                           # Las guías tienen edición en español (*.es.md); los registros fechados, no
│   ├── manual-prices.md            # Flujo de carga, unidades, machine names y recuperación
│   ├── architecture.md             # Límites de ejecución, datos y servidor
│   ├── cuts-guide.md               # Terminología de cortes y contexto de preparación
│   ├── data-pipeline.md            # Fuentes, adaptadores, FX y contrato de observaciones
│   ├── artwork-prompts.md          # Fuentes del arte, prompts y evidencia fechada de visualización
│   └── TRUTH-HARMONY.md            # Registro fechado de implementación y verificación
├── price_contract.py               # Validación v2 automática, fusión y escrituras atómicas
├── official_prices.py              # Intentos independientes de BLS, INDEC y FX de valuación
├── ipcva_prices.py                 # Exportación del IPCVA para el AMBA y selección de la fuente principal
├── bcra_fx.py                      # Promedios de cotizaciones directas de USD del BCRA para los meses del IPCVA
├── scrape-retail.py                # Orquestación de fuentes, catálogo y adaptador del PDF del USDA
├── fetch-prices.sh                 # Actualización completa explícita; los modos de una sola fuente van por Python
├── serve.sh                        # Lanzador de archivos públicos en loopback
├── serve_public.py                 # Ruta manual en vivo sin caché; el resto sale de la copia pública
├── fetch-beef.sh                   # Enriquecimiento de archivo opcional; la página no lo necesita
├── tests/                          # Verificaciones de fuentes, contrato, visualización y servidor
│   └── fixtures/                   # Fotos históricas fijas y ejemplos de fuentes conservados
├── reports/                        # Informes de revisión históricos y propuestas opcionales
├── research_notes/                 # Evidencia fechada de revisiones y búsqueda de fuentes
├── roadmap.md                      # Alcance implementado y trabajo futuro opcional
└── README.md
```

---

## Primeros pasos

### Requisitos

- Un navegador moderno (Chrome, Safari, Firefox, Edge).
- Python 3.10+ para el lanzador local y el proceso de precios.
- Opcionales, para actualizar datos o correr verificaciones: `poppler` para `pdftotext` (`brew install poppler`) y Node.js para las pruebas del contrato del navegador.

### Correr la aplicación

Usá el lanzador de archivos públicos. Hace que funcione la ruta del JSON y mantiene el repositorio y los archivos privados fuera del directorio que se sirve.

```bash
./serve.sh
```

Abrí `http://127.0.0.1:8792`. Con `BEEF_CHART_PORT` elegís otro puerto. Para detenerlo, Ctrl-C.

- **Los cambios en los precios manuales** aparecen cuando guardás y recargás. El servidor lee directamente del proyecto solo ese archivo, con la caché desactivada.
- **Cualquier otro cambio** requiere reiniciar, porque el lanzador sirve una copia temporal del resto. No sirvas la raíz del repositorio ni uses `file://`, que no puede cargar el JSON.

**Idioma.** El botón recuerda tu elección en ese navegador y actualiza la URL. Para abrir directamente en español argentino, agregá `?lang=es-AR` antes de cualquier `#sección`; con `?lang=en` se abre en inglés. Un idioma indicado en la URL tiene prioridad sobre la preferencia guardada, y el almacenamiento es opcional. La búsqueda abarca ambos idiomas sin importar el idioma de la pantalla. Las monedas y las unidades son las mismas en los dos idiomas; el español da formato argentino a fechas, decimales, porcentajes, precios originales y tipo de cambio, y escribe los montos en dólares como `US$`, también en los ejes de los gráficos. El redondeo es solo de visualización y nunca altera la evidencia guardada: USD con dos decimales, variaciones respecto del benchmark con uno, y montos originales y tipo de cambio con hasta seis.

**Pantallas chicas y carga.** Los enlaces internos tienen en cuenta el encabezado fijo. Con 600 px o menos, los gráficos densos de recorrido y de precios se abren primero como tablas. Si abrís una ficha antes de que lleguen los precios, verás un aviso de carga y después se actualiza sola, sin perder el foco ni el punto de lectura. Si la carga falla, la ficha explica cómo recuperarse; si la carga sale bien pero ese corte no tiene observación, se muestra como "faltante", un estado distinto. Pecho y Cuadrada pueden mostrar sus propias observaciones argentinas futuras, con las mismas aclaraciones.

**Enlaces y copiado.** Un enlace como `http://127.0.0.1:8792/?cut=vacio&lang=es-AR` abre esa ficha directamente. Cerrarla quita el parámetro del corte; el botón para retomar queda junto a la búsqueda. Las notas se pueden leer y seleccionar. Si el portapapeles está bloqueado, el texto queda seleccionado para copiar con el comando habitual. El resumen del mercado separa los períodos reales de cada fuente de la fecha de compilación; **Fuentes y métodos** contiene las aclaraciones detalladas.

### Correr las pruebas

Corré solo lo que toca tu cambio. Ninguna consulta proveedores reales.

```bash
# Enlaces, guardado opcional, notas, resumen de fuentes e integración de la interfaz
node --test tests/test_reference_tools.cjs tests/test_snapshot_summary.cjs tests/test_v1_finish.cjs
```

```bash
# Precios manuales y ruta de recarga
node --test tests/test_manual_prices.cjs
PYTHONPATH=.:tests python3 -m unittest -q test_live_manual_server
```

Son 18 casos de precios manuales y siete del manejador HTTP. Las pruebas del manejador usan conexiones en memoria: sin listener ni navegador.

```bash
# Cobertura de cortes y visualización localizada
node --test tests/test_price_coverage.cjs tests/test_ipcva_ui.cjs tests/test_harmony_ui.cjs tests/test_language.cjs tests/test_organ_unit_scale.cjs
```

Otras verificaciones puntuales:

```bash
# Aislamiento de fuentes oficiales C06 y regresiones afectadas de BLS y escritura atómica
PYTHONPATH=.:tests python3 -m unittest test_official_prices test_truth_harmony.TruthHarmony.test_bls_period_sorting_skips_m13_and_records_actual_previous test_truth_harmony.TruthHarmony.test_invalid_data_never_replaces_good_file

# Contrato de precios de achuras en el navegador, al cambiar la visualización de precios
node --test tests/test_organ_unit_scale.cjs

# Evidencia de muestreo del catálogo y exposición compartida en fichas y tablas
PYTHONPATH=.:tests python3 -m unittest -q test_catalog_sampling
node --test tests/test_catalog_sampling.cjs

# Selección de idioma, traducciones, formatos y aclaraciones de precios sin cambios
node --test tests/test_language.cjs tests/test_organ_unit_scale.cjs tests/test_catalog_sampling.cjs

# Regresiones de las correcciones del 13 de octubre y rutas de evidencia y recuperación afectadas
PYTHONPATH=.:tests python3 -m unittest -q test_refresh_harmony test_official_prices test_organ_unit_scale test_catalog_sampling.CatalogSampling.test_failed_empty_and_replacement_preserve_observation_owned_evidence test_truth_harmony.TruthHarmony.test_cut_failures_do_not_block_healthy_cut_or_change_dates test_truth_harmony.TruthHarmony.test_invalid_data_never_replaces_good_file test_retail_prices.PriceMatching.test_alias_dedup_conversion_and_stock test_truth_harmony.TruthHarmony.test_uniform_unit_contract_for_all_cuts test_truth_harmony.TruthHarmony.test_species_and_prepared_products_fail_closed
node --test tests/test_harmony_ui.cjs tests/test_language.cjs tests/test_organ_unit_scale.cjs tests/test_catalog_sampling.cjs
```

### Actualizar los precios

La actualización es siempre un comando explícito. Abrir la aplicación nunca pide precios nuevos.

```bash
# Actualización completa (requiere pdftotext y Python 3.10+)
./fetch-prices.sh

# Solo el IPCVA y sus promedios mensuales directos del BCRA
python3 scrape-retail.py --ipcva-only

# Solo el PDF de ofertas anunciadas del USDA
python3 scrape-retail.py --usda-only

# Consulta puntual a Carrefour para cortes específicos
python3 scrape-retail.py --cuts bife_costilla molleja rinon lengua
```

Las fuentes fallan de forma independiente y cada lote se valida antes de fusionarse, así que un corte mal formado o un lote del USDA con problemas no impide que los lotes sanos lleguen a la escritura final. Una actualización parcial, sin coincidencias o fallida guarda las observaciones sanas y los estados fechados de cada intento, y después termina con código distinto de cero. Los resúmenes de Carrefour usan `ok`, `no_match`, `partial`, `error` y `partial_error`; revisá la cobertura de cada corte. `ok` significa que se obtuvieron observaciones de referencia, no que haya una oferta disponible para comprar ahora. Los precios originales del INDEC pueden avanzar con USD no disponible cuando falta el tipo de cambio mensual coincidente. Las observaciones nuevas del catálogo registran evidencia de muestreo acotada: llegar al límite de una consulta significa que los resultados pueden estar truncados, y una respuesta corta no asegura cobertura completa. Las observaciones históricas no reciben conteos de consulta inventados. Antes de dar los datos por actualizados, revisá los estados de las fuentes y las fechas originales de cada observación; el [contrato del proceso](docs/data-pipeline.es.md) tiene el detalle.

---

## Precios manuales

Cargá los precios locales en [`data/manual-prices.json`](data/manual-prices.json) con `date`, `item`, `machine_name`, un `price` numérico, `currency` y `unit`. Los precios del mercado argentino van en `ar`; los del mercado estadounidense, en `us`.

```json
{ "price": 18500, "currency": "ARS", "unit": "kg" }
{ "price": 8.50,  "currency": "USD", "unit": "lb" }
```

Hay diez cortes argentinos precargados con fecha y precio en null; una fila se ignora hasta completar ambos. Un precio manual reemplaza lo que se *muestra* para ese corte, mientras que las observaciones automáticas y la evidencia original de Carrefour se conservan. Los precios en pesos mantienen sus unidades originales, sin conversión supuesta. Guardá y recargá; no hace falta reiniciar. Un servidor iniciado antes de que existiera esta función necesita un reinicio para incorporarla. [Referencia de formato y machine names](docs/manual-prices.es.md).

---

## Estado y registros

El [registro de correcciones](docs/TRUTH-HARMONY.md) conserva el alcance y los resultados con fecha; la [hoja de ruta](roadmap.es.md) separa lo implementado de las extensiones opcionales. Hasta ahora está implementado: el aislamiento de fuentes y el muestreo del catálogo (C06/C14), la validación semántica compartida, la incorporación de IPCVA y BCRA, la reparación del PDF del USDA, la cobertura de cortes calificada por fuente y los precios manuales. Quedan registrados un fixture PDF/texto del USDA del 9 de octubre y una actualización exitosa de una sola fuente con 11 filas. Eso confirma un formato verificado, no que el proveedor siga disponible ni que se acepte cualquier informe.

El flujo actual de precios manuales pasó 18 casos de integración más siete del manejador HTTP. Los resultados anteriores del atlas, del navegador, del proceso de datos y de visualización (46 casos) son evidencia fechada, no verificaciones repetidas después de cada edición posterior. Siguen abiertos: la equivalencia exacta entre productos, la revisión de anatomía por especialistas y de derechos, el comportamiento en dispositivos y con tecnologías de asistencia, las tres observaciones de achuras sin publicar y la aceptación para producción.

### Qué leer después

- [Precios manuales](docs/manual-prices.es.md): el flujo de todos los días (editar → guardar → recargar) y todos los machine names.
- [Arquitectura](docs/architecture.es.md) y [proceso de datos](docs/data-pipeline.es.md): cómo funciona y los contratos de datos.
- [Guía de cortes](docs/cuts-guide.es.md) y [registro del arte](docs/artwork-prompts.md): terminología, qué significan las ilustraciones y evidencia conservada del arte.
- [Verdad y armonía](docs/TRUTH-HARMONY.md): resultados cronológicos de implementación y verificación. Los conteos, hashes y limitaciones corresponden a la pasada que los registró.
- [Hoja de ruta](roadmap.es.md): alcance actual y opciones a futuro.

Los informes de `reports/` y sus `research_notes/` son evaluaciones históricas atadas a su fecha de revisión: [revisión de mercado del 9 de octubre](reports/Beef%20market%20professional%20review.md), [revisión integral del 12 de octubre](reports/Beef%20chart%20comprehensive%20review.md) y [revisión de preparación del 14 de octubre](reports/Beef%20professional%20readiness%20review.md). Las instrucciones vigentes y los resultados posteriores están en los documentos de arriba. Los registros fechados y los informes están en inglés.

## Licencia

Por ahora no hay un archivo LICENSE versionado ni un manifiesto completo de derechos sobre recursos y datos. El código, las imágenes y los datos de origen necesitan una revisión aparte de procedencia y uso; que una fuente sea de acceso público no implica permiso general para redistribuirla.
