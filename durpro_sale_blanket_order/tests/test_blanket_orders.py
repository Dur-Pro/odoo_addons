import odoo.addons.sale_blanket_order.tests.test_blanket_orders as base_tests
from odoo.tests import Form
from odoo import fields


class TestSaleBlanketOrders(base_tests.TestSaleBlanketOrders):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_order_note = "Some fancy note"
        cls.incoterms = cls.env.ref("account.incoterm_EXW")
        cls.blanket_client_order_ref = "ABC123"

    def test_extra_fields_carry_to_sale_order(self):
        """We create a blanket order and create one sale orders, to make sure that
        our newly added incoterms field transfers along with the customer reference and
        blanket order notes."""
        with Form(self.blanket_order_obj) as blanket_order:
            blanket_order.partner_id = self.partner
            blanket_order.validity_date = fields.Date.to_string(self.tomorrow)
            blanket_order.payment_term_id = self.payment_term
            blanket_order.pricelist_id = self.sale_pricelist
            blanket_order.incoterms_id = self.incoterms
            blanket_order.note = self.blanket_order_note
            blanket_order.client_order_ref = self.blanket_client_order_ref
            with blanket_order.line_ids.new() as line:
                line.product_id = self.product
                line.original_uom_qty = 20.0
                line.price_unit = 30.0

        blanket_order = blanket_order.record
        blanket_order.sudo().action_confirm()

        wizard = self.blanket_order_wiz_obj.with_context(
            active_id=blanket_order.id, active_model="sale.blanket.order"
        ).create({})
        wizard.line_ids[0].qty = 10.0
        wizard.create_sale_order()

        order = blanket_order._get_sale_orders()
        self.assertEqual(order.incoterm, self.incoterms)
        # Conversion to HTML field on sale order requires wrapping with paragraph
        self.assertEqual(
            order.note,
            f"<p>{self.blanket_order_note}</p>",
        )
        self.assertEqual(order.client_order_ref, self.blanket_client_order_ref)
