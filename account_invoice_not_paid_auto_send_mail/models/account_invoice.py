# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    date_invoice_not_paid_send_mail = fields.Datetime(
        string='Fecha no pagado envio email' 
    )
    
    @api.one 
    def account_invoice_not_paid_auto_send_mail_item_real(self, mail_template_id, author_id):
        mail_template_id = self.env['mail.template'].browse(mail_template_id)                
                    
        mail_compose_message_vals = {                    
            'author_id': author_id,
            'record_name': self.number,                                                                                                                                                                                           
        }
        mail_compose_message_obj = self.env['mail.compose.message'].with_context().sudo().create(mail_compose_message_vals)
        return_onchange_template_id = mail_compose_message_obj.onchange_template_id(mail_template_id.id, 'comment', 'account.invoice', self.id)
                        
        mail_compose_message_obj.update({
            'author_id': author_id,
            'template_id': mail_template_id.id,                    
            'composition_mode': 'comment',                    
            'model': 'account.invoice',
            'res_id': self.id,
            'body': return_onchange_template_id['value']['body'],
            'subject': return_onchange_template_id['value']['subject'],
            'email_from': return_onchange_template_id['value']['email_from'],
            'attachment_ids': return_onchange_template_id['value']['attachment_ids'],                    
            'record_name': self.number,
            'no_auto_thread': False,                     
        })                                                   
        mail_compose_message_obj.send_mail_action()        
        #other                                                
        self.date_invoice_not_paid_send_mail = datetime.today()
    
    @api.one 
    def cron_account_invoice_not_paid_auto_send_mail_item(self):
        if self.date_invoice_not_paid_send_mail==False:
            if self.state=='open' and self.type=='out_invoice':
                if self.amount_total>0 and self.residual>0:
                    if self.payment_mode_id.payment_method_id.code!='sepa_direct_debit':
                        account_invoice_not_paid_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_not_paid_template_id'))
                        self.account_invoice_not_paid_auto_send_mail_item_real(account_invoice_not_paid_template_id)
    
    @api.multi    
    def cron_account_invoice_not_paid_auto_send_mail(self, cr=None, uid=False, context=None):
        account_invoice_not_paid_days_check = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_not_paid_days_check'))
        if account_invoice_not_paid_days_check>0:                
            current_date = datetime.now(pytz.timezone('Europe/Madrid'))
            date_due_filter = current_date + relativedelta(days=-account_invoice_not_paid_days_check) 
            
            account_invoice_ids = self.env['account.invoice'].search(
                [
                    ('state', '=', 'open'),
                    ('type', '=', 'out_invoice'),
                    ('payment_mode_id.payment_method_id.code', '!=', 'sepa_direct_debit'),
                    ('amount_total', '>', 0),
                    ('residual', '>', 0),
                    ('date_due', '<', date_due_filter.strftime("%Y-%m-%d")),
                    ('date_invoice_not_paid_send_mail', '=', False)                
                 ]
            )
            if len(account_invoice_ids)>0:
                for account_invoice_id in account_invoice_ids:
                    account_invoice_id.cron_account_invoice_not_paid_auto_send_mail_item()