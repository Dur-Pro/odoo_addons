from odoo import models, fields, api, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket")

    def action_view_ticket(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'form',
            'res_id': self.helpdesk_ticket_id.id,
        }

    @api.model_create_multi
    def create(self, vals_list):
        pos = super().create(vals_list)
        for po in pos.filtered('helpdesk_ticket_id'):
            po.message_post_with_view('helpdesk.ticket_creation',
                                      values={'self': po, 'ticket': po.helpdesk_ticket_id},
                                      subtype_id=self.env.ref('mail.mt_note').id)
        return pos
