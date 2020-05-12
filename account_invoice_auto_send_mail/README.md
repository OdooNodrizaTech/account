El módulo contiene el desarrollo para el envío automático de facturas por email


## Parámetros de configuración
```
account_invoice_auto_send_mail_template_id
account_invoice_auto_send_mail_author_id
account_invoice_auto_send_mail_days
``` 

## Cron:

### Account Invoice Auto Send Mail (3 dias)
Frecuencia: 1 vez al día (laborable)

Descripción: Envía todas las facturas de clientes (NO rectificativas) que estén abiertas o pagadas y que NO tengan fecha_envio_email
