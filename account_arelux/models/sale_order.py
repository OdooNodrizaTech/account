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
    total_cashondelivery = fields.Float( 
        string='Total contrareembolso'
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
        values = {
            'payment_mode_id': self.partner_id.customer_payment_mode_id and self.partner_id.customer_payment_mode_id.id or False
        }
        self.update(values)
    
        if self.partner_id.id>0:
            res_partner_ids = self.env['res.partner'].search(
                [
                    ('parent_id', '=', self.partner_id.id),
                    ('active', '=', True), 
                    ('type', '=', 'delivery')
                 ]
            )
            if len(res_partner_ids)>1:        
                values = {
                    #'partner_shipping_id': self.partner_id.id,
                    'partner_shipping_id': 0,
                }
                self.update(values)                                
    
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
        if values.get('opportunity_id')==False and values.get('create_uid')!=1:
            raise Warning("Para crear un presupuesto es necesario definir un flujo")
        else:            
            if values.get('claim')==True and values.get('claim_id')==False:
                raise Warning("Es necesario definir una reclamacion")
            else:
                if values.get('claim')==True and values.get('claim_id')!=False:
                    values['name'] = self.env['ir.sequence'].next_by_code('sale.order.claim') or 'New Claim'
                                
                return_val = super(SaleOrder, self).create(values)            
                
                if return_val.user_id.id!=False and return_val.partner_id.user_id.id!=False and self.user_id.id!=return_val.partner_id.user_id.id:
                    return_val.user_id = return_val.partner_id.user_id.id                        
                
                if return_val.user_id.id==6:
                    return_val.user_id = 0
                
                return_val.fix_copy_custom_field_opportunity_id()#Fix copy fields opportunity
                                
                return return_val                                
    
    @api.multi
    def write(self, vals):
        allow_write = True
        #date_order_management
        if vals.get('state')=='sent' and 'date_order_management' not in vals:
            vals['date_order_management'] = fields.datetime.now()                        
        #fix validate template_id
        template_id_check = self.template_id.id
        if 'template_id' in vals:
            template_id_check = vals['template_id']
            
            sale_quote_template_obj = self.env['sale.quote.template'].search([('id', '=', template_id_check)])[0]
            if sale_quote_template_obj.ar_qt_activity_type!=False:
                if sale_quote_template_obj.ar_qt_activity_type!=self.ar_qt_activity_type:
                    allow_write = False
                    raise Warning("La plantilla de presupuesto no corresponde con el tipo de actividad")                    
                
        if allow_write==True:                        
            return_object = super(SaleOrder, self).write(vals)
        
            if self.user_id.id!=False:        
                for message_follower_id in self.message_follower_ids:
                    if message_follower_id.partner_id.user_ids!=False:
                        for user_id in message_follower_id.partner_id.user_ids:
                            if user_id.id!=self.user_id.id:
                                self.env.cr.execute("DELETE FROM  mail_followers WHERE id = "+str(message_follower_id.id))                            
                                                                
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
            if self.partner_invoice_id.vat==False:
                allow_action_confirm = False
                raise Warning("Es necesario definir CIF/NIF para la direccion de facturacion antes de validar el pedido de venta.\n")            
            elif self.carrier_id.id>0 and self.partner_shipping_id.id>0:
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
            if self.need_check_credit_limit==True:
                future_max_credit_limit_allow = self.max_credit_limit_allow - self.amount_total
                if future_max_credit_limit_allow<=0:                   
                    allow_action_confirm = False
                    raise Warning("No se puede confirmar la venta porque no hay credito disponible o el importe total de esta venta es superior al credito disponible ("+str(future_max_credit_limit_allow)+")")
                
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
            account_arelux_payment_mode_id_cashondelivery = int(self.env['ir.config_parameter'].sudo().get_param('account_arelux_payment_mode_id_cashondelivery'))            
            if account_arelux_payment_mode_id_cashondelivery==self.payment_mode_id.id:
                if self.total_cashondelivery<10:
                    allow_action_confirm = False
                    raise Warning("No se puede confirmar la venta de contrareembolso con un total_contrareembolso menor de 10")
                                                                                                                         
        if allow_action_confirm==True:
            return super(SaleOrder, self).action_confirm()            
            
    @api.multi    
    def cron_fix_website_description_sale_quotes(self, cr=None, uid=False, context=None):                
        self.env.cr.execute("UPDATE sale_order_line SET website_description = NULL WHERE id > 0")
        self.env.cr.execute("UPDATE sale_order SET website_description = (SELECT website_description FROM sale_quote_template WHERE id = template_id)")                            
    
    @api.one    
    def action_account_invoice_not_create_partner_without_vat(self):
        return True
    
    @api.one
    def allow_generate_invoice(self):
        #check
        allow_generate_invoice = False
        need_delivery_something = False
        
        if self.invoice_status=='to invoice':
            total_qty_to_invoice = 0
                            
            for order_line in self.order_line:
                if order_line.product_id.invoice_policy=='order':                        
                    total_qty_to_invoice = total_qty_to_invoice + order_line.product_uom_qty
                else:
                    total_qty_to_invoice = total_qty_to_invoice + order_line.qty_delivered
                    need_delivery_something = True                
            
            if total_qty_to_invoice>0:
                current_date = fields.Datetime.from_string(str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
                allow_generate_invoice = False
                
                if need_delivery_something==True:
                    stock_picking_date_done = False
                    all_stock_picking_done = True
                    
                    stock_picking_ids = self.env['stock.picking'].search([('origin', '=', self.name),('state', 'not in', ('draft', 'cancel'))])
                    if stock_picking_ids!=False:                            
                        for stock_picking_id in stock_picking_ids:
                            if stock_picking_id.state=='done':
                                stock_picking_date_done = stock_picking_id.date_done
                            else:
                                all_stock_picking_done = False
                                                    
                    if all_stock_picking_done==True and stock_picking_date_done!=False:
                        allow_generate_invoice = True                                                                                                        
                else:
                    allow_generate_invoice = True
                
                #check nif
                if allow_generate_invoice==True:
                    if self.partner_invoice_id.vat==False:
                        allow_generate_invoice = False
                        self.action_account_invoice_not_create_partner_without_vat()#Fix Slack                        
                        
                        _logger.info('El pedido '+str(self.name)+' no se puede facturar porque el cliente NO tiene CIF')
        #return
        return allow_generate_invoice
          
    @api.multi    
    def cron_operations_sale_order_autogenerate_invoices(self, cr=None, uid=False, context=None):        
        current_date = datetime.today()
        allow_generate_invoices = True
        
        if current_date.day==31 and current_date.month==12:
            allow_generate_invoices = False
            
        if current_date.day==1 and current_date.month==1:
            allow_generate_invoices = False
        
        if allow_generate_invoices==True:
            sale_order_ids = self.env['sale.order'].search(
                [
                    ('state', '=', 'sale'),
                    ('amount_total', '>', 0),
                    ('payment_mode_id', '!=', False), 
                    ('invoice_status', '=', 'to invoice'),
                    ('disable_autogenerate_create_invoice', '=', False)
                 ]
            )
            if sale_order_ids!=False:
                web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                #group_by_partner_id
                sale_order_ids_by_partner_id = {}
                for sale_order_id in sale_order_ids:
                    #check
                    allow_generate_invoice = sale_order_id.allow_generate_invoice()[0]                    
                    #add if need
                    if allow_generate_invoice==True:                    
                        if sale_order_id.partner_invoice_id.id not in sale_order_ids_by_partner_id:
                            sale_order_ids_by_partner_id[sale_order_id.partner_invoice_id.id] = []
                        #add_sale_order_ids
                        sale_order_ids_by_partner_id[sale_order_id.partner_invoice_id.id].append(sale_order_id.id)
                
                if len(sale_order_ids_by_partner_id)>0:                
                    for partner_id in sale_order_ids_by_partner_id:
                        ids = sale_order_ids_by_partner_id[partner_id]                    
                        sale_order_ids_get = self.env['sale.order'].search([('id', 'in', ids)])
                        return_invoice_create = sale_order_ids_get.action_invoice_create()
                        #sale_order_ids
                        for sale_order_id_get in sale_order_ids_get:
                            sale_order_id_get.state = 'done'
                        #invoice_ids
                        invoice_id = return_invoice_create[0]
                        account_invoice_id = self.env['account.invoice'].search([('id', '=', invoice_id)])[0]
                        #save_log
                        automation_log_vals = {                    
                            'model': 'account.invoice',
                            'res_id': account_invoice_id.id,
                            'category': 'account_invoice',
                            'action': 'create',                                                                                                                                                                                           
                        }
                        automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)
                        #operations
                        if account_invoice_id.amount_total>0:
                            account_invoice_id.action_invoice_open()                        
                            account_invoice_id.action_send_account_invoice_create_message_slack()#Fix Slack
                            #save_log
                            automation_log_vals = {                    
                                'model': 'account.invoice',
                                'res_id': account_invoice_id.id,
                                'category': 'account_invoice',
                                'action': 'valid',                                                                                                                                                                                           
                            }
                            automation_log_obj = self.env['automation.log'].sudo().create(automation_log_vals)                                            
                            #send mail
                            account_invoice_id.cron_account_invoice_auto_send_mail_item()