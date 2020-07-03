# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
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
    weight = fields.Float(
        string='Peso (Kg)'
    )
    number_of_packages = fields.Integer(
        string='Paquetes'
    )