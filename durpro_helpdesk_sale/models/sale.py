# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Helpdesk Ticket',
        copy=False,
    )

    def action_view_ticket(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'form',
            'res_id': self.helpdesk_ticket_id.id,
        }

    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        result.update({'helpdesk_ticket_id': self.helpdesk_ticket_id.id})
        return result

    def create(self, vals_list):
        sos = super().create(vals_list)
        for so in sos.filtered('helpdesk_ticket_id'):
            so.message_post_with_view('helpdesk.ticket_creation',
                                      values={'self': so,
                                              'ticket': so.helpdesk_ticket_id},
                                      subtype_id=self.env.ref('mail.mt_note').id)
        return sos


class AccountMove(models.Model):
    _inherit = 'account.move'
   
    helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Helpdesk Ticket',
        states={'draft': [('readonly', False)]},
        copy=False,
    )


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    
    def _create_invoice(self, order, so_line, amount):
        res = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        res.helpdesk_ticket_id = order.helpdesk_ticket_id
        return res