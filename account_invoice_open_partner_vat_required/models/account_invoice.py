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
            base_partner_12 = self.env.ref('base.res_partner_12')
            _logger.info('base_partner_12.id')
            _logger.info(base_partner_12.id)
            _logger.info('item.partner_id.id')
            _logger.info(item.partner_id.id)
            if item.partner_id.id != base_partner_12.id:
                if not item.partner_id.vat:
                    allow_confirm = False
                    raise UserError(
                        _('It is necessary to define a CIF / NIF '
                          'for the customer of the invoice')
                    )
        # allow_confirm
        if allow_confirm:
            return super(AccountInvoice, self).action_invoice_open()
