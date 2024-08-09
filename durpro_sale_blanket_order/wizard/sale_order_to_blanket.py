from odoo import models, fields, api, _, Command
from odoo.exceptions import UserError


class SaleOrderToBlanketWizard(models.TransientModel):
    _name = "sale.to.blanket.wizard"
    _description = "Sale Order to Blanket Wizard"

    validity_date = fields.Date()
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
    )
    sale_order_action = fields.Selection(
        selection=[
            ("cancel", "Cancel Sales Order"),
            ("link", "Link to Blanket"),
            ("nothing", "Do Nothing"),
        ],
        default="cancel",
    )

    def action_create_blanket(self):
        blanket_order = self.env["sale.blanket.order"].create(
            {
                "partner_id": self.sale_order_id.partner_id.id,
                "pricelist_id": self.sale_order_id.pricelist_id.id,
                "currency_id": self.sale_order_id.currency_id.id,
                "analytic_account_id": self.sale_order_id.analytic_account_id.id,
                "payment_term_id": self.sale_order_id.payment_term_id.id,
                "company_id": self.sale_order_id.company_id.id,
                "validity_date": self.validity_date,
                "purpose": self.sale_order_id.purpose,
                "user_id": self.sale_order_id.user_id.id,
                "client_order_ref": self.sale_order_id.client_order_ref,
                "incoterms_id": self.sale_order_id.incoterm.id,
                "warehouse_id": self.sale_order_id.warehouse_id.id,
            }
        )
        if self.sale_order_id.order_line:
            self.env["sale.blanket.order.line"].create(
                [
                    {
                        "name": line.name,
                        "sequence": line.sequence,
                        "order_id": blanket_order.id,
                        "product_id": line.product_id.id,
                        "product_uom": line.product_uom.id,
                        "price_unit": line.price_unit,
                        "taxes_id": [Command.set(line.tax_id.ids)],
                        "original_uom_qty": line.product_uom_qty,
                        "display_type": line.display_type,
                        "sale_lines": (
                            [Command.set(line.ids)]
                            if self.sale_order_action == "link"
                            else False
                        ),
                    }
                    for line in self.sale_order_id.order_line
                ]
            )
        if self.sale_order_action == "cancel":
            self.sale_order_id._action_cancel()
        blanket_order.message_post(
            body=_(
                "<p>Blanket created from sales order %s</p>"
                % self.sale_order_id._get_html_link()
            ),
            body_is_html=True,
        )
        self.sale_order_id.message_post(
            body=_(
                "<p>Created new %s from this order.</p>"
                % blanket_order._get_html_link("Blanket Order")
            ),
            body_is_html=True,
        )
        return {
            "name": _("Blanket Order"),
            "type": "ir.actions.act_window",
            "res_model": "sale.blanket.order",
            "res_id": blanket_order.id,
            "view_mode": "form",
            "target": "current",
        }
