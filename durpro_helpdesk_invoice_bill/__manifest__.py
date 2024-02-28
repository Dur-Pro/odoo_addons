# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name': "Helpdesk Customer Invoice / Vendor Bill",
    'version': "17.0.0.2",
    'summary': "Allow generating a customer invoice or vendor bill from ticket.",
    'description': """
        Create a customer invoice or a vendor bill from a helpdesk ticket. 
    """,
    'category': 'Accounting',
    'author': 'Dur-Pro Ltée',
    'maintainer': 'Marc Durepos (mdurepos@durpro.com)',
    'depends': [
        'account',
        'sale',
        'purchase',
        'helpdesk',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_views.xml',
        'views/account_move_views.xml',
        'wizard/create_account_move_views.xml',
    ],
    'license': 'OEEL-1',
}
