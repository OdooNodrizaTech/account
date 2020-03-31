# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
from datetime import datetime

class AccountBankingMandate(models.Model):
    _inherit = 'account.banking.mandate'
    
    auto_create = fields.Boolean(
        string="Auto creado"
    )        
    
    @api.multi    
    def cron_fix_auto_create_banking_mandate(self, cr=None, uid=False, context=None):
        current_date = datetime.today()
        
        account_banking_mandate_ids = self.env['account.banking.mandate'].search([('state', '!=', 'cancel')])
        if len(account_banking_mandate_ids)>0:
            partner_bank_ids = account_banking_mandate_ids.mapped('partner_bank_id')
            res_partner_bank_ids = self.env['res.partner.bank'].search([('id', 'in', partner_bank_ids.ids)])
            if len(res_partner_bank_ids)>0:
                partner_ids = res_partner_bank_ids.mapped('partner_id')
                #buscamos cuentas bancarias de los contactos que NO son estos
                res_partner_bank_ids = self.env['res.partner.bank'].search([('partner_id', 'not in', partner_ids.ids)])
                if len(res_partner_bank_ids)>0:
                    for res_partner_bank_id in res_partner_bank_ids:
                        account_banking_mandate_vals = {
                            'auto_create': True,
                            'format': 'sepa',
                            'scheme': 'CORE',
                            'type': 'recurrent',
                            'recurrent_sequence_type': 'recurring',
                            'partner_bank_id': res_partner_bank_id.id,
                            'partner_id': res_partner_bank_id.partner_id.id,
                            'signature_date': current_date.strftime("%Y-%m-%d"),                                                             
                        }
                        account_banking_mandate_obj = self.env['account.banking.mandate'].sudo().create(account_banking_mandate_vals)
                        account_banking_mandate_obj.validate()                                                    