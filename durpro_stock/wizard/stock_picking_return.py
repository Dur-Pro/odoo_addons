from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        return_moves = res.get('product_return_moves', False)
        if return_moves:
            # return_moves is structured as [int, int, data : Dict] where data can have key to_refund
            for move in return_moves:
                move[2].update("to_refund", True)
        return res
