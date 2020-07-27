# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Shipping Expedition",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "delivery",
        "shipping_expedition"
    ],
    "data": [
        "views/account_invoice_view.xml",
        "views/delivery_carrier_view.xml",
        "views/shipping_expedition_view.xml",
    ],
    "installable": True
}
