from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class WorkOrderStage(models.Model):
    _name = 'durpro_fso.work_order.stage'
    _description = 'Field service work order stage'
    _order = 'sequence, id'

    code = fields.Char(string='Stage Code', required=True)
    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records '
                               'in that stage to display.')


class WorkOrder(models.Model):
    _name = 'durpro_fso.work_order'
    _description = 'Field service work order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'complete_name'

    sale_id = fields.Many2one('sale.order',
                              string="Sale Order",
                              required=True)

    name = fields.Char(string='Work Order Reference',
                       required=True,
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))

    next_intervention = fields.Integer(string='Next Intervention',
                                       required=True,
                                       copy=False,
                                       readonly=True,
                                       index=True,
                                       default=1)

    customer_id = fields.Many2one(string='Customer',
                                  related='sale_id.partner_id',
                                  store=True)

    customer_shipping_id = fields.Many2one(string='Delivery Address',
                                           related='sale_id.partner_shipping_id')

    stage_id = fields.Many2one('durpro_fso.work_order.stage',
                               string='Work Order Stages',
                               group_expand='_read_group_stage_ids',
                               default=lambda self: self.env.ref("durpro_fso.work_order_stage_draft"),
                               copy=False)

    customer_order_ref = fields.Char(string='Customer Reference',
                                     tracking=True,
                                     related='sale_id.client_order_ref')

    customer_pre_authorization_ref = fields.Char(string='Customer Pre-Authorization Reference',
                                                 tracking=True,
                                                 help='This is use to be able to execute the Work Order without PO if '
                                                      'you got an other authorization number and got to ask for the PO '
                                                      'number after the job get done')

    send_work_order_to = fields.Many2many(comodel_name='res.partner',
                                          relation='fso_send_work_order_partner_rel',
                                          string="Send work_order to",
                                          domain="[('parent_id', '=', customer_id)]")

    send_invoice_to = fields.Many2many(comodel_name='res.partner',
                                       relation='fso_send_invoice_partner_rel',
                                       string="Send invoice to",
                                       domain="[('parent_id', '=', customer_id)]")

    site_contact_ids = fields.Many2many(comodel_name='res.partner',
                                        string="Site Contacts",
                                        relation='fso_site_contact_partner_rel',
                                        domain="[('parent_id', '=', customer_id), ('is_site_contact', '=', 'True')]")

    technician_id = fields.Many2one(comodel_name='res.partner',
                                    string="Lead Technician",
                                    domain=lambda self: self._get_fso_partners_domain())

    assistant_ids = fields.Many2many(comodel_name='res.partner',
                                     string="Other Technician",
                                     relation='fso_assistant_partner_rel',
                                     domain=lambda self: self._get_fso_partners_domain())

    date_service = fields.Date(string="Service Date",
                               tracking=True,
                               copy=False)

    # TODO BV: Must find a way to get it from res.partner, adding a field or making average calculation
    time_travel_planned = fields.Float(string="Travel Time",
                                       tracking=True,
                                       default=0.5)

    # TODO BV: Those 3 fields need to be computed and inverse as changing one should result in related change elsewhere
    time_start_planned = fields.Datetime(string="Planned Start Time",
                                         tracking=True,
                                         copy=False)

    time_end_planned = fields.Datetime(string="Planned End Time",
                                       compute='_compute_time_end_planned')

    time_planned = fields.Float(string="Expected Duration",
                                tracking=True,
                                compute="_compute_time_planned",
                                copy=False)

    # TODO BV: Do we add validation on stage done to force filling those fields
    # TODO BV: Those 3 fields need to be computed and inverse as changing one should result in related change elsewhere
    time_start_actual = fields.Datetime(string="Actual Start Time",
                                        tracking=True,
                                        copy=False)

    time_end_actual = fields.Datetime(string="Actual End Time",
                                      tracking=True,
                                      copy=False)

    time_actual = fields.Float(string="Actual Duration",
                               tracking=True,
                               copy=False)

    # BV: Those are resources need to do the job, should be One2many with calendar
    tools_needed = fields.Char(string='tools needed',
                               tracking=True,
                               )

    intervention_ids = fields.One2many(comodel_name='durpro_fso.intervention',
                                       inverse_name='work_order_id',
                                       string="Interventions")

    equipment_count = fields.Integer("Equipments Count",
                                     compute='_compute_intervention_equipments',
                                     store=True)

    intervention_count = fields.Integer("Intervention Count", compute='_compute_intervention_count')
    intervention_done = fields.Integer("Intervention Done", compute='_compute_intervention_done')

    task_count = fields.Integer("Task Count", compute='_compute_task_count')
    task_done = fields.Integer("Task Done", compute='_compute_task_done')

    equipment_ids = fields.Many2many(comodel_name='durpro_fso.equipment',
                                     compute='_compute_intervention_equipments',
                                     store=True)

    delivery_count = fields.Integer(string='Delivery Count',
                                    related='sale_id.delivery_count',
                                    tracking=True,
                                    store=True)

    invoice_count = fields.Integer(string='Invoice Count',
                                   related='sale_id.invoice_count',
                                   tracking=True,
                                   store=True)

    product_line = fields.One2many(comodel_name='sale.order.line',
                                   compute='_split_order_line',
                                   string='Product Lines')

    labour_line = fields.One2many(comodel_name='sale.order.line',
                                  compute='_split_order_line',
                                  string='Labour Lines')

    complete_name = fields.Char(string="Name", compute='_compute_complete_name', store=True)

    @api.depends('intervention_ids.task_ids')
    def _compute_task_count(self):
        for wo in self:
            task_count = 0
            for interv in wo.intervention_ids:
                task_count += len(interv.task_ids)
            wo.task_count = task_count

    @api.depends('intervention_ids.task_ids', 'intervention_ids.task_ids.state')
    def _compute_task_done(self):
        for wo in self:
            task_done = 0
            for interv in wo.intervention_ids:
                task_done += len(interv.task_ids.filtered(lambda i: i.state == 'done'))
            wo.task_done = task_done

    @api.depends('intervention_ids')
    def _compute_intervention_count(self):
        for wo in self:
            wo.intervention_count = len(wo.intervention_ids)

    @api.depends('intervention_ids', 'intervention_ids.state')
    def _compute_intervention_done(self):
        for wo in self:
            wo.intervention_done = len(wo.intervention_ids.filtered(lambda i: i.state == 'done'))

    @api.depends('name', 'customer_id.name')
    def _compute_complete_name(self):
        """ Forms complete name of location from parent location to child location. """
        for work_order in self:
            work_order.complete_name = '%s/%s' % (work_order.customer_id.name, work_order.name)

    @api.depends('time_start_planned', 'time_planned', 'time_travel_planned')
    def _compute_time_end_planned(self):
        for work_order in self:
            duration = work_order.time_planned + 2 * work_order.time_travel_planned
            if duration > 10:
                duration_day = (duration // 8)
            else:
                duration_day = 0
            duration_hour = int(duration)
            duration_minute = int((duration - duration_hour) * 60)
            work_order.time_end_planned = work_order.time_start_planned
            if work_order.time_start_planned:
                work_order.time_start_planned = work_order.time_start_planned.replace(second=0, microsecond=0)
                work_order.time_end_planned = work_order.time_start_planned + timedelta(days=duration_day,
                                                                                        hours=duration_hour,
                                                                                        minutes=duration_minute)

    @api.depends('intervention_ids.time_estimate')
    def _compute_time_planned(self):
        for work_order in self:
            work_order.time_planned = sum(intervention.time_estimate for intervention in work_order.intervention_ids)

    @api.depends('sale_id.order_line.product_id.type')
    def _split_order_line(self):
        for work_order in self:
            order_lines = self.env['sale.order.line'].search([('order_id', '=', work_order.sale_id.id)])
            work_order.product_line = order_lines.filtered(lambda oline: oline.product_id.type != 'service')
            work_order.labour_line = order_lines.filtered(lambda oline: oline.product_id.type == 'service')

    @api.model
    def _read_group_stage_ids(self, groups, domain, order):
        stage_ids = self.env['durpro_fso.work_order.stage'].search([])
        return stage_ids

    @api.depends('intervention_ids.equipment_id')
    def _compute_intervention_equipments(self):
        for work_order in self:
            work_order.equipment_ids = [
                (6, 0, [intervention.equipment_id.id for intervention in work_order.intervention_ids])]
            work_order.equipment_count = len(work_order.equipment_ids)

    def _get_default_stage(self):
        default_stage = self.env.ref("durpro_fso.work_order_stage_draft")
        return default_stage

    def _get_fso_partners_domain(self):
        fso_partners = self.env['ir.default'].get('res.config.settings', 'fso_partners')
        return [('parent_id', 'in', fso_partners)]

    def _get_partners_parent_domain(self):
        customer_id = self.customer_id
        while customer_id.parent_id:
            customer_id = customer_id.parent_id
        return [('parent_id', '=', customer_id), ('type', '!=', 'site')]

    @api.onchange('date_service')
    def onchange_date_service(self):
        for work_order in self:
            if work_order.date_service:
                ds = work_order.date_service
                work_order.time_start_planned = datetime(ds.year, ds.month, ds.day, 12, 0, 0)
            else:
                work_order.time_start_planned = False

    def action_confirm(self):
        for work_order in self:
            record_id = self.env.ref('durpro_fso.work_order_stage_waiting_parts').id
            work_order.write({'stage_id': record_id})
        return True

    def action_set_to_schedule(self):
        for work_order in self:
            record_id = self.env.ref('durpro_fso.work_order_stage_to_schedule').id
            work_order.write({'stage_id': record_id})
        return True

    def action_schedule(self):
        for work_order in self:
            record_id = self.env.ref('durpro_fso.work_order_stage_scheduled').id
            work_order.write({'stage_id': record_id})
        return True

    def action_make_ready(self):
        for work_order in self:
            record_id = self.env.ref('durpro_fso.work_order_stage_ready').id
            work_order.write({'stage_id': record_id})
        return True

    def action_mark_done(self):
        for work_order in self:

            if work_order.intervention_ids and not all(
                    intervention.state == 'done' for intervention in work_order.intervention_ids):
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Manage interventions'),
                    'view_mode': 'form',
                    'res_model': 'durpro_fso.manage_intervention.wizard',
                    'target': 'new',
                }

            record_id = self.env.ref('durpro_fso.work_order_stage_done').id
            work_order.write({'stage_id': record_id})

        return True

    def action_view_invoice(self):
        return self.sale_id.action_view_invoice()

    def action_view_delivery(self):
        return self.sale_id.action_view_delivery()

    def action_invoice(self):
        if not all(picking.state in ['done', 'cancel'] for picking in self.sale_id.picking_ids):
            raise ValidationError(_('Please complete delivery before.'))
        # DJD: Removed due to incompatibility with v15 code.  Function action_invoice_create() no longer exists
        # on model sale.order. This functionality has been moved to the wizard sale_make_invoice_advance in the
        # sale module. For now, require user to go do the invoicing first, check for invoice status,
        # then continue.
        #
        # work_order.sale_id.action_invoice_create()
        elif self.sale_id.invoice_status == 'to invoice':
            raise ValidationError(_('Please complete invoicing before proceeding.'))
        elif self.sale_id.invoice_status == 'invoiced':
            for work_order in self:
                record_id = self.env.ref('durpro_fso.work_order_stage_invoiced').id
                work_order.write({'stage_id': record_id})
            return True
        else:
            for work_order in self:
                record_id = self.env.ref('durpro_fso.work_order_stage_exception').id
                work_order.write({'stage_id': record_id})

    def action_set_draft(self):
        for work_order in self:
            record_id = self.env.ref('durpro_fso.work_order_stage_draft').id
            work_order.write({'stage_id': record_id})

        return True

    def action_set_exception(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Set Exception'),
            'view_mode': 'form',
            'res_model': 'durpro_fso.set_exception.wizard',
            'target': 'new',
        }

    def copy_data(self, default=None):
        if default is None:
            default = {}
        if 'intervention_ids' not in default:
            default['intervention_ids'] = [(0, 0, line.copy_data()[0]) for line in self.intervention_ids]
        if 'equipment_ids' not in default:
            default['equipment_ids'] = self.equipment_ids
        return super(WorkOrder, self).copy_data(default)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                sale_order = self.env['sale.order'].browse(vals.get('sale_id'))
                work_order_ids = self.env['durpro_fso.work_order'].search([('sale_id', '=', vals.get('sale_id'))])
                vals['name'] = sale_order.name.replace('SO', 'FSO') + '-' + str((len(work_order_ids) + 1))
        return super(WorkOrder, self).create(vals_list)

    @api.constrains('stage_id')
    def check_validity(self):
        stage_plan = self.env.ref("durpro_fso.work_order_stage_draft").id
        stage_waiting_parts = self.env.ref("durpro_fso.work_order_stage_waiting_parts").id
        stage_to_schedule = self.env.ref("durpro_fso.work_order_stage_to_schedule").id
        stage_scheduled = self.env.ref("durpro_fso.work_order_stage_scheduled").id
        stage_ready = self.env.ref("durpro_fso.work_order_stage_ready").id
        stage_invoiced = self.env.ref("durpro_fso.work_order_stage_invoiced").id
        stage_exception = self.env.ref("durpro_fso.work_order_stage_exception").id

        if self.stage_id.id not in [stage_exception,
                                    stage_plan] and not self.date_service:
            raise ValidationError(_('The work order must have a planned service date!'))

        if self.stage_id.id not in [stage_exception,
                                    stage_plan,
                                    stage_waiting_parts,
                                    stage_to_schedule] and not self.technician_id:
            raise ValidationError(_('The work order must have a technician set.'))

        if self.stage_id.id not in [stage_exception,
                                    stage_plan,
                                    stage_waiting_parts,
                                    stage_to_schedule,
                                    stage_scheduled] and not (self.customer_order_ref or
                                                              self.customer_pre_authorization_ref):
            raise ValidationError(_('Need a customer Purchase Order (Customer Reference) on sale order or at least a '
                                    'pre-authorization number.'))

        if self.stage_id.id not in [stage_exception,
                                    stage_plan,
                                    stage_waiting_parts,
                                    stage_to_schedule,
                                    stage_scheduled]:
            if len(self.intervention_ids) == 0:
                raise ValidationError(_('Work Order need some intervention to be performed.'))
            else:
                for intervention in self.intervention_ids:
                    if not intervention.task_ids:
                        self.env['durpro_fso.task'].create({
                            'description': 'Execute intervention',
                            'intervention_id': intervention.id
                        })

        # if self.stage_id.id not in [stage_exception,
        #                             stage_plan,
        #                             stage_waiting_parts,
        #                             stage_to_schedule,
        #                             stage_scheduled,
        #                             stage_ready] and self.intervention_ids \
        #         and not all(intervention.state in ['done', 'bo'] for intervention in self.intervention_ids):
        #     raise ValidationError(_('All interventions must be completed and marked done.'))

        if self.stage_id.id in [stage_invoiced]:
            # if not all(picking.state in ['done', 'cancel'] for picking in self.sale_id.picking_ids):
            #     raise ValidationError(_('Please complete delivery before.'))

            # if not (self.sale_id.invoice_status in ['invoiced']):
            #     raise ValidationError(_('Please complete invoicing before.'))

            if not self.customer_order_ref:
                raise ValidationError(_('You just have a pre-authorization number, but you need a customer Purchase '
                                        'Order to create invoice.'))

    def action_navigate_to(self):
        self.ensure_one()
        company = self.env.company
        return {
            'type': 'ir.actions.act_url',
            'url': f'https://www.google.com/maps/dir/?api=1&origin='
                   f'{company.partner_id.partner_latitude},{ company.partner_id.partner_longitude}&destination='
                   f'{self.customer_shipping_id.partner_latitude},{self.customer_shipping_id.partner_longitude}'
        }
