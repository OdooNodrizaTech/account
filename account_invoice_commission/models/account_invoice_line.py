# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

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
        if self.commission_percent!=0 and self.price_subtotal>0 and self.product_id.id>0:
            commission_line_item = (self.price_subtotal/100)*self.commission_percent
            self.commission = "{:.2f}".format(commission_line_item)

    @api.model
    def define_account_invoice_line_header_info_commission(self):
        return {
            'number': 'Factura',
            'name': 'Descripcion linea',
            'origin': 'Origen',
            'date_invoice': 'Fecha factura',
            'date_paid_status': 'Fecha pagado',
            'partner_name': 'Cliente',
            'price_subtotal': 'Subtotal linea',
            'commission_percent': 'Comision %',
            'commission': 'Comision'
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
        #out_refund
        if self.invoice_id.type=='out_refund':
            return_info['price_subtotal'] = return_info['price_subtotal']*-1
            return_info['commission'] = return_info['commission'] * -1
        #return
        return return_info