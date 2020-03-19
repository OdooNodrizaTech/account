# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):     
        #account_move
        self.env.cr.execute("UPDATE account_move SET amount = ROUND(amount::numeric,3)")
        #account_move_line
        self.env.cr.execute("UPDATE account_move_line SET debit = ROUND(debit::numeric,3)")
        self.env.cr.execute("UPDATE account_move_line SET credit = ROUND(credit::numeric,3)")
        self.env.cr.execute("UPDATE account_move_line SET balance = ROUND(balance::numeric,3)")                                                                                   