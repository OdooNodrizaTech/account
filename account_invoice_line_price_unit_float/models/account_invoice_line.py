# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
import odoo.addons.decimal_precision as dp

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        digits=dp.get_precision('Price Unit')
    )