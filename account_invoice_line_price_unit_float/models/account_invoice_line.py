# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
import odoo.addons.decimal_precision as dp

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        digits=dp.get_precision('Price Unit')
    )