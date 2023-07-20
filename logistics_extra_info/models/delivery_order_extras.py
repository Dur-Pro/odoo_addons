# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _calculate_note(self):
        return self.sale_id.note if self.sale_id else ""

    package_type = fields.Char(string='Package type', size=32)
    net_weight = fields.Float(string='Net Weight', digits=(12, 1),
                              help="Net weight in lbs.")
    shipper = fields.Many2one('res.partner', 'Shipper',
                              help="The person who prepared the shipment.")
    verifier = fields.Many2one('res.partner', 'Verifier',
                               help="The person who verified the shipment.")
    carrier = fields.Char(string='Carrier (OLD)', size=64)
    carrier_account = fields.Char(string='Carrier Account (OLD)', size=64)
    printed = fields.Boolean(string='Printed',
                             help="Indicates whether this picking has been printed already.")
    shipping_cost = fields.Float(string='Shipping Cost (OLD)', digits=(7, 2),
                                 help="Total cost of this shipment in Canadian Dollars")
    promised_date = fields.Date(string='Promised Date',
                                help="Delivery date initially promised to the client.")
    expected_date = fields.Date(string='Expected Ship Date',
                                help="Expected delivery date based on promised dates from suppliers.")
    client_order_ref = fields.Char(related='sale_id.client_order_ref', string="Customer Reference", copy=False)

    note = fields.Html(string='Notes', default=_calculate_note)

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


class StockMove(models.Model):
    _inherit = 'stock.move'

    purchase_order = fields.Many2one('purchase.order', 'Purchase Order',
                                     help="Purchase order for this move line")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
