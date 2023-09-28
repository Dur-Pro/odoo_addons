from odoo import models, fields, _, api, Command
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class BinConversion(models.Model):
    _name = 'product.bin.conversion'
    _description = 'Conversion from Bin to Stock Location'

    target_location_path = fields.Char('Location to Use')
    loc_case = fields.Char('Product Bin', readonly=True)
    location_id = fields.Many2one(comodel_name='stock.location', string="Created Location")
    putaway_rules = fields.Many2many(comodel_name='stock.putaway.rule', string="Created Putaway Rule")

    # Actions
    @api.model
    def action_update_values(self):
        self._create_new_locations()
        self._delete_obsolete_locations()

    @api.model
    def action_create_locations(self):
        warehouse_location = self.env['stock.warehouse'].browse(1).view_location_id
        conversions_to_update = self.env['product.bin.conversion'].search([('location_id', '=', False)])
        for rec in conversions_to_update:
            rec.location_id = rec._create_location(warehouse_location)

    @api.model
    def action_create_putaway_rules(self):
        warehouse_location = self.env['stock.warehouse'].browse(1).view_location_id
        recs = self.env['product.bin.conversion'].search([('location_id', '!=', warehouse_location.id),
                                                          ('putaway_rules', '=', False)])
        for rec in recs:
            rec._create_putaway_rules(warehouse_location)

    @api.model
    def action_apply_rules_to_available_stock(self):
        warehouse_location = self.env['stock.warehouse'].browse(1).view_location_id
        # Update existing move lines to pull from the new locations
        sql = """UPDATE stock_move_line 
                 SET location_id=COALESCE((
                    SELECT location_out_id 
                    FROM stock_putaway_rule 
                    WHERE location_in_id=stock_move_line.location_id 
                          AND product_id=stock_move_line.product_id), stock_move_line.location_id)
                 WHERE state not in ('done', 'cancel') AND location_id=%s"""
        self.env.cr.execute(sql, [warehouse_location.id])
        # Update the existing quants to point to the new locations
        sql = """UPDATE stock_quant
                 SET location_id=COALESCE((
                    SELECT location_out_id 
                    FROM stock_putaway_rule 
                    WHERE location_in_id=stock_quant.location_id 
                          AND product_id=stock_quant.product_id), stock_quant.location_id)
                 WHERE quantity > 0 AND location_id=%s"""
        self.env.cr.execute(sql, [warehouse_location.id])

    # Helper methods

    def _create_putaway_rules(self, location_in):
        products = self.env['product.product'].search(
            [('product_tmpl_id.loc_case', '=', self.loc_case), ('company_id', '=', 1)])
        vals = [{
            'location_in_id': location_in.id,
            'product_id': product.id,
            'location_out_id': self.location_id.id,
            'company_id': 1,
        } for product in products]
        self.putaway_rules = self.env['stock.putaway.rule'].create(vals)


    @api.model
    def _create_new_locations(self):
        new_bins_sql = """SELECT distinct loc_case 
                      FROM product_template
                      WHERE loc_case NOT IN (SELECT DISTINCT loc_case FROM product_bin_conversion)"""
        self.env.cr.execute(new_bins_sql)
        new_bins = [row['loc_case'] for row in self.env.cr.dictfetchall()]
        vals = []
        for loc_case in new_bins:
            path = self._convert_bin_to_location(loc_case)
            vals.append({'loc_case': loc_case, 'target_location_path': path})
        self.create(vals)

    @api.model
    def _convert_bin_to_location(self, loc_case: str) -> str:
        warehouse_prefix = self.env['stock.warehouse'].browse(1).view_location_id.complete_name
        suffix = loc_case and "/" + loc_case.replace("-", "/") or ""
        return warehouse_prefix + suffix

    @api.model
    def _delete_obsolete_locations(self):
        sql = """DELETE FROM product_bin_conversion
                 WHERE loc_case NOT IN (SELECT DISTINCT loc_case FROM product_template)"""
        self.env.cr.execute(sql)
        self.invalidate_cache()

    def _create_location(self, warehouse_location):
        path = self.target_location_path.replace(warehouse_location.complete_name, "").strip("/")
        parent_location = warehouse_location
        if path:
            for loc_name in path.split("/"):
                loc = self.env['stock.location'].search(
                    [('name', '=', loc_name), ('location_id', '=', parent_location.id)])
                if not loc:
                    loc = self.env['stock.location'].create({
                        'name': loc_name,
                        'location_id': parent_location.id,
                        'company_id': 1,
                        'usage': 'internal',
                    })
                parent_location = loc
        return parent_location
