# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'                                
   
    @api.multi    
    def cron_odoo_float_round(self, cr=None, uid=False, context=None):
        self.env.cr.execute("UPDATE account_invoice SET amount_total = ROUND(amount_total::numeric,2) WHERE id IN (SELECT id FROM account_invoice WHERE amount_total <> ROUND(amount_total::NUMERIC,2))")