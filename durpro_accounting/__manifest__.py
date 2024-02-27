{
    "name": "Durpro Accounting",
    "description": """Module for configuring Durpro's basic accounting needs.""",
    "version": "16.0.1.0.0",
    "license": "Other proprietary",
    "author": "Durpro Ltd",
    "maintainer": "Marc Durepos <mdurepos@durpro.com>",
    "category": "Accounting",
    "depends": [
        # "account_3way_match",
        "account_invoice_reference",
    ],
    "demo": [],
    'data': [
        # "data/account_financial_report_data.xml",
        "views/account_view.xml",
        "views/account_move_views.xml",
        # "views/account_bank_statement_views.xml",
    ],
    'test': [],
    'installable': True,
    'active': False,
}
