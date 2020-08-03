# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Shipping Expedition Nacex",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account_invoice_shipping_expedition",
        "arelux_partner_questionnaire"  # https://github.com/OdooNodrizaTech/arelux
    ],
    "data": [
        "views/account_invoice_view.xml",
    ],
    "installable": True
}
