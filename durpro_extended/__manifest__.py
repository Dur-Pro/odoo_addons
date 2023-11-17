{
    "name": "Durpro Extended",
    "version": "0.1",
    "author": "Benoît Vézina",
    "category": "Durpro",
    "license": "Other proprietary",
    "depends": [
        'durpro_base',
        'durpro_helpdesk_fso',
        'le_website_faq_page',
        'mass_mailing',
        # 'shipstation_shipping_odoo_integration',
        # 'social',
        # 'website_blog',
        # 'website_forum',
        'website_hr_recruitment',
        'website_sale',
        'website_slides',
        "durpro_purchase",
    ],
    "description": """
        Extended Durpro made in house, main goal is to let Durpro add his own modification in Libeo environnement with the less huddle
    """,
    "demo": [],
    "data": [
        "views/menu.xml",
    ],
    "installable": True,
    "application": True,
}
