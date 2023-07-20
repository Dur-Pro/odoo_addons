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
    "name": "Durpro Reports",
    "version": "15.0.2.0.5",
    "license": "Other proprietary",
    "author": "Durpro Ltd",
    "category": "Generic Modules",
    "depends": ["delivery",
                "sale_stock",
                "sale_crm",
                "logistics_extra_info",
                "account_reports",
                "account_payment_term_discount",
                "l10n_ca",
    ],
    "description": """Durpro reports modifications for various modules, including:
Pickings.
    """,
    "demo": [],
    'data': [
        'data/account_financial_report_data.xml',
        'data/res_country_data.xml',
        'views/account_report_search_template_view.xml',
        'report/account_report.xml',
        'report/stock_report_templates.xml',
        'report/sale_report_templates.xml',
        'report/report_invoice_document_durpro.xml',
        'report/stock_report_views.xml',
        'report/report_payment_receipt_templates.xml',
        'report/report_client_account_statement.xml',
        'report/partner_report.xml',
        'report/report_template.xml',
    ],
    'test': [],
    'installable': True,
    'active': False,
    'assets': {
        'web.assets_backend': [
            'durpro_reports/static/src/js/account_reports_currency_dropdown.js',
            'durpro_reports/static/src/js/M2MFilters.js',
        ],
    }
}
