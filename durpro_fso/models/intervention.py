from odoo import api, fields, models, _


class InterventionType(models.Model):
    _name = 'durpro_fso.intervention.type'
    _description = 'Field service intervention type'
    _order = 'id'

    name = fields.Char(string='Name', required=True, translate=True)


class Intervention(models.Model):
    _name = 'durpro_fso.intervention'
    _description = 'Field service intervention'
    _order = 'sequence'

    work_order_id = fields.Many2one(comodel_name='durpro_fso.work_order',
                                    string="Work Order")

    date_planned = fields.Date(string='Planned date',
                               related='work_order_id.date_service')

    customer_id = fields.Many2one(comodel_name='res.partner',
                                  related='work_order_id.customer_id')

    equipment_id = fields.Many2one(comodel_name='durpro_fso.equipment',
                                   string="Equipment",
                                   domain="[('partner_id','=', customer_id)]",
                                   required=True)

    sequence = fields.Integer()

    name = fields.Char(string='Reference',
                       required=True,
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))

    description = fields.Text(string="Description")

    task_ids = fields.One2many(comodel_name='durpro_fso.task',
                               inverse_name='intervention_id',
                               string="Tasks")

    time_estimate = fields.Float(string="Estimated Time",
                                 compute="_compute_time_estimate")

    comments = fields.Text(string="Comments")

    state = fields.Selection([('to_do', 'To Do'),
                              ('done', 'Done'),
                              ('bo', 'Back Order'),
                              ('exception', 'Need task!')],
                             string="Status",
                             compute="_compute_state")

    next_task = fields.Integer(string='Next Task',
                               required=True,
                               copy=False,
                               readonly=True,
                               index=True,
                               default=1)

    def copy_data(self, default=None):
        if default is None:
            default = {}
        if 'task_ids' not in default:
            default['task_ids'] = [(0, 0, line.copy_data()[0]) for line in self.task_ids]
        return super(Intervention, self).copy_data(default)

    @api.depends('task_ids.time_estimate')
    def _compute_time_estimate(self):
        for rec in self:
            rec.time_estimate = sum(task.time_estimate for task in rec.task_ids)

    @api.depends('task_ids.state')
    def _compute_state(self):
        for rec in self:
            if rec.task_ids and all(task.state == 'done' for task in rec.task_ids):
                rec.state = 'done'
            elif rec.task_ids and any(task.state == 'to_do' for task in rec.task_ids):
                rec.state = 'to_do'
            elif rec.task_ids and all(task.state in ['done', 'bo'] for task in rec.task_ids):
                rec.state = 'bo'
            else:
                rec.state = 'exception'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            work_order = self.env['durpro_fso.work_order'].browse(vals.get('work_order_id'))
            vals['name'] = work_order.name + 'I' + str(work_order.next_intervention)
            work_order.write({'next_intervention': work_order.next_intervention + 1})
        result = super(Intervention, self).create(vals)
        return result
