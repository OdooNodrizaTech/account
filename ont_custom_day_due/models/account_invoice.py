# -*- coding: utf-8 -*-
from openerp import api, models, fields

import datetime

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        
        res = super(AccountInvoice, self)._onchange_payment_term_date_invoice()
        
        if (int(self.partner_id.custom_day_due_1)>0) or (int(self.partner_id.custom_day_due_2)>0) or (int(self.partner_id.custom_day_due_3)>0) or (int(self.partner_id.custom_day_due_4)>0):
        
            date_due = datetime.datetime.strptime(self.date_due, "%Y-%m-%d")
            day_date_due = int(date_due.strftime('%d'))
            
            custom_days_due = []
            #custom_day_due_1
            custom_day_due_1 = int(self.partner_id.custom_day_due_1)
            if(custom_day_due_1>0):         
                custom_days_due.append(custom_day_due_1)
                
            #custom_day_due_2
            custom_day_due_2 = int(self.partner_id.custom_day_due_2)
            if(custom_day_due_2>0):         
                custom_days_due.append(custom_day_due_2)
                        
            #custom_day_due_3
            custom_day_due_3 = int(self.partner_id.custom_day_due_3)
            if(custom_day_due_3>0):         
                custom_days_due.append(custom_day_due_3)
                
            #custom_day_due_4
            custom_day_due_4 = int(self.partner_id.custom_day_due_4)
            if(custom_day_due_4>0):         
                custom_days_due.append(custom_day_due_4)                        
            
            if not (day_date_due in custom_days_due):          
                while not (day_date_due in custom_days_due):
                    date_due = datetime.datetime.strptime(self.date_due, "%Y-%m-%d")
                    modified_date = date_due + datetime.timedelta(days=1)
                    self.date_due = datetime.datetime.strftime(modified_date, "%Y-%m-%d")
                
                    date_due = datetime.datetime.strptime(self.date_due, "%Y-%m-%d")
                    day_date_due = int(date_due.strftime('%d'))                                                    
                                                                                   