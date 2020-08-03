# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import api, models, _
from odoo.exceptions import Warning as UserError
_logger = logging.getLogger(__name__)

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
        if carrier_id.carrier_type == 'txt':
            # define
            lines = {}
            # xlrd
            book = xlrd.open_workbook(file_contents=file_encoded)
            sheet_names = book.sheet_names()
            sheet = book.sheet_by_name(str(sheet_names[0]))
            # generate_keys
            data_lines = []
            for row_index in range(2, sheet.nrows):
                data_line = []
                values_row = sheet.row_values(row_index)
                for value_row in values_row:
                    data_line.append(str(value_row))
                data_lines.append(data_line)
            # num_factura
            num_factura = '%s/%s' % (
                data_lines[1][23],
                data_lines[1][22].replace('.0', '')
            )
            if num_factura != self.reference:
                raise UserError(
                    _('The invoice number of the line does '
                      'not match that of the invoice')
                )
            else:
                for row_index in range(1, len(data_lines)):
                    data_line = data_lines[row_index]
                    # replace
                    data_line[3] = data_line[3].replace('.0', '')
                    data_line[4] = data_line[4].replace('.0', '')
                    data_line[9] = int(data_line[9].replace('.0', ''))
                    data_line[10] = int(data_line[10].replace('.0', ''))
                    data_line[19] = int(data_line[19].replace('.0', ''))
                    # define
                    if data_line[3] != '0':
                        albaran = '%s - %s' % (
                            data_line[3],
                            data_line[4]
                        )
                    else:
                        albaran = str(data_line[4])
                    # others
                    referencia = str(data_line[5])
                    number_of_packages = data_line[9]
                    weight = data_line[10]
                    cost = data_line[17]
                    tax = data_line[19]
                    cost_with_tax = data_line[20]
                    # add_line
                    lines[albaran] = {
                        'code': albaran,
                        'origin': referencia,
                        'number_of_packages': number_of_packages,
                        'weight': weight,
                        'cost': cost,
                        'tax': tax,
                        'cost_with_tax': cost_with_tax
                    }
            # shipping_expedition_datas_lines_process
            super(AccountInvoice, self).shipping_expedition_datas_lines_process(lines)
        # return
        return return_action
