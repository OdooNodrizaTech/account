# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        allow_confirm = True
        # check
        for obj in self:
            if obj.partner_id.vat == False:
                allow_confirm = False
                raise Warning("Es necesario definir un CIF/NIF para el cliente de la factura")
        # allow_confirm
        if allow_confirm == True:
            return super(AccountInvoice, self).action_invoice_open()