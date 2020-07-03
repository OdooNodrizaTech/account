# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    date_paid_status = fields.Datetime(
        string='Fecha fin pago',
        readonly=True
    )

    @api.one
    def write(self, vals):
        # stage date_paid_status
        if vals.get('state') == 'paid' and self.date_paid_status == False:
            vals['date_paid_status'] = fields.datetime.now()
        # write
        return super(AccountInvoice, self).write(vals)