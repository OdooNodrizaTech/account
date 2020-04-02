# -*- coding: utf-8 -*-
{
    'name': 'Ont Margin Account',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account', 'sale', 'ont_margin_sale'],
    'data': [
        'views/account_invoice.xml',
    ],
    'installable': True,
    'auto_install': False,    
}