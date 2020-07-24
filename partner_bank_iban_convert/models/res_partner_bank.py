# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.exceptions import Warning
from datetime import datetime

import requests, json

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.one
    def check_iban_convert(self):
        if self.acc_number:
            if self.acc_type == 'bank':
                if self.bank_id:
                    if self.bank_id.code:
                        if self.acc_country_id:
                            if self.acc_country_id.code:
                                # limpiamos caracteres + reemplazamos espacios
                                account_number = str(self.acc_number).strip().replace(' ', '')                   
                                # revisamos longitud de la cuenta bancaria
                                if len(account_number) == 20:
                                    account_number = account_number.replace(self.bank_id.code, '')
                                # request
                                url = 'https://openiban.com/v2/calculate/%s/%s/%s' % (
                                    self.acc_country_id.code,
                                    self.bank_id.code,
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
                                                    self.acc_number = str(response_json['iban'])
                                                    self.acc_type = 'iban'                            

    @api.model
    def create(self, values):
        return_item = super(ResPartnerBank, self).create(values)
        # check_iban_convert
        return_item.check_iban_convert()
        # return
        return return_item
    
    @api.one
    def write(self, vals):                        
        return_write = super(ResPartnerBank, self).write(vals)
        # check_iban_convert
        self.check_iban_convert()
        # return
        return return_write