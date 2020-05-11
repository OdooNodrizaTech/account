# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'                    
    
    @api.multi
    def action_confirm(self):
        allow_action_confirm = True
        
        if self.amount_total>0:        
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