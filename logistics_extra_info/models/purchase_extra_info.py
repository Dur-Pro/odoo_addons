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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    carrier = fields.Char(string='Carrier NAME DURPRO', size=64, tracking=True)
    carrier_account = fields.Char(string='Carrier Account', size=64, tracking=True)
    customs_broker = fields.Char(string='Customs Broker', size=64, tracking=True)
    po_conf_number = fields.Char(string='Purchase Order Confirmation', size=64, tracking=True)
    # po_conf_date = fields.Date(string='Estimated Ship Date', help="Promised date on supplier order confirmation.")

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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
