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

from odoo import api, models, fields
import time


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    carrier = fields.Char(string='Carrier', size=64)
    carrier_account = fields.Char(string='Carrier Account', size=64)


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     def _action_launch_stock_rule(self, previous_product_uom_qty=False):
#         res = super(SaleOrderLine, self)._action_launch_stock_rule(previous_product_uom_qty)
#         print("action---------------------")
#         for order in self.mapped('order_id'):
#             print(order)
#             print(order.picking_ids)
#             print(order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel')))
#             for pick in order.picking_ids:
#                 print(pick.name)
#                 print(pick.state)
#             for picking in order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel')):
#                 print(picking)
#                 picking.write({
#                     'carrier': order.carrier,
#                     'carrier_account': order.carrier_account,
#                     'note': order.note,
#                 })
#                 print(picking)
#         return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
