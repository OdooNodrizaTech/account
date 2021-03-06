# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_move_create(self):
        super(AccountInvoice, self).action_move_create()
        for inv in self:
            custom_days_due = inv.generate_custom_days_due()
            if len(custom_days_due) > 0:
                date_due = False
                day_date_due = False
                for line_id in inv.move_id.line_ids:
                    if line_id.debit > 0:
                        date_due = datetime.datetime.strptime(
                            line_id.date_maturity.strftime("%Y-%m-%d"),
                            "%Y-%m-%d"
                        )
                        day_date_due = int(date_due.strftime('%d'))
                        while not (day_date_due in custom_days_due):
                            modified_date = date_due + datetime.timedelta(days=1)
                            line_id.date_maturity = datetime.datetime.strftime(
                                modified_date,
                                "%Y-%m-%d"
                            )
                            date_due = datetime.datetime.strptime(
                                line_id.date_maturity.strftime("%Y-%m-%d"),
                                "%Y-%m-%d"
                            )
                            day_date_due = int(date_due.strftime('%d'))

    @api.model
    def generate_custom_days_due(self):
        custom_days_due = []
        if self.type == "in_invoice":
            if self.partner_id.custom_day_due_1_purchase \
                    or self.partner_id.custom_day_due_2_purchase \
                    or self.partner_id.custom_day_due_3_purchase \
                    or self.partner_id.custom_day_due_4_purchase:
                # custom_day_due_1_purchase
                if self.partner_id.custom_day_due_1_purchase \
                        and self.partner_id.custom_day_due_1_purchase.isnumeric():
                    custom_day_due_1 = int(self.partner_id.custom_day_due_1_purchase)
                    if custom_day_due_1 > 0:
                        custom_days_due.append(custom_day_due_1)
                # custom_day_due_2_purchase
                if self.partner_id.custom_day_due_2_purchase \
                        and self.partner_id.custom_day_due_2_purchase.isnumeric():
                    custom_day_due_2 = int(self.partner_id.custom_day_due_2_purchase)
                    if custom_day_due_2 > 0:
                        custom_days_due.append(custom_day_due_2)
                # custom_day_due_3_purchase
                if self.partner_id.custom_day_due_3_purchase \
                        and self.partner_id.custom_day_due_3_purchase.isnumeric():
                    custom_day_due_3 = int(self.partner_id.custom_day_due_3_purchase)
                    if custom_day_due_3 > 0:
                        custom_days_due.append(custom_day_due_3)
                # custom_day_due_4_purchase
                if self.partner_id.custom_day_due_4_purchase \
                        and self.partner_id.custom_day_due_4_purchase.isnumeric():
                    custom_day_due_4 = int(self.partner_id.custom_day_due_4_purchase)
                    if custom_day_due_4 > 0:
                        custom_days_due.append(custom_day_due_4)
        else:
            if self.partner_id.custom_day_due_1 \
                    or self.partner_id.custom_day_due_2 \
                    or self.partner_id.custom_day_due_3 \
                    or self.partner_id.custom_day_due_4:
                # custom_day_due_1
                if self.partner_id.custom_day_due_1 \
                        and self.partner_id.custom_day_due_1.isnumeric():
                    custom_day_due_1 = int(self.partner_id.custom_day_due_1)
                    if custom_day_due_1 > 0:
                        custom_days_due.append(custom_day_due_1)
                # custom_day_due_2
                if self.partner_id.custom_day_due_2 \
                        and self.partner_id.custom_day_due_2.isnumeric():
                    custom_day_due_2 = int(self.partner_id.custom_day_due_2)
                    if custom_day_due_2 > 0:
                        custom_days_due.append(custom_day_due_2)
                # custom_day_due_3
                if self.partner_id.custom_day_due_3 \
                        and self.partner_id.custom_day_due_3.isnumeric():
                    custom_day_due_3 = int(self.partner_id.custom_day_due_3)
                    if custom_day_due_3 > 0:
                        custom_days_due.append(custom_day_due_3)
                # custom_day_due_4
                if self.partner_id.custom_day_due_4 \
                        and self.partner_id.custom_day_due_4.isnumeric():
                    custom_day_due_4 = int(self.partner_id.custom_day_due_4)
                    if custom_day_due_4 > 0:
                        custom_days_due.append(custom_day_due_4)

        return custom_days_due

    @api.multi
    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        super(AccountInvoice, self)._onchange_payment_term_date_invoice()
        for item in self:
            if item.date_due:
                custom_days_due = item.generate_custom_days_due()
                if len(custom_days_due) > 0:
                    date_due = datetime.datetime.strptime(
                        item.date_due.strftime("%Y-%m-%d"),
                        "%Y-%m-%d"
                    )
                    day_date_due = int(date_due.strftime('%d'))
                    if not (day_date_due in custom_days_due):
                        while not (day_date_due in custom_days_due):
                            date_due = datetime.datetime.strptime(
                                item.date_due.strftime("%Y-%m-%d"),
                                "%Y-%m-%d"
                            )
                            modified_date = date_due + datetime.timedelta(days=1)
                            item.date_due = datetime.datetime.strftime(
                                modified_date,
                                "%Y-%m-%d"
                            )
                            date_due = datetime.datetime.strptime(
                                item.date_due.strftime("%Y-%m-%d"),
                                "%Y-%m-%d"
                            )
                            day_date_due = int(date_due.strftime('%d'))
