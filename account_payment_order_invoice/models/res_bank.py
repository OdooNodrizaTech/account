# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner'
    )
