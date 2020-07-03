# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):     
        self.env.cr.execute("UPDATE account_move_line SET debit = ROUND(debit::numeric,2) WHERE id IN (SELECT id FROM account_move_line WHERE debit <> ROUND(debit::NUMERIC,2))")
        self.env.cr.execute("UPDATE account_move_line SET credit = ROUND(credit::numeric,2) WHERE id IN (SELECT id FROM account_move_line WHERE credit <> ROUND(credit::NUMERIC,2))")
        self.env.cr.execute("UPDATE account_move_line SET balance = ROUND(balance::numeric,2) WHERE id IN (SELECT id FROM account_move_line WHERE balance <> ROUND(balance::NUMERIC,2))")