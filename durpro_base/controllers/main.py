from odoo.addons.web.controllers.export import CSVExport

# LIBEO : Activate raw_data mode on CSVExport so negative values don't have an extra quote
# See : https://github.com/odoo/odoo/issues/18798
class CSVExport(CSVExport):
    raw_data = True