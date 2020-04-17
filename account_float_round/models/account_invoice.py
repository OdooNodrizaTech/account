# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):
        self.env.cr.execute("UPDATE account_invoice SET amount_total = ROUND(amount_total::numeric,3)")