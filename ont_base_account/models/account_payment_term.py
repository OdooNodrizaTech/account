# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'
    _order = 'position'
    
    position = fields.Integer(
        string='Posicion'
    )
    payment_order_ok = fields.Boolean(
        string='Seleccionable en las ordenes'
    )
    payment_mode_id = fields.Many2many(
        comodel_name='account.payment.mode', 
        string='Modos de pago',
    )    