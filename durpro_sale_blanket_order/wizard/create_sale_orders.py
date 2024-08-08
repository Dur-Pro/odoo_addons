from odoo import models, Command


class BlanketOrderWizard(models.TransientModel):
    _inherit = "sale.blanket.order.wizard"

    def _prepare_so_vals(
        self,
        customer,
        user_id,
        currency_id,
        pricelist_id,
        payment_term_id,
        order_lines_by_customer,
    ):
        vals = super()._prepare_so_vals(
            customer,
            user_id,
            currency_id,
            pricelist_id,
            payment_term_id,
            order_lines_by_customer,
        )
        vals.update(
            incoterm=self.blanket_order_id.incoterms_id.id,
            note=self.blanket_order_id.note,
            client_order_ref=self.blanket_order_id.client_order_ref,
            tag_ids=[Command.set(self.blanket_order_id.tag_ids.ids)],
            purpose=self.blanket_order_id.purpose,
        )
        if self.blanket_order_id.warehouse_id:
            vals.update(warehouse_id=self.blanket_order_id.warehouse_id.id)
        return vals
