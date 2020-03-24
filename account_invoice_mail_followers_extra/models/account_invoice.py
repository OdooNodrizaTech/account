# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):    
        account_invoice_mail_followers_extra_ids = self.env['account_invoice_mail_followers_extra'].search([('partner_id', '=', int(self.partner_id.id))])    
        for account_invoice_mail_followers_extra_id in account_invoice_mail_followers_extra_ids:
            for partner_id_extra in account_invoice_mail_followers_extra_id.partner_ids_extra:   
                mail_followers_vals = {
                    'partner_id': int(partner_id_extra.id),
                    'res_model': 'account.invoice',
                    'res_id': self.id,                                        
                }
                mail_followers_obj = self.env['mail.followers'].sudo().create(mail_followers_vals)                                            
                        
        return super(AccountInvoice, self).action_invoice_open()                                                                                                                                         