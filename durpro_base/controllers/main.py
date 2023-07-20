from odoo.addons.web.controllers import main


# LIBEO : Activate raw_data mode on CSVExport so negative values don't have an extra quote
# See : https://github.com/odoo/odoo/issues/18798
class CSVExport(main.CSVExport):
    raw_data = True
