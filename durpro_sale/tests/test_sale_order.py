from odoo.tests import TransactionCase, Form
from odoo.exceptions import ValidationError


class TestSaleOrder(TransactionCase):
    def _create_sale_order(self, partner=None):
        return self.env['sale.order'].create({
            'partner_id': partner or self._create_partner().id,
        })

    def _create_partner(self, name='Test Partner', street='123 ABC Street', street2='', city='Example Town',
                        state=None, country=None):
        return self.env['res.partner'].create({
            'name': name or 'Test Partner',
            'street': street,
            'street2': street2,
            'city': city,
            'state_id': state and state.id or self.env.ref('base.state_ca_qc').id,
            'country_id': country and country.id or self.env.ref('base.ca').id,
        })

    def _create_sale_order_line(self, sale_order, product=None):
        return self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': product and product.id or self._create_product().id,
        })

    def _create_product(self, name='Test Product', type='consu', standard_price=1.0):
        return self.env['product.product'].create({
            'name': name,
            'type': type,
            'standard_price': standard_price,
        })

    def test_sale_order_can_be_confirmed_without_ref_by_default(self):
        so = self._create_sale_order()
        sol = self._create_sale_order_line(so)

        settings = self.env['res.config.settings'].create({})
        self.assertFalse(settings.require_sale_reference)

        so.action_confirm()  # Shouldn't get a user error here

        self.assertIn(so.state, ['sale', 'done'])

    def test_sale_order_cannot_be_confirmed_without_ref_when_setting_enabled(self):
        self.env['ir.config_parameter'].sudo().set_param('durpro_sale.require_sale_reference', True)
        so = self._create_sale_order()
        self._create_sale_order_line(so)
        with self.assertRaises(ValidationError):
            so.action_confirm()

    def test_sale_order_can_be_confirmed_with_ref_when_setting_enabled(self):
        so = self._create_sale_order()
        sol = self._create_sale_order_line(so)
        settings_form = Form(self.env['res.config.settings'])
        settings_form.require_sale_reference = True
        settings_form.save()
        so.client_order_ref = "Test PO"

        so.action_confirm()

        self.assertIn(so.state, ['sale', 'done'])
