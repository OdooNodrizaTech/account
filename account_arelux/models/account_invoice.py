# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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
        return_object = super(AccountInvoice, self).write(vals)
        #check_message_follower_ids
        self.check_message_follower_ids()
        #return
        return return_object
        
    @api.one
    def check_message_follower_ids(self):
        if self.user_id.id!=False:        
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids!=False:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id==self.user_id.id or user_id.id==1:
                            message_follower_id.sudo().unlink()
            
    @api.one    
    def action_send_account_invoice_create_message_slack(self):
        return True
        
    @api.one    
    def action_send_account_invoice_out_refund_create_message_slack(self):
        return True                                                                                                                                                                