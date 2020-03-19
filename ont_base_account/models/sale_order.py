# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    payment_mode_id = fields.Many2one(
        comodel_name='account.payment.mode', 
        string='Modo de pago',
    )
    
    @api.multi
    def action_confirm(self):    
        if self.partner_id.vat==False:
            raise Warning("Es necesario definir VAT para el cliente antes de validar el pedido de venta.\n")            
        elif self.carrier_id>0 and self.partner_shipping_id>0:
            if self.carrier_id>0 and self.partner_shipping_id>0 and self.partner_shipping_id.street==False:
                raise Warning("Es necesario definir una direccion para realizar el envio.\n")                
            elif self.carrier_id>0 and self.partner_shipping_id>0 and self.partner_shipping_id.city==False:
                raise Warning("Es necesario definir una ciudad/poblacion para realizar el envio.\n")                
            elif self.carrier_id>0 and self.partner_shipping_id>0 and self.partner_shipping_id.zip==False:
                raise Warning("Es necesario definir una codigo postal para realizar el envio.\n")                
            elif self.carrier_id>0 and self.partner_shipping_id>0 and self.partner_shipping_id.country_id==0:
                raise Warning("Es necesario definir una pais para realizar el envio.\n")                
            elif self.carrier_id>0 and self.partner_shipping_id>0 and self.partner_shipping_id.state_id==0:
                raise Warning("Es necesario definir una provincia para realizar el envio.\n")                
            else:
                return super(SaleOrder, self).action_confirm()                                                                                 
        else:
            return super(SaleOrder, self).action_confirm()                                                                                        