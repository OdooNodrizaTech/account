# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
import base64

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    is_supplier_delivery_carrier = fields.Boolean(
        compute='_get_is_supplier_delivery_carrier',
        string='Is supplier delivery carrier'
    )
    shipping_expedition_datas = fields.Binary(
        string="Shipping Expedition Data",
        stored=False
    )
    shipping_expedition_ids = fields.One2many('shipping.expedition', 'account_invoice_id', string='Shipping Expedition Ids', readonly=True)

    @api.one
    def shipping_expedition_datas_lines_process(self, carrier_type, lines):
        auto_create_new_shipping_expedition = False
        if len(lines)>0:
            delivery_codes = []
            origins = []
            for line_key in lines:
                line = lines[line_key]
                delivery_codes.append(str(line['delivery_code']))
            #search all
            shipping_expedition_ids = self.env['shipping.expedition'].sudo().search(
                [
                    ('delivery_code', 'in', delivery_codes),
                    ('carrier_id.carrier_type', '=', carrier_type)
                ]
            )
            if len(shipping_expedition_ids)>0:
                for shipping_expedition_id in shipping_expedition_ids:
                    line = lines[str(shipping_expedition_id.delivery_code)]
                    #update
                    shipping_expedition_id.account_invoice_id = self.id
                    shipping_expedition_id.invoice_date = self.date_invoice
                    shipping_expedition_id.currency_id = self.currency_id.id
                    shipping_expedition_id.cost = line['cost']
                    #state
                    if shipping_expedition_id.state!='delivered':
                        shipping_expedition_id.state = 'delivered'
                    #remove
                    del lines[str(shipping_expedition_id.delivery_code)]
            #auto-create
            if auto_create_new_shipping_expedition==True and len(lines)>0:
                _logger.info('Faltarian por crear ' + str(len(lines)) + ' expediciones que nos han facturado y no teniamos')
                lines_old = lines
                lines = {}
                origins = []
                for line_key_old in lines_old:
                    line_old = lines_old[line_key_old]
                    lines[str(line_old['origin'])] = line_old
                    origins.append(str(line_old['origin']))

                stock_picking_ids = self.env['stock.picking'].sudo().search(
                    [
                        ('name', 'in', origins),
                        ('carrier_id.carrier_type', '=', carrier_type)
                    ]
                )
                _logger.info(len(stock_picking_ids))
                if len(stock_picking_ids)>0:
                    for stock_picking_id in stock_picking_ids:
                        line = lines[str(stock_picking_id.name)]
                        shipping_expedition_vals = {
                            'picking_id': stock_picking_id.id,
                            'partner_id': stock_picking_id.partner_id.id,
                            'delivery_code': line['delivery_code'],
                            'date': line['date'],
                            'origin': stock_picking_id.name,
                            'carrier_id': stock_picking_id.carrier_id.id,
                            'account_invoice_id': self.id,
                            'invoice_date': self.date_invoice,
                            'currency_id': self.currency_id.id,
                            'cost': line['cost'],
                            'state': 'delivered',
                        }
                        res_partner_obj = self.env['shipping.expedition'].create(shipping_expedition_vals)

    @api.one
    def shipping_expedition_datas_override(self, file_encoded):
        return False

    @api.one
    def write(self, vals):
        if 'shipping_expedition_datas' in vals:
            if vals['shipping_expedition_datas'] != False:
                if self.is_supplier_delivery_carrier == True:
                    file_encoded = base64.b64decode(vals['shipping_expedition_datas'])
                    self.shipping_expedition_datas_override(file_encoded)
            # remove
            del vals['shipping_expedition_datas']
            # write
        return super(AccountInvoice, self).write(vals)

    @api.one
    def _get_is_supplier_delivery_carrier(self):
        for item in self:
            item.is_supplier_delivery_carrier = False
            if item.type in ['in_invoice', 'in_refund']:
                if item.reference!=False:
                    delivery_carrier_ids = self.env['delivery.carrier'].sudo().search([('supplier_partner_id', '=', item.partner_id.id)])
                    if len(delivery_carrier_ids)>0:
                        item.is_supplier_delivery_carrier = True

    @api.one
    def _get_delivery_carrier_filter_partner_id(self):
        delivery_carrier_id = False
        if self.is_supplier_delivery_carrier==True:
            delivery_carrier_ids = self.env['delivery.carrier'].sudo().search([('supplier_partner_id', '=', self.partner_id.id)])
            if len(delivery_carrier_ids) > 0:
                delivery_carrier_id = delivery_carrier_ids[0]
        #return
        return delivery_carrier_id