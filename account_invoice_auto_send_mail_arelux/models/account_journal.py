# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    invoice_mail_template_id_arelux = fields.Many2one(
        comodel_name='mail.template',
        domain=[('model_id.model', '=', 'account.invoice'),('ar_qt_activity_type', '=', 'arelux')],
        string='Invoice mail template id Arelux'
    )
    invoice_mail_template_id_todocesped = fields.Many2one(
        comodel_name='mail.template',
        domain=[('model_id.model', '=', 'account.invoice'),('ar_qt_activity_type', '=', 'todocesped')],
        string='Invoice mail template id Todocesped'
    )
    invoice_mail_template_id_evert = fields.Many2one(
        comodel_name='mail.template',
        domain=[('model_id.model', '=', 'account.invoice'),('ar_qt_activity_type', '=', 'evert')],
        string='Invoice mail template id Evert'
    )
    invoice_mail_template_id_both = fields.Many2one(
        comodel_name='mail.template',
        domain=[('model_id.model', '=', 'account.invoice')],
        string='Invoice mail template id Both'
    )