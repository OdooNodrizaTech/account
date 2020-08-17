# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, _
from odoo.exceptions import Warning as UserError
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        allow_confirm = True
        # check
        for item in self:
            _logger.info('self.env.ref')
            _logger.info(item.env.ref)
            if item.env.ref not in 'demo_invoice_':
                if not item.partner_id.vat:
                    allow_confirm = False
                    raise UserError(
                        _('It is necessary to define a CIF / NIF '
                          'for the customer of the invoice')
                    )
        # allow_confirm
        if allow_confirm:
            return super(AccountInvoice, self).action_invoice_open()
