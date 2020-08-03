# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, tools


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'                     

    @api.multi
    def action_invoice_open(self):
        # action
        return_action = super(AccountInvoice, self).action_invoice_open()
        # operations
        for obj in self:
            if obj.amount_total > 0:
                if obj.type == 'out_invoice':
                    transaction_ids = []
                    for line_id in obj.invoice_line_ids:
                        order_line_ids = self.env['sale.order.line'].sudo().search(
                            [
                                ('invoice_lines', 'in', invoice_line_id.id)
                            ]
                        )
                        if order_line_ids:
                            for order_line_id in order_line_ids:
                                for transaction_id in order_line_id.order_id.transaction_ids:
                                    if transaction_id.id not in transaction_ids:
                                        transaction_ids.append(int(transaction_id.id))
                    # check
                    if len(transaction_ids) > 0:
                        transaction_ids = self.env['payment.transaction'].sudo().search(
                            [
                                ('id', 'in', transaction_ids),
                                ('state', '=', 'done'),
                                ('amount', '>', 0)
                            ]
                        )
                        if transaction_ids:
                            payment_ids = self.env['account.payment'].sudo().search(
                                [
                                    ('payment_transaction_id', 'in', transaction_ids.ids),
                                    ('state', '!=', 'draft'),
                                ]
                            )
                            if payment_ids:
                                for payment_id in payment_ids:
                                    if payment_id.payment_type == 'inbound':
                                        for move_line_id in payment_id.move_line_ids:
                                            if move_line_id.credit > 0:
                                                obj.assign_outstanding_credit(move_line_id.id)                                    
        # return
        return return_action
