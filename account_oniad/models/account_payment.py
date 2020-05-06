# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    oniad_product_id = fields.Many2one(
        comodel_name='product.template',         
        string='OniAd Producto'
    )
    oniad_purchase_price = fields.Monetary(         
        string='OniAd Coste'
    )                
                     