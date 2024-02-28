{
    "name": "Durpro base",
    "version": "17.0.0.2",
    "license": "Other proprietary",
    "author": "Durpro Ltd (Frédérick Capovilla, Libeo)",
    "category": "Generic Modules",
    "depends": [
        # Extensions Durpro
        "account_invoice_reference",
        "baseline_selling_checklist",
        "customer_product_code",
        "durpro_customer_reference",
        # "durpro_reports",
        "logistics_extra_info",
        "product_landed_cost",
        "sale_reference",
        "hr_expense",
        "durpro_sale",
        "durpro_accounting",
    ],
    "description": """
    This module adds basic adjustments and dependencies for Durpro.
    """,
    "demo": [],
    'data': [
        'security/ir.model.access.csv',
        'data/groups.xml',
        'views/hr_expense_view.xml',
        'views/payment_view.xml',
        'views/product_view.xml',
        'views/stock_view.xml',
        'views/res_company.xml',
        'wizard/inventory_valuation.xml',
        'wizard/pricelist_import.xml',
    ],
    'test': [],
    'installable': True,
    'active': False
}
