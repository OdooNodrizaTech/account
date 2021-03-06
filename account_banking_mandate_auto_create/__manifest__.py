# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Accounting Banking Mandate Auto Create",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "sale",
        "account",
        "account_banking_mandate"  # https://github.com/OCA/bank-payment
    ],
    "data": [
        "data/ir_cron.xml",
        "views/account_banking_mandate_view.xml",
    ],
    "installable": True
}
