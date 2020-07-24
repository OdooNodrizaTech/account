# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ShippingExpedition(models.Model):
    _inherit = 'shipping.expedition'

    account_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Account Invoice Id'
    )
    invoice_date = fields.Date(
        string='Invoice date'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
    )
    cost = fields.Monetary(
        string='Cost'
    )
    weight = fields.Float(
        string='Weight'
    )
    number_of_packages = fields.Integer(
        string='Number of packages'
    )