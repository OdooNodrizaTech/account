# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import Warning

import xlsxwriter
import os
import unidecode
from zipfile import ZipFile

import logging
_logger = logging.getLogger(__name__)

class WizardAccountInvoiceLineCommission(models.TransientModel):
    _name = 'wizard.account.invoice.line.commission'
    _description = 'Wizard Account Invoice Line Commission'

    #data = fields.Binary('Content', readonly=True)
    from_date = fields.Date(
        string='Date from',
        help='Date from invoice payment end date',
        required=True
    )
    to_date = fields.Date(
        string='Date to',
        help='Date to the invoice payment end date',
        required=True
    )
    user_ids = fields.Many2many(
        'res.users',
        domain=[('sale_team_id', '!=', False)],
        string='Users',
        help='Invoice users',
        required=True,
        store=True
    )
    paid = fields.Boolean(
        string='Paid',
        help='Invoices that are already defined with a commission payment date or NOT were filtered',
        required=True,
        default=False
    )
    mark_as_paid = fields.Boolean(
        string='Mark as paid',
        help='If YES is checked, the commission payment date will be auto-defined NOW for all invoice lines (which have a commission) and their invoices',
        required=True,
        default=True
    )

    @api.multi
    def generate_file(self):
        self.ensure_one()
        for item in self:
            # user_ids
            user_ids = []
            for user_id in item.user_ids:
                user_ids.append(user_id.id)
            # operations
            if len(user_ids) == 0:
                raise Warning(_('It is necessary to select at least 1 user'))
            else:
                filters = [
                    ('state', '=', 'paid'),
                    ('type', 'in', ('out_invoice', 'out_refund')),
                    ('date_paid_status', '!=', False),
                    ('date_paid_status', '>=', item.from_date.strftime("%Y-%m-%d")),
                    ('date_paid_status', '<=', item.to_date.strftime("%Y-%m-%d")),
                    ('user_id', 'in', user_ids)
                ]
                # paid
                if not item.paid:
                    filters.append(('commission_date_paid', '=', False))
                else:
                    filters.append(('commission_date_paid', '!=', False))
                # search
                account_invoice_ids = self.env['account.invoice'].sudo().search(filters)
                # operations
                if len(account_invoice_ids) == 0:
                    raise Warning(_('No invoices matching the criteria were found'))
                else:
                    # res_users
                    res_users_ids = self.env['res.users'].sudo().search(
                        [
                            ('id', 'in', account_invoice_ids.mapped('user_id').ids)
                        ],
                        order="name asc"
                    )
                    if res_users_ids:
                        res_users_id_info = {}
                        account_invoice_line_by_user_id = {}
                        # define
                        for res_users_id in res_users_ids:
                            res_users_id_info[res_users_id.id] = {
                                'id': res_users_id.id,
                                'name': res_users_id.name,
                                'name_unidecode': unidecode.unidecode(res_users_id.name.lower().replace(' ', '-')),
                                'total_price_subtotal': 0,
                                'total_commission': 0,
                            }
                            account_invoice_line_by_user_id[res_users_id.id] = []
                            # account_invoice_lines
                            account_invoice_line_ids = self.env['account.invoice.line'].sudo().search(
                                [
                                    ('invoice_id', 'in', account_invoice_ids.ids),
                                    ('invoice_id.user_id', '=', res_users_id.id),
                                    ('commission', '>', 0)
                                ]
                            )
                            if account_invoice_line_ids:
                                for account_invoice_line_id in account_invoice_line_ids:
                                    info_line = account_invoice_line_id.define_account_invoice_line_info_commission()[0]
                                    # res_users_id_info
                                    res_users_id_info[res_users_id.id]['total_price_subtotal'] += info_line['price_subtotal']
                                    res_users_id_info[res_users_id.id]['total_commission'] += info_line['commission']
                                    # fields_round
                                    fields = ['price_subtotal', 'commission_percent', 'commission']
                                    for field in fields:
                                        if field in info_line:
                                            info_line[field] = "{0:.2f}".format(info_line[field])
                                    # append
                                    account_invoice_line_by_user_id[res_users_id.id].append(info_line)
                                # format round
                                res_users_id_info[res_users_id.id]['total_price_subtotal'] = "{0:.2f}".format(res_users_id_info[res_users_id.id]['total_price_subtotal'])
                                res_users_id_info[res_users_id.id]['total_commission'] = "{0:.2f}".format(res_users_id_info[res_users_id.id]['total_commission'])
                        # define
                        path_file = os.path.abspath(__file__).split('wizard/')[0]
                        header_info_line = self.env[ 'account.invoice.line'].sudo().define_account_invoice_line_header_info_commission()
                        # generate zip file
                        file_names = []
                        for res_users_id in res_users_ids:
                            res_users_id_info_item = res_users_id_info[res_users_id.id]
                            if res_users_id.id not in account_invoice_line_by_user_id:
                                _logger.info(_('Very strange that ID %s does not exist in account_invoice_line_by_user_id') % res_users_id.id)
                            else:
                                # xlsx
                                xlsx_name = '%s%s.xlsx' % (path_file, res_users_id_info_item['name_unidecode'])
                                file_names.append(xlsx_name)
                                workbook = xlsxwriter.Workbook(xlsx_name)
                                worksheet = workbook.add_worksheet()
                                # header
                                row = 0
                                col = 0
                                for header_info_line_item in header_info_line:
                                    worksheet.write(row, col, str(header_info_line[header_info_line_item]))
                                    col += 1
                                # increase row
                                row += 1
                                # account_invoice_lines_by_user_id
                                account_invoice_lines_by_user_id = account_invoice_line_by_user_id[res_users_id.id]
                                for account_invoice_line_by_user_id in account_invoice_lines_by_user_id:
                                    col = 0
                                    for item in account_invoice_line_by_user_id:
                                        value_item = str(account_invoice_line_by_user_id[item])
                                        worksheet.write(row, col, value_item)
                                        col += 1
                                    # increase row
                                    row += 1
                                # add_total new line
                                last_account_invoice_lines_by_user_id = account_invoice_lines_by_user_id[len(account_invoice_lines_by_user_id)-1]
                                col = 0
                                for item in last_account_invoice_lines_by_user_id:
                                    if item == 'price_subtotal':
                                        worksheet.write(row, col, res_users_id_info_item['total_price_subtotal'])
                                    elif item == 'commission':
                                        worksheet.write(row, col, res_users_id_info_item['total_commission'])
                                    # increase_col
                                    col += 1
                                # close
                                workbook.close()
                        # generate_zip_file
                        if len(file_names)>0:
                            zip_name = '%scomisiones.zip' % (path_file)
                            # zip_operations
                            zipObj = ZipFile(zip_name, 'w')
                            # Add multiple files to the zip
                            for file_name in file_names:
                                file_name_split = file_name.split('/')
                                file_name_real = file_name_split[len(file_name_split)-1]
                                zipObj.write(file_name, file_name_real)
                            # close the Zip File
                            zipObj.close()
                            # descargar
                            # append
                            file_names.append(zip_name)
                            # eliminar archivos
                            for file_name in file_names:
                                # os.remove(file_name)
                                _logger.info(_('Here we will delete the file% s') % file_name)
        # return
        return True

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.account.invoice.line.commission',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }