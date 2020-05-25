# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime
import decimal

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one 
    def cron_account_invoice_auto_send_mail_item(self):
        _logger.info('Operaciones cron_account_invoice_auto_send_mail_item factura ' + str(self.id))
        if self.type == 'out_invoice' and self.date_invoice_send_mail == False and self.state in ['open', 'paid']:
            current_date = fields.Datetime.from_string(str(datetime.today().strftime("%Y-%m-%d")))
            days_difference = (current_date - fields.Datetime.from_string(self.date_invoice)).days            
            account_invoice_auto_send_mail_days = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_days'))
            #send_invoice
            send_invoice = False
            if self.state=='paid':
                 send_invoice = True
            else:
                if days_difference>=account_invoice_auto_send_mail_days:
                    send_invoice = True
            #override
            if send_invoice==False:                
                for invoice_line_id in self.invoice_line_ids:
                    for sale_line_id in invoice_line_id.sale_line_ids:
                        if sale_line_id.order_id.external_sale_order_id.id>0:
                            if sale_line_id.order_id.external_sale_order_id.external_source_id.id>0:
                                if sale_line_id.order_id.external_sale_order_id.external_source_id.type=='shopify':
                                    if days_difference >= 0:
                                        send_invoice = True
            #send_invoice
            _logger.info(send_invoice)
            if send_invoice==True:                        
                account_invoice_auto_send_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_template_id'))
                account_invoice_auto_send_mail_author_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_author_id'))
                #account_invoice_auto_send_mail_item_real
                self.account_invoice_auto_send_mail_item_real(account_invoice_auto_send_mail_template_id, account_invoice_auto_send_mail_author_id)
    
    @api.one 
    def account_invoice_auto_send_mail_item_real(self, mail_template_id, author_id):
        #change mail_template_id
        if self.ar_qt_activity_type=='arelux':
            custom_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_arelux_template_id'))
        elif self.ar_qt_activity_type=='todocesped':
            custom_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_todocesped_template_id'))
        elif self.ar_qt_activity_type=='evert':
            custom_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_evert_template_id'))
        elif self.ar_qt_activity_type=='both':
            custom_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_both_template_id'))
        else:
            custom_mail_template_id = int(self.env['ir.config_parameter'].sudo().get_param('account_invoice_auto_send_mail_customer_activity_type_arelux_template_id'))
        #account_invoice_auto_send_mail_item_real
        return super(AccountInvoice, self).account_invoice_auto_send_mail_item_real(custom_mail_template_id, author_id)        