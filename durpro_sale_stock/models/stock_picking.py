from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _calculate_note(self):
        return self.sale_id.note if self.sale_id else ""

    client_order_ref = fields.Char(
        related='sale_id.client_order_ref',
        string="Customer Reference",
        copy=False
    )

    note = fields.Html(
        string='Notes',
        default=_calculate_note
    )

    # this replace SaleOrderLine._action_launch_stock_rule solution because picking are not allways created
    # before it got called, moving it to the creation of picking should fix it
    @api.model
    def create(self, vals):
        picking = super(StockPicking, self).create(vals)

        if 'origin' in vals:
            sale_order = self.env['sale.order'].search([('name', '=', vals['origin'])], limit=1)
            if sale_order:
                picking.write({
                    'carrier': sale_order.carrier,
                    'carrier_account': sale_order.carrier_account,
                    'note': sale_order.note,
                })
        return picking

