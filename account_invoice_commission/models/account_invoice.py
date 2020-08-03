# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    commission = fields.Float(
        string='Comission'
    )
    commission_date_paid = fields.Date(
        string='Comission date paid',
        readonly=True
    )

    @api.multi
    def action_invoice_open(self):
        return_action = super(AccountInvoice, self).action_invoice_open()
        # action_regenerate_commission_percent_lines
        for item in self:
            item.action_regenerate_commission_percent_lines()
        # return
        return return_action

    @api.multi
    def write(self, vals):
        need_regenerate_commission = False
        # stage date_paid_status
        if vals.get('state') == 'paid':
            need_regenerate_commission = True
        # write
        return_object = super(AccountInvoice, self).write(vals)
        # action_regenerate_commission
        if need_regenerate_commission:
            self.action_regenerate_commission()
        # return
        return return_object

    @api.multi
    def action_regenerate_commission_multi(self):
        for item in self:
            item.action_regenerate_commission_percent_lines()
            item.action_regenerate_commission()

    @api.multi
    def action_regenerate_commission_percent_lines(self):
        for item in self:
            if item.type in ['out_invoice', 'out_refund']:
                if item.state in ['open', 'paid']:
                    if item.user_id:
                        item_u = item.user_id
                        for line_id in item.invoice_line_ids:
                            if line_id.product_id:
                                line_id_p = line_id.product_id
                                if not line_id_p.not_allow_account_invoice_commission:
                                    if line_id_p.type != 'service':
                                        line_id.commission_percent = \
                                            item_u.invoice_commission_percent

    @api.multi
    def action_regenerate_commission(self):
        for item in self:
            if item.type in ['out_invoice', 'out_refund']:
                if item.state == 'paid':
                    if item.invoice_line_ids:
                        # calculate_comission
                        commission = 0
                        # operations
                        for line_id in item.invoice_line_ids:
                            line_id.action_calculate_commission()
                            # commission
                            commission += line_id.commission
                        # commission
                        item.commission = "{:.2f}".format(commission)
