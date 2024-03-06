from odoo import api, models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    carrier = fields.Char(string='Carrier NAME DURPRO', size=64, tracking=True)
    carrier_account = fields.Char(string='Carrier Account', size=64, tracking=True)
    customs_broker = fields.Char(string='Customs Broker', size=64, tracking=True)
    po_conf_number = fields.Char(string='Purchase Order Confirmation', size=64, tracking=True)

    def _create_picking(self):
        result = super()._create_picking()
        for order in self:
            for picking in order.picking_ids:
                picking.write({
                    'carrier': order.carrier,
                    'carrier_account': order.carrier_account,
                    'note': order.notes,
                })
        return result
