# -*- coding: utf-8 -*-
from openerp import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    custom_day_due_1 = fields.Char('Dia de pago 1')
    custom_day_due_2 = fields.Char('Dia de pago 2')
    custom_day_due_3 = fields.Char('Dia de pago 3')
    custom_day_due_4 = fields.Char('Dia de pago 4')                                           