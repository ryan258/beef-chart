# Cargar un precio manual

[English](manual-prices.md) · **Español (Argentina)**

Editá `data/manual-prices.json`. Cada precio tiene seis campos: **date, item, machine_name, price, currency, unit**. Los precios del mercado argentino van bajo `ar` y los del estadounidense bajo `us`. La sección le dice a la página a qué mercado pertenece un precio; la moneda sola no lo indica.

El archivo activo ya trae diez cortes argentinos con fecha y precio en null. Completá esas filas directamente, en vez de reemplazar el archivo por el ejemplo de abajo. Los montos de acá son solo ejemplos:

```json
{
  "ar": [
    {
      "date": "2026-10-15",
      "item": "Pecho — precio que me pasó un amigo",
      "machine_name": "pecho",
      "price": 18500,
      "currency": "ARS",
      "unit": "kg"
    }
  ],
  "us": [
    {
      "date": "2026-10-15",
      "item": "Brisket entero — carnicería del barrio",
      "machine_name": "brisket_whole",
      "price": 8.50,
      "currency": "USD",
      "unit": "lb"
    }
  ]
}
```

Los nombres de los campos y los valores de `currency` y `unit` se escriben exactamente así, en inglés: la página los lee tal cual. Lo que escribas en `item` es texto libre, en el idioma que prefieras.

## Los seis campos

Estas reglas valen para las filas completas. Las filas sin terminar se ignoran, como se explica más abajo.

- **date:** el día en que viste el precio, con el formato `AAAA-MM-DD`. Se rechazan las fechas futuras y las imposibles.
- **item:** tu propia descripción. Si te sirve, poné acá la carnicería, la ciudad, si es con o sin hueso, o las palabras exactas de tu amigo. No hay campos aparte para el lugar ni la fuente, y lo que no indiques queda sin especificar.
- **machine_name:** la clave estable de la [tabla de más abajo](#machine-names). También se acepta como alias el ID visible de la ficha. Un nombre nunca prueba que el producto sea equivalente: vos elegís el corte que el precio realmente describe.
- **price:** un número JSON positivo, sin comillas ni separadores de miles. Usá punto decimal para las fracciones, por ejemplo `8.50`. Ojo: en el JSON, `18500` va así y `8.50` con punto, aunque en la pantalla en español se muestren con coma.
- **currency:** `"ARS"` para pesos argentinos o `"USD"` para dólares estadounidenses. Se rechazan los símbolos de moneda y las cadenas que mezclan monto y unidad.
- **unit:** `"kg"` o `"lb"`. Solo se admiten `"ARS"` con `"kg"` y `"USD"` con `"lb"`. Cualquier otra combinación se rechaza de forma explícita; no se adivina ninguna conversión.

Guardá el archivo y recargá la página. El servidor local lee los precios manuales de nuevo en cada consulta y desactiva la caché para esa ruta. Un servidor que ya estaba corriendo antes de esta función necesita un reinicio; después de eso, alcanza con recargar la página.

## Completar los diez cortes de a poco

`data/manual-prices.json` ya contiene Cogote, Pecho, Garrón, Bife de costilla, Mollejas, Riñón, Lengua, Aguja, Entraña y Tapa de cuadril, cada uno con su nombre, su machine name, la moneda `"ARS"` y la unidad `"kg"`. Reemplazá `"date": null` por la fecha real de observación entre comillas, y `"price": null` por un número positivo. No hace falta copiar ni importar nada. `data/manual-prices.template.json` es una planilla en blanco opcional que la aplicación ni carga ni necesita.

Una fila sin fecha o sin precio es un **borrador** y se ignora. Cuentan como vacíos null, un campo omitido, una cadena vacía y una cadena de solo espacios. Si completás un solo campo, no cambia nada en pantalla: la observación de la fuente sigue seleccionada hasta que estén los dos y la fila pase la validación. Dejá los demás cortes sin terminar todo el tiempo que quieras.

Cuando están la fecha y el precio, rigen todas las reglas: el esquema de seis campos y las verificaciones de número, fecha, moneda, unidad y machine name. El cero, los montos negativos, los booleanos y las cadenas numéricas no cuentan como vacíos y se rechazan. Una fila completa e inválida rechaza toda la capa manual con una explicación; nunca se saltea en silencio. Las filas que no son objetos y los nombres de campo desconocidos también se rechazan, para que un error de tipeo no pase inadvertido.

## Qué hace un precio cargado

Un precio manual reemplaza la observación que se muestra para ese corte en ese mercado, aunque haya una observación automática más reciente. Su fecha real sigue visible, y la página lo rotula como **Precio manual**, con la disponibilidad y la especificación exacta del producto sin verificar. Los dos países pueden usar cualquiera de los dos formatos de moneda y unidad admitidos.

- **ARS/kg original sigue siendo ARS/kg.** No se adivina ningún tipo de cambio, y estos precios no aparecen como puntos USD/libra en el gráfico.
- **USD/libra original puede aparecer en el gráfico,** marcado con una daga (`†`).
- **Las tarjetas, la cobertura, las fichas y la tabla de evidencia** muestran el precio manual seleccionado. Las observaciones de las fuentes siguen en la tabla de evidencia completa y, cuando fueron reemplazadas, en una sección desplegable de la ficha. La evidencia original de Carrefour y sus marcas de precio no publicado no cambian.
- **Un precio manual de achuras es una observación aparte.** No verifica ni reescala el registro anterior del catálogo.

Si borrás la fecha o el precio, la fila vuelve a ser un borrador y toma su lugar el siguiente precio manual elegible o la observación automática. Si varias filas corresponden al mismo mercado y corte, gana la de fecha de observación más reciente; con la misma fecha, gana la fila de más abajo. El archivo conserva todas las filas. Al quitar la entrada seleccionada vuelve la siguiente manual o, si no quedan, la fuente automática. Una lista `ar` o `us` vacía desactiva los reemplazos de ese mercado.

Si una fila completa es inválida o hay una fila mal formada, la página rechaza la capa manual y muestra el mercado y el número de fila cuando puede. La evidencia automática sigue disponible. Antes de aplicar precios manuales se necesita una foto automática válida, y las filas se procesan aparte del contrato de la fuente automática, que sigue validando primero la foto del scraper.

Los scrapers escriben solamente `data/prices.json` y nunca tocan este archivo. No hay comando de importación ni editor en la interfaz. El lanzador sirve el archivo manual como dato público de la aplicación, así que cargá solo descripciones que no te moleste ver en el atlas.

## Machine names

Usá la clave de la sección del mercado que estás editando. Los cortes sin cobertura automática también aceptan precios manuales.

| Corte | `ar` machine_name | `us` machine_name |
|---|---|---|
| Cogote | `cogote` | `cogote` |
| Aguja | `aguja` | `chuck_roast` |
| Paleta | `paleta` | `paleta` |
| Pecho | `pecho` | `brisket_whole` |
| Brazuelo | `osobuco` | `brazuelo` |
| Bife ancho | `bife_ancho` | `ribeye_bnls` |
| Asado de tira | `asado` | `short_ribs` |
| Matambre | `matambre` | `matambre` |
| Bife de chorizo | `bife_angosto` | `strip_bnls` |
| Vacío | `vacio` | `flank` |
| Tapa de cuadril | `tapa` | `tapa` |
| Cuadril | `cuadril` | `sirloin_steak` |
| Colita de cuadril | `colita` | `tri_tip` |
| Bola de lomo | `bola_lomo` | `round_roast` |
| Nalga | `nalga` | `round_steak` |
| Cuadrada | `cuadrada` | `bottom_round` |
| Garrón | `garron` | `garron` |
| Lomo | `lomo` | `tenderloin` |
| Entraña | `entrana` | `skirt` |
| Peceto | `peceto` | `eye_round` |
| Bife de costilla | `bife_costilla` | `bife-costilla` |
| Mollejas | `molleja` | `molleja` |
| Riñón | `rinon` | `rinon` |
| Lengua | `lengua` | `lengua` |
| Carne picada (referencia) | `ground_beef` | `ground_beef` |

## Verificación puntual

`node --test tests/test_manual_prices.cjs` corre casos acotados y sin conexión para el formato numérico, la conservación de las fuentes, la salida de visualización local, la alternativa cuando falla la carga del archivo y la restauración del original al quitar un reemplazo. Los precios de ejemplo existen solo en memoria, y las pruebas no editan los archivos de precios de producción ni consultan ninguna fuente. También cubren los borradores sin terminar y la carga gradual junto con las verificaciones vecinas de visualización de precios. Esto comprueba funciones y callbacks de gráficos con dobles locales; no verifica el diseño en el navegador ni el comportamiento con tecnologías de asistencia.

Para la ruta local de recarga, `PYTHONPATH=.:tests python3 -m unittest -q test_live_manual_server` corre siete casos del manejador, sin navegador ni listener. Esos siete y los 18 casos de precios manuales pasaron en la actualización que solo cambió la recarga.
