{
    "name": "Durpro Purchase",
    "version": "17.0.1.3.0",
    "license": "Other proprietary",
    "author": "Durpro Ltd",
    "category": "Purchase",
    "depends": [
        "purchase",
        "durpro_base",
        "fims_purchase_down_payments",
        "product_pricelist_supplierinfo",
    ],
    "description": """
    This module adds basic adjustments to the purchase module for Durpro.
    """,
    'data': [
        'data/groups.xml',
        'views/purchase_view.xml',
    ],
    'test': [],
    'installable': True,
    'auto-install': True,
    'active': False
}
