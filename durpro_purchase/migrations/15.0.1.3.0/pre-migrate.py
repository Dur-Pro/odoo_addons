from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    cr.execute("""
    UPDATE ir_model_data SET module='durpro_purchase' 
    WHERE model='res.groups' and name='group_purchase_unlock'
    """)
