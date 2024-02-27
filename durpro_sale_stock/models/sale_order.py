from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    carrier = fields.Char(string='Carrier', size=64, tracking=True)
    carrier_account = fields.Char(string='Carrier Account', size=64, tracking=True)
