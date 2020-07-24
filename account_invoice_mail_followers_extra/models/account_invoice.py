# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        for item in self:   
            account_invoice_mail_followers_extra_ids = self.env['account.invoice.mail.followers.extra'].search(
                [
                    ('partner_id', '=', item.partner_id.id)
                ]
            )
            for account_invoice_mail_followers_extra_id in account_invoice_mail_followers_extra_ids:
                for partner_id_extra in account_invoice_mail_followers_extra_id.partner_ids_extra:
                    mail_followers_ids = self.env['mail.followers'].search(
                        [
                            ('partner_id', '=', self.partner_id.id),
                            ('res_model', '=', 'account.invoice'),
                            ('res_id', '=', self.id)
                        ]
                    )
                    if len(mail_followers_ids) == 0:
                        vals = {
                            'partner_id': partner_id_extra.id,
                            'res_model': 'account.invoice',
                            'res_id': item.id,
                            'subtype_ids': [(4, 1)]
                        }
                        self.env['mail.followers'].sudo().create(vals)
        # return
        return super(AccountInvoice, self).action_invoice_open()