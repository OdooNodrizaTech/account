# -*- coding: utf-8 -*-
{
    'name': 'Account Invoice Shipping Expedition Nacex',
    'version': '10.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account_invoice_shipping_expedition', 'arelux_partner_questionnaire'],
    'data': [
        'views/account_invoice.xml',
    ],
    'installable': True,
    'auto_install': False,
}