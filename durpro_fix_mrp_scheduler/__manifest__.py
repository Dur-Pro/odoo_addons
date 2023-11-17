# -*- coding: utf-8 -*-
{
    'name': "Durpro Scheduler Fix",

    'summary': """
        Includes stock moves that are in "waiting" state.""",

    'description': """
        Fix for the following situation:
        
        1. SO with an item quantity 2 gets confirmed, only 1 in in stock.
        2. Draft PO gets created to order the remaining 1.
        3. Second SO with a quantity 1 gets confirmed, new OUT reserves the 1 in stock.
        4. First OUT never gets fulfilled because it is understocked by 1 unit. 
    """,

    'author': "Dur-Pro Ltd.",
    'website': "http://www.durpro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '15.0.0.1',
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
