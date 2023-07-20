# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_assign(self):
        # Modification of the original to check availability to break the mto chains if stock has been added
        # or unreserved
        super()._action_assign()
        for move in self.filtered(lambda r: r.state in ('partially_available', 'waiting', 'confirmed')):
            rounding = move.product_uom.rounding
            available = 0.0
            if move.product_id:
                available = self.env['stock.quant']._get_available_quantity(move.product_id, move.location_id)
            missing_reserved_uom_quantity = move.product_uom_qty - move.reserved_availability
            need = move.product_uom._compute_quantity(missing_reserved_uom_quantity,
                                                      move.product_id.uom_id, rounding_method='HALF-UP')
            if available and need:
                taken_quantity = move._update_reserved_quantity(need, available, move.location_id)
                comp = float_compare(taken_quantity, need, precision_rounding=rounding)
                if comp == 0:
                    move.state = 'assigned'
                elif comp < 0:
                    move.state = 'partially_available'
