{
    "name": "Durpro fso",
    "version": "0.4",
    "author": "Libéo & Benoît Vézina",
    "license": "AGPL-3",
    "category": "Durpro",
    "depends": [
        'sale_stock',
    ],
    "description": """
        Extension Field Service Operations
    """,
    "demo": [],
    "data": [
        "data/work_order_stage_data.xml",
        "security/ir.model.access.csv",
        "views/sale_order.xml",
        # "views/work_order.xml",
        "views/intervention.xml",
        # "views/equipment.xml",
        # "views/equipment_location.xml",
        # "views/task.xml",
        # "views/menu.xml",
        # "views/res_config.xml",
        # "views/res_partner.xml",
        "report/sale_report_templates.xml",
        "report/work_order_report_templates.xml",
        "wizard/exception_wizard_view.xml",
        "wizard/intervention_wizard_view.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "/durpro_fso/static/src/scss/durpro_fso.scss",
        ],
    },
    "installable": True,
    "application": True,
}
