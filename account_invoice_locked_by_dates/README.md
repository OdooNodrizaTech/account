El módulo contiene el desarrollo que permite bloquear la cancelación de facturas según la fecha de factura.

## Parámetros de configuración
```
account_invoice_locked_by_date_date_limit
```


Al intentar cancelar una factura o validarla se comprueba su fecha_factura (en el caso de una factura a un cliente) o la fecha_contable (en el caso de una factura de un proveedor) y según lo definido en el parámetro de configuración permitirá o no cancelarla/validarla.
