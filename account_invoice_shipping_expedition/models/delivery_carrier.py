# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    supplier_partner_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('supplier', '=', True)],
        string='Supplier Partner Id'
    )
