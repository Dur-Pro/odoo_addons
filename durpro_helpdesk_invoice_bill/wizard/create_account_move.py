# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreateAccountMove(models.TransientModel):
    _name = 'helpdesk.create.account_move'
    _description = 'Create a Customer Invoice'

    move_type = fields.Selection([('in_invoice', "Bill"), ('out_invoice', 'Invoice')])
    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Related ticket', required=True)
    company_id = fields.Many2one(related='helpdesk_ticket_id.company_id')
    partner_id = fields.Many2one('res.partner', string="Partner")
    sale_id = fields.Many2one('sale.order', string="Sale Order", domain=[('partner_id', '=', partner_id)])
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order", domain=[('partner_id', '=', partner_id)])

    @api.model
    def default_get(self, fields_list):
        defaults = super(CreateAccountMove, self).default_get(fields_list)
        partner_id = defaults['partner_id'] if 'partner_id' in defaults else False
        if partner_id:
            if defaults['move_type'] == 'out_invoice':
                partner = self.env['res.partner'].browse(partner_id)
                if partner:
                    defaults.update({'partner_id': partner})
        return defaults

    def _generate_invoice_values(self):
        self.ensure_one()
        return {
            'helpdesk_ticket_id': self.helpdesk_ticket_id.id,
            'partner_id': self.partner_id.id,
            'name': '/',
            # 'invoice_origin': self.sale_id.name if self.sale_id else False,
            'move_type': 'out_invoice',
        }

    def _generate_bill_values(self):
        self.ensure_one()
        return {
            'helpdesk_ticket_id': self.helpdesk_ticket_id.id,
            'partner_id': self.partner_id.id,
            'invoice_payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
            # 'invoice_origin': self.purchase_id.name if self.purchase_id else False,
            'move_type': 'in_invoice',
            'name': '/',
        }

    def action_generate_invoice(self):
        self.ensure_one()
        return self.env['account.move'].create(self._generate_invoice_values())

    def action_generate_and_view_invoice(self):
        self.ensure_one()
        new_move = self.action_generate_invoice()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice from Tickets'),
            'res_model': 'account.move',
            'res_id': new_move.id,
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
        }

    def action_generate_bill(self):
        self.ensure_one()
        return self.env['account.move'].create(self._generate_bill_values())

    def action_generate_and_view_bill(self):
        self.ensure_one()
        new_move = self.action_generate_bill()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bill from Tickets'),
            'res_model': 'account.move',
            'res_id': new_move.id,
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
        }


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.model
    def _default_ticket_id(self):
        ticket_id = self._context.get('helpdesk_ticket_id')
        if ticket_id:
            return self.env['helpdesk.ticket'].browse(ticket_id)

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Related ticket', default=_default_ticket_id)

    # Nasty rewrite since method depends on active_ids which we can't change
    @api.depends('helpdesk_ticket_id')
    @api.depends_context('sale_id', 'active_ids')
    def create_invoices(self):
        if self.helpdesk_ticket_id:
            active_ids = self._context.get('sale_id', [])
            return super().with_context({'active_ids': active_ids}).create_invoices()
        else:
            return super().create_invoices()

    def _prepare_invoice_values(self, order, so_line):
        invoice_vals = super()._prepare_invoice_values(order, so_line)
        invoice_vals['helpdesk_ticket_id'] = self.env.context.get('helpdesk_ticket_id')
        return invoice_vals
