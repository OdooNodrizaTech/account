# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from datetime import datetime


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'
    
    amount_untaxed_invoice = fields.Float( 
        string='Amount untaxed invoice'
    )
    invoice_id = fields.Many2one(
        comodel_name='account.invoice',     
        string='Invoice'
    )                                
   
    @api.multi
    def generated2uploaded(self):
        if self.payment_type == 'inbound' and self.amount_untaxed_invoice > 0 and not self.invoice_id.id:
            product_id = int(self.env['ir.config_parameter'].sudo().get_param('account_payment_order_invoice_product_id'))
            if product_id > 0:
                product = self.env['product.product'].browse(product_id)
                vals = {
                    'partner_id': self.company_partner_bank_id.bank_id.partner_id.id,
                    'date': datetime.today(),
                    'date_invoice': datetime.today(),
                    'state': 'draft',
                    'type': 'in_invoice',
                    'comment': ' ',                                         
                }
                account_invoice_obj = self.env['account.invoice'].sudo().create(vals)
                self.invoice_id = account_invoice_obj.id
                
                vals = {
                    'invoice_id': self.invoice_id.id,
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 1,
                    'price_unit': self.amount_untaxed_invoice,
                    'account_id': product.property_account_expense_id.id,                    
                }                
                account_invoice_line_obj = self.env['account.invoice.line'].sudo().create(vals)
                account_invoice_line_obj._onchange_product_id()
                account_invoice_obj.compute_taxes()        
        # super
        return super(AccountPaymentOrder, self).generated2uploaded()                                                                                      