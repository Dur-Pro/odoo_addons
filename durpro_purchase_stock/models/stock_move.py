from odoo import models, fields, api, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    purchase_order = fields.Many2one(
        comodel_name='purchase.order',
        string='Purchase Order',
        help="Purchase order for this move line"
    )
