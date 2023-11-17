# -*- coding: utf-8 -*-

{
    'name': 'Ticket to Sale Order',
    'license': 'Other proprietary',
    'version': '15.0.0.1',
    'category' : 'Sales/Sales',
    'summary': """Allows your helpdesk team to create sales orders from helpdesk tickets.""",
    'description': """
       Convert helpdesk tickets into sales orders.
    """,
    'author': 'Dur-Pro Ltée',
    'maintainer': 'Marc Durepos (mdurepos@durpro.com)',
    'depends': [
        'sale',
        'helpdesk',
    ],
    'data': [
        'views/account_move_view.xml',
        'views/helpdesk_ticket_views.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
    'application': False,
}
