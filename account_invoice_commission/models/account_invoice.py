# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
        
    commission = fields.Float( 
        string='Comission'
    )
    commission_date_paid = fields.Date(
        string='Comission date paid',
        readonly=True
    )

    @api.one
    def action_invoice_open(self):
        return_action = super(AccountInvoice, self).action_invoice_open()
        # action_regenerate_commission_percent_lines
        self.action_regenerate_commission_percent_lines()
        # return
        return return_action

    @api.one
    def write(self, vals):
        need_regenerate_commission = False
        # stage date_paid_status
        if vals.get('state') == 'paid':
            need_regenerate_commission = True
        # write
        return_object = super(AccountInvoice, self).write(vals)
        # action_regenerate_commission
        if need_regenerate_commission:
            self.action_regenerate_commission()
        # return
        return return_object        
    
    @api.multi    
    def action_regenerate_commission_multi(self):
        for item in self:
            item.action_regenerate_commission_percent_lines()
            item.action_regenerate_commission()    
    
    @api.one    
    def action_regenerate_commission_percent_lines(self):
        if self.type in ['out_invoice', 'out_refund']:
            if self.state in ['open', 'paid']:
                if self.user_id:
                    for invoice_line_id in self.invoice_line_ids:
                        if invoice_line_id.product_id:
                            if not invoice_line_id.product_id.not_allow_account_invoice_commission:
                                if invoice_line_id.product_id.type != 'service':
                                    invoice_line_id.commission_percent = self.user_id.invoice_commission_percent
    
    @api.one    
    def action_regenerate_commission(self):
        if self.type in ['out_invoice', 'out_refund']:
            if self.state == 'paid':
                if self.invoice_line_ids:
                    # calculate_comission
                    commission = 0
                    # operations
                    for invoice_line_id in self.invoice_line_ids:
                        invoice_line_id.action_calculate_commission()                            
                        # commission
                        commission += invoice_line_id.commission                                                                                               
                    # commission
                    self.commission = "{:.2f}".format(commission)