from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    require_sale_reference = fields.Boolean(
        string="Require Sale Order Reference",
        help="When checked, sale orders can only be confirmed if their reference field is filled.",
        config_parameter="durpro_sale.require_sale_reference",
    )
