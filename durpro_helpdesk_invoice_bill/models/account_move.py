# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import api, models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    helpdesk_ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket',
        help='Ticket this invoice was generated from',
        readonly=True
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | {'helpdesk_ticket_id'}

    def action_view_ticket(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'form',
            'res_id': self.helpdesk_ticket_id.id,
        }

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves.filtered('helpdesk_ticket_id'):
            move.message_post_with_view('helpdesk.ticket_creation',
                                        values={'self': move,
                                                'ticket': move.helpdesk_ticket_id},
                                        subtype_id=self.env.ref('mail.mt_note').id)
        return moves
