# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):     
        self.env.cr.execute("UPDATE account_move_line SET debit = ROUND(debit::numeric,3)")
        self.env.cr.execute("UPDATE account_move_line SET credit = ROUND(credit::numeric,3)")
        self.env.cr.execute("UPDATE account_move_line SET balance = ROUND(balance::numeric,3)")