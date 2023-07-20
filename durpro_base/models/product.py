from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    loc_case = fields.Char(string='Bin Location')

    # DJD: Removing probably old code to deconflict with OCA/product_attribute/product_pricelist_supplierinfo/models/product_template.py
    #      which has equivalent, more up-to-date code that correctly handles UOM conversions.
    #
    # def _get_supplierinfo_pricelist_price(
    #         self, rule, date=None, quantity=None, product_id=None):
    #     """Method for getting the price from supplier info."""
    #     self.ensure_one()
    #     if product_id:
    #         domain = [
    #             '|',
    #             ('product_id', '=', product_id),
    #             ('product_tmpl_id', '=', self.id),
    #         ]
    #     else:
    #         domain = [
    #             ('product_tmpl_id', '=', self.id),
    #         ]
    #     if not rule.no_supplierinfo_min_quantity and quantity:
    #         domain += [
    #             '|',
    #             ('min_qty', '=', False),
    #             ('min_qty', '<=', quantity),
    #         ]
    #     if date:
    #         domain += [
    #             '|',
    #             ('date_start', '=', False),
    #             ('date_start', '<=', date),
    #             '|',
    #             ('date_end', '=', False),
    #             ('date_end', '>=', date),
    #         ]
    #     # We use a different default order because we are interested in getting
    #     # the price for lowest minimum quantity if no_supplierinfo_min_quantity
    #     if rule.no_supplierinfo_min_quantity:
    #         supplierinfos = self.env['product.supplierinfo'].search(
    #             domain, order='min_qty,sequence,price',
    #         )
    #     else:
    #         supplierinfos = self.env['product.supplierinfo'].search(
    #             domain, order='min_qty desc,sequence,price',
    #         )
    #     price = supplierinfos[:1].price
    #     if price:
    #         # We have to replicate this logic in this method as pricelist
    #         # method are atomic and we can't hack inside.
    #         # Verbatim copy of part of product.pricelist._compute_price_rule.
    #         qty_uom_id = self._context.get('uom') or self.uom_id.id
    #         price_uom = self.env['uom.uom'].browse([qty_uom_id])
    #         convert_to_price_uom = (
    #             lambda price: self.uom_id._compute_price(
    #                 price, price_uom))
    #         price_limit = price
    #         price = (price - (price * (rule.price_discount / 100))) or 0.0
    #         if rule.price_round:
    #             price = tools.float_round(
    #                 price, precision_rounding=rule.price_round)
    #         if rule.price_surcharge:
    #             price_surcharge = convert_to_price_uom(rule.price_surcharge)
    #             price += price_surcharge
    #         if rule.price_min_margin:
    #             price_min_margin = convert_to_price_uom(rule.price_min_margin)
    #             price = max(price, price_limit + price_min_margin)
    #         if rule.price_max_margin:
    #             price_max_margin = convert_to_price_uom(rule.price_max_margin)
    #             price = min(price, price_limit + price_max_margin)
    #     return price


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.onchange('name')
    def onchange_name(self):
        if self.name and self.name.property_purchase_currency_id:
            currency = self.name.property_purchase_currency_id
            self.currency_id = currency.id or self.env.user.company_id.currency_id.id
