# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def define_account_invoice_line_header_info_commission(self):
        return_info = super(AccountInvoiceLine, self).define_account_invoice_line_header_info_commission()
        return_info['ar_qt_activity_type'] = 'Tipo de actividad'
        return return_info

    @api.one
    def define_account_invoice_line_info_commission(self):
        return_info = super(AccountInvoiceLine, self).define_account_invoice_line_info_commission()
        return_info['ar_qt_activity_type'] = self.invoice_id.ar_qt_activity_type
        return return_info