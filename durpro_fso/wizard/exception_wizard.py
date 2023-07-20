from odoo import api, fields, models, _


class SetExceptionWizard(models.TransientModel):
    _name = 'durpro_fso.set_exception.wizard'
    _description = 'Field service work order exception wizard'

    exception_note = fields.Text('Reason for the exception', required=True)

    def set_exception(self):
        work_order = self.env['durpro_fso.work_order'].search([('id', '=', self.env.context.get('active_id', None))])
        work_order.message_post(body='Exception reason: ' + self.exception_note)
        work_order.stage_id = self.env.ref('durpro_fso.work_order_stage_exception').id
