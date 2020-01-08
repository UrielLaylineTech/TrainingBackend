# -*- coding: utf-8 -*-

import datetime
from lxml import etree
from dateutil.relativedelta import relativedelta
import re
import logging
from pytz import timezone

import requests

from odoo import api, fields, models
from odoo.addons.web.controllers.main import xml2json_from_elementtree
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'
    # adding BOI to options of selecting the company's currency provider
    currency_provider = fields.Selection(selection_add=[('boi', 'Bank Of Israel')])
   

    @api.model
    def set_special_defaults_on_install(self):
        res = super(ResCompany, self).set_special_defaults_on_install()
        for company in self.env['res.company'].search([]):
            if company.country_id.code == 'IL':
                #Bank of Israel configured as currency provider of Israeli companies
                company.currency_provider = 'boi'
        return res


    
    def _parse_boi_data(self, available_currencies):
        ''' This method is used to update the currencies by using BOI service provider.
            Rates are given against ILS
        '''
        request_url = "https://www.boi.org.il/currency.xml"
        try:
            parse_url = requests.request('GET', request_url)
        except:
            #connection error, the request wasn't successful
            return False

        xmlstr = etree.fromstring(parse_url.content)
        data = xml2json_from_elementtree(xmlstr)
        rates_dict = {}

        available_currency_names = available_currencies.mapped('name')

        for child_node in data['children']:
            
            if child_node['tag'] == 'CURRENCY':
                for sub_child in child_node['children']:
                    if sub_child['tag'] == "CURRENCYCODE":
                        currency_code = sub_child['children'][0]

                        add_to_dict = False

                        if currency_code in available_currency_names:
                            rate_xml = None
                            add_to_dict = True

                    elif sub_child['tag'] == 'UNIT':
                        currency_xml = sub_child['children'][0]
                    elif sub_child['tag'] == 'RATE':
                        rate_xml = sub_child['children'][0]
 
                if add_to_dict:
                    #compute actual rate against ILS by dividing units by rate.
                    rates_dict[currency_code] = (float(currency_xml) / float(rate_xml), fields.Date.today())

        if 'ILS' in available_currency_names:
            rates_dict['ILS'] = (1.0, fields.Date.today())

        return rates_dict


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'