# -*- coding: utf-8 -*-
{
    'name': 'Account Invoice Comission',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account', 'sale', 'ont_base_account'],
    'data': [
        'views/account_invoice.xml',
        'views/product_template.xml',
        'views/res_users.xml'        
    ],
    'installable': True,
    'auto_install': False,    
}