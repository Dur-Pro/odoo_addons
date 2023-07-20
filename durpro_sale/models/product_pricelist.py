from odoo import fields, models, api


class Pricelist(models.Model):
    """
    Extends the basic product sales price list to include chatter.
    """
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.activity.mixin', 'mail.thread']


