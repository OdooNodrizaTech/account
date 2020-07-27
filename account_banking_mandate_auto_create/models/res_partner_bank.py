# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from datetime import datetime


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.model
    def create(self, values):
        return_create = super(ResPartnerBank, self).create(values)
        return_create.auto_create_banking_mandate_item()        
        return return_create        
        
    @api.one    
    def auto_create_banking_mandate_item(self):
        current_date = datetime.today()
        
        res_partner_banks_ids_get = self.env['res.partner.bank'].search(
            [
                ('partner_id', '=', self.partner_id.id)
            ]
        )
        if res_partner_banks_ids_get:
            for res_partner_banks_id_get in res_partner_banks_ids_get:
                if not res_partner_banks_id_get.partner_id.supplier:
                    account_banking_mandate_ids_get = self.env['account.banking.mandate'].search(
                        [
                            ('state', '!=', 'expired'),
                            ('partner_bank_id', '=', res_partner_banks_id_get.id)
                        ]
                    )
                    if len(account_banking_mandate_ids_get) == 0:
                        vals = {
                            'auto_create': True,
                            'format': 'sepa',
                            'scheme': 'CORE',
                            'type': 'recurrent',
                            'recurrent_sequence_type': 'recurring',
                            'partner_bank_id': self.id,
                            'partner_id': self.partner_id.id,
                            'signature_date': current_date.strftime("%Y-%m-%d"),                                                             
                        }
                        account_banking_mandate_obj = self.env['account.banking.mandate'].sudo().create(vals)
                        account_banking_mandate_obj.validate()
