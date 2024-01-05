from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.module.module'].search([('name', '=', 'sale')]).button_immediate_upgrade()
