# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Account Invoice Auto Send Mail Arelux',
    'version': '10.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account_invoice_auto_send_mail', 'external_odoo_base'],
    'data': [
        'data/ir_configparameter_data.xml',                 
    ],
    'installable': True,
    'auto_install': False,    
}