# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    supplier_partner_id = fields.Many2one(
        comodel_name='res.partner',
        domain=[('supplier', '=', True)],
        string='Supplier Partner Id'
    )
    supplier_product_template_id = fields.Many2one(
        comodel_name='product.template',
        domain=[('purchase_ok', '=', True)],
        string='Supplier Product Template Id'
    )