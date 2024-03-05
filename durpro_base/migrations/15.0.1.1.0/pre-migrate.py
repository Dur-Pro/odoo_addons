from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    cr.execute("DELETE from ir_model_fields WHERE name='loc_case'")

    env = api.Environment(cr, SUPERUSER_ID, {})

    to_install = env['ir.module.module'].search(
        [('name', 'in', ('durpro_stock', 'durpro_sale_stock', 'durpro_purchase_stock'))])
    to_uninstall = env['ir.module.module'].search([
        ('name', 'in', ('logistics_extra_info', 'durpro_bin_conversions')),
        ('state', '=', 'installed')
    ])
    if to_install:
        to_install.button_install()
    if to_uninstall:
        to_uninstall.button_uninstall()
