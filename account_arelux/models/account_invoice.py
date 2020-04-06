# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
            
    total_cashondelivery = fields.Float(
        compute='_total_cashondelivery',
        store=False, 
        string='Total contrareembolso pedido'
    )
    date_paid_status = fields.Datetime(
        string='Fecha fin pago', 
        readonly=True
    )
    hide_fiscal_position_description = fields.Boolean(
        string='Ocultar mensaje pos fiscal',
        default=False 
    )
    #override date
    date = fields.Date(
        string='Fecha contable',
        copy=False,
        help="Dejar vacio para usar la fecha de factura",
        track_visibility='always',
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )    
    
    @api.model
    def create(self, values):                    
        # Override the original create function for the res.partner model
        if 'origin' in values and values['origin']!=False:
            sale_order_ids = self.env['sale.order'].search([('name', '=', values['origin'])])            
            if sale_order_ids!=False:
                for sale_order_id in sale_order_ids:
                    if sale_order_id.payment_mode_id.id>0:
                        values['payment_mode_id'] = sale_order_id.payment_mode_id.id
                        
                        if sale_order_id.payment_mode_id.payment_method_id.mandate_required==True:
                            if sale_order_id.partner_id.bank_ids!=False:                            
                                for bank_id in sale_order_id.partner_id.bank_ids:
                                    if bank_id.mandate_ids!=False:                                        
                                        for mandate_id in bank_id.mandate_ids:                                            
                                            if mandate_id.state=='valid':
                                                values['mandate_id'] = mandate_id.id                            
        #create            
        return_object = super(AccountInvoice, self).create(values)            
        self.check_message_follower_ids()                
                            
        return return_object                                    
    
    @api.one
    def write(self, vals):
        # stage date_paid_status
        if vals.get('state')=='paid' and self.date_paid_status==False:
            vals['date_paid_status'] = fields.datetime.now()
        #write                                                                
        return_object = super(AccountInvoice, self).write(vals)
        
        self.check_message_follower_ids()
        
        return return_object
        
    @api.one
    def check_message_follower_ids(self):
        if self.user_id.id!=False:        
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids!=False:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id==self.user_id.id or user_id.id==1:
                            self.env.cr.execute("DELETE FROM  mail_followers WHERE id = "+str(message_follower_id.id))        
                    
    @api.one        
    def _financed_bbva(self):          
        if self.id!=False and self.origin!='':
            sale_order_obj = self.env['sale.order'].search([('name', '=', self.origin)])
            self.financed_bbva = sale_order_obj.financed_bbva                                                                                                                                                                                                                                          
    
    @api.one        
    def _total_cashondelivery(self):                      
        if self.id!=False and self.origin!='':
            sale_order_obj = self.env['sale.order'].search([('name', '=', self.origin)])            
            self.total_cashondelivery = sale_order_obj.total_cashondelivery
            
    @api.one    
    def action_send_account_invoice_create_message_slack(self):
        return True
        
    @api.one    
    def action_send_account_invoice_out_refund_create_message_slack(self):
        return True                                                                                                                                                                