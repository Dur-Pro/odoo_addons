from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero
from odoo.addons.stock.models.stock_move_line import StockMoveLine as ParentStockMoveLine


class StockMove(models.Model):
    _inherit = "stock.move"

    loc_case = fields.Char(related='product_id.loc_case')
    sale_order_line_description = fields.Text(related='sale_line_id.name', string='Sale description')
