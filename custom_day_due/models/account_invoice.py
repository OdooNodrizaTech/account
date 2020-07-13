# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    @api.one
    def action_move_create(self):        
        res = super(AccountInvoice, self).action_move_create()                            
        for inv in self:
            custom_days_due = inv.generate_custom_days_due()
            if len(custom_days_due)>0:
                date_due = False
                day_date_due = False
                                                                                                                
                for line_id in inv.move_id.line_ids:
                    if line_id.debit>0:
                        
                        date_due = datetime.datetime.strptime(line_id.date_maturity.strftime("%Y-%m-%d"), "%Y-%m-%d")
                        day_date_due = int(date_due.strftime('%d'))
                                                                                  
                        while not (day_date_due in custom_days_due):                            
                            modified_date = date_due + datetime.timedelta(days=1)
                            line_id.date_maturity = datetime.datetime.strftime(modified_date, "%Y-%m-%d")                                                                                              
                        
                            date_due = datetime.datetime.strptime(line_id.date_maturity.strftime("%Y-%m-%d"), "%Y-%m-%d")
                            day_date_due = int(date_due.strftime('%d'))                        
    
    def generate_custom_days_due(self):
        custom_days_due = []
        
        if self.type=="in_invoice":
            if self.partner_id.custom_day_due_1_purchase!=False or self.partner_id.custom_day_due_2_purchase!=False or self.partner_id.custom_day_due_3_purchase!=False or self.partner_id.custom_day_due_4_purchase!=False:            
                #custom_day_due_1_purchase
                if self.partner_id.custom_day_due_1_purchase!=False and self.partner_id.custom_day_due_1_purchase.isnumeric()==True: 
                    custom_day_due_1 = int(self.partner_id.custom_day_due_1_purchase)
                    if(custom_day_due_1>0):         
                        custom_days_due.append(custom_day_due_1)
                    
                #custom_day_due_2_purchase
                if self.partner_id.custom_day_due_2_purchase!=False and self.partner_id.custom_day_due_2_purchase.isnumeric()==True:
                    custom_day_due_2 = int(self.partner_id.custom_day_due_2_purchase)
                    if(custom_day_due_2>0):         
                        custom_days_due.append(custom_day_due_2)
                            
                #custom_day_due_3_purchase
                if self.partner_id.custom_day_due_3_purchase!=False and self.partner_id.custom_day_due_3_purchase.isnumeric()==True:
                    custom_day_due_3 = int(self.partner_id.custom_day_due_3_purchase)
                    if(custom_day_due_3>0):         
                        custom_days_due.append(custom_day_due_3)
                    
                #custom_day_due_4_purchase
                if self.partner_id.custom_day_due_4_purchase!=False and self.partner_id.custom_day_due_4_purchase.isnumeric()==True:
                    custom_day_due_4 = int(self.partner_id.custom_day_due_4_purchase)
                    if(custom_day_due_4>0):         
                        custom_days_due.append(custom_day_due_4)
                    
        else:
            if self.partner_id.custom_day_due_1!=False or self.partner_id.custom_day_due_2!=False or self.partner_id.custom_day_due_3!=False or self.partner_id.custom_day_due_4!=False:        
                #custom_day_due_1
                if self.partner_id.custom_day_due_1!=False and self.partner_id.custom_day_due_1.isnumeric()==True:
                    custom_day_due_1 = int(self.partner_id.custom_day_due_1)
                    if(custom_day_due_1>0):         
                        custom_days_due.append(custom_day_due_1)
                    
                #custom_day_due_2
                if self.partner_id.custom_day_due_2!=False and self.partner_id.custom_day_due_2.isnumeric()==True:
                    custom_day_due_2 = int(self.partner_id.custom_day_due_2)
                    if(custom_day_due_2>0):         
                        custom_days_due.append(custom_day_due_2)
                            
                #custom_day_due_3
                if self.partner_id.custom_day_due_3!=False and self.partner_id.custom_day_due_3.isnumeric()==True:
                    custom_day_due_3 = int(self.partner_id.custom_day_due_3)
                    if(custom_day_due_3>0):         
                        custom_days_due.append(custom_day_due_3)
                    
                #custom_day_due_4
                if self.partner_id.custom_day_due_4!=False and self.partner_id.custom_day_due_4.isnumeric()==True:
                    custom_day_due_4 = int(self.partner_id.custom_day_due_4)
                    if(custom_day_due_4>0):         
                        custom_days_due.append(custom_day_due_4)
                    
        return custom_days_due
    
    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):    
        res = super(AccountInvoice, self)._onchange_payment_term_date_invoice()        
        self.ensure_one()
                                    
        if self.date_due!=False:
            old_date_due = self.date_due
            
            custom_days_due = self.generate_custom_days_due()
            if len(custom_days_due)>0:                            
                date_due = datetime.datetime.strptime(self.date_due.strftime("%Y-%m-%d"), "%Y-%m-%d")
                day_date_due = int(date_due.strftime('%d'))
                
                if not (day_date_due in custom_days_due):              
                    while not (day_date_due in custom_days_due):                            
                        date_due = datetime.datetime.strptime(self.date_due.strftime("%Y-%m-%d"), "%Y-%m-%d")
                        modified_date = date_due + datetime.timedelta(days=1)
                        self.date_due = datetime.datetime.strftime(modified_date, "%Y-%m-%d")                                                                                                                
                    
                        date_due = datetime.datetime.strptime(self.date_due.strftime("%Y-%m-%d"), "%Y-%m-%d")
                        day_date_due = int(date_due.strftime('%d'))