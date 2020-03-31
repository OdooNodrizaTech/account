# -*- coding: utf-8 -*-
{
    'name': 'Accounting Banking Mandate Auto Create',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'account', 'account_banking_mandate', 'ont_automation_base'],
    'data': [
        'data/ir_cron.xml',
        'views/account_banking_mandate_view.xml',                 
    ],
    'installable': True,
    'auto_install': False,    
}