# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.one
    def action_invoice_open(self):
        validate_invoice_ok = True                
                
        date_limit = str(self.env['ir.config_parameter'].sudo().get_param('account_invoice_locked_by_date_date_limit'))
        if date_limit!=False:
            current_date = datetime.today()
            current_date_strftime = current_date.strftime("%Y-%m-%d")
            #to_date
            current_date_format = datetime.strptime(current_date_strftime, "%Y-%m-%d").date()
            date_limit = datetime.strptime(date_limit, "%Y-%m-%d").date()
            #validations
            if current_date_format<=date_limit:#absurd limitation
                _logger.info('Limitacion absurda, la fecha de bloqueo de las facturas es mayor que la fecha actual')
            else:        
                if self.type=='out_invoice' or self.type=='out_refund':
                    if self.date_invoice!=False:
                        if self.date_invoice<=date_limit:
                            validate_invoice_ok = False        
                            raise Warning("La fecha de factura especificada no puede ser inferior a la que se usa para bloquear facturas "+str(date_limit)+".\n")
                else:
                    if self.date!=False:                        
                        if self.date<=date_limit:
                            validate_invoice_ok = False        
                            raise Warning("La fecha contable especificada de la factura no puede ser inferior a la que se usa para bloquear facturas "+str(date_limit)+".\n")                
                    else:
                        if self.date_invoice<=date_limit:
                            validate_invoice_ok = False        
                            raise Warning("La fecha de factura especificada no puede ser inferior a la que se usa para bloquear facturas "+str(date_limit)+".\n")                                                                              
                
        if validate_invoice_ok==True:
            return super(AccountInvoice, self).action_invoice_open()
            
    @api.one
    def action_invoice_cancel(self):
        cancel_invoice_ok = True                
        
        date_limit = str(self.env['ir.config_parameter'].sudo().get_param('account_invoice_locked_by_date_date_limit'))
        if date_limit!=False:
            current_date = datetime.today()
            current_date_strftime = current_date.strftime("%Y-%m-%d")
            #to_date
            current_date_format = datetime.strptime(current_date_strftime, "%Y-%m-%d").date()
            date_limit = datetime.strptime(date_limit, "%Y-%m-%d").date()
            #validations
            if current_date_format<=date_limit:#absurd limitation
                _logger.info('Limitacion absurda, la fecha de bloqueo de las facturas es mayor que la fecha actual')
            else:
                if self.type=='out_invoice' or self.type=='out_refund':
                    if self.date_invoice<=date_limit:
                        cancel_invoice_ok = False        
                        raise Warning("No se puede cancelar la facturada al ser la fecha de la misma inferior a la que se usa para bloquear facturas "+str(date_limit)+".\n")
                else:
                    if self.date!=False:
                        if self.date<=date_limit:
                            cancel_invoice_ok = False        
                            raise Warning("No se puede cancelar la facturada al ser la fecha contable de la misma inferior a la que se usa para bloquear facturas "+str(date_limit)+".\n")
    
        if cancel_invoice_ok==True:
            return super(AccountInvoice, self).action_invoice_cancel()                                                                                                                                                                                            