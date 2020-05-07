# -*- coding: utf-8 -*-
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceMailFollowersExtra(models.Model):
    _name = 'account.invoice.mail.followers.extra'
    _description = 'Account Invoice Mail Followers Extra'
    
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        domain=[('customer', '=', True)],
        string='Cliente',
    )
    partner_ids_extra = fields.Many2many(
        comodel_name='res.partner', 
        string='Seguidores adicionales facturas'
    )                                                                        