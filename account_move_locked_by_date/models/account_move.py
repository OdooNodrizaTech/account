# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, _
from datetime import datetime
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def _check_lock_date(self):
        res = super()._check_lock_date()
        lock_to_date = str(self.env['ir.config_parameter'].sudo().get_param(
            'account_locked_by_date_limit')
        )
        for move in self:
            if move.date <= lock_to_date:
                message = _("No puedes crear/Modificar asientos con "
                            "fecha anterior a %s (Fecha asiento: %s)") % (
                    lock_to_date, move.date
                )
                raise UserError(message)
        return res
