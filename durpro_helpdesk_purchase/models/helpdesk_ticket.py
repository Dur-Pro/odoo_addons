from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    purchase_order_ids = fields.One2many(
        comodel_name='purchase.order',
        inverse_name='helpdesk_ticket_id',
        string='Purchase Orders',
        help='Purchase orders associated to this ticket',
        copy=False
    )

    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count')

    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        self.purchase_order_count = len(self.purchase_order_ids)

    def action_view_purchase_order(self):
        purchase_order_form_view = self.env.ref('purchase.purchase_order_form')
        purchase_list_view = self.env.ref('purchase.purchase_order_tree')

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'context': {
                'create': False
            }
        }

        if self.purchase_order_count == 1:
            action.update(
                res_id=self.purchase_order_ids[0].id,
                views=[(purchase_order_form_view.id, 'form')]
            )
        else:
            action.update(
                domain=[('id', 'in', self.purchase_order_ids.ids)],
                views=[(purchase_list_view.id, 'tree'), (purchase_order_form_view.id, 'form')],
                name=_('Purchase Orders from Ticket')
            )
        return action

    def action_generate_purchase_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create a Purchase Order'),
            'res_model': 'helpdesk.create.purchase',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_ticket_id': self.id,
                'default_user_id': False,
                'default_partner_id': self.partner_id.id if self.partner_id else False
            }
        }
