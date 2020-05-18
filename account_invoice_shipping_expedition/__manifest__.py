# -*- coding: utf-8 -*-
{
    'name': 'Account Invoice Shipping Expedition',
    'version': '10.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account', 'delivery', 'shipping_expedition'],
    'data': [
        'views/account_invoice.xml',
        'views/delivery_carrier.xml',
    ],
    'installable': True,
    'auto_install': False,
}