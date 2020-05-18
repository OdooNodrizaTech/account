# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning
import base64

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    is_supplier_delivery_carrier = fields.Boolean(
        compute='_get_is_supplier_delivery_carrier',
        string='Is supplier delivery carrier'
    )

    @api.one
    def generate_invoice_line_ids_custom(self, supplier_lines):
        return super(AccountInvoice, self).generate_invoice_line_ids_custom(supplier_lines)

    @api.one
    def write(self, vals):
        if 'shipping_expedition_datas' in vals:
            if vals['shipping_expedition_datas']!=False:
                if self.is_supplier_delivery_carrier == True:
                    delivery_carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
                    if delivery_carrier_id.carrier_type=='nacex':
                        if len(self.invoice_line_ids)>0:
                            raise Warning("Es necesario que no haya lineas definidas previamente")
                        else:
                            supplier_lines = []
                            file_encoded = base64.b64decode(vals['shipping_expedition_datas'])
                            file_encoded_split = file_encoded.split('\n')
                            if len(file_encoded_split)>1:
                                line = 1
                                for file_encoded_line in file_encoded_split:
                                    line_data = file_encoded_line.split(';')
                                    if len(line_data)>1:#Skip last line empty
                                        #remove ' character
                                        item_count = 0
                                        for line_data_item in line_data:
                                            line_data[item_count] = line_data_item[1:-1]
                                            item_count += 1
                                        #operations
                                        if line>1:
                                            #data
                                            key_0 = line_data[0]
                                            tipo = line_data[1]
                                            if key_0=='1' and tipo=='FRE':
                                                num_factura = line_data[2]
                                                departamento = line_data[3]
                                                albaran = line_data[4]
                                                cost = line_data[22].replace(',', '.')
                                                #ooperations
                                                if departamento!='ONLINE':
                                                    _logger.info('NO es Online (RARO)')
                                                else:
                                                    if num_factura!=self.reference:
                                                        _logger.info('El n factura de la linea no coincide con el de la factura')
                                                    else:
                                                        #search_stock_picking
                                                        shipping_expedition_ids = self.env['shipping.expedition'].sudo().search(
                                                            [
                                                                ('delivery_code', '=', albaran),
                                                                ('carrier_id.carrier_type', '=', 'nacex')
                                                            ]
                                                        )
                                                        if len(shipping_expedition_ids)==0:
                                                            _logger.info('Raro, la referencia '+str(albaran)+' no la tenemos y nos la facturan')
                                                        else:
                                                            shipping_expedition_id = shipping_expedition_ids[0]
                                                            _logger.info('Actualizamos respecto a la expedicion ' + str(shipping_expedition_id.id))
                                                            #update
                                                            shipping_expedition_id.account_invoice_id = self.id
                                                            shipping_expedition_id.invoice_date = self.date_invoice
                                                            shipping_expedition_id.currency_id = self.currency_id.id
                                                            shipping_expedition_id.cost = cost
                                    #line
                                    line += 1
            #remove
            del vals['shipping_expedition_datas']
        # write
        return super(AccountInvoice, self).write(vals)