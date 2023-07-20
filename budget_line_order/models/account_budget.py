from odoo import api, models, fields

class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    _order = "sequence, id asc"

    sequence = fields.Integer(string='Sequence', default=10)
