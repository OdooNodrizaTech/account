# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields
from odoo.exceptions import Warning
import pandas as pd
import io

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def shipping_expedition_datas_override(self, file_encoded):
        return_action = super(AccountInvoice, self).shipping_expedition_datas_override(file_encoded)
        #operations
        delivery_carrier_id = self._get_delivery_carrier_filter_partner_id()[0]
        if delivery_carrier_id.carrier_type == 'txt':
            with io.StringIO(file_encoded) as fh:
                df = pd.io.excel.read_excel(fh, sheetname=0)
                _logger.info(df.head(5))
            #file_encoded > convertir de excel a csv
            #shipping_expedition_datas_lines_process
            super(AccountInvoice, self).shipping_expedition_datas_lines_process('nacex', lines)
        #return
        return return_action