from odoo import models, fields, api, _

from odoo.addons.stock_dropshipping.models import sale

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sequence_no = fields.Integer(
        string="#",
        compute="_compute_sequence_no",
        inverse="_inverse_sequence_no",
    )

    @api.depends('sequence')
    def _compute_sequence_no(self):
        for rec in self:
            rec.sequence_no = rec.sequence

    def _inverse_sequence_no(self):
        for rec in self:
            rec.sequence = rec.sequence_no

    def _get_qty_procurement(self, previous_product_uom_qty):
        # Overwrite the version from stock_dropshipping to overcome a bug where it assumes an SO line is a drop ship
        # just because it has a related RFQ. This comes up specifically with the app rfq_from_quotation.
        # The original method in stock_dropshipping returns the quantity of PO lines as positive
        purchase_lines_sudo = self.sudo().purchase_line_ids
        is_dropship = all([r.order_id.default_location_dest_id_usage == 'customer' for r in purchase_lines_sudo])
        if is_dropship and purchase_lines_sudo.filtered(lambda r: r.state != 'cancel'):
            qty = 0.0
            for po_line in purchase_lines_sudo.filtered(lambda r: r.state != 'cancel'):
                qty += po_line.product_uom._compute_quantity(po_line.product_qty, self.product_uom, rounding_method='HALF-UP')
            return qty
        else:
            return super(sale.SaleOrderLine, self)._get_qty_procurement(previous_product_uom_qty=previous_product_uom_qty)

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        recs.order_id.update_sequence_nos()
        return recs