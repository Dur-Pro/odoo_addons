from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purpose = fields.Char(string="Purpose", help="What is this sale order for?")
    client_order_ref = fields.Char(string="Client PO #", tracking=True)

    # Override to allow editing
    date_order = fields.Datetime(
        string='Order Date',
        required=True,
        readonly=True,
        index=True,
        copy=False,
        default=fields.Datetime.now,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders."
    )

    @api.model
    def delete_rule(self):
        if self.env.ref('sale.menu_sale_quotations', raise_if_not_found=False):
            self.env.ref('sale.menu_sale_quotations').unlink()
        if self.env.ref('sale.menu_sale_order', raise_if_not_found=False):
            self.env.ref('sale.menu_sale_order').unlink()

    def action_confirm(self):
        ref_required = self.env['ir.config_parameter'].sudo().get_param(
            'durpro_sale.require_sale_reference',
            False
        )
        if ref_required and not self.client_order_ref:
            raise ValidationError(_("Customer reference (PO number) is required to confirm an order."))
        else:
            return super(SaleOrder, self).action_confirm()
