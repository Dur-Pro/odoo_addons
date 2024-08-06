from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    blanket_order_count = fields.Integer(
        compute="_compute_blanket_order_count",
    )

    @api.depends("order_line.blanket_order_line")
    def _compute_blanket_order_count(self):
        for rec in self:
            rec.blanket_order_count = len(rec.order_line.blanket_order_line)

    def _get_blanket_orders(self):
        return self.order_line.blanket_order_line.order_id

    def action_view_blanket_orders(self):
        blanket_orders = self._get_blanket_orders()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_blanket_order.act_open_blanket_order_view"
        )
        action["domain"] = [("id", "in", blanket_orders.ids)]
        if len(blanket_orders) == 1:
            action["res_id"] = blanket_orders.id
            action["views"] = [(False, "form"), (False, "tree")]
        return action
