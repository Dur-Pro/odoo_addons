from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_amount(self):
        super()._compute_amount()
        for move in self:
            if move.move_type == 'entry' or move.is_outbound():
                move.amount_residual_signed = move.amount_residual
            else:
                move.amount_residual_signed = -move.amount_residual
