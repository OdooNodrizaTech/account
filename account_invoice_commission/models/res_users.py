# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

                    
class ResUsers(models.Model):
    _inherit = 'res.users'

    invoice_commission_percent = fields.Float(
        string='% Invoice commision'
    )            