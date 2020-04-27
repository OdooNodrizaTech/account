# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'
    
    invoice_description = fields.Text(
        string='Descripcion en factura'
    )