# -*- coding: utf-8 -*-
{
    'name': "Durpro Check Availability Fix",

    'summary': """
        Bypasses the MTO functionality and chained stock moves if stock is already available to fulfill a move.""",

    'description': """
        Bypasses the MTO functionality and chained stock moves if stock is already available to fulfill a move.
    """,

    'author': "Dur-Pro Ltd.",
    'website': "http://www.durpro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1.1',
    "license": "Other proprietary",

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
