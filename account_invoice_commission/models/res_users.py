# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)
                    
class ResUsers(models.Model):
    _inherit = 'res.users'

    invoice_commission_percent = fields.Float(
        string='% Comision facturas'
    )            