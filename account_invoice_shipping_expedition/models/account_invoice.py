# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields, _
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
    shipping_expedition_ids = fields.One2many(
        'shipping.expedition',
        'account_invoice_id',
        string='Shipping Expedition Ids',
        readonly=True
    )

    @api.one
    def shipping_expedition_datas_lines_process(self, lines):
        auto_create_new_shipping_expedition = False
        delivery_carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
        if len(lines) > 0:
            # filter_key
            filter_key = False
            # filter_values
            filter_values = []
            for line_key in lines:
                line = lines[line_key]
                # filter_key
                if not filter_key:
                    if 'delivery_code' in line:
                        filter_key = 'delivery_code'
                    else:
                        filter_key = 'code'
                # append
                filter_values.append(str(line[filter_key]))
            # search all
            shipping_expedition_ids = self.env['shipping.expedition'].sudo().search(
                [
                    (filter_key, 'in', filter_values),
                    ('carrier_id.carrier_type', '=', delivery_carrier_id.carrier_type)
                ]
            )
            if shipping_expedition_ids:
                for shipping_expedition_id in shipping_expedition_ids:
                    line = lines[str(shipping_expedition_id[filter_key])]
                    # update
                    shipping_expedition_id.account_invoice_id = self.id
                    shipping_expedition_id.invoice_date = self.date_invoice
                    shipping_expedition_id.currency_id = self.currency_id.id
                    shipping_expedition_id.number_of_packages = line['number_of_packages']
                    shipping_expedition_id.weight = line['weight']
                    shipping_expedition_id.cost = line['cost']
                    # state
                    if shipping_expedition_id.state != 'delivered':
                        shipping_expedition_id.state = 'delivered'
                    # remove
                    del lines[str(shipping_expedition_id[filter_key])]
            # auto-create
            if auto_create_new_shipping_expedition and len(lines) > 0:
                _logger.info(
                    _('Missing to create %s expeditions that have invoiced us and we did not have')
                    % len(lines)
                )
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
                        ('carrier_id.carrier_type', '=', delivery_carrier_id.carrier_type)
                    ]
                )
                _logger.info(len(stock_picking_ids))
                if stock_picking_ids:
                    for stock_picking_id in stock_picking_ids:
                        line = lines[str(stock_picking_id.name)]
                        vals = {
                            'picking_id': stock_picking_id.id,
                            'partner_id': stock_picking_id.partner_id.id,
                            'origin': stock_picking_id.name,
                            'carrier_id': stock_picking_id.carrier_id.id,
                            'account_invoice_id': self.id,
                            'invoice_date': self.date_invoice,
                            'currency_id': self.currency_id.id,
                            'number_of_packages': line['number_of_packages'],
                            'weight': line['weight'],
                            'cost': line['cost'],
                            'state': 'delivered',
                        }
                        # delivery_code
                        if 'delivery_code' in line:
                            vals['delivery_code'] = line['delivery_code']
                        # code
                        if 'code' in line:
                            vals['code'] = line['code']
                        # date
                        if 'date' in line:
                            vals['date'] = line['date']
                        # create
                        self.env['shipping.expedition'].create(vals)

    @api.one
    def shipping_expedition_datas_override(self, file_encoded):
        return False

    @api.one
    def write(self, vals):
        if 'shipping_expedition_datas' in vals:
            if vals['shipping_expedition_datas']:
                if self.is_supplier_delivery_carrier :
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
                if item.reference:
                    delivery_carrier_ids = self.env['delivery.carrier'].sudo().search(
                        [
                            ('supplier_partner_id', '=', item.partner_id.id)
                        ]
                    )
                    if delivery_carrier_ids:
                        item.is_supplier_delivery_carrier = True

    @api.one
    def _get_delivery_carrier_filter_partner_id(self):
        delivery_carrier_id = False
        if self.is_supplier_delivery_carrier:
            delivery_carrier_ids = self.env['delivery.carrier'].sudo().search(
                [
                    ('supplier_partner_id', '=', self.partner_id.id)
                ]
            )
            if delivery_carrier_ids:
                delivery_carrier_id = delivery_carrier_ids[0]
        # return
        return delivery_carrier_id
