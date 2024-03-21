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
    'name': 'Logistics extra info',
    'version': '17.0.1.0.0',
    'category': 'Generic Modules/Purchasing',
    "license": "AGPL-3",
    'complexity': "expert",
    'description': """
    Adds carrier and carrier account to sales order view.
    Adds fields for inco terms, carrier, carrier account, customs broker to the purchase orders.
    Adds package type field, makes weight manually filled, adds transport cost, adds shipper & verifier fields to picking view.
    """,
    'author': 'Durpro Ltd, Samuel Perron (Libeo)',
    'website': 'http://libeo.com',
    'depends': [
        'sale',
        'stock_delivery',
        'purchase',
    ],
    'data': [
        'views/sales_order_view.xml',
        'views/purchase_view.xml',
        'views/picking_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
