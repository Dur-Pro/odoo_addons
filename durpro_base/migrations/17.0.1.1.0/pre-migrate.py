def migrate(cr, version):
    modules_to_uninstall = [
        'account_payment_term_discount',
        'amount_residual_signed_fix',
        'bemade_multiple_billing_contacts',
        'bemade_odoo_partner_scrapper',
        'bemade_odoo_partner_scrapper_js_only',
        'bemade_open_project_details',
        'bemade_user_custom_apps_order',
        'crm_phonecall',
        'database_cleanup_test',
        'discuss_search_view_cr',
        'document_knowledge',
        'document_page',
        'durpro_extended',
        'durpro_fso',
        'hr_attendance_fix',
        'mail_attach_existing_attachment',
        'mail_show_follower',
        'menu_sequence_per_user',
        'mrp_production_serial_matrix',
        'owncloud_odoo',
        'project_duplicate_subtask',
        'project_task_default_stage',
        'prt_mail_messages',
        'purchase_delivery_split_date',
        'purchase_location_by_line',
        'zb_alias_name',
    ]

    sql = f"""
    UPDATE ir_module_module
    SET state='to remove'
    WHERE name in ({modules_to_uninstall}) and state='installed'
    """

    cr.execute(sql)
