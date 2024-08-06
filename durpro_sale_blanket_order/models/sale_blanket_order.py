from odoo import models, fields, api, _


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    incoterms_id = fields.Many2one(
        "account.incoterms",
        "Incoterm",
        help="International Commercial Terms are a series of predefined commercial"
        " terms used in international transactions.",
    )

    tag_ids = fields.Many2many(
        comodel_name="crm.tag",
        string="Tags",
    )
