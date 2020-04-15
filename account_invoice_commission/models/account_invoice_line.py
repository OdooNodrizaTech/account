# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
        
    commission = fields.Float( 
        string='Commission'
    )
    commission_percent = fields.Float( 
        string='Commission %'
    )
    
    @api.one
    def action_calculate_commission(self):
        self.commission = 0        
        if self.commission_percent!=0 and self.price_subtotal>0 and self.product_id.id>0:
            commission_line_item = (self.price_subtotal/100)*self.commission_percent
            self.commission = "{:.2f}".format(commission_line_item)            