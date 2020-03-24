# -*- coding: utf-8 -*-
from openerp import api, models, fields

import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceMailFollowersExtra(models.Model):
    _name = 'account_invoice_mail_followers_extra'
    
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        domain=[('customer', '=', True)],
        string='Cliente',
    )
    partner_ids_extra = fields.Many2many(
        comodel_name='res.partner', 
        string='Seguidores adicionales facturas'
    )                                                                        