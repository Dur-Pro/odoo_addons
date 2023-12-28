from odoo import api, SUPERUSER_ID


def migrate(env, version):
    """ Uninstall the durpro_15_16_accounting_fix module after running it"""
    env['ir.module.module'].search(
        [('name', '=', 'durpro_15_16_accounting_fix')]
    ).button_immediate_uninstall()

