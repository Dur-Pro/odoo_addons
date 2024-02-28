# -*- coding: utf-8 -*-
{
    'name': "Create PO from Ticket",
    'summary': "Allow creating a purchase order from Helpdesk tickets.",
    'description': """
        Allows creation of Purchase Orders from a Helpdesk ticket. 
    """,
    'version': '17.0.0.1',
    'category': 'Purchase',
    'author': 'Dur-Pro Ltée',
    'maintainer': 'Marc Durepos (mdurepos@durpro.com)',
    'depends': [
        'purchase',
        'helpdesk',
    ],
    'data': [
        'views/helpdesk_views.xml',
        'views/purchase_views.xml',
        'wizard/helpdesk_create_purchase_views.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'OEEL-1',
}
