# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import Warning as UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        allow_confirm = True
        # check
        for item in self:
            if itemtype == "in_invoice" and not item.reference:
                allow_confirm = False
                raise UserError(
                    _('It is necessary to define a supplier reference to validate the purchase invoice')
                )
        # allow_confirm
        if allow_confirm:
            return super(AccountInvoice, self).action_invoice_open()
