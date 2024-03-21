from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    cr.execute("""
    DELETE FROM ir_ui_view where id=1040 
    """)