Funcionalidad para definir importe de comisión en las facturas (calculado de la suma de las comisiones de las lineas).

Se añade dentro de cada usuario (comercial) un valor de: % comisión en facturas
Cada vez que se valide una factura de clientes (factura o rectificativa) se definirá el % que tenga en ese momento el comercial de la factura (siempre que sea > 0%) siempre que el producto NO sea un servicio y que NO esté marcado el check de "No comisiones" en el producto (esos productos se omitirían de las comisiones).

Cuando la factura se marca como pagada se calcula el importe de comisión de todas las líneas y la comisión total de la factura (sumando la comisión de todas las líneas).

Existe un botón dentro de la factura de 'Calcular comisión' que permite forzar este proceso manualmente.
