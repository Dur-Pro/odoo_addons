def migrate(cr, version):
    cr.execute("DELETE FROM ir_ui_view WHERE id in (SELECT res_id FROM ir_model_data WHERE model='ir.ui.view' and module='durpro_reports')")