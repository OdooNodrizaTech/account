Justo después de validar una factura se buscan las líneas de cada factura y las líneas de pedidos de venta para obtener los pedidos de venta (sale_order) y de esa forma, buscar todas las transacciones (payment.transaction) completadas (done) vinculadas con ese/os pedidos de venta.
Con las transacciones anteriores se buscan pagos (acccount.payment) que NO estén en borrador y vinculadas con esas transacciones para vincular esos pagos con la factura en cuestión y darla como pagada.

## Nota:
- Solo afecta a las facturas de tipo: out_invoice (Facturas de cliente)
- Solo afecta a las facturas de importe > 0
