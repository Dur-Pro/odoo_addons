from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "blanket_order_line")
    def _compute_name(self):
        """Override to grab the name from the blanket order line if there is one."""
        for line in self:
            if line.blanket_order_line:
                line.name = line.blanket_order_line.name
            else:
                super(SaleOrderLine, line)._compute_name()
