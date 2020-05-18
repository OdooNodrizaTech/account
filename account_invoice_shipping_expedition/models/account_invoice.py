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
    supplier_lines_datas = fields.Binary(
        string="Supplier Lines Data",
        stored=False
    )

    '''
    @api.one
    def generate_invoice_line_ids_custom(self, supplier_lines):
        if len(supplier_lines)>0:
            delivery_carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
            if delivery_carrier_id.supplier_product_template_id.id>0:
                for supplier_line in supplier_lines:
                    account_invoice_line = {
                        'invoice_id': self.id,
                        'shipping_expedition_id': supplier_line['shipping_expedition_id'],
                        'name': supplier_line['name'],
                        'product_id': delivery_carrier_id.supplier_product_template_id.id,
                        'price_unit': supplier_line['cost'],
                        'currency_id': self.currency_id.id,
                        'quantity': 1
                    }
                    #account_id
                    if delivery_carrier_id.supplier_product_template_id.property_account_expense_id.id>0:
                        account_invoice_line['account_id'] = delivery_carrier_id.supplier_product_template_id.property_account_expense_id.id
                    else:
                        account_invoice_line['account_id'] = delivery_carrier_id.supplier_product_template_id.categ_id.property_account_expense_categ_id.id
                    account_invoice_line_obj = self.env['account.invoice.line'].sudo().create(account_invoice_line)
                    account_invoice_line_obj._onchange_product_id()
                    #account_invoice_line_obj._onchange_account_id()
                    #update_name
                    account_invoice_line_obj.name = account_invoice_line['name']
    '''

    @api.one
    def generate_invoice_line_ids_custom(self, supplier_lines):
        if len(supplier_lines) > 0:
            delivery_carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
            if delivery_carrier_id.supplier_product_template_id.id > 0:
                total_lines = len(supplier_lines)
                _logger.info('Total lineas a crear '+str(total_lines))
                count = 1
                for supplier_line in supplier_lines:
                    account_invoice_line = {
                        'invoice_id': self.id,
                        'shipping_expedition_id': supplier_line['shipping_expedition_id'],
                        'name': supplier_line['name'],
                        'product_id': delivery_carrier_id.supplier_product_template_id.id,
                        'price_unit': supplier_line['cost'],
                        'currency_id': self.currency_id.id,
                        'quantity': 1
                    }
                    # account_id
                    if delivery_carrier_id.supplier_product_template_id.property_account_expense_id.id > 0:
                        account_invoice_line['account_id'] = delivery_carrier_id.supplier_product_template_id.property_account_expense_id.id
                    else:
                        account_invoice_line['account_id'] = delivery_carrier_id.supplier_product_template_id.categ_id.property_account_expense_categ_id.id
                    account_invoice_line_obj = self.env['account.invoice.line'].sudo().create(account_invoice_line)
                    taxes = account_invoice_line_obj.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == account_invoice_line_obj.invoice_id.company_id) or account_invoice_line_obj.account_id.tax_ids or account_invoice_line_obj.invoice_id.company_id.account_purchase_tax_id
                    account_invoice_line_obj.invoice_line_tax_ids = fp_taxes = account_invoice_line_obj.invoice_id.fiscal_position_id.map_tax(taxes, account_invoice_line_obj.product_id, account_invoice_line_obj.invoice_id.partner_id)
                    #count
                    count += 1
                    _logger.info('Creando linea '+str(count)+'/ '+str(total_lines))
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