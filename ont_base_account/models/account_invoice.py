# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    inv_vat = fields.Char(
        string='VAT',
        related='partner_id.vat'
    )
    partner_bank_name = fields.Char(
        compute='_partner_bank_name',
        string='Banco'
    )
    
    @api.multi
    def action_invoice_open(self):
        allow_confirm = True
        #check
        for obj in self:
            if obj.partner_id.vat==False:
                allow_confirm = False
                raise Warning("Es necesario definir un CIF/NIF para el cliente de la factura.\n")
            elif obj.type=="in_invoice" and obj.reference==False:
                allow_confirm = False
                raise Warning("Es necesario definir una referencia de proveedor para validar la factura de compra.\n")
        #allow_confirm
        if allow_confirm==True:
            return super(AccountInvoice, self).action_invoice_open()        
    
    @api.multi        
    def _partner_bank_name(self):
        for obj in self:
            obj.partner_bank_name = ''
            if obj.partner_bank_id.id>0:
                if obj.partner_bank_id.bank_id.id>0:
                    obj.partner_bank_name = obj.partner_bank_id.bank_id.name + ' ' + obj.partner_bank_id.acc_number[-4:]
                else:
                    obj.partner_bank_name = obj.partner_bank_id.acc_number                                                                                                                                                                                                          