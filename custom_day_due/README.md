El módulo contiene el desarrollo que permite añadir los días de pago personalizados para clientes y proveedores

 
## account.invoice (Factura)

Cuando se valida una factura de un cliente o proveedor que según su término de pago NO tiene un pago inmediato (0 días), para cada vencimiento (apunte contable que se crea con la respectiva fecha de vencimiento) que se genera revisa si el día es el que corresponde y lo aproxima a alguno de los definidos (si hay alguno definido) en días de pago según sea para 'cliente' o 'proveedor'
