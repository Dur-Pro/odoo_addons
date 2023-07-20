from odoo import api, fields, models


class ProductCategoryDefault(models.Model):
    _name = 'product.category.default'
    _description = 'Product Category Default'

    @api.model
    def _get_field_list(self):
        field_list = self.env['ir.model.fields'].search([('model', '=', 'product.template')])
        field_selection = []
        for field in field_list:
            field_selection.append((field.name, field.field_description))
        return field_selection

    field = fields.Selection(selection='_get_field_list', string='Field')
    value = fields.Char(string='Value')
    product_category_id = fields.Many2one('product.category', string='Product category')


