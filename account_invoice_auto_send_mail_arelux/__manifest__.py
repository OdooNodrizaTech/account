# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Auto Send Mail Arelux",
    "version": "12.0.1.0.0",
    "category": "Sales Management",
    "website": "https://nodrizatech.com/",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account_invoice_auto_send_mail",
        "arelux_partner_questionnaire"
    ],
    "data": [
        "views/account_journal_view.xml",
    ],
    "installable": True,
}