# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'                     
    
    @api.multi
    def action_invoice_open(self):
        #action
        return_action = super(AccountInvoice, self).action_invoice_open()
        #operations
        for obj in self:
            if obj.amount_total>0:
                if obj.type=='out_invoice':
                    transaction_ids = []
                    for invoice_line_id in obj.invoice_line_ids:
                        sale_order_line_invoice_rel_ids = self.env['sale.order.line'].sudo().search([('invoice_lines', 'in', invoice_line_id.id)])
                        if len(sale_order_line_invoice_rel_ids)>0:
                            for sale_order_line_invoice_rel_id in sale_order_line_invoice_rel_ids:
                                for transaction_id in sale_order_line_invoice_rel_id.order_id.transaction_ids:
                                    if transaction_id.id not in transaction_ids:
                                        transaction_ids.append(int(transaction_id.id))
                    #check
                    if len(transaction_ids)>0:
                        payment_transaction_ids = self.env['payment.transaction'].sudo().search(
                            [
                                ('id', 'in', transaction_ids),
                                ('state', '=', 'done'),
                                ('amount', '>', 0)
                            ]
                        )
                        if len(payment_transaction_ids)>0:
                            account_payment_ids = self.env['account.payment'].sudo().search(
                                [
                                    ('payment_transaction_id', 'in', payment_transaction_ids.ids),
                                    ('state', '!=', 'draft'),
                                ]
                            )
                            if len(account_payment_ids)>0:
                                for account_payment_id in account_payment_ids:
                                    if account_payment_id.payment_type=='inbound':
                                        for move_line_id in account_payment_id.move_line_ids:                        
                                            if move_line_id.credit>0:
                                                obj.assign_outstanding_credit(move_line_id.id)                                    
        #return
        return return_action        