from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_order_line_description = fields.Text(related='sale_line_id.name', string='Sale description')
