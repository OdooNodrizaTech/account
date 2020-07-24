# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

                    
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    not_allow_account_invoice_commission = fields.Boolean(
        string='Not commission',
        help='Not allow commission in invoice'
    )            