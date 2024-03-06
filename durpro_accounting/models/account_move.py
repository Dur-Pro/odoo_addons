from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_total_in_currency = fields.Monetary(
        string='Total in Currency',
        store=False,
        readonly=True,
        compute='_compute_amount_total_in_currency',
        currency_field='currency_id'
    )
    def _compute_amount_total_in_currency(self):
        for move in self:
            move.amount_total_in_currency = abs(move.amount_total_in_currency_signed)

