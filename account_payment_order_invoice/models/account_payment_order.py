# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import decimal

import logging
_logger = logging.getLogger(__name__)

class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'
    
    amount_untaxed_invoice = fields.Float( 
        string='Base imponible factura'
    )
    invoice_id = fields.Many2one(
        comodel_name='account.invoice',     
        string='Factura'
    )                                
   
    @api.multi
    def generated2uploaded(self):
        if self.payment_type=='inbound' and self.amount_untaxed_invoice>0 and self.invoice_id.id==False:
            account_payment_order_invoice_product_id = int(self.env['ir.config_parameter'].sudo().get_param('account_payment_order_invoice_product_id'))
            if account_payment_order_invoice_product_id>0:
                product = self.env['product.product'].browse(account_payment_order_invoice_product_id)         
                account_invoice_vals = {
                    'partner_id': self.company_partner_bank_id.bank_id.partner_id.id,
                    'date': datetime.today(),
                    'date_invoice': datetime.today(),
                    'state': 'draft',
                    'type': 'in_invoice',
                    'comment': ' ',                                         
                }
                account_invoice_obj = self.env['account.invoice'].sudo().create(account_invoice_vals)
                self.invoice_id = account_invoice_obj.id
                
                account_invoice_line_vals = {
                    'invoice_id': self.invoice_id.id,
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 1,
                    'price_unit': self.amount_untaxed_invoice,
                    'account_id': product.property_account_expense_id.id,                    
                }                
                account_invoice_line_obj = self.env['account.invoice.line'].sudo().create(account_invoice_line_vals)
                account_invoice_line_obj._onchange_product_id()
                account_invoice_obj.compute_taxes()        
        #super        
        return super(AccountPaymentOrder, self).generated2uploaded()                                                                                      