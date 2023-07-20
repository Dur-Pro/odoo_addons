from odoo import models, fields, api, _


class HelpdeskCreatePurchaseWizard(models.TransientModel):
    _name = "helpdesk.create.purchase"
    _description = "Create Purchase Order from Helpdesk Ticket"

    ticket_id = fields.Many2one("helpdesk.ticket", string="Helpdesk Ticket")
    partner_id = fields.Many2one("res.partner", string="Supplier")
    company_id = fields.Many2one(related='ticket_id.company_id')

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | {'helpdesk_ticket_id'}

    def action_generate_and_view_order(self):
        self.ensure_one()
        new_po = self.action_generate_order()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order from Ticket'),
            'res_model': 'purchase.order',
            'res_id': new_po.id,
            'view_mode': 'form',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
            'context': {}
        }

    def action_generate_order(self):
        self.ensure_one()
        return self.env['purchase.order'].create(self._generate_po_values())

    def _generate_po_values(self):
        return {
            'partner_id': self.partner_id.id,
            'helpdesk_ticket_id': self.ticket_id.id,
            'company_id': self.company_id.id,
        }
