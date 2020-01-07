# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Live Currency Exchange Rate - BOI',
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'description': """Import exchange rates from the Internet for bank of israel.
""",
    'depends': [
        'account',
        'currency_rate_live',
    ],
    'data': [
    ],
    'installable': True,
    'auto_install': True,
    # 'license': 'OEEL-1',
}
