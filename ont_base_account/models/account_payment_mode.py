# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'
    _order = 'position'
    
    position = fields.Integer(
        string='Posicion'
    )