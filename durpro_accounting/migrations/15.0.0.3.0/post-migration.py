from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """ Uninstall the durpro_15_16_accounting_fix module after running it"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.module.module'].search(
        [('name', '=', 'durpro_15_16_accounting_fix')]
    ).button_immediate_uninstall()

