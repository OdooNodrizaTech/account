# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
import requests
import json


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.multi
    def check_iban_convert(self):
        for item in self:
            if item.acc_number:
                if item.acc_type == 'bank':
                    if item.bank_id:
                        if item.bank_id.code:
                            if item.acc_country_id:
                                if item.acc_country_id.code:
                                    # limpiamos caracteres + reemplazamos espacios
                                    account_number = item.acc_number.strip().replace(
                                        ' ',
                                        ''
                                    )
                                    # revisamos longitud de la cuenta bancaria
                                    if len(account_number) == 20:
                                        account_number = account_number.replace(
                                            item.bank_id.code,
                                            ''
                                        )
                                    # request
                                    url = '%s/v2/calculate/%s/%s/%s' % (
                                        'https://openiban.com',
                                        item.acc_country_id.code,
                                        item.bank_id.code,
                                        account_number
                                    )
                                    response = requests.get(url)
                                    if response.status_code == 200:
                                        response_json = json.loads(response.text)
                                        if 'valid' in response_json:
                                            if response_json['valid']:
                                                if 'iban' in response_json:
                                                    if response_json['iban'] != '':
                                                        # update
                                                        item.acc_number = \
                                                            str(response_json['iban'])
                                                        item.acc_type = 'iban'

    @api.model
    def create(self, values):
        return_item = super(ResPartnerBank, self).create(values)
        # check_iban_convert
        return_item.check_iban_convert()
        # return
        return return_item

    @api.multi
    def write(self, vals):
        return_write = super(ResPartnerBank, self).write(vals)
        # check_iban_convert
        for item in self:
            item.check_iban_convert()
        # return
        return return_write
