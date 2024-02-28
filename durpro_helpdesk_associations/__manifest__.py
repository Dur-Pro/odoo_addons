# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name': "Associate Helpdesk Tickets to Documents",
    'summary': "Allow associating different records to a ticket.",
    'description': """
        Allows association of a helpdesk ticket to an existing SO, PO, invoice, vendor bill, or FSO work order. 
    """,
    'version': '17.0.0.1',
    'category': 'Services/Helpdesk',
    'author': 'Dur-Pro Ltée',
    'maintainer': 'Marc Durepos (mdurepos@durpro.com)',
    'depends': [
        'account',
        'sale',
        'purchase',
        'helpdesk',
        'durpro_helpdesk_invoice_bill',
        'durpro_helpdesk_fso',
        'durpro_helpdesk_sale',
        'durpro_helpdesk_purchase',
    ],
    'data': [
        'views/helpdesk_views.xml',
        'wizard/helpdesk_association_views.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'OEEL-1',
}
