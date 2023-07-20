{
    "name": "Product Forecast With Pending Field",
    "version": "1.0.1.1",
    "license": "GPL-3",
    "author": "Durpro Ltd",
    "category": "Inventory",
    "maintainer": "Marc Durepos (mdurepos@durpro.com)",
    "depends": [
        # Extensions Durpro
        "product",
        "stock",
        "purchase",
        "sale",
        "sale_stock",
        "sale_purchase_stock",
    ],
    "description": """
    This module adds the forecast with pending field to product variant search views. 
    """,
    "demo": [],
    'data': [
        'views/product_view.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}
