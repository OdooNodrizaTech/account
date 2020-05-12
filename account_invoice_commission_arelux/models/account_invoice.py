# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
        
    @api.one    
    def action_regenerate_commission_percent_lines(self):
        return_action = super(AccountInvoice, self).action_regenerate_commission_percent_lines()
        #override
        for invoice_line_id in self.invoice_line_ids:
            if invoice_line_id.commission_percent>0:
                if self.ar_qt_activity_type=='evert':
                    invoice_line_id.commission_percent = 1
        #return
        return return_action