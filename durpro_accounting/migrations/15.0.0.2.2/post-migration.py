from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, dict())
    merge_account_types(env, env.ref('durpro_accounting.account_type_income_tax'))
    merge_account_types(env, env.ref('durpro_accounting.account_type_capital'))


def merge_account_types(env, new_account_type):
    old_types = env['account.account.type'].search(
        [('name', '=', new_account_type.name), ('id', '!=', new_account_type.id)])
    if old_types:
        accounts = env['account.account'].search([('user_type_id', 'in', old_types.ids)])
        accounts.user_type_id = new_account_type
        old_types.unlink()
