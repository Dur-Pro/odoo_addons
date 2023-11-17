# -*- coding: utf-8 -*-

{
    'name': 'Durpro Payment',
    'license': 'Other proprietary',
    'version': '15.0.0.1',
    'category': 'Accounting/Payment',
    'summary': """Adds the ability to send payment receipts by email.""",
    'description': """Send payment receipts by email.""",
    'author': 'Dur-Pro Ltée',
    'maintainer': 'Marc Durepos (mdurepos@durpro.com)',
    'depends': ['account'],
    'data': [
        'data/mail_template_data.xml',
        'views/company_views.xml',
        'views/account_payment_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
