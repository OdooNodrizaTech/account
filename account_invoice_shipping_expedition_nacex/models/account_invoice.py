# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def shipping_expedition_datas_override(self, file_encoded):
        return_action = super(AccountInvoice, self).shipping_expedition_datas_override(file_encoded)
        #operations
        delivery_carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
        if delivery_carrier_id.carrier_type == 'nacex':
            lines = {}
            file_encoded_split = file_encoded.split('\n')
            if len(file_encoded_split) > 1:
                line = 1
                for file_encoded_line in file_encoded_split:
                    line_data = file_encoded_line.split(';')
                    if len(line_data) > 1:  # Skip last line empty
                        # remove ' character
                        item_count = 0
                        for line_data_item in line_data:
                            line_data[item_count] = line_data_item[1:-1]
                            item_count += 1
                        # operations
                        if line > 1:
                            # data
                            key_0 = line_data[0]
                            tipo = line_data[1]
                            if key_0 == '1' and tipo == 'FRE':
                                num_factura = line_data[2]
                                departamento = line_data[3]
                                albaran = line_data[4]
                                #fecha_albaran
                                fecha_albaran = line_data[5]
                                fecha_albaran_split = fecha_albaran.split('/')
                                fecha_albaran = fecha_albaran_split[2]+'-'+fecha_albaran_split[1]+'-'+fecha_albaran_split[0]
                                #others
                                referencia = line_data[6]
                                cost = line_data[22].replace(',', '.')
                                # ooperations
                                if departamento != 'ONLINE':
                                    _logger.info('NO es Online (RARO)')
                                else:
                                    if num_factura != self.reference:
                                        _logger.info('El n factura de la linea no coincide con el de la factura')
                                    else:
                                        lines[albaran] = {
                                            'delivery_code': albaran,
                                            'origin': referencia,
                                            'date': fecha_albaran,
                                            'cost': cost
                                        }
                    # line
                    line += 1
            #shipping_expedition_datas_lines_process
            super(AccountInvoice, self).shipping_expedition_datas_lines_process('nacex', lines)
        #return
        return return_action