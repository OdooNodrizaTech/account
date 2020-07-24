# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Payment Order Invoice",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "purchase",
        "account_payment_order"
    ],
    "data": [
        "data/ir_configparameter_data.xml",
        "views/account_payment_order_view.xml",
        #"views/res_bank_view.xml",
    ],
    "installable": True
}