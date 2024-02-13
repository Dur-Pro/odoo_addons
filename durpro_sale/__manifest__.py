# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    "name": "Durpro Sale",
    "version": "15.0.1.2.1",
    "license": "Other proprietary",
    "author": "Durpro Ltd",
    "category": "Generic Modules",
    "depends": ["sale",
                "stock_dropshipping",
                "product",
                "durpro_accounting",
                ],
    "description": """Module for setting up the Sales app according to Durpro's
    needs.""",
    "demo": [],
    'data': [
        "views/sale_view.xml",
        "views/product_pricelist_view.xml",
        "views/res_config_settings_views.xml",
        "report/sale_report_templates.xml",
    ],
    'test': [],
    'installable': True,
    'active': False,
    'assets': {

    }
}
