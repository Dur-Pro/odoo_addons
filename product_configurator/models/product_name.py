from odoo import fields, models


# TODO vérifier permissions
class ProductName(models.Model):
    _name = 'product.name'
    _description = 'Product Name'

    level = fields.Selection([
        ('category', 'Category'),
        ('type', 'Type'),
        ('subtype', 'Subtype'),
        ('variant', 'Variant'),
        ('size', 'Size'),
        ('connection_type', 'Connection type'),
        ('material', 'Material'),
        ('manufacturer', 'Manufacturer'),
        ('model', 'Model'),
        ('qty', 'Quantity'),
    ], required=True, string='Level')
    name = fields.Char(required=True, string='Name')
