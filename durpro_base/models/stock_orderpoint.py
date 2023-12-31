import logging
from collections import defaultdict
from datetime import datetime, time
from dateutil import relativedelta
from itertools import groupby
from psycopg2 import OperationalError

from odoo import SUPERUSER_ID, _, api, fields, models, registry
from odoo.addons.stock.models.stock_rule import ProcurementException
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import add, float_compare, frozendict, split_every


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    def action_open_orderpoints(self):
        return self._get_orderpoint_action()

    def _get_orderpoint_action(self):
        """Create manual orderpoints for missing product in each warehouses. It also removes
        orderpoints that have been replenish. In order to do it:
        - It uses the report.stock.quantity to find missing quantity per product/warehouse, ignoring archived warehouses
        - It checks if orderpoint already exist to refill this location.
        - It checks if it exists other sources (e.g RFQ) tha refill the warehouse.
        - It creates the orderpoints for missing quantity that were not refill by an upper option.

        return replenish report ir.actions.act_window
        """
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_orderpoint_replenish")
        action['context'] = self.env.context
        # Search also with archived ones to avoid to trigger product_location_check SQL constraints later
        # It means that when there will be a archived orderpoint on a location + product, the replenishment
        # report won't take in account this location + product and it won't create any manual orderpoint
        # In master: the active field should be remove
        orderpoints = self.env['stock.warehouse.orderpoint'].with_context(active_test=False).search([])
        # Remove previous automatically created orderpoint that has been refilled.
        orderpoints_removed = orderpoints._unlink_processed_orderpoints()
        orderpoints = orderpoints - orderpoints_removed
        to_refill = defaultdict(float)
        all_product_ids = []
        all_warehouse_ids = []
        # Take 3 months since it's the max for the forecast report
        to_date = add(fields.date.today(), months=3)
        qty_by_product_warehouse = self.env['report.stock.quantity'].read_group(
            [('date', '=', to_date), ('state', '=', 'forecast'), ('warehouse_id.active', '=', True)],
            ['product_id', 'product_qty', 'warehouse_id'],
            ['product_id', 'warehouse_id'], lazy=False)
        for group in qty_by_product_warehouse:
            warehouse_id = group.get('warehouse_id') and group['warehouse_id'][0]
            if group['product_qty'] >= 0.0 or not warehouse_id:
                continue
            all_product_ids.append(group['product_id'][0])
            all_warehouse_ids.append(warehouse_id)
            to_refill[(group['product_id'][0], warehouse_id)] = group['product_qty']
        if not to_refill:
            return action

        # Recompute the forecasted quantity for missing product today but at this time
        # with their real lead days.
        key_to_remove = []
        pwh_per_day = defaultdict(list)
        for (product, warehouse) in to_refill.keys():
            product = self.env['product.product'].browse(product).with_prefetch(all_product_ids)
            warehouse = self.env['stock.warehouse'].browse(warehouse).with_prefetch(all_warehouse_ids)
            rules = product._get_rules_from_location(warehouse.lot_stock_id)
            lead_days = rules.with_context(bypass_delay_description=True)._get_lead_days(product)[0]
            pwh_per_day[(lead_days, warehouse)].append(product.id)
        # group product by lead_days and warehouse in order to read virtual_available
        # in batch
        for (days, warehouse), p_ids in pwh_per_day.items():
            products = self.env['product.product'].browse(p_ids)
            qties = products.with_context(
                warehouse=warehouse.id,
                to_date=fields.datetime.now() + relativedelta.relativedelta(days=days)
            ).read(['virtual_available'])
            for qty in qties:
                if float_compare(qty['virtual_available'], 0, precision_rounding=product.uom_id.rounding) >= 0:
                    key_to_remove.append((qty['id'], warehouse.id))
                else:
                    to_refill[(qty['id'], warehouse.id)] = qty['virtual_available']

        for key in key_to_remove:
            del to_refill[key]
        if not to_refill:
            return action

        # Remove incoming quantity from other origin than moves (e.g RFQ)
        product_ids, warehouse_ids = zip(*to_refill)
        dummy, qty_by_product_wh = self.env['product.product'].browse(product_ids)._get_quantity_in_progress(
            warehouse_ids=warehouse_ids)
        rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        # Group orderpoint by product-warehouse
        orderpoint_by_product_warehouse = self.env['stock.warehouse.orderpoint'].read_group(
            [('id', 'in', orderpoints.ids)],
            ['product_id', 'warehouse_id', 'qty_to_order:sum'],
            ['product_id', 'warehouse_id'], lazy=False)
        orderpoint_by_product_warehouse = {
            (record.get('product_id')[0], record.get('warehouse_id')[0]): record.get('qty_to_order')
            for record in orderpoint_by_product_warehouse
        }
        for (product, warehouse), product_qty in to_refill.items():
            qty_in_progress = qty_by_product_wh.get((product, warehouse)) or 0.0
            qty_in_progress += orderpoint_by_product_warehouse.get((product, warehouse), 0.0)
            # Add qty to order for other orderpoint under this warehouse.
            if not qty_in_progress:
                continue
            to_refill[(product, warehouse)] = product_qty + qty_in_progress
        to_refill = {k: v for k, v in to_refill.items() if float_compare(
            v, 0.0, precision_digits=rounding) < 0.0}

        lot_stock_id_by_warehouse = self.env['stock.warehouse'].with_context(active_test=False).search_read([
            ('id', 'in', [g[1] for g in to_refill.keys()])
        ], ['lot_stock_id'])
        lot_stock_id_by_warehouse = {w['id']: w['lot_stock_id'][0] for w in lot_stock_id_by_warehouse}

        # With archived ones to avoid `product_location_check` SQL constraints
        orderpoint_by_product_location = self.env['stock.warehouse.orderpoint'].with_context(active_test=False).read_group(
            [('id', 'in', orderpoints.ids)],
            ['product_id', 'location_id', 'ids:array_agg(id)'],
            ['product_id', 'location_id'], lazy=False)
        orderpoint_by_product_location = {
            (record.get('product_id')[0], record.get('location_id')[0]): record.get('ids')[0]
            for record in orderpoint_by_product_location
        }

        orderpoint_values_list = []
        for (product, warehouse), product_qty in to_refill.items():
            lot_stock_id = lot_stock_id_by_warehouse[warehouse]
            orderpoint_id = orderpoint_by_product_location.get((product, lot_stock_id))
            if orderpoint_id:
                self.env['stock.warehouse.orderpoint'].browse(orderpoint_id).qty_forecast += product_qty
            else:
                orderpoint_values = self.env['stock.warehouse.orderpoint']._get_orderpoint_values(product, lot_stock_id)
                orderpoint_values.update({
                    'name': _('Replenishment Report'),
                    'warehouse_id': warehouse,
                    'company_id': self.env['stock.warehouse'].browse(warehouse).company_id.id,
                })
                orderpoint_values_list.append(orderpoint_values)

        orderpoints = self.env['stock.warehouse.orderpoint'].with_user(SUPERUSER_ID).create(orderpoint_values_list)
        for orderpoint in orderpoints:
            orderpoint_wh = orderpoint.location_id.warehouse_id
            orderpoint.route_id = next(
                (r for r in orderpoint.product_id.route_ids if not r.supplied_wh_id or r.supplied_wh_id == orderpoint_wh),
                orderpoint.route_id)
            if not orderpoint.route_id:
                orderpoint._set_default_route_id()
            orderpoint.qty_multiple = orderpoint._get_qty_multiple_to_order()
        return action
