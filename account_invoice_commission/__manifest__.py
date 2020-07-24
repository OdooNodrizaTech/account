# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Comission",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "sale",
        "account_invoice_date_paid_status"
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/product_template_view.xml",
        "views/res_users_view.xml",
        "wizard/account_invoice_line_commission.xml",
    ],
    "installable": True
}