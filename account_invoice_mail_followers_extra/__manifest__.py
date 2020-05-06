# -*- coding: utf-8 -*-
{
    'name': 'Account Invoice Mail Followers Extra',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'contacts', 'account'],
    'data': [
        'views/account_invoice_mail_followers_extra.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,    
}