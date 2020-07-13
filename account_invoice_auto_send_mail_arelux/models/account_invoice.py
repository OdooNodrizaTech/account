# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def account_invoice_auto_send_mail_item_real(self, mail_template_id, author_id):
        # change mail_template_id
        if self.ar_qt_activity_type == 'arelux':
            custom_mail_template_id = self.journal_id.invoice_mail_template_id_arelux
        elif self.ar_qt_activity_type == 'todocesped':
            custom_mail_template_id = self.journal_id.invoice_mail_template_id_todocesped
        elif self.ar_qt_activity_type == 'evert':
            custom_mail_template_id = self.journal_id.invoice_mail_template_id_evert
        elif self.ar_qt_activity_type == 'both':
            custom_mail_template_id = self.journal_id.invoice_mail_template_id_both
        else:
            custom_mail_template_id = self.journal_id.invoice_mail_template_id_arelux
        # account_invoice_auto_send_mail_item_real
        return super(AccountInvoice, self).account_invoice_auto_send_mail_item_real(custom_mail_template_id, author_id)