{
    "name": "Durpro base",
    "version": "15.0.0.2",
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
        # Not working anymore
        # "google_drive_report",
        "logistics_extra_info",
        "product_landed_cost",
        "sale_reference",
        "hr_expense",
        "durpro_sale",
        "durpro_accounting",

        # Extensions supplémentaires
        # REMOVE FOR MIGRATION, RE-ADD IT AFTER PURCHASE ON ODOO 13.0
        # "account_excel_report",
        # "account_payment_order",
        # BV: Get rid of it in Enterprise Got to see impact on old data
        # "currency_rate_update",
        # REMOVE FOR MIGRATION TEST, RE-ADD IT AFTER PURCHASE ON ODOO 12.0
        # "account_parent",
        # AVAILABLE, BUY IT For 13
        # "dev_invoice_multi_payment",
        "mass_editing",
        ### "crm_phonecall",
        # "product_pricelist_supplierinfo",
        ### "date_range",
        # "account_tax_balance",
        # DID NOT EXIST IN 14.0
        # "account_check_printing_report_base",
        # NOT IN 12.0, did try easy fix, not working
        # "account_financial_report_date_range",
        # NOT IN 13.0, did not try easy fix
        # "hr_expense_cancel",
        # NEED PURCHASE 13.0, did not hold data, can be remove then replace with other case no version over 13.0
        # "r3x_stock_valuation_report",
        ### "sale_force_invoiced",
        ## "stock_production_lot_active",
        ## "stock_picking_back2draft",
        ## "stock_picking_operation_quick_change",
        # "web_sheet_full_width",
        # "web_widget_datepicker_fulloptions",

        # Extensions installées manuellement
        # BUGGY IN 13.0, did not try easy fix
        # "account_financial_report",
        # DOES NOT EXIST in 14.0
        # "account_payment_show_invoice",
        #  WHY DID I MISS THOSE TWO NOTHING AFTER 13.0/14.0 AND NATIVE IN 15.0
        #  "hr_commission",
        #  "sale_commission",
        # "purchase_delivery_split_date",
        # "purchase_location_by_line",
        # DROP IN 12
        # "sale_order_dates",
        ## "stock_picking_invoice_link",
    ],
    "description": """
    This module adds basic adjustments and dependencies for Durpro.
    """,
    "demo": [],
    'data': [
        'security/ir.model.access.csv',
        # CHANGE THE CRON TIME WHEN IT GONNA EXIST
        # 'data/cron.xml',
        'data/groups.xml',
        # REMOVE IN 13.0 CAUSE SOME FIELDS DO NOT EXIST
        # 'data/parameters.xml',
        # Issue with credit field missing
        # BV: WTF an other Jquery inject
        # 'views/assets.xml',
        'views/hr_expense_view.xml',
        # DJD: Not required as BOM cost calculation behaviour native in v15
        # 'views/mrp_view.xml',
        'views/payment_view.xml',
        'views/product_view.xml',
        'views/stock_view.xml',
        'views/res_company.xml',
        'wizard/inventory_valuation.xml',
        # DJD: Not required as BOM cost calculation behaviour native in v15
        # 'wizard/mrp_product_produce.xml',
        'wizard/pricelist_import.xml',
    ],
    'test': [],
    'installable': True,
    'active': False
}
