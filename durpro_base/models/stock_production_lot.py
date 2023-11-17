from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProductionLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def create(self, vals):
        if 'product_id' in vals or 'name' in vals:
            name = vals.get('name', None)
            product_id = vals.get('product_id', None)
            if self.env['stock.production.lot'].search_count([('name', '=', name), ('product_id', '=', product_id)]):
                product = self.env['product.product'].browse(product_id)
                raise ValidationError(
                    _('The combination of serial number and product must be unique! (Serial Number=%s Product=%s)') % (
                        name, product.display_name if product else ''
                    )
                )
        return super(ProductionLot, self).create(vals)

    def write(self, vals):
        if 'product_id' in vals or 'name' in vals:
            for rec in self:
                name = vals.get('name', rec.name)
                product_id = vals.get('product_id', rec.product_id.id)
                if self.env['stock.production.lot'].search_count([('name', '=', name), ('product_id', '=', product_id)]):
                    product = self.env['product.product'].browse(product_id)
                    raise ValidationError(
                        _('The combination of serial number and product must be unique! (Serial Number=%s Product=%s)') % (
                            name, product.display_name
                        )
                    )
        return super(ProductionLot, self).write(vals)
