El módulo contiene el desarrollo para el envío automático de facturas no pagadas por email


## Parámetros de configuración
```
account_invoice_not_paid_days_check
account_invoice_not_paid_template_id
``` 

## Cron:

### Automation Account Invoice Not Paid
Frecuencia: 1 vez al día (laborable)

Descripción: Envía todas las facturas de clientes (NO rectificativas) que estén abiertas, deban algo, NO sean de sepa y que NO tengan fecha_envio_email_no_pagado
