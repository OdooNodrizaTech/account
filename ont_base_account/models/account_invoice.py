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
        if self.partner_id.vat==False:
            raise Warning("Es necesario definir un CIF/NIF para el cliente de la factura.\n")
        elif self.type=="in_invoice" and self.reference==False:
            raise Warning("Es necesario definir una referencia de proveedor para validar la factura de compra.\n")            
        else:
            return super(AccountInvoice, self).action_invoice_open()
    
    @api.multi        
    def _partner_bank_name(self):
        for account_invoice in self:
            account_invoice.partner_bank_name = ''
            if account_invoice.partner_bank_id.id>0:
                if account_invoice.partner_bank_id.bank_id.id>0:
                    account_invoice.partner_bank_name = account_invoice.partner_bank_id.bank_id.name + ' ' + account_invoice.partner_bank_id.acc_number[-4:]
                else:
                    account_invoice.partner_bank_name = account_invoice.partner_bank_id.acc_number                                                                                                                                                                                                          