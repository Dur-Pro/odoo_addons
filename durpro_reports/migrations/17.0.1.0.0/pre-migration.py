
def migrate(cr, version):
    queries = [
        "delete from ir_ui_view where inherit_id in (select res_id from ir_model_data where module='durpro_reports' and model='ir.ui.view');",
        "delete from ir_ui_view where id in (select res_id from ir_model_data where module='durpro_reports' and model='ir.ui.view');",
        "delete from ir_ui_view where inherit_id in (select res_id from ir_model_data where model='ir.ui.view' and module='sale_blanket_order');",
        "delete from ir_ui_view where id in (select res_id from ir_model_data where model='ir.ui.view' and module='sale_blanket_order');",
    ]
    for query in queries:
        cr.execute(query)
