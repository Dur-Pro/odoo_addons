{
    "name": "Durpro Purchase",
    "version": "15.0.1.1.0",
    "license": "Other proprietary",
    "author": "Durpro Ltd",
    "category": "Purchase",
    "depends": [
        "purchase",
        "durpro_base",
        "fims_purchase_down_payments",
    ],
    "description": """
    This module adds basic adjustments to the purchase module for Durpro.
    """,
    "demo": [],
    'data': [
        'views/purchase_view.xml',
        'report/purchase_templates.xml',
    ],
    'test': [],
    'installable': True,
    'active': False
}
