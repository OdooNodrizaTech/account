# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)
                    
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    not_allow_account_invoice_commission = fields.Boolean(
        string='No comisiones',
        help='No permitir comisiones en facturas'
    )            