from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    ap_email = fields.Char(string="AP Email",
                           help="Email address used as default sender when sending vendor payment notices.")
