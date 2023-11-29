from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    loc_case = fields.Char(string='Bin Location')


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.onchange('name')
    def onchange_name(self):
        if self.name and self.name.property_purchase_currency_id:
            currency = self.name.property_purchase_currency_id
            self.currency_id = currency.id or self.env.user.company_id.currency_id.id
