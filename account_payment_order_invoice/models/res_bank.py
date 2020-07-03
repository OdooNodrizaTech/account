# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ResBank(models.Model):
    _inherit = 'res.bank'
    
    partner_id = fields.Many2one(
        comodel_name='res.partner',     
        string='Contacto'
    )                                                                                                           