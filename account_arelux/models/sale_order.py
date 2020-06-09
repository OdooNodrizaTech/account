# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
                        
    show_total = fields.Boolean( 
        string='Mostrar total'
    )
    proforma = fields.Boolean( 
        string='Proforma'
    )        
    date_order_management = fields.Datetime(
        string='Fecha gestion', 
        readonly=True
    )
    date_order_send_mail = fields.Datetime(
        string='Fecha envio email', 
        readonly=True
    )        
    disable_autogenerate_create_invoice = fields.Boolean( 
        string='Desactivar auto facturar'
    )    
    partner_id_email = fields.Char(
        compute='_partner_id_email',
        store=False,
        string='Email'
    )
    partner_id_phone = fields.Char(
        compute='_partner_id_phone',
        store=False,
        string='Telefono'
    )
    partner_id_mobile = fields.Char(
        compute='_partner_id_mobile',
        store=False,
        string='Movil'
    )
    partner_id_state_id = fields.Many2one(
        comodel_name='res.country.state',
        compute='_get_partner_id_state_id',
        store=False,
        string='Provincia'
    )
    
    @api.one        
    def action_update_lines_prices_pricelist(self):
        if self.state in ['draft', 'sent']:
            if self.pricelist_id.id>0 and self.order_line!=False:
                for order_line in self.order_line: 
                    order_line.product_uom_change()
    
    @api.onchange('partner_id')
    def onchange_partner_id_override(self):
        if self.partner_id.id>0:
            self.payment_mode_id = self.partner_id.customer_payment_mode_id.id or False
            #partner_shipping_id
            res_partner_ids = self.env['res.partner'].search(
                [
                    ('parent_id', '=', self.partner_id.id),
                    ('active', '=', True), 
                    ('type', '=', 'delivery')
                 ]
            )
            if len(res_partner_ids)>1:
                self.partner_shipping_id = 0
            elif len(res_partner_ids)==1:
                res_partner_id = res_partner_ids[0]
                self.partner_shipping_id = res_partner_id.id                                
    
    @api.model
    def fix_copy_custom_field_opportunity_id(self):
        if self.id>0:
            if self.opportunity_id.id>0:
                #user_id
                if self.opportunity_id.user_id.id>0 and self.opportunity_id.user_id.id!=self.user_id.id:
                    self.user_id = self.opportunity_id.user_id.id
                #team_id                    
                if self.opportunity_id.team_id.id>0 and self.opportunity_id.team_id.id!=self.team_id.id:
                    self.team_id = self.opportunity_id.team_id.id                                                              
    
    @api.model
    def create(self, values):            
        return_val = super(SaleOrder, self).create(values)            
        
        if return_val.user_id.id!=False and return_val.partner_id.user_id.id!=False and self.user_id.id!=return_val.partner_id.user_id.id:
            return_val.user_id = return_val.partner_id.user_id.id                        
        
        if return_val.user_id.id==6:
            return_val.user_id = 0
        
        return_val.fix_copy_custom_field_opportunity_id()#Fix copy fields opportunity
                        
        return return_val                                
    
    @api.multi
    def write(self, vals):
        #date_order_management
        if vals.get('state')=='sent' and 'date_order_management' not in vals:
            vals['date_order_management'] = fields.datetime.now()                            
                                        
        return_object = super(SaleOrder, self).write(vals)
    
        if self.user_id.id!=False:        
            for message_follower_id in self.message_follower_ids:
                if message_follower_id.partner_id.user_ids!=False:
                    for user_id in message_follower_id.partner_id.user_ids:
                        if user_id.id!=self.user_id.id:
                            message_follower_id.sudo().unlink()
                                                            
        return return_object                    
    
    @api.one        
    def _get_partner_id_state_id(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_state_id = sale_order_obj.partner_id.state_id.id
    
    @api.one        
    def _partner_id_email(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_email = sale_order_obj.partner_id.email
            
    @api.one        
    def _partner_id_phone(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_phone = sale_order_obj.partner_id.phone
            
    @api.one        
    def _partner_id_mobile(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_mobile = sale_order_obj.partner_id.mobile                                                  
    
    @api.onchange('user_id')
    def change_user_id(self):                    
        if self.user_id.id>0:
            if self.user_id.sale_team_id.id>0:
                self.team_id = self.user_id.sale_team_id.id
                                                        
    @api.onchange('template_id')
    def change_template_id(self):
        if self.template_id.id>0:
            if self.template_id.delivery_carrier_id.id>0:
                self.carrier_id = self.template_id.delivery_carrier_id
            else:
                self.carrier_id = False                    
    
    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        
        if self.amount_total>0:    
            if self.carrier_id.id>0 and self.partner_shipping_id.id>0:
                if self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.street==False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una direccion para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.city==False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una ciudad/poblacion para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.zip==False:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una codigo postal para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.country_id==0:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una pais para realizar el envio.\n")                
                elif self.carrier_id.id>0 and self.partner_shipping_id.id>0 and self.partner_shipping_id.state_id==0:
                    allow_action_confirm = False
                    raise Warning("Es necesario definir una provincia para realizar el envio.\n")
                    
            if allow_action_confirm==True and self.amount_total>0 and self.claim==False and self.payment_mode_id.id==0:
                allow_action_confirm = False
                raise Warning("Es necesario definir un modo de pago.\n")
            
            if allow_action_confirm==True and self.amount_total>0 and self.claim==False and self.payment_term_id.id==0:
                allow_action_confirm = False
                raise Warning("Es necesario definir un plazo de pago.\n")
                
        if allow_action_confirm==True and self.amount_total>0 and self.claim==False:
            payment_mode_ids_allow = []
            for payment_mode_id in self.payment_term_id.payment_mode_id:
                payment_mode_ids_allow.append(payment_mode_id.id)
                
            if not self.payment_mode_id.id in payment_mode_ids_allow:
                allow_action_confirm = False
                raise Warning("El modo de pago es incompatible con el plazo de pago.\n")                                                                   
        
        if allow_action_confirm==True:
            if allow_action_confirm==True:
                account_payment_mode_sepa_credit = int(self.env['ir.config_parameter'].sudo().get_param('account_payment_mode_sepa_credit'))
                if self.payment_mode_id.id==account_payment_mode_sepa_credit:            
                    partner_id_check = self.partner_invoice_id.id
                    if self.partner_invoice_id.parent_id.id>0:
                        partner_id_check = self.partner_invoice_id.parent_id.id    
                                 
                    res_partner_bank_ids = self.env['res.partner.bank'].search([('partner_id', '=', partner_id_check)])
                    if len(res_partner_bank_ids)==0:
                        allow_action_confirm = False
                        raise Warning("No se puede confirmar la venta porque no hay una cuenta creada para la direccion de facturacion seleccionada")
                    else:
                        res_partner_banks_ids_need_check = []
                        for res_partner_bank_id in res_partner_bank_ids:
                            if res_partner_bank_id.partner_id.supplier==False:
                                res_partner_banks_ids_need_check.append(res_partner_bank_id.id)
                                                    
                        account_banking_mandate_ids = self.env['account.banking.mandate'].search([('partner_bank_id', '=', res_partner_banks_ids_need_check)])
                        if len(account_banking_mandate_ids)==0:
                            allow_action_confirm = False
                            raise Warning("No se puede confirmar la venta porque no hay un mandato bancario creado para la direccion de facturacion seleccionada")
                                                                                                                         
        if allow_action_confirm==True:
            return super(SaleOrder, self).action_confirm()        