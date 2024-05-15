from odoo import models, api


class IncoTerm(models.Model):
    _inherit = 'account.incoterms'

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.code}] {rec.name}"

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, order=None):
        args = list(args or [])
        if name:
            args += ['|', ['code', operator, name], ['name', operator, name]]
            return self._search(args, limit=limit, order=order)
        else:
            return super()._name_search(name, args, operator, limit, order)

