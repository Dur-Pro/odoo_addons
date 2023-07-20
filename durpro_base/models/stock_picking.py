from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    has_empty_loc_cases = fields.Boolean('Has Empty Bin Locations?', compute='_compute_has_empty_loc_cases')
    items_summary = fields.Char("Items Summary", compute="_compute_items_summary")

    @api.depends('move_lines.loc_case')
    def _compute_has_empty_loc_cases(self):
        for rec in self:
            rec.has_empty_loc_cases = bool(rec.move_lines.filtered(lambda l: not l.loc_case))

    @api.depends('move_lines')
    def _compute_items_summary(self):
        for rec in self:
            rec.items_summary = ""
            for index, line in enumerate(rec.move_lines):
                rec.items_summary += str(round(line.product_qty)) + "x " + (line.product_id.default_code or "")
                if index < len(rec.move_lines) - 1:
                    rec.items_summary += ", "
                if index > 4:
                    rec.items_summary += " ..."
                    return
