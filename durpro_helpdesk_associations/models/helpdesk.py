# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, api, fields, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def action_associate(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Associate a Record'),
            'res_model': 'helpdesk.ticket.associate',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_ticket_id': self.id,
                'default_user_id': False,
            }

        }