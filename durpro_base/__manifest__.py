{
    "name": "Durpro base",
    "version": "17.0.1.1.0",
    "license": "Other proprietary",
    "author": "Durpro Ltd (Frédérick Capovilla, Libeo)",
    "category": "Generic Modules",
    "depends": [
        # Extensions Durpro
        "account_invoice_reference",
        "baseline_selling_checklist",
        "customer_product_code",
        "durpro_customer_reference",
        "product_landed_cost",
        "sale_reference",
        "hr_expense",

        # Extensions supplémentaires
        "mass_editing",
    ],
    "description": """
    This module adds basic adjustments and dependencies for Durpro.
    """,
    "demo": [],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_expense_view.xml',
        'views/payment_view.xml',
        'views/product_view.xml',
        'views/res_company.xml',
        # 'wizard/inventory_valuation.xml',
        'wizard/pricelist_import.xml',
    ],
    'test': [],
    'installable': True,
    'active': False
}
