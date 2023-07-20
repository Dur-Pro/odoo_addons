# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, api, fields, _


# class HelpdeskTeam(models.Model):
#     _inherit = 'helpdesk.team'
#
#     @api.model
#     def _default_fsm_project_id(self):
#         project = self.env['project.project'].search([('is_fsm', '=', True)], limit=1)
#         return project
#
#     fsm_project_id = fields.Many2one('project.project', string='FSM Project', domain=[('is_fsm', '=', True)],
#     default=_default_fsm_project_id)
#
#     # ---------------------------------------------------
#     # Mail gateway
#     # ---------------------------------------------------
#
#     def _mail_get_message_subtypes(self):
#         res = super()._mail_get_message_subtypes()
#         if len(self) == 1:
#             task_done_subtype = self.env.ref('helpdesk_fsm.mt_team_ticket_task_done')
#             if not self.use_fsm and task_done_subtype in res:
#                 res -= task_done_subtype
#         return res

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    # use_fsm = fields.Boolean(related='team_id.use_fsm')
    fso_ids = fields.One2many('durpro_fso.work_order', 'helpdesk_ticket_id',
                              string='FSO Tasks', help='FSO Tasks generated from this ticket', copy=False)
    fso_count = fields.Integer(compute='_compute_fso_count')

    @api.depends('fso_ids')
    def _compute_fso_count(self):
        ticket_groups = self.env['durpro_fso.work_order'].read_group([('helpdesk_ticket_id', '!=', False)], ['id:count_distinct'], ['helpdesk_ticket_id'])
        ticket_count_mapping = dict(map(lambda group: (group['helpdesk_ticket_id'][0], group['helpdesk_ticket_id_count']), ticket_groups))
        for ticket in self:
            ticket.fso_count = ticket_count_mapping.get(ticket.id, 0)

    def action_view_fso(self):
        fso_form_view = self.env.ref('durpro_fso.work_order_view_form')
        fso_list_view = self.env.ref('durpro_fso.work_order_view_tree')
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'durpro_fso.work_order',
            'context': {
                'create': False,
            },
        }

        if len(self.fso_ids) == 1:
            action.update(res_id=self.fso_ids[0].id,
                          views=[(fso_form_view.id, 'form')])
        else:
            action.update(domain=[('id', 'in', self.fso_ids.ids)],
                          views=[(fso_list_view.id, 'tree'), (fso_form_view.id, 'form')],
                          name=_('FSO from Tickets'))
        return action

    def action_generate_fso(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create a Field Service Workorder'),
            'res_model': 'helpdesk.create.fso',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'use_fsm': True,
                'default_helpdesk_ticket_id': self.id,
                'default_user_id': False,
                'default_partner_id': self.partner_id.id if self.partner_id else False,
                'default_name': self.name,
            }
        }

    # ---------------------------------------------------
    # Mail gateway
    # ---------------------------------------------------

    # def _mail_get_message_subtypes(self):
    #     res = super()._mail_get_message_subtypes()
    #     if len(self) == 1 and self.team_id:
    #         task_done_subtype = self.env.ref('helpdesk_fso.mt_ticket_task_done')
    #         if not self.team_id.use_fsm and task_done_subtype in res:
    #             res -= task_done_subtype
    #     return res
