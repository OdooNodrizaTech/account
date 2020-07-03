# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):
        self.env.cr.execute("UPDATE account_move SET amount = ROUND(amount::numeric,2) WHERE id IN (SELECT id FROM account_move WHERE amount <> ROUND(amount::NUMERIC,2))")