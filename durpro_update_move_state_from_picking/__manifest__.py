# -*- coding: utf-8 -*-
{
    'name': "Update Stock Move State from Picking",

    'summary': """
        Allows the updating of stock move states from the stock picking form view.""",

    'description': """
        Utility to allow administrators to fix stock moves that get cancelled or stuck in waiting another move. 
    """,

    'author': "Dur-Pro Ltd.",
    'website': "http://www.durpro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '17.0.0.1',
    "license": "Other proprietary",

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        "views/stock_picking_view.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
