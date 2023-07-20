from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ManageInterventionWizard(models.TransientModel):
    _name = 'durpro_fso.manage_intervention.wizard'
    _description = 'Field service work order intervention wizard'

    def create_back_order(self):
        work_order = self.env['durpro_fso.work_order'].search([('id', '=', self.env.context.get('active_id', None))])

        back_work_order = self.env['durpro_fso.work_order'].create({
            'sale_id': work_order.sale_id.id,
            'stage_id': self.env.ref("durpro_fso.work_order_stage_draft").id,
            'send_work_order_to': [(6, 0, work_order.send_work_order_to.ids)],
            'send_invoice_to': [(6, 0, work_order.send_invoice_to.ids)],
            'site_contact_ids': [(6, 0, work_order.site_contact_ids.ids)],
            'time_travel_planned': work_order.time_travel_planned
        })

        for intervention in work_order.intervention_ids.filtered(lambda intervention: intervention.state == 'to_do'):
            new_intervention = self.env['durpro_fso.intervention'].create({
                'work_order_id': back_work_order.id,
                'equipment_id': intervention.equipment_id.id,
                'description': intervention.description,
                'comments': intervention.comments
            })

            for task in intervention.task_ids.filtered(lambda task: task.state == 'to_do'):
                self.env['durpro_fso.task'].create({
                    'sequence': task.sequence,
                    'description': task.description,
                    'comments': task.comments,
                    'time_estimate': task.time_estimate,
                    'intervention_id': new_intervention.id
                })
                task.write({'state': 'bo'})

        record_id = self.env.ref('durpro_fso.work_order_stage_done').id
        work_order.write({'stage_id': record_id})

    def mark_all_done(self):
        work_order = self.env['durpro_fso.work_order'].search([('id', '=', self.env.context.get('active_id', None))])
        for intervention in work_order.intervention_ids.filtered(lambda intervention: intervention.state == 'to_do'):
            for task in intervention.task_ids.filtered(lambda task: task.state == 'to_do'):
                task.state = 'done'

        record_id = self.env.ref('durpro_fso.work_order_stage_done').id
        work_order.write({'stage_id': record_id})