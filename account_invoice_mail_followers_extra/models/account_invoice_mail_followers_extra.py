# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoiceMailFollowersExtra(models.Model):
    _name = 'account.invoice.mail.followers.extra'
    _description = 'Account Invoice Mail Followers Extra'
    
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        domain=[('customer', '=', True)],
        string='Contact',
    )
    partner_ids_extra = fields.Many2many(
        comodel_name='res.partner', 
        string='Followers extra bills'
    )
