# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'

    account_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Account Invoice Id'
    )
    invoice_date = fields.Date(
        string='Fecha factura'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
    )
    cost = fields.Monetary(
        string='Coste'
    )