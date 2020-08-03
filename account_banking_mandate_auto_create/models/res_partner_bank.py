# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from datetime import datetime


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.model
    def create(self, values):
        res = super(ResPartnerBank, self).create(values)
        res.auto_create_banking_mandate_item()
        return res
        
    @api.one    
    def auto_create_banking_mandate_item(self):
        current_date = datetime.today()
        partner_banks_ids = self.env['res.partner.bank'].search(
            [
                ('partner_id', '=', self.partner_id.id)
            ]
        )
        if partner_banks_ids:
            for partner_bank_id in partner_banks_ids:
                if not partner_bank_id.partner_id.supplier:
                    mandate_ids = self.env['account.banking.mandate'].search(
                        [
                            ('state', '!=', 'expired'),
                            ('partner_bank_id', '=', partner_bank_id.id)
                        ]
                    )
                    if len(mandate_ids) == 0:
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
                        mandate_obj = self.env['account.banking.mandate'].sudo().create(vals)
                        mandate_obj.validate()
