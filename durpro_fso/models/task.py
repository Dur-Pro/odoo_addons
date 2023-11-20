from odoo import api, fields, models, _


class Task(models.Model):
    _name = 'durpro_fso.task'
    _order = 'sequence'
    _description = 'Field service work order task'

    intervention_id = fields.Many2one('durpro_fso.intervention', string="Intervention")
    sequence = fields.Integer()

    name = fields.Char(string='Task Reference',
                       required=True,
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))

    description = fields.Text(string="Description")
    time_estimate = fields.Float(string="Estimated Time",
                                 default=0.25)
    comments = fields.Text(string="Comments")

    state = fields.Selection([('to_do', 'To Do'),
                              ('done', 'Done'),
                              ('bo', 'Back Order')],
                             string="Status",
                             default='to_do')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                intervention = self.env['durpro_fso.intervention'].browse(vals.get('intervention_id'))
                vals['name'] = intervention.name + 'T' + str(intervention.next_task)
                intervention.write({'next_task': intervention.next_task + 1})
        return super(Task, self).create(vals_list)
