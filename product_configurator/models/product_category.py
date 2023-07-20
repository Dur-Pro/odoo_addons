from odoo import _, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category'

    help = fields.Char(string='Help')
    category_default_ids = fields.One2many(
        comodel_name='product.category.default',
        inverse_name='product_category_id',
        string='Default values'
    )
