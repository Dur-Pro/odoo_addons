from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero
from odoo.addons.stock.models.stock_move_line import StockMoveLine as ParentStockMoveLine


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sale_order_line_description = fields.Text(related='move_id.sale_order_line_description')
