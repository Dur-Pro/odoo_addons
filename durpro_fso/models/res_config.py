from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fso_partners = fields.Many2many('res.partner',
                                    'durpro_fso_config_partners_rel',
                                    string='FSO Partners')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_default = self.env['ir.default'].sudo()
        ir_default.set('res.config.settings', 'fso_partners', self.fso_partners.ids or None)
