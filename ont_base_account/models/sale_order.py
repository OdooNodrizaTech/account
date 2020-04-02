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