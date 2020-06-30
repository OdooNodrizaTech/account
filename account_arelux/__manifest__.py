# -*- coding: utf-8 -*-
{
    'name': 'Account Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'account', 'survey', 'crm_claim'],
    'data': [
        'views/account_invoice.xml',            
        'views/sale_order.xml',        
        'views/resources.xml',
    ],
    'installable': True,
    'auto_install': False,    
}