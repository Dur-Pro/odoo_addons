from odoo import models, fields


class SignTemplate(models.Model):
    _inherit = 'sign.template'

    project_id = fields.Many2one('project.project')
