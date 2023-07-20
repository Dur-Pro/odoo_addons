from odoo import api, models, fields


class Product(models.Model):
    _inherit = "product.product"

    pending_incoming = fields.Float("Pending incoming",
                                    compute="_compute_forecasted_with_pending",
                                    digits="Product Unit of Measure",
                                    compute_sudo=False,
                                    help="Incoming quantity on RFQs and any other draft moves."
                                    )
    pending_outgoing = fields.Float("Pending outgoing",
                                    compute="_compute_forecasted_with_pending",
                                    digits="Product Unit of Measure",
                                    compute_sudo=False,
                                    help="Outgoing quantity on quotes and any other draft moves."
                                    )
    virtual_available_with_pending = fields.Float(
        "Forecasted With Pending",
        compute="_compute_forecasted_with_pending",
        digits="Product Unit of Measure",
        compute_sudo=False,
        help="Forecast quantity including pending moves (RFQs, quotes, etc.)"
    )

    @api.depends("qty_available")
    def _compute_forecasted_with_pending(self):
        if self.env.context.get('warehouse'):
            warehouse = self.env['stock.warehouse'].browse(self.env.context.get('warehouse'))
        else:
            warehouse = self.env['stock.warehouse'].browse(self.get_warehouses()[0]['id'])
        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
            [('id', 'child_of', warehouse.view_location_id.id)],
            ['id'],
        )]
        in_domain, out_domain = self._move_draft_domain(wh_location_ids)
        incoming_moves = self.env['stock.move'].read_group(in_domain, ['product_qty:sum'], 'product_id')
        incoming_quantities = {move['product_id']: move['product_qty'] for move in incoming_moves}
        outgoing_moves = self.env['stock.move'].read_group(out_domain, ['product_qty:sum'], 'product_id')
        outgoing_quantities = {move['product_id']: move['product_qty'] for move in outgoing_moves}
        for product in self:
            in_sum = incoming_quantities[product.id] if product.id in incoming_quantities else 0
            out_sum = outgoing_quantities[product.id] if product.id in outgoing_quantities else 0
            product.pending_incoming = in_sum
            product.pending_outgoing = out_sum
            product.virtual_available_with_pending = product.qty_available + in_sum - out_sum

    def _product_domain(self):
        if self._name == 'product.template':
            return [('product_tmpl_id', 'in', self.ids)]
        else:
            return [('product_id', 'in', self.ids)]

    def _move_domain(self, wh_location_ids):
        move_domain = self._product_domain()
        move_domain += [('product_uom_qty', '!=', 0)]
        out_domain = move_domain + [
            '&',
            ('location_id', 'in', wh_location_ids),
            ('location_dest_id', 'not in', wh_location_ids),
        ]
        in_domain = move_domain + [
            '&',
            ('location_id', 'not in', wh_location_ids),
            ('location_dest_id', 'in', wh_location_ids),
        ]
        return in_domain, out_domain

    def _move_draft_domain(self, wh_location_ids):
        in_domain, out_domain = self._move_domain(wh_location_ids)
        in_domain += [('state', '=', 'draft')]
        out_domain += [('state', '=', 'draft')]
        return in_domain, out_domain

    def get_warehouses(self):
        return self.env['stock.warehouse'].search_read(fields=['id', 'name', 'code'])

