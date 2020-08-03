# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, _
from odoo.exceptions import Warning as UserError

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot import xlrd')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def shipping_expedition_datas_override(self, file_encoded):
        self.ensure_one()
        return_action = super(AccountInvoice, self).shipping_expedition_datas_override(
            file_encoded
        )
        # operations
        carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
        if carrier_id.carrier_type == 'cbl':
            # define
            lines = {}
            # xlrd
            book = xlrd.open_workbook(file_contents=file_encoded)
            sheet_names = book.sheet_names()
            sheet = book.sheet_by_name(str(sheet_names[0]))
            values_line_33 = sheet.row_values(32)
            num_factura = str(values_line_33[4])
            if num_factura != self.reference:
                raise UserError(
                    _('The invoice number of the line does not match '
                      'that of the invoice')
                )
            else:
                data_lines = []
                find_total = False
                for row_index in xrange(73, sheet.nrows):
                    if not find_total:
                        row_values = sheet.row_values(row_index)
                        row_value_0 = row_values[0]
                        if row_value_0 != '':
                            if row_value_0 == 'Total':
                                find_total = True
                            else:
                                data_lines.append({
                                    'fecha': row_values[0],
                                    'exp': str(row_values[2]),
                                    'bultos': int(str(row_values[3]).replace('.0', '')),
                                    'kilos': int(str(row_values[4]).replace('.0', '')),
                                    'origen_destino': str(row_values[5]),
                                    'albaran': str(row_values[6]),
                                    'remitente': str(row_values[7]),
                                    'portes': str(row_values[8].replace(',', '.')),
                                    'seguro': str(row_values[11].replace(',', '.')),
                                    'total': str(row_values[14].replace(',', '.'))
                                })
                # generate_lines
                for row_index in xrange(1, len(data_lines)):
                    data_line = data_lines[row_index]
                    # add_line
                    lines[data_line['exp']] = {
                        'code': data_line['exp'],
                        'origin': data_line['albaran'],
                        'number_of_packages': data_line['bultos'],
                        'weight': data_line['kilos'],
                        'cost': data_line['total'],
                    }
            # shipping_expedition_datas_lines_process
            super(AccountInvoice, self).shipping_expedition_datas_lines_process(lines)
        # return
        return return_action
