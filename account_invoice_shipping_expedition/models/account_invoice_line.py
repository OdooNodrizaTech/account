# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    shipping_expedition_id = fields.Many2one(
        comodel_name='shipping.expedition',
        string='Shipping Expedition Id'
    )

    @api.model
    def create(self, values):
        record = super(AccountInvoiceLine, self).create(values)
        #operations
        if record.shipping_expedition_id.id>0:
            record.shipping_expedition_id.account_invoice_line_id = record.id
            record.shipping_expedition_id.invoice_date = record.invoice_id.date_invoice
            record.shipping_expedition_id.currency_id = record.invoice_id.currency_id.id
            record.shipping_expedition_id.cost = record.price_unit
            #state
            if record.shipping_expedition_id.state!='delivered':
                record.shipping_expedition_id.state = 'delivered'
        #return
        return record