# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
        
    commission = fields.Float( 
        string='Comision'
    )
    commission_percent = fields.Float( 
        string='Comision %'
    )
    
    @api.one
    def action_calculate_commission(self):
        self.commission = 0        
        if self.commission_percent != 0 and self.price_subtotal > 0 and self.product_id:
            commission_line_item = (self.price_subtotal/100)*self.commission_percent
            self.commission = "{:.2f}".format(commission_line_item)

    @api.model
    def define_account_invoice_line_header_info_commission(self):
        return {
            'number': _('Invoice'),
            'name': _('Line description'),
            'origin': _('Origin'),
            'date_invoice': _('Date invoice'),
            'date_paid_status': _('Date paid status'),
            'partner_name': _('Customer'),
            'price_subtotal': _('Price subtotal'),
            'commission_percent': _('Comission %'),
            'commission': _('Comisison')
        }

    @api.one
    def define_account_invoice_line_info_commission(self):
        return_info = {
            'number': self.invoice_id.number,
            'name': self.name,
            'origin': self.invoice_id.origin or '',
            'date_invoice': self.invoice_id.date_invoice.strftime("%Y-%m-%d"),
            'date_paid_status': self.invoice_id.date_paid_status.strftime("%Y-%m-%d"),
            'partner_name': self.invoice_id.partner_id.name,
            'price_subtotal': self.price_subtotal,
            'commission_percent': self.commission_percent,
            'commission': self.commission,
        }
        # out_refund
        if self.invoice_id.type == 'out_refund':
            return_info['price_subtotal'] = return_info['price_subtotal']*-1
            return_info['commission'] = return_info['commission'] * -1
        # return
        return return_info