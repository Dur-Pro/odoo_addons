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
    "name": "Supplier Invoice Reference Field in Search View",
    "version": "2.0",
    "author": "Durpro Ltd (Refactor by Samuel Perron, Libeo)",
    "category": "Generic Modules",
    "license": "AGPL-3",
    "depends": [
        "base", "account"
    ],
    "demo": [],
    "description": """
    Adds the supplier invoice number field from a Supplier Invoice to the
    search view.
    """,
    'data': [
        'views/account_invoice_view.xml'
    ],
    'test': [],
    'installable': True,
    'active': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
