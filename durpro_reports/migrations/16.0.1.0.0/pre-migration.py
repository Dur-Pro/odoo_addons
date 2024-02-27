def migrate(cr, version):
    cr.execute("""
    WITH reports_views as (SELECT res_id FROM ir_model_data WHERE model='ir.ui.view' and module='durpro_reports')
    DELETE FROM ir_ui_view WHERE id in (select * from reports_views) OR inherit_id in (select * from reports_views)
    """)