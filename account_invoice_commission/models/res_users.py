# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)
                    
class ResUsers(models.Model):
    _inherit = 'res.users'

    invoice_commission_percent = fields.Float(
        string='% Comision facturas'
    )            