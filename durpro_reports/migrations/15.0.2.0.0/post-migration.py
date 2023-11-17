from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    _logger.info("Running pre-migration script for durpro_reports 15.0.2.0.0")
    env = api.Environment(cr, SUPERUSER_ID, dict())
    module = env['ir.module.module'].search([('name','=','dev_invoice_multi_payment')])
    if module and module.state == 'installed':
        _logger.info("Uninstalling dev_multiple_invoice_payment in durpro_reports post_init_hook.")
        module.button_uninstall()

