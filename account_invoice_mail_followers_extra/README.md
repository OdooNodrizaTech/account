El módulo contiene el desarrollo para añadir un nuevo modelo account_invoice_mail_followers_extra que está disponible en Odoo desde el apartado Contactos > Configuración > Seguidores extra facturas

El objetivo de este módulo es que para un contacto (contacto A) podamos añadir seguidores adicionales (contacto B, contacto D y contacto E).

Cada vez que se valida una factura se revisa si ese partner_id tiene "Seguidores extra" y en ese caso, los añade como seguidores de factura. 

Este desarrollo se ha realizado con el objetivo de que al enviar por email una factura (por defecto cualquier email se envía a todos los seguidores de la factura -salvo al remitente) llegue a diferentes personas de Contabilidad, etc sin necesidad de añadir a los seguidores manualmente.
