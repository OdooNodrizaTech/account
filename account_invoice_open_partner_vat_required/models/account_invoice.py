# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, tools, _
from odoo.exceptions import Warning as UserError
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        allow_confirm = True
        # check
        for obj in self:
            test_condition = (tools.config['test_enable'] and
                              not self.env.context.get('test_vat'))

            _logger.info('test_condition')
            _logger.info(test_condition)
            _logger.info('test_enable')
            _logger.info(tools.config['test_enable'])
            _logger.info('self.env.context')
            _logger.info(self.env.context)

            if not test_condition and not obj.partner_id.vat:
                allow_confirm = False
                raise UserError(
                    _('It is necessary to define a CIF / NIF '
                      'for the customer of the invoice')
                )
        # allow_confirm
        if allow_confirm:
            return super(AccountInvoice, self).action_invoice_open()
