from openupgradelib import openupgrade
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """ Install the durpro_15_16_accounting_fix module within a module
    upgrade so that Odoo.sh will not have a time limit for it. """

    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.module.module'].search(
        [('name', '=', 'durpro_15_16_accounting_fix')]
    ).button_immediate_install()

