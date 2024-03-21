from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    cr.execute("""
    DELETE from ir_ui_view WHERE 
        inherit_id IN (
            SELECT id from ir_model_data WHERE model='ir.ui.view' and module='durpro_reports'
            )
        OR
        id in (
            SELECT id from ir_model_data WHERE model='ir.ui.view' and module='durpro_reports'
            )""")