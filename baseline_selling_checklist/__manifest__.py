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
    'name': 'Baseline Selling Checklist',
    'version': '2.0.1',
    'category': 'Generic Modules/CRM',
    "license": "AGPL-3",
    'complexity': "beginner",
    'description': """Adds tabs with questions to answer on opportunities,
    based on the Baseline Selling sales methodology.
    """,
    'author': 'Marc Durepos, Durpro Ltd (Refactor by Samuel Perron, Libeo)',
    'website': 'http://www.durpro.com',
    'depends': [
        'crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        # DESACTIVER DANS 13.0, refaire vue dans 15.0
        # 'views/crm_lead_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
