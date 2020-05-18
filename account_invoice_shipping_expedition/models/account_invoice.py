# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

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