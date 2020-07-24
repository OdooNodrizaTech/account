# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, _
from odoo.exceptions import Warning
from datetime import datetime

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def action_invoice_open(self):
        validate_invoice_ok = True                
                
        date_limit = str(self.env['ir.config_parameter'].sudo().get_param('account_invoice_locked_by_date_date_limit'))
        if date_limit:
            current_date = datetime.today()
            current_date_strftime = current_date.strftime("%Y-%m-%d")
            # to_date
            current_date_format = datetime.strptime(current_date_strftime, "%Y-%m-%d").date()
            date_limit = datetime.strptime(date_limit, "%Y-%m-%d").date()
            # validations
            if current_date_format <= date_limit:# absurd limitation
                _logger.info(_('Absurd limitation, the invoice blocking date is greater than the current date'))
            else:        
                if self.type in ['out_invoice', 'out_refund']:
                    if self.date_invoice:
                        if self.date_invoice <= date_limit:
                            validate_invoice_ok = False        
                            raise Warning(_('The specified invoice date cannot be less than the one used to block invoices %s') % date_limit)
                else:
                    if self.date:
                        if self.date <= date_limit:
                            validate_invoice_ok = False        
                            raise Warning(_('The specified accounting date of the invoice cannot be less than the one used to block invoices %s') % date_limit)
                    else:
                        if self.date_invoice <= date_limit:
                            validate_invoice_ok = False        
                            raise Warning(_('The specified invoice date cannot be less than the one used to block invoices %s') % date_limit)
                
        if validate_invoice_ok:
            return super(AccountInvoice, self).action_invoice_open()

    @api.one
    def action_invoice_cancel(self):
        cancel_invoice_ok = True                
        
        date_limit = str(self.env['ir.config_parameter'].sudo().get_param('account_invoice_locked_by_date_date_limit'))
        if date_limit:
            current_date = datetime.today()
            current_date_strftime = current_date.strftime("%Y-%m-%d")
            # to_date
            current_date_format = datetime.strptime(current_date_strftime, "%Y-%m-%d").date()
            date_limit = datetime.strptime(date_limit, "%Y-%m-%d").date()
            # validations
            if current_date_format <= date_limit:# absurd limitation
                _logger.info(_('Absurd limitation, the invoice blocking date is greater than the current date'))
            else:
                if self.type in ['out_invoice', 'out_refund']:
                    if self.date_invoice <= date_limit:
                        cancel_invoice_ok = False        
                        raise Warning(_('The invoice cannot be canceled as the date of the invoice is lower than the one used to block invoices %s') % date_limit)
                else:
                    if self.date:
                        if self.date <= date_limit:
                            cancel_invoice_ok = False        
                            raise Warning(_('The invoice cannot be canceled as the accounting date of the invoice is lower than the one used to block invoices %s') % date_limit)
    
        if cancel_invoice_ok:
            return super(AccountInvoice, self).action_invoice_cancel()                                                                                                                                                                                            