# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    sale_order_ids = fields.One2many('sale.order', 'helpdesk_ticket_id', string="Sale Orders",
                                     help='Sale orders associated to this ticket.', copy=False)
    sale_order_count = fields.Integer(compute="_compute_sale_order_count")

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        self.sale_order_count = len(self.sale_order_ids)

    def action_view_sale_order(self):
        self.ensure_one()
        sale_order_form_view = self.env.ref('sale.view_order_form')
        sale_order_tree_view = self.env.ref('sale.view_order_tree')

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'context': {
                'create': False
            }
        }

        if self.sale_order_count == 1:
            action.update(
                res_id=self.sale_order_ids[0].id,
                views=[(sale_order_form_view.id, 'form')]
            )
        else:
            action.update(
                domain=[('id', 'in', self.sale_order_ids.ids)],
                views=[(sale_order_tree_view.id, 'tree'), (sale_order_form_view.id, 'form')],
                name=_('Purchase Orders from Ticket')
            )
        return action

    def action_convert_to_sale_order(self):
        self.ensure_one()
        so = self.env['sale.order'].create(self._generate_so_values())
        self.message_change_thread(so)
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'helpdesk_ticket'),
                                                        ('res_id', '=', self.id)])
        attachments.sudo().write({'res_model': 'sale_order', 'res_id': so.id})
        self.action_archive()
        return self.action_view_sale_order()

    def _generate_so_values(self):
        team = self.user_id.sale_team_id if self.user_id else self.env.user.sale_team_id
        if not team:
            raise UserError(_('Creating sale orders is reserved to sales users. Assign the user to sale team first.'))
        team_id = team.id
        return {
            'partner_id': self.partner_id.id,
            'helpdesk_ticket_id': self.id,
            'company_id': self.company_id.id,
            'team_id': team_id,
        }
