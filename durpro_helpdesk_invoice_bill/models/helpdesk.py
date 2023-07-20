# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, api, fields, _

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    move_ids = fields.One2many('account.move', 'helpdesk_ticket_id', string='Account Moves',
                               help='Invoices / vendor bills generated from this ticket', copy=False,)

    invoice_count = fields.Integer(compute='_compute_counts')
    bill_count = fields.Integer(compute='_compute_counts')

    @api.depends('move_ids')
    def _compute_counts(self):
        self.invoice_count = len(self._get_invoice_ids())
        self.bill_count = len(self._get_bill_ids())

    def action_view_invoice(self):
        invoice_form_view = self.env.ref('account.view_move_form')
        invoice_list_view = self.env.ref('account.view_out_invoice_tree')
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {
                'create': False,
            },
        }

        if len(self._get_invoice_ids()) == 1:
            action.update(res_id=self._get_invoice_ids()[0].id,
                          views=[(invoice_form_view.id, 'form')])
        else:
            action.update(domain=[('id', 'in', self._get_invoice_ids().ids)],
                          views=[(invoice_list_view.id, 'tree'), (invoice_form_view.id, 'form')],
                          name=_('Invoices from Ticket'))
        return action

    def action_view_bill(self):
        bill_form_view = self.env.ref('account.view_move_form')
        bill_list_view = self.env.ref('account.view_in_invoice_tree')
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {
                'create': False,
            },
        }

        if len(self._get_bill_ids()) == 1:
            action.update(res_id=self._get_bill_ids()[0].id,
                          views=[(bill_form_view.id, 'form')])
        else:
            action.update(domain=[('id', 'in', self._get_bill_ids().ids)],
                          views=[(bill_list_view.id, 'tree'), (bill_form_view.id, 'form')],
                          name=_('Invoices from Ticket'))
        return action

    def action_generate_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create an Invoice'),
            'res_model': 'helpdesk.create.account_move',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_type': 'out_invoice',
                'default_helpdesk_ticket_id': self.id,
                'default_user_id': False,
                'default_partner_id': self.partner_id.id if self.partner_id else False,
                'default_name': self.name,
            }
        }

    def action_generate_bill(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create a Vendor Bill'),
            'res_model': 'helpdesk.create.account_move',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_type': 'in_invoice',
                'default_helpdesk_ticket_id': self.id,
                'default_user_id': False,
                'default_partner_id': self.partner_id.id if self.partner_id else False,
                'default_name': self.name,
            }
        }

    def _get_invoice_ids(self):
        return self.move_ids.filtered(lambda r: r.move_type == 'out_invoice')

    def _get_bill_ids(self):
        return self.move_ids.filtered(lambda r: r.move_type == 'in_invoice')